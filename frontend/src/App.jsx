import { useContext, useEffect, useState } from 'react'
import './App.css'
import useChat from './hooks/useChat'
import UserTextArea from './components/UserTextArea'
import UserChatBubble from './components/UserChatBubble'
import ChatbotChatBubble from './components/ChatbotChatBubble'
import SendButton from './components/SendButton'
import SidePanel from './components/SidePanel'
import ToggleSidePanelButton from './components/ToggleSidePanelButton'
import LoginModal from './components/LoginModal'
import LoginButton from './components/LoginButton'
import RegisterModal from './components/RegisterModal'
import LogoutButton from './components/LogoutButton'
import AuthContext from './context/AuthContext.jsx'
import UserIcon from './components/UserIcon.jsx'
import UserChat from './components/UserChat.jsx';
import NewChatButton from './components/NewChatButton.jsx'

function App() {
  const [ prompt, setPrompt ] = useState('');
  const [ toggleSidePanel, setSidePanel ] = useState(true);
  const { messages, handleUserInput, clearChat, chats, updateChatSidebar, updateUserChat, deleteUserChat } = useChat();
  const [ toggleLoginModal, setLoginModal ] = useState(false);
  const [ toggleRegisterModal, setRegisterModal ] = useState(false);

  const { user, firstName, lastName, checkAuth } = useContext(AuthContext);

  // User login persistence after refresh
  useEffect(() => {
    checkAuth();
    updateChatSidebar();
  }, []);

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
      {/* Login Modal */}
      {toggleLoginModal && <LoginModal onRegister={() => {setRegisterModal(true); setLoginModal(false);}} onClose={() => setLoginModal(false)} onLogin={clearChat}/>}

      {/* Register Modal */}
      {toggleRegisterModal && <RegisterModal onLogin={() => {setLoginModal(true); setRegisterModal(false)}} onClose={() => setRegisterModal(false)}/>}
      
      {/* Sidepanel */}
      <div className='sidePanelContainer'> 
        <div className='sidePanelWrapper'> 
          <SidePanel isOpen={toggleSidePanel}>
            <div className='sidePanelHeader'>
              <NewChatButton isOpen={toggleSidePanel} onClick={clearChat}/>
              <ToggleSidePanelButton isOpen={toggleSidePanel} onClick={handleToggleState} />
            </div>
              {user ?  <>
              <div className='userIconWrapper'>
                <UserIcon isOpen={toggleSidePanel} firstName={firstName} lastName={lastName} />
              </div>
              <LogoutButton onLogout={clearChat}/>
              {chats.map(chat => (
                <UserChat key={chat.chatID} title={chat.title} onClick={() => updateUserChat(chat.chatID)} onDelete={() => deleteUserChat(chat.chatID)}/>
              ))}
              </> : <LoginButton onClick={() => {setLoginModal(true); setRegisterModal(false)}}/> }
          </SidePanel>
        </div>
      </div>  

      {/* Input Area */}
      <div className='inputAreaContainer'>
        <div className='inputAreaWrapper'>
        <UserTextArea value={prompt} onChange={handlePromptChange} 
        onKeyDown={(e) => {
          if(e.key === 'Enter')
          {
            e.preventDefault();
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
