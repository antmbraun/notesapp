import { useState, useEffect } from 'react'
import { Routes, Route, Link} from 'react-router-dom'
import './scss/main.scss'
import Noteform from './components/Noteform'
import Note from './components/Note'
import Header from './components/Header'
import NotFound from './components/NotFound'

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
  }

  useEffect(() => {
    fetchNotes()
  }, [])

  if (loading) {
    return <div className="content-container"><p className="">Loading notes...</p></div>
  }
  if (error) {
    return <div className="content-container"><p className="">{error}</p></div>  
  }


  return (
    <div className="content-container">
      {notes.length === 0 ? (
        <p>
          No notes yet.{' '}
          <Link className="link" to="/add" onClick={() => setShowNoteForm(true)}>
            Create your first note!
          </Link>
        </p>
      ) : (
        <div className="note-grid">
          {notes.map((note, index) => (
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
          ))}
        </div>
      )}
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
        <Route path="*" element={<NotFound />} />
      </Routes>
    </div>
  )
}

export default App