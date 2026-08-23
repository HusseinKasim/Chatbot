import { Sidebar, SidebarHeader, SidebarContent, SidebarFooter, SidebarTrigger, useSidebar, SidebarGroup } from '@/components/ui/sidebar';
import NewChatButton from './NewChatButton';
import UserIcon from './UserIcon';
import LoginButton from './LoginButton';
import LogoutButton from './LogoutButton';
import UserChat from './UserChat';
import { useState } from 'react';

export default function SidePanel({user, firstName, lastName, chats, clearChat, updateUserChat, deleteUserChat, setLoginModal, setRegisterModal}) {
  const { open } = useSidebar();
  const [ selectedChat, setSelectedChat ] = useState(null);

  return(
    <Sidebar collapsible='icon'>
      <SidebarHeader>
        <div className='grid grid-cols-[1fr_auto] items-center'>
          <NewChatButton isOpen={open} onClick={clearChat}/>
          <div className='flex justify-end pt-[10px]'>
            <SidebarTrigger className='text-[var(--color-text)] hover:bg-[var(--color-chats-hover)]'/>
          </div>
        </div>
        { user ? (
          <>
          <UserIcon isOpen={open} firstName={firstName} lastName={lastName} />
          </>
         ) : null }
      </SidebarHeader>

      <SidebarContent className='pt-[20px]'>
        <SidebarGroup>
        {user ? (
          <>
            <div className='pl-[15px] text-[var(--color-text-muted)]'>
              <text>Recent Chats</text>
            </div>
            {chats.map(chat => (
              <UserChat key={chat.chatID} title={chat.title} onClick={() => {
                setSelectedChat(chat.chatID);
                updateUserChat(chat.chatID);
              }
            } onDelete={() => deleteUserChat(chat.chatID)} isSelected={selectedChat == chat.chatID}/>
            ))}
          </>
        ) : null }
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter>
        {user ? <LogoutButton onLogout={clearChat} />
        : <LoginButton onClick={() => {setLoginModal(true); setRegisterModal(false) }} />}
      </SidebarFooter>
    </Sidebar>
  )
}
