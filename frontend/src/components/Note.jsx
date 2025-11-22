//  Display the note as single component

function Note({ note }) {
  return (
    <div className="note">
      <h2>{note.title}</h2>
      <p>{note.content}</p>
    </div>
  )
}

export default Note;