import { useState, useEffect } from 'react'
import './scss/main.scss'
import Noteform from './components/Noteform'

const API_URL = import.meta.env.DEV ? '/api' : 'http://localhost:8000'

function App() {
  const [notes, setNotes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showNoteForm, setShowNoteForm] = useState(false)

  const fetchNotes = async () => {
    try {
      setLoading(true)
      const response = await fetch(`${API_URL}/notes`)
      if (!response.ok) {
        throw new Error('Failed to fetch notes')
      }
      const data = await response.json()
      setNotes(data)
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  // Fetch notes on mount
  useEffect(() => {
    fetchNotes()
  }, [])

  // Refresh notes when returning to homepage from form
  useEffect(() => {
    if (!showNoteForm) {
      fetchNotes()
    }
  }, [showNoteForm])

  const handleNoteCreated = () => {
    // Close form and refresh notes
    setShowNoteForm(false)
    fetchNotes()
  }

  const handleCancel = () => {
    setShowNoteForm(false)
  }

  if (loading) return <div>Loading notes...</div>
  if (error) return <div>Error: {error}</div>

  if (showNoteForm) {
    return (
      <div className="app">
        <button className="back-button" onClick={handleCancel}>← Back to Notes</button>
        <Noteform onSubmit={handleNoteCreated} onCancel={handleCancel} />
      </div>
    )
  }

  return (
    <div className="app">
      <h1>Notes App</h1>
      <div className="notes-container">
        {notes.length === 0 ? (
          <p>
            No notes yet.{' '}
            <a 
              className="link"
              href="#" 
              onClick={(e) => {
                e.preventDefault()
                setShowNoteForm(true)
              }}
            >
              Create your first note!
            </a>
          </p>
        ) : (
          notes.map((note, index) => (
            <a href={`/notes/${note.id}`} key={index} className="note-card">
              {note.title && <h2>{note.title}</h2>}
              {note.summary && (
                <p className="summary">
                 {note.summary}
                </p>
              )}
              {note.created_at && (
                <small>
                  Created: {new Date(note.created_at).toLocaleString()}
                </small>
              )}
            </a>
          ))
        )}
      </div>
      <button className="button-primary" onClick={() => setShowNoteForm(true)}>Add a new note</button>
    </div>
  )
}

export default App