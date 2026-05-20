import {useState, useContext} from 'react'
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

    async function handleUserInput(prompt){
        if(user == null)
        {
            handleGuestInput(prompt);
        }
        else
        {
            handleLoggedInUserInput(prompt, chatID);
            updateChatSidebar(chats);
        }
    }

    function clearChat(){
        setMessages([
            {'role': 'assistant', 'content': 'Hello! Please enter a prompt.'} 
        ]);
    }

    async function handleGuestInput(prompt){
        // Add prompt to messages list
        const updatedMessages = [...messages, {'role': 'user', 'content': prompt}]
        setMessages(updatedMessages);

        // Send prompt to backend via HTTP POST
        const response = await fetch('/api/process-guest-prompt', {
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

    async function handleLoggedInUserInput(prompt, chatID)
    {
        // Send prompt to backend via HTTP POST
        const response = await fetch('/api/process-user-prompt', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ prompt: prompt, chatID: chatID }),
        credentials: 'include'
        })

        // Return and print data from backend
        const data = await response.json();
        console.log(data.chatID);
        
        // Update ChatID if it was null
        setChatID(data.chatID);
        
        setMessages(prev => [...prev, {'role': 'user', 'content': prompt}]);
        setMessages(prev => [...prev, {'role': 'assistant', 'content': data.response}]);
    }

    async function updateChatSidebar(user){
        // Send prompt to backend via HTTP POST
        const response = await fetch('/api/get-user-chats', {
        method: 'GET',
        credentials: 'include'
        })

        const data = await response.json();
        if(data != null)
        {
            setChats(/* ADD ALL chat_id and chat_title values to the chats state*/);
        }   
    }

    return { messages, handleUserInput, clearChat, chats };
}
