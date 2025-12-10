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
      <div className="app content-container paragraph">
        <p>Note not found. <Link to="/" className="link">Back to Notes</Link></p>
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

  const editNote = async (noteIndex) => {
    navigate(`/edit/${noteIndex}`)
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
        <span className="button-group as-fe">
          <button
            onClick={() => editNote(noteIndex)}
            className="button button-primary"
          >
            Edit
          </button>
          <button
            onClick={() => deleteNote(noteIndex)}
            className="button button-danger"
          >
            Delete
          </button>
        </span>
      </div>
    </div>
  )
}

export default Note