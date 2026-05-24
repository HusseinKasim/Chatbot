import { useState } from 'react'
import '../App.css'

export default function NewChatButton({isOpen, onClick}) {
  return(
    <>  
      <button className={isOpen ? 'newChatButton open' : 'newChatButton close'} onClick={onClick}>
        <img src='/assets/add.png'/>
        {
          isOpen ? <>
            New Chat
          </>
          :
          <>
          </>
        }
      </button>
    </>
  )
}
