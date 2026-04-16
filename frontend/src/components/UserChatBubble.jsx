import { useState } from 'react'
import '../App.css'

export default function UserChatBubble({key, value}) {
  return(
    <>
    <textarea className='userChatBubble' key={key} value={value} readOnly></textarea>
    </>
  )
}
