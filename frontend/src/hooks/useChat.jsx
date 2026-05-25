import {useState, useContext, useEffect} from 'react'
import '../App.css'
import AuthContext from '../context/AuthContext';

export default function useChat()
{
    const [messages, setMessages] = useState([
        {'role': 'assistant', 'content': 'Hello! Please enter a prompt.'} 
    ])
    const [chatID, setChatID] = useState(0);
    const [chats, setChats] = useState([
        {'chatID': 0, 'title': 'New Chat'}
    ])
    const { user } = useContext(AuthContext);

    useEffect(() => {
        if(user){
            updateChatSidebar();
        }
        else{
            setChats([{'chatID': 0, 'title': 'New Chat'}]);
            setMessages([{'role': 'assistant', 'content': 'Hello! Please enter a prompt.'}]);
            setChatID(0);
        }
    }, [user]);

    async function handleUserInput(prompt){
        if(user == null)
        {
            handleGuestInput(prompt);
        }
        else
        {
            handleLoggedInUserInput(prompt);
        }
    }

    function clearChat(){
        setMessages([
            {'role': 'assistant', 'content': 'Hello! Please enter a prompt.'} 
        ]);
        
        setChatID(0);
    }

    async function handleGuestInput(prompt){
        // Add prompt to messages list
        const updatedMessages = [...messages, {'role': 'user', 'content': prompt}]
        setMessages(updatedMessages);

        // Send prompt to backend via HTTP POST
        const response = await fetch('/api/guest-prompt', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ messages: updatedMessages }),
        credentials: 'include'
        })

        // Return and print data from backend
        const data = await response.json();

        // Add response to messages list 
        setMessages(prev => [...prev, {'role': 'assistant', 'content': data.response}])
    }

    async function handleLoggedInUserInput(prompt)
    {
        // Send prompt to backend via HTTP POST
        const response = await fetch('/api/user-prompt', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ prompt: prompt, chatID: chatID }),
        credentials: 'include'
        })

        // Return and print data from backend
        const data = await response.json();
        
        // Update ChatID if it was null
        setChatID(data.chatID);
        
        setMessages(prev => [...prev, {'role': 'user', 'content': prompt}]);
        setMessages(prev => [...prev, {'role': 'assistant', 'content': data.response}]);
    }

    async function updateChatSidebar(){
        // Fetch user chats from backend via HTTP GET
        const response = await fetch('/api/user-chats', {
        method: 'GET',
        credentials: 'include'
        })

        const data = await response.json();
        if(data.chats != null)
        {
            setChats(
                data.chats.map(chat => ({
                    chatID: chat.id,
                    title: chat.chat_title
                }))
            );
        }
    }

    async function updateUserChat(chatID){
        setChatID(chatID);
        
        // Fetch chat messages from backend via HTTP GET
        const response = await fetch(`/api/chat-messages?chatID=${chatID}`, {
        method: 'GET',
        credentials: 'include'
        })
        
        const data = await response.json();
        if(data.messages != null)
        {
            setMessages(
                data.messages.map(message => ({
                    role: message.role,
                    content: message.message_text
                }))
            )
        }
    }

    async function deleteUserChat(chatID){
        // Delete user chat from DB via HTTP DELETE
        const response = await fetch(`/api/chat-delete?chatID=${chatID}`, {
        method: 'DELETE',
        credentials: 'include'
        })

        // Add error handling for when no response 
        const data = await response.json();
    }

    return { messages, handleUserInput, clearChat, chats, updateChatSidebar, updateUserChat, deleteUserChat };
}
