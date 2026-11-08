import {useState, useContext, useEffect} from 'react'
import AuthContext from '../context/AuthContext';

export default function useDocument()
{
    const [documentID, setDocumentID] = useState(0);
    const [document, setDocument] = useState({'documentID': 0, 's3_url': ''});
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
        // Fetch user documents from backend via HTTP GET
        try{
            let response = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/api/documents/`, {
            method: 'GET',
            credentials: 'include'
            })

            const data = await response.json();
            if(data.documents != null)
            {
                setDocuments(
                    data.documents.map(document => ({
                        documentID: document.id,
                        title: document.document_name
                    }))
                );
            }
        }
        catch(err){
            console.log('Error when updating documents sidebar: ' + err);
        }
    }

    async function loadS3Document(documentID){
        setDocumentID(documentID)

        // Fetch user document from S3 via backend via HTTP GET
        try{
            let response = await fetchWithAuth(`${import.meta.env.VITE_API_URL}/api/documents/load/${documentID}`, {
            method: 'GET',
            credentials: 'include'
            })

            const data = await response.json();
            if(data.documentID != null)
            {
                setDocument({
                        documentID: data.documentID,
                        documentTitle: data.documentTitle,
                        s3_url: data.s3_url
                    }
                );
            }
        }
        catch(err){
            console.log('Error when loading the document: ' + err);
        }
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

    function clearDocument(){
        setDocument({
            documentID: 0,
            s3_url: ''
        })
    }

    return { document, documents, updateDocumentSidebar, loadS3Document, clearDocument};
}
