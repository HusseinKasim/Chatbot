import { useState } from 'react'
import '../App.css'

export default function UserChatBubble({key, value}) {
  return(
    <>
    <div className='userChatBubble' key={key}>{value}</div>
    </>
  )
}
