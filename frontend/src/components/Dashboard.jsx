import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import Navbar from './Navbar'
import API_BASE_URL from '../config'
import './Dashboard.css'

function Dashboard() {
  const [domain, setDomain] = useState('')
  const [scans, setScans] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    fetchScans()
    // Poll for updates every 3 seconds
    const interval = setInterval(fetchScans, 3000)
    return () => clearInterval(interval)
  }, [])

  const fetchScans = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/scans`)
      setScans(response.data)
    } catch (err) {
      console.error('Error fetching scans:', err)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await axios.post(`${API_BASE_URL}/api/scans`, {
        domain: domain.trim()
      })
      setDomain('')
      fetchScans()
      navigate(`/scan/${response.data.id}`)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to start scan')
    } finally {
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

  return (
    <>
      <Navbar />
      <div className="dashboard-container">
        <div className="dashboard-content">
          <h1>Security Scanner Dashboard</h1>
          <p className="dashboard-subtitle">
            Comprehensive vulnerability assessment and security scanning
          </p>

          <div className="scan-form-card">
            <h2>Start New Scan</h2>
            <form onSubmit={handleSubmit}>
              {error && <div className="error-message">{error}</div>}
              <div className="form-group">
                <label>Target Domain</label>
                <input
                  type="text"
                  value={domain}
                  onChange={(e) => setDomain(e.target.value)}
                  placeholder="example.com"
                  required
                  className="domain-input"
                />
              </div>
              <button type="submit" disabled={loading} className="scan-button">
                {loading ? 'Starting Scan...' : '🚀 Start Scan'}
              </button>
            </form>
          </div>

          <div className="scans-section">
            <h2>Recent Scans</h2>
            {scans.length === 0 ? (
              <div className="empty-state">
                <p>No scans yet. Start your first scan above!</p>
              </div>
            ) : (
              <div className="scans-grid">
                {scans.map((scan) => (
                  <div
                    key={scan.id}
                    className="scan-card"
                    onClick={() => navigate(`/scan/${scan.id}`)}
                  >
                    <div className="scan-header">
                      <h3>{scan.domain}</h3>
                      <span
                        className="status-badge"
                        style={{ backgroundColor: getStatusColor(scan.status) }}
                      >
                        {scan.status}
                      </span>
                    </div>
                    <div className="scan-info">
                      <p>
                        <strong>Created:</strong>{' '}
                        {new Date(scan.created_at).toLocaleString()}
                      </p>
                      {scan.current_step && (
                        <p className="current-step">
                          <strong>Status:</strong> {scan.current_step}
                        </p>
                      )}
                      {scan.status === 'running' && (
                        <div className="progress-bar">
                          <div
                            className="progress-fill"
                            style={{ width: `${scan.progress}%` }}
                          />
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  )
}

export default Dashboard

