import { useState } from 'react'
import '../App.css'

export default function RegisterModal({onLogin, onClose}) {
    const [ firstName, setFirstName ] = useState('');
    const [ lastName, setLastName ] = useState('');
    const [ email, setEmail ] = useState('');
    const [ password, setPassword ] = useState('');

    async function handleRegister() 
    {
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

  return(
    <> 
    <div className='modalBackdrop'>
      <div className='registerModalContainer'>
        <div className='modalHeader'>
          <label className='loginTitle'> Register </label>
          <button className='closeButton' onClick={onClose}> X </button> 
        </div>

        <div className='modalBody'>
          <div className='loginComponents'>
            <div className='names'>
                <input type='email' className='firstName' placeholder='First Name' value={firstName} onChange={(e) => setFirstName(e.target.value)}></input>
                <input type='email' className='lastName' placeholder='Last Name' value={lastName} onChange={(e) => setLastName(e.target.value)}></input>
            </div>
            <input type='email' className='emailTextArea' placeholder='Email' value={email} onChange={(e) => setEmail(e.target.value)}></input>
            <input type='password' className='passwordTextArea' placeholder='Password' value={password} onChange={(e) => setPassword(e.target.value)}></input>
            
            <div className='loginButtonDiv'>
              <button className='modalLoginButton' onClick={() => handleRegister()}> Register </button>
            </div>
        </div>

         <div className='actions'>
          <p className='registerText'> Already have an account? </p>
          <button className='registerButton' onClick={onLogin}> Login now!</button>
         </div>
        </div>
      </div>
    </div>
    </>
  )
}
