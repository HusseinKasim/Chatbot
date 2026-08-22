import { useContext, useEffect, useState } from 'react'
import './App.css'
import useChat from './hooks/useChat'
import UserTextArea from './components/UserTextArea'
import UserChatBubble from './components/UserChatBubble'
import ChatbotChatBubble from './components/ChatbotChatBubble'
import SendButton from './components/SendButton'
import SidePanel from './components/SidePanel'
import LoginModal from './components/LoginModal'
import RegisterModal from './components/RegisterModal'
import AuthContext from './context/AuthContext.jsx'
import UploadButton from './components/UploadButton.jsx'
import useUpload from './hooks/useUpload.jsx'
import { SidebarInset, SidebarProvider } from './components/ui/sidebar'

function App() {
  const [ prompt, setPrompt ] = useState('');
  const [ toggleLoginModal, setLoginModal ] = useState(false);
  const [ toggleRegisterModal, setRegisterModal ] = useState(false);

  const { messages, handleUserInput, clearChat, chats, updateChatSidebar, updateUserChat, deleteUserChat } = useChat();
  
  const { uploadDocument } = useUpload();

  const { user, firstName, lastName, checkAuth } = useContext(AuthContext);

  // User login persistence after refresh
  useEffect(() => {
    checkAuth();
    updateChatSidebar();
  }, []);

  function handlePromptChange(e) {
    setPrompt(e.target.value);
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
      {/* Login Modal */}
      {toggleLoginModal && <LoginModal onRegister={() => {setRegisterModal(true); setLoginModal(false);}} onClose={() => setLoginModal(false)} onLogin={clearChat} onLoginClose={() => setLoginModal(false)}/>}

      {/* Register Modal */}
      {toggleRegisterModal && <RegisterModal onLogin={() => {setLoginModal(true); setRegisterModal(false)}} onClose={() => setRegisterModal(false)}/>}
      
      {/* Sidepanel */}
      <SidebarProvider>
        <SidePanel user={user} firstName={firstName} lastName={lastName} chats={chats} clearChat={clearChat} updateUserChat={updateUserChat} deleteUserChat={deleteUserChat} setLoginModal={setLoginModal} setRegisterModal={setRegisterModal} />
        <SidebarInset className='relative flex min-h-svh flex-col'>
          
          {/* Chat Area */}
          <div className='min-h-0 flex-1 overflow-y-auto'>
            <div className='mx-auto flex w-[75%] flex-col gap-5 pb-32 pt-[4%]'>
              {messages.map((message) => {
                if(message.role === 'user')
                {
                return(
                  <div className='flex flex-col items-end'>
                    <UserChatBubble value={message.content} />
                  </div>
                  );
                }
                return(
                  <div className='flex flex-col items-start pb-5'>
                    <ChatbotChatBubble value={message.content} />
                  </div>
                  );
                }
              )}
            </div>
          </div>

          {/* Input Area */}
          <div className='absolute bottom-8 left-1/2 z-10 w-1/2 -translate-x-1/2'>
            <div className='relative'>
              <UploadButton onFileSelect={uploadDocument} />
              <UserTextArea value={prompt} onChange={handlePromptChange} 
              onKeyDown={(e) => {
                if(e.key === 'Enter')
                {
                  e.preventDefault();
                  handleSend(prompt);
                }
              }} isLoggedIn={user} 
              />
              <SendButton onClick={(e) => {
                handleSend(prompt);
              }}/>
            </div>
          </div>
        </SidebarInset>
      </SidebarProvider> 
    </>
  )
}

export default App;
