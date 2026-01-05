import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import axios from 'axios'
import Navbar from './Navbar'
import API_BASE_URL from '../config'
import './ScanDetail.css'

function ScanDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [scan, setScan] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')

  useEffect(() => {
    fetchScan()
    // Poll for updates every 2 seconds if scan is running
    const interval = setInterval(() => {
      fetchScan()
    }, 2000)
    return () => clearInterval(interval)
  }, [id])

  const fetchScan = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/scans/${id}`)
      setScan(response.data)
      setLoading(false)
    } catch (err) {
      console.error('Error fetching scan:', err)
      setLoading(false)
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return '#4caf50'
      case 'running':
        return '#2196f3'
      case 'failed':
        return '#f44336'
      default:
        return '#ff9800'
    }
  }

  if (loading) {
    return (
      <>
        <Navbar />
        <div className="loading">Loading scan details...</div>
      </>
    )
  }

  if (!scan) {
    return (
      <>
        <Navbar />
        <div className="scan-detail-container">
          <div className="error-state">Scan not found</div>
        </div>
      </>
    )
  }

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'subfinder', label: 'Subfinder Results' },
    { id: 'httpx', label: 'Live Subdomains' },
    { id: 'nuclei', label: 'Nuclei Results' },
    { id: 'katana', label: 'Katana Results' },
    { id: 'xss', label: 'XSS Parameters' },
    { id: 'dalfox', label: 'Dalfox Results' }
  ]

  return (
    <>
      <Navbar />
      <div className="scan-detail-container">
        <button onClick={() => navigate('/dashboard')} className="back-button">
          ← Back to Dashboard
        </button>

        <div className="scan-header-card">
          <div className="scan-title">
            <h1>{scan.domain}</h1>
            <span
              className="status-badge-large"
              style={{ backgroundColor: getStatusColor(scan.status) }}
            >
              {scan.status}
            </span>
          </div>
          <div className="scan-meta">
            <p>
              <strong>Created:</strong> {new Date(scan.created_at).toLocaleString()}
            </p>
            <p>
              <strong>Updated:</strong> {new Date(scan.updated_at).toLocaleString()}
            </p>
            {scan.current_step && (
              <p className="current-step">
                <strong>Current Step:</strong> {scan.current_step}
              </p>
            )}
          </div>
          {scan.status === 'running' && (
            <div className="progress-section">
              <div className="progress-bar-large">
                <div
                  className="progress-fill-large"
                  style={{ width: `${scan.progress}%` }}
                />
              </div>
              <p className="progress-text">{scan.progress}% Complete</p>
            </div>
          )}
        </div>

        <div className="results-section">
          <div className="tabs">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                className={`tab ${activeTab === tab.id ? 'active' : ''}`}
                onClick={() => setActiveTab(tab.id)}
              >
                {tab.label}
              </button>
            ))}
          </div>

          <div className="tab-content">
            {activeTab === 'overview' && (
              <div className="overview">
                <h2>Scan Overview</h2>
                <div className="overview-grid">
                  <div className="overview-card">
                    <h3>Subfinder</h3>
                    <p>
                      {scan.subfinder_results
                        ? `${scan.subfinder_results.split('\n').filter(l => l.trim()).length} subdomains found`
                        : 'Pending'}
                    </p>
                  </div>
                  <div className="overview-card">
                    <h3>Live Subdomains</h3>
                    <p>
                      {scan.httpx_results
                        ? `${scan.httpx_results.split('\n').filter(l => l.trim()).length} live hosts`
                        : 'Pending'}
                    </p>
                  </div>
                  <div className="overview-card">
                    <h3>Nuclei</h3>
                    <p>
                      {scan.nuclei_results
                        ? `${scan.nuclei_results.split('\n').filter(l => l.trim()).length} findings`
                        : 'Pending'}
                    </p>
                  </div>
                  <div className="overview-card">
                    <h3>Katana</h3>
                    <p>
                      {scan.katana_results
                        ? `${scan.katana_results.split('\n').filter(l => l.trim()).length} URLs crawled`
                        : 'Pending'}
                    </p>
                  </div>
                  <div className="overview-card">
                    <h3>XSS Parameters</h3>
                    <p>
                      {scan.xss_results
                        ? `${scan.xss_results.split('\n').filter(l => l.trim()).length} parameters`
                        : 'Pending'}
                    </p>
                  </div>
                  <div className="overview-card">
                    <h3>Dalfox</h3>
                    <p>
                      {scan.dalfox_results
                        ? 'Results available'
                        : 'Pending'}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'subfinder' && (
              <div className="result-content">
                <h2>Subfinder Results</h2>
                <pre className="result-text">
                  {scan.subfinder_results || 'No results yet...'}
                </pre>
              </div>
            )}

            {activeTab === 'httpx' && (
              <div className="result-content">
                <h2>Live Subdomains (httpx)</h2>
                <pre className="result-text">
                  {scan.httpx_results || 'No results yet...'}
                </pre>
              </div>
            )}

            {activeTab === 'nuclei' && (
              <div className="result-content">
                <h2>Nuclei Vulnerability Scan Results</h2>
                <pre className="result-text">
                  {scan.nuclei_results || 'No results yet...'}
                </pre>
              </div>
            )}

            {activeTab === 'katana' && (
              <div className="result-content">
                <h2>Katana Crawl Results</h2>
                <pre className="result-text">
                  {scan.katana_results || 'No results yet...'}
                </pre>
              </div>
            )}

            {activeTab === 'xss' && (
              <div className="result-content">
                <h2>XSS Parameter Discovery</h2>
                <pre className="result-text">
                  {scan.xss_results || 'No results yet...'}
                </pre>
              </div>
            )}

            {activeTab === 'dalfox' && (
              <div className="result-content">
                <h2>Dalfox XSS Test Results</h2>
                <pre className="result-text">
                  {scan.dalfox_results || 'No results yet...'}
                </pre>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  )
}

export default ScanDetail

