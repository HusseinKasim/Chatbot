import { useState } from 'react'
import '../App.css'

export default function SendButton({onClick}) {
  return(
    <>  
      <button className='sendButton' onClick={onClick}>
        <img src='/assets/send.png'/>
      </button>
    </>
  )
}
