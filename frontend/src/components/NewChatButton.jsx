import { useState } from 'react'
import '../App.css'

export default function NewChatButton({onClick}) {
  return(
    <>  
      <button className='newChatButton' onClick={onClick}>
        New Chat
      </button>
    </>
  )
}
