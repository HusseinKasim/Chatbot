import { useState } from 'react'
import './App.css'
import useChat from './hooks/useChat'
import UserTextArea from './components/UserTestArea'
import UserChatBubble from './components/UserChatBubble'
import ChatbotChatBubble from './components/ChatbotChatBubble'
import SendButton from './components/SendButton'

function App() {
  const [prompt, setPrompt] = useState('');
  const { messages, handleUserInput } = useChat();

  function handlePromptChange(e) {
    setPrompt(e.target.value);
  }

  return (
    <>
    <div className='inputContainer'>
      <UserTextArea value={prompt} onChange={handlePromptChange}/>
      <SendButton onClick={(e) => {
        // Check for empty prompt
        if(prompt != null && prompt != ''){ 
          handleUserInput(prompt);
          setPrompt('')
        }
      }}/>
    </div>

    <div className='chatAreaContainer'>
    {messages.map((message) => {
      if(message.role === 'user')
      {
        return(
                <div className='chatBubblesContainer'>
                  <UserChatBubble value={message.content} />
                </div>
          );
      }
      return(
            <div className='chatbotBubblesContainer'>
              <ChatbotChatBubble value={message.content} />
            </div>
        );
      }
    )}
    </div>
    </>
  )
}

export default App;
