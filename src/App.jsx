import { useState } from 'react'
import './App.css'

function App() {
  const [prompt, setPrompt] = useState('');
  const [userMessage, setUserMessage] = useState() // TEST

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
    setUserMessage(<UserChatBubble value={prompt}/>); // TEST
  }

  return (
    <>
    <div className='container'>
      <UserTextArea value={prompt} onChange={handleChangePrompt}/>
      <SendButton onClick={(e) => {
        if(prompt != null && prompt != ""){ // Check for empty prompt
          sendUserInput(e);
        }
      }}/>
    </div>

    <div>
      {userMessage}
    </div>
    </> // userMessage is a TEST
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

function UserChatBubble({value}) { // textarea is a TEST
  return(
    <>
    <textarea className='userChatBubble' value={value} readOnly></textarea>
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
