# Security Scanner Web Application

A comprehensive security vulnerability scanning web application similar to rengine, with a modern UI and full authentication system. This application runs multiple security tools in sequence to perform comprehensive vulnerability assessments.

## Features

- 🔐 **User Authentication**: Register and login system with JWT tokens
- 🎯 **Multi-Tool Scanning**: Integrates multiple security tools:
  - **Subfinder**: Subdomain enumeration
  - **httpx**: Live subdomain checking
  - **Nuclei**: Vulnerability scanning
  - **Katana**: Web crawling
  - **XSS Discovery**: Parameter discovery and filtering
  - **Dalfox**: XSS vulnerability testing
- 📊 **Real-time Progress**: Live updates on scan progress
- 🎨 **Modern UI**: Beautiful, responsive React frontend
- 💾 **Results Storage**: All scan results stored in database

## Prerequisites

Before running the application, you need to install the following security tools:

### Required Tools

1. **Subfinder**
   ```bash
   go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
   ```

2. **httpx**
   ```bash
   go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
   ```

3. **Nuclei**
   ```bash
   go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
   nuclei -update-templates
   ```

4. **Katana**
   ```bash
   go install -v github.com/projectdiscovery/katana/cmd/katana@latest
   ```

5. **uro** (Optional, for URL normalization)
   ```bash
   pip install uro
   ```

6. **Dalfox**
   ```bash
   go install github.com/hahwul/dalfox/v2@latest
   ```

**Note**: Make sure all tools are in your PATH so they can be executed from anywhere.

## Installation

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

## Running the Application

### Start the Backend

1. From the `backend` directory:
   ```bash
   python main.py
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`

### Start the Frontend

1. From the `frontend` directory:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`

## Usage

1. **Register an Account**: 
   - Navigate to `http://localhost:5173/register`
   - Create a new account with email, username, and password

2. **Login**:
   - Use your credentials to login at `http://localhost:5173/login`

3. **Start a Scan**:
   - Enter a target domain (e.g., `example.com`)
   - Click "Start Scan"
   - Monitor progress in real-time

4. **View Results**:
   - Click on any scan to view detailed results
   - Browse through different result tabs:
     - Overview: Summary of all scan results
     - Subfinder Results: Discovered subdomains
     - Live Subdomains: Active hosts
     - Nuclei Results: Vulnerability findings
     - Katana Results: Crawled URLs
     - XSS Parameters: Discovered parameters
     - Dalfox Results: XSS test results

## Project Structure

```
.
├── backend/
│   ├── main.py           # FastAPI application
│   ├── database.py       # Database configuration
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── auth.py           # Authentication logic
│   ├── scanner.py        # Security tool execution
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── context/      # React context (Auth)
│   │   └── App.jsx       # Main app component
│   ├── package.json      # Node.js dependencies
│   └── vite.config.js    # Vite configuration
└── README.md
```

## API Endpoints

- `POST /api/register` - Register a new user
- `POST /api/token` - Login and get JWT token
- `GET /api/me` - Get current user info
- `POST /api/scans` - Create a new scan
- `GET /api/scans` - List all scans for current user
- `GET /api/scans/{id}` - Get scan details

## Security Notes

⚠️ **Important**: This application is designed for localhost use and security testing. 

- Change the `SECRET_KEY` in `backend/auth.py` for production use
- The application stores scan results in a SQLite database
- All security tools must be properly installed and accessible
- Use responsibly and only on systems you own or have permission to test

## Troubleshooting

### Tools Not Found
If you get "tool not found" errors:
- Ensure all tools are installed and in your PATH
- Test each tool manually from the command line
- On Windows, you may need to add Go bin directory to PATH:
  ```
  C:\Users\<YourUser>\go\bin
  ```

### Nuclei Templates Not Found
- Run `nuclei -update-templates` to download templates
- Templates are usually stored in `~/nuclei-templates` or `/opt/nuclei-templates`

### Database Issues
- The SQLite database (`scanner.db`) is created automatically
- If you need to reset, delete `scanner.db` and restart the backend

## License

This project is for educational and authorized security testing purposes only.

