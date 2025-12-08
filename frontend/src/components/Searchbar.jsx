import { useState } from 'react'

function Searchbar() {
  const [searchQuery, setSearchQuery] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    console.log(searchQuery)
  }

  return (
    <form className="searchbar" onSubmit={handleSubmit}>
      <input type="text" placeholder="Search" value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} />
    </form>
  )
}

export default Searchbar