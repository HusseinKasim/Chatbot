import { useState } from 'react'
import '../App.css'

export default function LoginModal({onRegister, onClose}) {
  const [ email, setEmail ] = useState('');
  const [ password, setPassword ] = useState('');

  async function handleLogin() 
  {
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

      console.log("Logged in");

      {/* MUST REPLACE LOGIN BUTTON WITH LOGOUT BUTTON AND ADD USER NAME AND ICON TO SHOW HE IS LOGGED IN */}
  }

  return(
    <> 
    <div className='modalBackdrop'>
      <div className='loginModalContainer'>
        <div className='modalHeader'>
          <label className='loginTitle'> Login </label>
          <button className='closeButton' onClick={onClose}> X </button> 
        </div>

        <div className='modalBody'>
          <div className='loginComponents'>
            <input type='email' className='emailTextArea' placeholder='Email' value={email} onChange={(e) => setEmail(e.target.value)}></input>
            <input type='password' className='passwordTextArea' placeholder='Password' value={password} onChange={(e) => setPassword(e.target.value)}></input>
            
            <div className='loginButtonDiv'>
              <button className='modalLoginButton' onClick={() => handleLogin()}> Login </button>
            </div>
        </div>

         <div className='actions'>
          <p className='registerText'> Not registered yet? </p>
          <button className='registerButton' onClick={onRegister}> Register now!</button>
         </div>

        </div>
      </div>
    </div>
    </>
  )
}
