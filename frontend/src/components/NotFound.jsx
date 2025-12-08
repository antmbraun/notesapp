import { Link } from 'react-router-dom'

function NotFound() {
  return (

    <div className="content-container">
      <div className="not-found">
        <h1>404 - Page Not Found</h1>
        <p>The page you are looking for does not exist.</p>
        <Link to="/" className="link">Back to Notes</Link>
      </div>
    </div>
  )
}

export default NotFound