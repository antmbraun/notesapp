import { useState, useEffect, useCallback } from 'react'
import { Routes, Route } from 'react-router-dom'
import './scss/main.scss'
import Noteform from './components/Noteform'
import Note from './components/Note'
import Header from './components/Header'
import NotFound from './components/NotFound'
import HomePage from './components/HomePage'

const API_URL = import.meta.env.DEV ? '/api' : 'http://localhost:8000'

function App() {
  const [notes, setNotes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchNotes = useCallback(async () => {
    try {
      setLoading(true)
      const response = await fetch(`${API_URL}/notes`)
      if (!response.ok) {
        throw new Error('Failed to fetch notes. Are you sure the API is running?')
      }
      const data = await response.json()
      setNotes(data)
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchNotes()
  }, [fetchNotes])

  return (
    <div className="app">
      <Header notes={notes} />
      <Routes>
        <Route path="/" element={<HomePage notes={notes} loading={loading} error={error} fetchNotes={fetchNotes} />} />
        <Route path="/add" element={<Noteform />} />
        <Route path="/notes/:index" element={<Note />} />
        <Route path="/edit/:index" element={<Noteform notes={notes} />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </div>
  )
}

export default App