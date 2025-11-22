import { useState } from 'react'

function Noteform({ onSubmit, onCancel }) {
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

      const data = await response.json()
      
      // Reset form
      setTitle('')
      setContent('')
      
      // Notify parent component
      if (onSubmit) {
        onSubmit(data.note)
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div>
      <h1>Add a new note</h1>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit}>
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
        />
        <button type="submit" disabled={isSubmitting || !content.trim()}>
          {isSubmitting ? 'Adding...' : 'Add note'}
        </button>
        {onCancel && (
          <button type="button" onClick={onCancel} disabled={isSubmitting}>
            Cancel
          </button>
        )}
      </form>
    </div>
  )
}

export default Noteform