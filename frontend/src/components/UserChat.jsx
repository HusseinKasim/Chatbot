import { useState } from 'react'
import '../App.css'

export default function UserChat({isOpen, title}) {
  return(
    <>
    <button className={`userChat ${isOpen ? 'open' : 'close'}`}>
      {title}
    </button>
    </>
  )
}

 