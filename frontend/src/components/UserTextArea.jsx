import { useState } from 'react'
import '../App.css'

export default function UserTextArea({value, onChange, onKeyDown}) {
  return(
    <>
    <textarea className='userTextArea' value={value} onChange={onChange} onKeyDown={onKeyDown} placeholder='Ask a question...'></textarea>
    </>
  )
}

