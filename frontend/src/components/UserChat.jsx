import { useState } from 'react'
import '../App.css'

export default function UserChat({isOpen, title, onClick}) {
  return(
    <>
    <button className={`userChat ${isOpen ? 'open' : 'close'}`} onClick={onClick}>
      {title}
    </button>
    </>
  )
}

 