import { createContext, useContext, useState } from "react";

const AuthContext = createContext();

export function AuthProvider({children}) {
    const [ firstName, setFirstName ] = useState('');
    const [ lastName, setLastName ] = useState('');
    const [ email, setEmail ] = useState('');
    const [ password, setPassword ] = useState('');
    const [ user, setUser ] = useState(null);
    
    function handleFirstNameChange(e) {
    setFirstName(e.target.value);
    } 

    function handleLastNameChange(e) {
    setLastName(e.target.value);
    } 

    function handleEmailChange(e) {
    setEmail(e.target.value);
    } 

    function handlePasswordChange(e) {
    setPassword(e.target.value);
    } 

    const register = async () => {
        // Create data payload
        const payload = {
            firstName, 
            lastName,
            email,
            password
        };

        // Send user data to backend via HTTP POST
        try{
            const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload),
            credentials: 'include'
            })
            return true;
        }
        catch(err)
        {
            console.log('Registration error: ' + err);
            return false;
        }
        
    }

    const login = async () => {
        // Create data payload
        const payload = {
            email,
            password
        };

        // Get user data from backend via HTTP POST
        try{
            const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload),
            credentials: 'include'
            })

            const data = await response.json();
            if(data.response == 'authentificated')
            {
                await checkAuth(); // Set user
                return true;
            }
            else
            {
                console.log('Wrong login info'); // MUST DISPLAY ON UI
                return false;
            }
        }
        catch(err)
        {
            console.log('Login Error: ' + err);
            return false;
        }
    }

    const logout = async () => {
        try{
            const response = await fetch('/api/auth/logout', {
            method: 'POST',
            credentials: 'include'
            })
        }
        catch(err){
            console.log('Logout error:' + err);
        }

        console.log("Logged out");
        setUser(null);
    }

    const checkAuth = async () => {
        try{
            const response = await fetch('/api/auth/me', {
                method: 'GET',
                credentials: 'include'
            });

            const data = await response.json();
            if(data.response != null)
            {
                setUser(data.id);
                setFirstName(data.firstname);
                setLastName(data.lastname);
                console.log('Logged in');
            }
        }
        catch(err){
            console.log('Authentication error:' + err);
        }
    }
    
    return(
        <AuthContext.Provider value={{user, firstName, lastName, email, password, handleFirstNameChange, handleLastNameChange, handleEmailChange, handlePasswordChange, register, login, logout, checkAuth}}>
        {children}
        </AuthContext.Provider>
    );
}

export default AuthContext