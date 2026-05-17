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
        const response = await fetch('/api/register', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload),
        credentials: 'include'
        })
    }

    const login = async () => {
        // Create data payload
        const payload = {
            email,
            password
        };

        // Get user data from backend via HTTP POST
        const response = await fetch('/api/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload),
        credentials: 'include'
        })

        const data = await response.json();
        if(data.response == 'authentificated')
        {
            checkAuth(); // Set user
        }
        else
        {
            console.log('Wrong login info'); // MUST DISPLAY ON UI
        }

        {/* MUST REPLACE LOGIN BUTTON WITH LOGOUT BUTTON AND ADD USER NAME AND ICON TO SHOW HE IS LOGGED IN */}
    }

    const logout = async () => {
        const response = await fetch('/api/logout', {
        method: 'POST',
        credentials: 'include'
        })

        console.log("Logged out");
        setUser(null);
    }

    const checkAuth = async () => {
        const response = await fetch('/api/me', {
            credentials: 'include'
        });

        const data = await response.json();
        if(data.response != null)
        {
            setUser(data);
            console.log('Logged in');
        }
    }

    return(
        <AuthContext.Provider value={{user, firstName, lastName, email, password, handleFirstNameChange, handleLastNameChange, handleEmailChange, handlePasswordChange, register, login, logout, checkAuth}}>
        {children}
        </AuthContext.Provider>
    );
}

export default AuthContext