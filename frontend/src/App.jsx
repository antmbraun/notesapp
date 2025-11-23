import { useState, useEffect } from 'react'
import { Routes, Route, Link, useNavigate } from 'react-router-dom'
import './scss/main.scss'
import Noteform from './components/Noteform'
import Note from './components/Note'
import Header from './components/Header'

const API_URL = import.meta.env.DEV ? '/api' : 'http://localhost:8000'

function HomePage() {
  const [notes, setNotes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

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

  console.log(notes)

  useEffect(() => {
    fetchNotes()
  }, [])

  if (loading) return <div>Loading notes...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <div className="content-container">
      <div className="note-grid">
      {notes.length === 0 ? (
        <p>
          No notes yet.{' '}
          <Link className="link" to="/add" onClick={() => setShowNoteForm(true)}>
            Create your first note!
          </Link>
        </p>
      ) : (
        notes.map((note, index) => (
          <Link
            to={`/notes/${index}`}
            state={{ notes, noteIndex: index }}
            key={index}
            className="note-card"
          >
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
          </Link>
          ))
        )}
      </div>
    </div>
  )
}

function App() {
  return (
    <div className="app">
      <Header />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/add" element={<Noteform />} />
        <Route path="/notes/:index" element={<Note />} />
      </Routes>
    </div>
  )
}

export default App