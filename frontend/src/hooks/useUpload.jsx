import {useState, useContext, useEffect} from 'react'
import AuthContext from '../context/AuthContext';
import useChat from './useChat';

export default function useUpload()
{
    const [documentID, setDocumentID] = useState(0);
    const { user } = useContext(AuthContext);
    const { fetchWithAuth } = useChat();
    
    function uploadDocument(document){
        sendDocument(document);
    }

    async function sendDocument(document){

        const formData = new FormData();
        formData.append('pdfFile', document)

        const response = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/api/upload/`, {
            method: 'POST',
            body: formData,
            credentials: 'include'
        })

        const data = await response.json();

        if(data['response'] == 'success')
            console.log('File successfully uploaded');
    }

    return { uploadDocument };
}
