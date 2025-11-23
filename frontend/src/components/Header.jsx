import { Link, useLocation } from 'react-router-dom'
import { FaPlus } from 'react-icons/fa'

function Header() {
  const location = useLocation()
  const isAddPage = location.pathname === '/add'

  return (
    <header className="header">
      <Link to="/" className="header-title">
        <h1>Notes App</h1>
      </Link>
      {!isAddPage && (
        <Link to="/add">
          <FaPlus className="add-icon" />
        </Link>
      )}
    </header>
  )
}

export default Header