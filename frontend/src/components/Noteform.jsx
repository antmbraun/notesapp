import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'

function Noteform() {
  const navigate = useNavigate()
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setIsSubmitting(true)

    try {
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

      // Reset form
      setTitle('')
      setContent('')
      
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
    const titleField = document.querySelector('input[type="text"]')
    if (titleField) {
      titleField.focus()
    }
  }, [])

  return (
    <div className="content-container">
      {error && <div className="error-message">{error}</div>}

      <form onSubmit={handleSubmit}>
        <Link to="/" className="back-button as-fe">
            Cancel
        </Link>
        <input 
          type="text" 
          placeholder="Title (optional)" 
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          disabled={isSubmitting}
        />
        <textarea 
          placeholder="Content" 
          value={content}
          onChange={(e) => setContent(e.target.value)}
          required
          disabled={isSubmitting}
          style={{ height: '50vh' }}
        />
        <button type="submit" disabled={isSubmitting || !content.trim()}>
          {isSubmitting ? 'Adding...' : 'Add note'}
        </button>

      </form>
    </div>
  )
}

export default Noteform