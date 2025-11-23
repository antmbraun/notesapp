import { useParams, Link, useLocation, useNavigate } from 'react-router-dom'

function Note() {
  const { index } = useParams()
  const location = useLocation()
  const navigate = useNavigate()
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

  const deleteNote = async (noteIndex) => {
    if (!confirm('Are you sure you want to delete this note?')) {  
      return
    }
    try {
      const response = await fetch(`/api/notes/${noteIndex}`, {
        method: 'DELETE',
      })
      if (!response.ok) {
        throw new Error('Failed to delete note')
      }
      navigate('/')
    }
    catch (error) {
      console.error('Error deleting note:', error)
    }
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

        <button 
          onClick={() => deleteNote(noteIndex)}
          className="button button-danger as-fe"
        >
          Delete
        </button>
      </div>
    </div>
  )
}

export default Note