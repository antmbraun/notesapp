import { useParams, Link, useLocation } from 'react-router-dom'

function Note() {
  const { index } = useParams()
  const location = useLocation()
  const notes = location.state?.notes || []
  const noteIndex = parseInt(index, 10)
  const note = notes[noteIndex]

  if (!note) {
    return (
      <div className="app">
        <Link to="/" className="back-button">← Back to Notes</Link>
        <div>Note not found</div>
      </div>
    )
  }

  return (
    <div className="content-container">
      <div className="note-detail">
        {note.title && <h1 className="note-title">{note.title}</h1>}
        {note.updated_at && (
          <small>
            Updated: {new Date(note.updated_at).toLocaleString()}
          </small>
        )}
        {note.summary && (
          <div className="note-summary">
            <strong>Summary:</strong> {note.summary}
          </div>
        )}
        <div className="note-content">
          <p>{note.content}</p>
        </div>

        {note.created_at && (
          <small>
            Created: {new Date(note.created_at).toLocaleString()}
          </small>
        )}
      </div>
    </div>
  )
}

export default Note