'use client'

import React, { createContext, useContext, useEffect, useState } from 'react'
import {
  User,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  GoogleAuthProvider,
  signInWithPopup,
  sendPasswordResetEmail,
} from 'firebase/auth'
import { auth } from '../firebase/config'
import { apiClient } from '../api/client'

interface AuthContextType {
  user: User | null
  loading: boolean
  signup: (email: string, password: string, name: string) => Promise<void>
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  loginWithGoogle: () => Promise<void>
  resetPassword: (email: string) => Promise<void>
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType)

export const useAuth = () => useContext(AuthContext)

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      setUser(user)
      
      if (user) {
        // Get Firebase token and send to backend
        const token = await user.getIdToken()
        apiClient.setAuthToken(token)
        
        // Sync user with backend
        try {
          await apiClient.post('/users/sync', {
            uid: user.uid,
            email: user.email,
            displayName: user.displayName,
            photoURL: user.photoURL,
          })
        } catch (error) {
          console.error('Error syncing user:', error)
        }
      } else {
        apiClient.setAuthToken(null)
      }
      
      setLoading(false)
    })

    return unsubscribe
  }, [])

  const signup = async (email: string, password: string, name: string) => {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password)
    // Update profile with name
    await apiClient.post('/users/sync', {
      uid: userCredential.user.uid,
      email: userCredential.user.email,
      displayName: name,
    })
  }

  const login = async (email: string, password: string) => {
    await signInWithEmailAndPassword(auth, email, password)
  }

  const logout = async () => {
    await signOut(auth)
  }

  const loginWithGoogle = async () => {
    const provider = new GoogleAuthProvider()
    await signInWithPopup(auth, provider)
  }

  const resetPassword = async (email: string) => {
    await sendPasswordResetEmail(auth, email)
  }

  const value = {
    user,
    loading,
    signup,
    login,
    logout,
    loginWithGoogle,
    resetPassword,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
