import { useState } from 'react'
import '../App.css'
import deleteIcon from '/assets/delete.png'

export default function UserChat({isOpen, title, onClick, onDelete}) {
  return(
    <>
    <div className='userChatWrapper'>
      <button className={`userChat ${isOpen ? 'open' : 'close'}`} onClick={onClick}>
        {title}
      </button>
      
      <button className='deleteChatButton' onClick={onDelete}>
        <img src={deleteIcon}/>
      </button>

    </div>
    </>
  )
}

 