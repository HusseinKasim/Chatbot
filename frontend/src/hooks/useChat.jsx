import { useState } from 'react'
import '../App.css'

export default function useChat()
{
    const [messages, setMessages] = useState([
        {'role': 'chatbot', 'text': 'Hello! Please enter a prompt.'} 
    ])

    async function handleUserInput(prompt){
        // Add prompt to messages list
        setMessages(prev => [...prev, {'role': 'user', 'text': prompt}])
        console.log(prompt);
        
        // Send prompt to backend via HTTP POST
        const response = await fetch('http://127.0.0.1:8003/api/process-prompt', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ prompt }),
        })

        // Return and print data from backend
        const data = await response.json();

        // Add response to messages list 
        setMessages(prev => [...prev, {'role': 'chatbot', 'text': data.response.prompt}])
        console.log(data.response.prompt)
    }

    return { messages, handleUserInput };
}