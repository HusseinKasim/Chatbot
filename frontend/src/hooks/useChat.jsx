import { useState } from 'react'
import '../App.css'

export default function useChat()
{
    const [messages, setMessages] = useState([
        {'role': 'assistant', 'content': 'Hello! Please enter a prompt.'} 
    ])

    async function handleUserInput(prompt){
        // Add prompt to messages list
        const updatedMessages = [...messages, {'role': 'user', 'content': prompt}]
        setMessages(updatedMessages);

        console.log(prompt);
        
        // Send prompt to backend via HTTP POST
        const response = await fetch('http://127.0.0.1:8003/api/process-prompt', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ messages: updatedMessages }),
        })

        // Return and print data from backend
        const data = await response.json();

        // Add response to messages list 
        setMessages(prev => [...prev, {'role': 'assistant', 'content': data.response}])
        console.log(data.response.prompt)
    }

    return { messages, handleUserInput };
}