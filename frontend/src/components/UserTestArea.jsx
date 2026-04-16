import { useState } from 'react'
import '../App.css'

export default function UserTextArea({value, onChange}) {
  return(
    <>
    <textarea className='userTextArea' value={value} onChange={onChange} placeholder='Ask a question...'></textarea>
    </>
  )
}

