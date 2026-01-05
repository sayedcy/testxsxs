import React, { createContext, useContext, useState, useEffect } from 'react'
import axios from 'axios'
import API_BASE_URL from '../config'

const AuthContext = createContext()

export function useAuth() {
  return useContext(AuthContext)
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      fetchUser()
    } else {
      setLoading(false)
    }
  }, [])

  const fetchUser = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/me`)
      setUser(response.data)
    } catch (error) {
      console.error('Fetch user error:', error)
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    } finally {
      setLoading(false)
    }
  }

  const login = async (email, password) => {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)
    
    const response = await axios.post(`${API_BASE_URL}/api/token`, formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    
    const token = response.data.access_token
    localStorage.setItem('token', token)
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    
    await fetchUser()
    return response.data
  }

  const register = async (email, username, password) => {
    try {
      console.log('Registering user:', { email, username, apiUrl: API_BASE_URL })
      const response = await axios.post(`${API_BASE_URL}/api/register`, {
        email,
        username,
        password
      })
      console.log('Registration successful:', response.data)
      return response.data
    } catch (error) {
      console.error('Registration API error:', error)
      console.error('Error details:', error.response?.data)
      // Re-throw with better error message
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
    setUser(null)
  }

  const value = {
    user,
    login,
    register,
    logout,
    loading
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

