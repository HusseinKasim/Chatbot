import { useState } from 'react'
import './App.css'
import useChat from './hooks/useChat'
import UserTextArea from './components/UserTestArea'
import UserChatBubble from './components/UserChatBubble'
import ChatbotChatBubble from './components/ChatbotChatBubble'
import SendButton from './components/SendButton'
import SidePanel from './components/SidePanel'
import ToggleSidePanelButton from './components/ToggleSidePanelButton'

function App() {
  const [ prompt, setPrompt ] = useState('');
  const [ toggleSidePanel, setSidePanel ] = useState(true);
  const { messages, handleUserInput } = useChat();

  function handlePromptChange(e) {
    setPrompt(e.target.value);
  }

  function handleToggleState()
  {
    setSidePanel(!toggleSidePanel);
  }

  function handleSend(prompt)
  {
    // Check for empty prompt
    if(prompt != null && prompt != '')
    { 
      handleUserInput(prompt);
      setPrompt('')
    }
  }

  return (
    <>
    <div className="container">
      {/* Sidepanel */}
      <div className='sidePanelContainer'> 
        <div className='sidePanelWrapper'> 
          <SidePanel isOpen={toggleSidePanel} />
          <div className='sidePanelHeader'>
            <ToggleSidePanelButton isOpen={toggleSidePanel} onClick={handleToggleState} />
          </div>
        </div>
      </div>  

      {/* Input Area */}
      <div className='inputAreaContainer'>
        <div className='inputAreaWrapper'>
        <UserTextArea value={prompt} onChange={handlePromptChange} 
        onKeyDown={(e) => {
          if(e.key === 'Enter')
          {
            handleSend(prompt);
          }
        }}/>
        <SendButton onClick={(e) => {
          handleSend(prompt);
        }}/>
        </div>
      </div>

        {/* Chat Area */}
      <div className='chatAreaContainer'>
        <div className='bubblesContainer'>
      {messages.map((message) => {
        if(message.role === 'user')
        {
          return(
                    <div className='userChatBubbleContainer'>
                      <UserChatBubble value={message.content} />
                    </div>
            );
        }
        return(
                <div className='chatbotChatBubbleContainer'>
                  <ChatbotChatBubble value={message.content} />
                </div>
          );
        }
      )}
      </div>
    </div>
    </div>
    </>
  )
}

export default App;
