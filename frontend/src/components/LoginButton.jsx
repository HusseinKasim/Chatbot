import { useState } from 'react'
import '../App.css'

export default function LoginButton({isOpen, onClick}) {
  return(
    <>  
      <button className='loginButton' onClick={onClick}>
        Login
      </button>
    </>
  )
}
