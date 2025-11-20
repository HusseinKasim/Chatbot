import { useState } from 'react'
import './App.css'

function App() {
  return (
    <>
    <div class='container'>
      <UserTextArea />
      <SendButton />
    </div>
    </>
  )
}

function UserTextArea() {
  return(
    <>
    <textarea className='userTextArea' placeholder='Ask a question...'></textarea>
    </>
  )
}

function SendButton() {
  return(
    <>
    <button className='sendButton'>Send</button>
    </>
  )
}

function UserChatBubble() {
  return(
    <>
    </>
  )
}

function ChatbotChatBubble() {
  return(
    <>
    </>
  )
}

export default App
