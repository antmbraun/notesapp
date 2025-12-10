import { useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'

function HomePage({ notes, loading, error, fetchNotes }) {
  const location = useLocation()

  useEffect(() => {
    // Refresh notes whenever we navigate to the home page
    if (location.pathname === '/') {
      fetchNotes()
    }
  }, [location.pathname, fetchNotes])

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
          <Link className="link" to="/add">
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

              <p className="note-card-preview">
                {
                  note.content.length < 100 ? note.content :
                    note.summary && note.summary !== 'No summary available' ? note.summary :
                      note.content.slice(0, 100) + '...'
                }
              </p>

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

export default HomePage