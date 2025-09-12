"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { X, Eye, EyeOff } from "lucide-react"
import { useAuth } from "@/contexts/auth-context"

interface AuthModalProps {
  isOpen: boolean
  onClose: () => void
  mode: "login" | "register"
  onModeChange: (mode: "login" | "register") => void
}

export function AuthModal({ isOpen, onClose, mode, onModeChange }: AuthModalProps) {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    name: "",
    confirmPassword: "",
  })
  const [isLoading, setIsLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const { login, register } = useAuth()

  if (!isOpen) return null

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      if (mode === "register") {
        if (formData.password !== formData.confirmPassword) {
          alert("Şifrələr uyğun gəlmir!")
          return
        }
        // Email-dən username yaratmaq
        const username = formData.email.split('@')[0].replace(/[^a-zA-Z0-9]/g, '') + Math.floor(Math.random() * 1000)
        
        await register({
          username: username, 
          email: formData.email,
          first_name: formData.name.split(" ")[0] || "",
          last_name: formData.name.split(" ").slice(1).join(" ") || "",
          password: formData.password,
        })
      } else {
        // Login logic will be implemented with Django backend
        login({
          id: 1,
          name: formData.name || "İstifadəçi",
          email: formData.email,
        })
        console.log("Login:", formData)
      }
      onClose()
    } catch (error) {
      console.error("Auth error:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }))
  }

  return (
    <div className="fixed inset-0 z-[9999] overflow-hidden">
      <div className="absolute inset-0 bg-black bg-opacity-50" onClick={onClose} />
      <div className="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 w-full max-w-md bg-white rounded-lg shadow-xl">
        <div className="p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold">{mode === "login" ? "Giriş" : "Qeydiyyat"}</h2>
            <Button variant="ghost" size="sm" onClick={onClose}>
              <X className="h-5 w-5" />
            </Button>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {mode === "register" && (
              <div>
                <Label htmlFor="name">Ad Soyad</Label>
                <Input
                  id="name"
                  name="name"
                  type="text"
                  required
                  value={formData.name}
                  onChange={handleInputChange}
                  placeholder="Adınızı daxil edin"
                />
              </div>
            )}

            <div>
              <Label htmlFor="email">E-mail</Label>
              <Input
                id="email"
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={handleInputChange}
                placeholder="E-mail ünvanınızı daxil edin"
              />
            </div>

            <div>
              <Label htmlFor="password">Şifrə</Label>
              <div className="relative">
                <Input
                  id="password"
                  name="password"
                  type={showPassword ? "text" : "password"}
                  required
                  value={formData.password}
                  onChange={handleInputChange}
                  placeholder="Şifrənizi daxil edin"
                  className="pr-10"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 focus:outline-none"
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>

            {mode === "register" && (
              <div>
                <Label htmlFor="confirmPassword">Şifrəni Təkrarla</Label>
                <div className="relative">
                  <Input
                    id="confirmPassword"
                    name="confirmPassword"
                    type={showConfirmPassword ? "text" : "password"}
                    required
                    value={formData.confirmPassword}
                    onChange={handleInputChange}
                    placeholder="Şifrənizi təkrar daxil edin"
                    className="pr-10"
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 focus:outline-none"
                  >
                    {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>
            )}

            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? "Gözləyin..." : mode === "login" ? "Giriş Et" : "Qeydiyyatdan Keç"}
            </Button>
          </form>

          {/* Switch Mode */}
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              {mode === "login" ? "Hesabınız yoxdur?" : "Artıq hesabınız var?"}
              <Button
                variant="link"
                className="ml-1 p-0 h-auto"
                onClick={() => onModeChange(mode === "login" ? "register" : "login")}
              >
                {mode === "login" ? "Qeydiyyatdan keçin" : "Giriş edin"}
              </Button>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
