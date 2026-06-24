import {useState, useContext, useEffect} from 'react'
import '../App.css'
import AuthContext from '../context/AuthContext';
const RENDER_BACKEND = import.meta.env.VITE_RENDER_BACKEND;

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
        try{
            const response = await fetch(`https://chatbot-backend-km58.onrender.com/api/prompt/guest`, {
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
        catch(err){
            console.log('Prompt error: ' + err);
        }
    }

    async function handleLoggedInUserInput(prompt)
    {
        setMessages(prev => [...prev, {'role': 'user', 'content': prompt}]);
        
        // Send prompt to backend via HTTP POST
        try{
            let response = await fetchWithAuth(`https://chatbot-backend-km58.onrender.com/api/prompt/user`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ prompt: prompt, chatID: chatID }),
            credentials: 'include'
            })

        // Return and print data from backend
        const data = await response.json();
        
        // Update ChatID if it was null
        setChatID(data.chatID);
        
        setMessages(prev => [...prev, {'role': 'assistant', 'content': data.response}]);
        }
        catch(err){
            console.log('Prompt error: ' + err);
        }
    }

    async function updateChatSidebar(){
        // Fetch user chats from backend via HTTP GET
        try{
            let response = await fetchWithAuth(`https://chatbot-backend-km58.onrender.com/api/chats/`, {
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
        catch(err){
            console.log('Error when updating chat sidebar: ' + err);
        }
    }

    async function updateUserChat(chatID){
        setChatID(chatID);
        
        // Fetch chat messages from backend via HTTP GET
        try{
            let response = await fetchWithAuth(`https://chatbot-backend-km58.onrender.com/api/chats/${chatID}/messages`, {
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
        catch(err){
            console.log('Error when retreiving chat messages: ' + err);
        }
    }

    async function deleteUserChat(chatID){
        // Delete user chat from DB via HTTP DELETE
        try{
            let response = await fetchWithAuth(`https://chatbot-backend-km58.onrender.com/api/chats/${chatID}`, {
            method: 'DELETE',
            credentials: 'include'
            })

            // Add error handling for when no response 
            const data = await response.json();
        }
        catch(err){
            console.log('Error when deleting user chat: ' + err);
        }
    }

    async function fetchWithAuth(url, options={}){
        let response = await fetch(url, options)
        if(response.status == 401) // Unauthorized (bad access token)
        {
            // Use refresh token to create new access token
            const refreshResponse = await fetch(`https://chatbot-backend-km58.onrender.com/api/auth/refresh`, {
            method: 'POST',
            credentials: 'include'
            })

            if(refreshResponse.ok)
            {
                // Retry
                response = await fetch(url, options)
            }
        }
        return response;
    }

    return { messages, handleUserInput, clearChat, chats, updateChatSidebar, updateUserChat, deleteUserChat };
}
