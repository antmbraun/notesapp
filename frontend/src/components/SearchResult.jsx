import { Link } from 'react-router-dom'

function SearchResult({ note, index, query }) {

  
  // Filter the note content so that we only display the part of the content that contains the query
  // Content is a string, so we need to find the query in the content and return the 20 characters before and after the query
    // Find the query in the content (case-insensitive)
  const queryLower = query.toLowerCase()
  const contentLower = note.content.toLowerCase()
  const queryIndex = contentLower.indexOf(queryLower)

 // Get snippet: 20 characters before and after the query, or first 40 chars if query not found
 let resultSnippet
 if (queryIndex !== -1) {
   const start = Math.max(0, queryIndex - 20)
   const end = Math.min(note.content.length, queryIndex + query.length + 20)
   resultSnippet = note.content.slice(start, end)
   // Add ellipsis if needed
   if (start > 0) resultSnippet = '...' + resultSnippet
   if (end < note.content.length) resultSnippet = resultSnippet + '...'
 } else {
   // Fallback: show first 40 characters
   resultSnippet = note.content.slice(0, 40) + (note.content.length > 40 ? '...' : '')
  }

  return (
    <div className="search-result">
      <Link to={`/notes/${index}`} key={index} className="link">
        {note.title && <h2>{note.title}</h2>}
        <p>{resultSnippet}</p>
      </Link>
    </div>
  )
}

export default SearchResult