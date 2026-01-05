import subprocess
import os
import json
import re
from pathlib import Path
from sqlalchemy.orm import Session
from models import ScanJob, ScanStatus
from schemas import ScanJobCreate, ScanJobResponse
import asyncio
from datetime import datetime

# Create results directory
RESULTS_DIR = Path("./scan_results")
RESULTS_DIR.mkdir(exist_ok=True)

def create_scan_job(db: Session, scan: ScanJobCreate, user_id: int) -> ScanJob:
    db_scan = ScanJob(domain=scan.domain, owner_id=user_id, status=ScanStatus.PENDING)
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)
    return db_scan

def get_scan_job(db: Session, scan_id: int, user_id: int):
    scan = db.query(ScanJob).filter(ScanJob.id == scan_id, ScanJob.owner_id == user_id).first()
    if scan:
        return scan
    return None

def list_scan_jobs(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    scans = db.query(ScanJob).filter(ScanJob.owner_id == user_id).offset(skip).limit(limit).all()
    return scans

def run_scan_workflow(scan_id: int, domain: str):
    """Run the complete security scanning workflow"""
    import asyncio
    from database import SessionLocal
    
    # Run async workflow
    asyncio.run(run_scan_workflow_async(scan_id, domain))

async def run_scan_workflow_async(scan_id: int, domain: str):
    """Async implementation of the scan workflow"""
    from database import SessionLocal
    
    db = SessionLocal()
    try:
        scan = db.query(ScanJob).filter(ScanJob.id == scan_id).first()
        if not scan:
            return
        
        scan.status = ScanStatus.RUNNING
        scan.current_step = "Starting scan..."
        scan.progress = 0
        db.commit()
        
        # Step 1: Subdomain Enumeration
        scan.current_step = "Running Subfinder..."
        scan.progress = 10
        db.commit()
        subs_file = RESULTS_DIR / f"scan_{scan_id}_subs.txt"
        subfinder_result = await run_subfinder(domain, str(subs_file))
        scan.subfinder_results = subfinder_result
        scan.progress = 20
        db.commit()
        
        # Step 2: Live Subdomains
        scan.current_step = "Checking live subdomains with httpx..."
        scan.progress = 30
        db.commit()
        httpx_file = RESULTS_DIR / f"scan_{scan_id}_httpx.txt"
        httpx_result = await run_httpx(str(subs_file), str(httpx_file))
        scan.httpx_results = httpx_result
        scan.progress = 40
        db.commit()
        
        # Step 3: Nuclei Scan
        scan.current_step = "Running Nuclei vulnerability scan..."
        scan.progress = 50
        db.commit()
        nuclei_file = RESULTS_DIR / f"scan_{scan_id}_nuclei.txt"
        nuclei_result = await run_nuclei(str(httpx_file), str(nuclei_file))
        scan.nuclei_results = nuclei_result
        scan.progress = 60
        db.commit()
        
        # Step 4: Katana Crawling
        scan.current_step = "Crawling with Katana..."
        scan.progress = 70
        db.commit()
        katana_file = RESULTS_DIR / f"scan_{scan_id}_katana.txt"
        katana_result = await run_katana(str(httpx_file), str(katana_file))
        scan.katana_results = katana_result
        scan.progress = 80
        db.commit()
        
        # Step 5: XSS Parameter Discovery
        scan.current_step = "Discovering XSS parameters..."
        scan.progress = 85
        db.commit()
        xss_file = RESULTS_DIR / f"scan_{scan_id}_xss.txt"
        xss_result = await run_xss_discovery(str(katana_file), str(xss_file))
        scan.xss_results = xss_result
        scan.progress = 90
        db.commit()
        
        # Step 6: Dalfox XSS Testing
        scan.current_step = "Testing XSS vulnerabilities with Dalfox..."
        scan.progress = 95
        db.commit()
        dalfox_file = RESULTS_DIR / f"scan_{scan_id}_dalfox.json"
        dalfox_result = await run_dalfox(str(xss_file), str(dalfox_file))
        scan.dalfox_results = dalfox_result
        scan.progress = 100
        scan.current_step = "Scan completed!"
        scan.status = ScanStatus.COMPLETED
        db.commit()
        
    except Exception as e:
        scan.status = ScanStatus.FAILED
        scan.current_step = f"Error: {str(e)}"
        db.commit()
    finally:
        db.close()

async def run_subfinder(domain: str, output_file: str) -> str:
    """Run subfinder for subdomain enumeration"""
    try:
        cmd = ["subfinder", "-d", domain, "-o", output_file, "-all"]
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                results = f.read()
            return results[:10000]  # Limit to 10KB
        return f"Subfinder completed. Output saved to {output_file}"
    except FileNotFoundError:
        return "Error: subfinder not found. Please install it: https://github.com/projectdiscovery/subfinder"
    except Exception as e:
        return f"Error running subfinder: {str(e)}"

async def run_httpx(input_file: str, output_file: str) -> str:
    """Run httpx to check live subdomains"""
    try:
        if not os.path.exists(input_file):
            return "Error: Input file not found"
        
        cmd = ["httpx", "-l", input_file, "-o", output_file]
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                results = f.read()
            return results[:10000]
        return f"Httpx completed. Output saved to {output_file}"
    except FileNotFoundError:
        return "Error: httpx not found. Please install it: https://github.com/projectdiscovery/httpx"
    except Exception as e:
        return f"Error running httpx: {str(e)}"

async def run_nuclei(input_file: str, output_file: str) -> str:
    """Run nuclei for vulnerability scanning"""
    try:
        if not os.path.exists(input_file):
            return "Error: Input file not found"
        
        # Get nuclei templates directory (common locations)
        templates_dirs = [
            os.path.expanduser("~/nuclei-templates"),
            "/opt/nuclei-templates",
            "./nuclei-templates"
        ]
        templates_dir = None
        for td in templates_dirs:
            if os.path.exists(td):
                templates_dir = td
                break
        
        if not templates_dir:
            return "Error: nuclei-templates directory not found"
        
        cmd = ["nuclei", "-l", input_file, "-t", templates_dir, "-es", "info,low", "-o", output_file]
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                results = f.read()
            return results[:10000]
        return f"Nuclei completed. Output saved to {output_file}"
    except FileNotFoundError:
        return "Error: nuclei not found. Please install it: https://github.com/projectdiscovery/nuclei"
    except Exception as e:
        return f"Error running nuclei: {str(e)}"

async def run_katana(input_file: str, output_file: str) -> str:
    """Run katana for web crawling"""
    try:
        if not os.path.exists(input_file):
            return "Error: Input file not found"
        
        cmd = ["katana", "-list", input_file, "-o", output_file]
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                results = f.read()
            return results[:10000]
        return f"Katana completed. Output saved to {output_file}"
    except FileNotFoundError:
        return "Error: katana not found. Please install it: https://github.com/projectdiscovery/katana"
    except Exception as e:
        return f"Error running katana: {str(e)}"

async def run_xss_discovery(input_file: str, output_file: str) -> str:
    """Discover XSS parameters using filtering and uro"""
    try:
        if not os.path.exists(input_file):
            return "Error: Input file not found"
        
        # Read katana results
        with open(input_file, 'r') as f:
            urls = f.readlines()
        
        # Filter URLs with parameters and exclude file extensions
        excluded_extensions = [
            'css', 'woff', 'woff2', 'txt', 'js', 'm4r', 'm4p', 'm4b', 'ipa', 'asa', 'pkg',
            'crash', 'asf', 'asx', 'wax', 'wmv', 'wmx', 'avi', 'bmp', 'class', 'divx',
            'doc', 'docx', 'exe', 'gif', 'gz', 'gzip', 'ico', 'jpg', 'jpeg', 'jpe', 'webp',
            'json', 'mdb', 'mid', 'midi', 'mov', 'qt', 'mp3', 'm4a', 'mp4', 'm4v', 'mpeg',
            'mpg', 'mpe', 'webm', 'mpp', 'otf', 'odb', 'odc', 'odf', 'odg', 'odp', 'ods',
            'odt', 'ogg', 'pdf', 'png', 'pot', 'pps', 'ppt', 'pptx', 'ra', 'ram', 'svg',
            'svgz', 'swf', 'tar', 'tif', 'tiff', 'ttf', 'wav', 'wma', 'wri', 'xla', 'xls',
            'xlsx', 'xlt', 'xlw', 'zip'
        ]
        
        filtered_urls = []
        for url in urls:
            url = url.strip()
            if '=' in url:
                # Check if URL ends with excluded extension
                url_lower = url.lower()
                excluded = False
                for ext in excluded_extensions:
                    if url_lower.endswith(f'.{ext}'):
                        excluded = True
                        break
                if not excluded:
                    filtered_urls.append(url)
        
        # Remove duplicates
        filtered_urls = list(set(filtered_urls))
        
        # Write to temp file for uro
        temp_file = input_file + ".temp"
        with open(temp_file, 'w') as f:
            f.write('\n'.join(filtered_urls))
        
        # Run uro to normalize URLs
        try:
            cmd = ["uro", "-i", temp_file]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            uro_output = stdout.decode() if stdout else '\n'.join(filtered_urls)
        except FileNotFoundError:
            # If uro not found, use filtered URLs directly
            uro_output = '\n'.join(filtered_urls)
        
        # Run httpx on filtered URLs
        temp_httpx = temp_file + ".httpx"
        with open(temp_httpx, 'w') as f:
            f.write(uro_output)
        
        try:
            cmd = ["httpx", "-l", temp_httpx, "-o", output_file]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
        except FileNotFoundError:
            # If httpx fails, just save the filtered URLs
            with open(output_file, 'w') as f:
                f.write(uro_output)
        
        # Clean up temp files
        for tf in [temp_file, temp_httpx]:
            if os.path.exists(tf):
                os.remove(tf)
        
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                results = f.read()
            return results[:10000]
        return f"XSS discovery completed. Output saved to {output_file}"
    except Exception as e:
        return f"Error in XSS discovery: {str(e)}"

async def run_dalfox(input_file: str, output_file: str) -> str:
    """Run dalfox for XSS testing"""
    try:
        if not os.path.exists(input_file):
            return "Error: Input file not found"
        
        cmd = ["dalfox", "file", input_file, "--format", "json", "-o", output_file]
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                results = f.read()
            try:
                # Try to parse and format JSON
                json_data = json.loads(results)
                return json.dumps(json_data, indent=2)[:10000]
            except:
                return results[:10000]
        return f"Dalfox completed. Output saved to {output_file}"
    except FileNotFoundError:
        return "Error: dalfox not found. Please install it: https://github.com/hahwul/dalfox"
    except Exception as e:
        return f"Error running dalfox: {str(e)}"

