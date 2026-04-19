import { useState } from 'react'
import '../App.css'

export default function ChatbotChatBubble({key, value}) {
  return(
    <>
    <div className='chatbotChatBubble' key={key}>{value}</div>
    </>
  )
}

 