import { useState } from 'react'
import './App.css'

function App() {
  const [prompt, setPrompt] = useState('');
  const [userMessage, setUserMessage] = useState([])

  function handleChangePrompt(e) {
    setPrompt(e.target.value);
  }

  function sendUserInput(e) {
    e.preventDefault();

    // Send prompt to backend via HTTP POST
    fetch("http://127.0.0.1:8003/capture_prompt", {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ prompt }),
    })

    // Clear textarea
    setPrompt('');

    // Create user chat bubble
    setUserMessage(prev => [...prev, prompt]);
  }

  return (
    <>
    <div className='inputContainer'>
      <UserTextArea value={prompt} onChange={handleChangePrompt}/>
      <SendButton onClick={(e) => {
        if(prompt != null && prompt != ""){ // Check for empty prompt
          sendUserInput(e);
        }
      }}/>
    </div>

    <div className='chatAreaContainer'>
      <div className='chatBubblesContainer'>
        {userMessage.map((message, index) => (
          <UserChatBubble key={index} value={message} />
        ))}
      </div>
    </div>
    </>
  )
}

function UserTextArea({value, onChange}) {
  return(
    <>
    <textarea className='userTextArea' value={value} onChange={onChange} placeholder='Ask a question...'></textarea>
    </>
  )
}

function SendButton({onClick}) {
  return(
    <>
      <button className='sendButton' onClick={onClick}>Send</button>
    </>
  )
}

function UserChatBubble({key, value}) {
  return(
    <>
    <textarea className='userChatBubble' key={key} value={value} readOnly></textarea>
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
