import { Sidebar, SidebarHeader, SidebarContent, SidebarFooter, SidebarTrigger, useSidebar } from '@/components/ui/sidebar';
import NewChatButton from './NewChatButton';
import UserIcon from './UserIcon';
import LoginButton from './LoginButton';
import LogoutButton from './LogoutButton';
import UserChat from './UserChat';

export default function SidePanel({user, firstName, lastName, chats, clearChat, updateUserChat, deleteUserChat, setLoginModal, setRegisterModal}) {
  const { open } = useSidebar();

  return(
    <Sidebar collapsible='icon'>
      <SidebarHeader>
        <div className='grid grid-cols-[1fr_auto] items-center'>
          <NewChatButton isOpen={open} onClick={clearChat}/>
          <div className='flex justify-end pt-[10px]'>
            <SidebarTrigger />
          </div>
        </div>
        { user ? (
          <>
          <UserIcon isOpen={open} firstName={firstName} lastName={lastName} />
          </>
         ) : null }
      </SidebarHeader>

      <SidebarContent className={'pt-[20px]'}>
        {user ? (
          <>
            {chats.map(chat => (
              <UserChat key={chat.chatID} title={chat.title} onClick={() => updateUserChat(chat.chatID)} onDelete={() => deleteUserChat(chat.chatID)} />
            ))}
          </>
        ) : null }
      </SidebarContent>

      <SidebarFooter>
        {user ? <LogoutButton onLogout={clearChat} />
        : <LoginButton onClick={() => {setLoginModal(true); setRegisterModal(false) }} />}
      </SidebarFooter>
    </Sidebar>
  )
}
