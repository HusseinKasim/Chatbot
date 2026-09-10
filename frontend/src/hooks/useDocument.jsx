import {useState, useContext, useEffect} from 'react'
import AuthContext from '../context/AuthContext';

export default function useDocument()
{
    const [documents, setDocuments] = useState([
        {'documentID': 0, 'title': 'New Document'}
    ])
    const { user } = useContext(AuthContext);

    useEffect(() => {
        if(user){
            updateDocumentSidebar();
        }
    }, [user]);

    async function updateDocumentSidebar(){
        // Fetch user chats from backend via HTTP GET
        /*
        try{
            let response = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/api/documents/`, {
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
            console.log('Error when updating documents sidebar: ' + err);
        }
        */
    }

    async function fetchWithAuth(url, options={}){
        let response = await fetch(url, options)
        if(response.status == 401) // Unauthorized (bad access token)
        {
            // Use refresh token to create new access token
            const refreshResponse = await fetch(`${import.meta.env.VITE_API_URL}/api/auth/refresh`, {
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

    return { documents, updateDocumentSidebar };
}
