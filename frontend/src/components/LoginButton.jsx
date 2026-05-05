import { useState } from 'react'
import '../App.css'

export default function LoginButton({onClick}) {
  return(
    <>  
      <button className='loginButton' onClick={onClick}>
        Login
      </button>
    </>
  )
}
