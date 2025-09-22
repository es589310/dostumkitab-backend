"use client"

import { createContext, useContext, useState, type ReactNode } from "react"

interface User {
  id: number
  name: string
  email: string
}

interface AuthContextType {
  user: User | null
  login: (user: User) => void
  register: (userData: { username: string; email: string; password: string; first_name?: string; last_name?: string }) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)

  const login = (userData: User) => {
    setUser(userData)
    // In real app, save to localStorage or handle JWT tokens
    localStorage.setItem("user", JSON.stringify(userData))
  }

  const register = async (userData: { username: string; email: string; password: string; first_name?: string; last_name?: string }) => {
    try {
      const response = await fetch('/api/auth/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Qeydiyyat zamanı xəta baş verdi')
      }

      const data = await response.json()
      // Register uğurlu olduqdan sonra avtomatik login et
      login({
        id: data.user.id,
        name: `${data.user.first_name} ${data.user.last_name}`.trim() || data.user.username,
        email: data.user.email,
      })
    } catch (error) {
      console.error('Register error:', error)
      throw error
    }
  }

  const logout = () => {
    setUser(null)
    localStorage.removeItem("user")
  }

  const isAuthenticated = user !== null

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        register,
        logout,
        isAuthenticated,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}
