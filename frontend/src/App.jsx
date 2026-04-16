import { useState } from 'react'
import './App.css'
import UserTextArea from './components/UserTestArea'
import UserChatBubble from './components/UserChatBubble'
import ChatbotChatBubble from './components/ChatbotChatBubble'
import SendButton from './components/SendButton'

function App() {
  const [prompt, setPrompt] = useState('');
  const [userMessage, setUserMessage] = useState([])
  const [chatbotMessage, setChatbotMessage] = useState([])

  function handleChangePrompt(e) {
    setPrompt(e.target.value);
  }

  async function sendUserInput(e) {
    e.preventDefault();

    // Send prompt to backend via HTTP POST
    const response = await fetch("http://127.0.0.1:8003/api/capture-prompt", {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ prompt }),
    })

    // Return and print data from backend
    const data = await response.json();
    console.log(data["response"]["prompt"]);

    // Clear textarea
    setPrompt('');

    // Create user chat bubble
    setUserMessage(prev => [...prev, prompt]);

    // Create chatbot chat bubble
    setChatbotMessage(prev => [...prev, data["response"]["prompt"]]);
  }

  return (
    <>
    <div className='inputContainer'>
      <UserTextArea value={prompt} onChange={handleChangePrompt}/>
      <SendButton onClick={(e) => {
        // Check for empty prompt
        if(prompt != null && prompt != ""){ 
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

      <div className='chatbotBubblesContainer'>
      {chatbotMessage.map((message, index) => (
          <ChatbotChatBubble key={index} value={message} />
        ))}
        </div>
    </div>
    </>
  )
}

export default App;
