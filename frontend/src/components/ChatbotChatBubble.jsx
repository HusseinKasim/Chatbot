import { useState } from 'react'
import '../App.css'

export default function ChatbotChatBubble({key, value}) {
  return(
    <>
    <textarea className='chatbotChatBubble' key={key} value={value} readOnly></textarea>
    </>
  )
}

 