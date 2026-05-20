import { useState } from 'react'
import '../App.css'

export default function UserChat({key, title}) {
  return(
    <>
    <button className='userChat' key={key}>{title}</button>
    </>
  )
}

 