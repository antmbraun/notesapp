import { useState, useEffect } from 'react'
import { useNavigate, Link, useLocation } from 'react-router-dom'

function Noteform({ notes }) {
  const navigate = useNavigate()
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState(null)
  const location = useLocation()
  const pathname = location.pathname
  const noteIndex = parseInt(location.pathname.split('/').pop(), 10)

  useEffect(() => {
    // If editing, set the form to the note data
    if (pathname.includes('edit')) {
      const note = notes[noteIndex]
      if (note) {
        setTitle(note.title || '')
        setContent(note.content || '')
      }
    }
    // If adding, reset form
    else {
      setTitle('')
      setContent('')
    }
  }, [pathname, notes, location.pathname, noteIndex])

  const handleSubmit = async (e) => {
    const form = e.target

    // Check HTML5 validation before preventing default
    // This allows browser to show validation messages properly
    if (!form.checkValidity()) {
      form.reportValidity()
      e.preventDefault()
      return
    }

    e.preventDefault()

    // Additional check for whitespace-only content
    if (!content.trim()) {
      const textarea = form.querySelector('textarea')
      if (textarea) {
        console.log('Content cannot be empty')
        textarea.setCustomValidity('Content cannot be empty')
        textarea.reportValidity()

        textarea.oninput = () => {
          textarea.setCustomValidity('')
          textarea.reportValidity()
        }
      }
      return
    }

    setError(null)
    setIsSubmitting(true)

    try {
      // If editing, update the note 
      if (pathname.includes('edit')) {
        const response = await fetch(`/api/notes/${noteIndex}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            title: title.trim() || null,
            content: content.trim(),
          }),
        })

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.detail || 'Failed to update note')
        }

      }

      // If adding, create a new note
      else {
        const response = await fetch('/api/notes', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            title: title.trim() || null,
            content: content.trim(),
          }),
        })

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.detail || 'Failed to create note')
        }
      }


      // Navigate back to home page
      navigate('/')
    } catch (err) {
      setError(err.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  // On load give focus to title field
  useEffect(() => {
    const titleField = document.querySelector('.note-form input[type="text"]')
    if (titleField) {
      titleField.focus()
    }
  }, [])

  return (
    <div className="content-container">
      {error && <div className="error-message">{error}</div>}

      <form className="note-form" onSubmit={handleSubmit}>
        <button onClick={() => navigate('/')} className="button button-secondary as-fe">
          Cancel
        </button>
        <input
          type="text"
          placeholder="Title (optional)"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          disabled={isSubmitting}
        />
        <textarea
          name="content"
          placeholder="Content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          required
          disabled={isSubmitting}
          style={{ height: '50vh' }}
        />
        <button type="submit" disabled={isSubmitting} className="button button-primary as-fe">
          {isSubmitting ? 'Saving...' : 'Save'}
        </button>

      </form>
    </div>
  )
}

export default Noteform