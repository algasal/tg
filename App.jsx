import { useState } from 'react'
import Login from './components/Login'
import Register from './components/Register'
import Dashboard from './components/Dashboard'
import './App.css'

function App() {
  const [user, setUser] = useState(null)
  const [currentView, setCurrentView] = useState('login') // 'login', 'register', 'dashboard'

  const handleLogin = (userData) => {
    setUser(userData)
    setCurrentView('dashboard')
  }

  const handleRegister = (userData) => {
    // Após o registro, redireciona para o login
    setCurrentView('login')
  }

  const handleLogout = () => {
    setUser(null)
    setCurrentView('login')
  }

  const switchToRegister = () => {
    setCurrentView('register')
  }

  const switchToLogin = () => {
    setCurrentView('login')
  }

  if (currentView === 'dashboard' && user) {
    return <Dashboard user={user} onLogout={handleLogout} />
  }

  if (currentView === 'register') {
    return (
      <Register 
        onRegister={handleRegister}
        onSwitchToLogin={switchToLogin}
      />
    )
  }

  return (
    <Login 
      onLogin={handleLogin}
      onSwitchToRegister={switchToRegister}
    />
  )
}

export default App
