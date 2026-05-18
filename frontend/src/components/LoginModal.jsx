import { useState, useContext } from 'react'
import '../App.css'
import AuthContext from '../context/AuthContext.jsx';

export default function LoginModal({onRegister, onClose, onLogin}) {
  const { login, email, password, handleEmailChange, handlePasswordChange } = useContext(AuthContext);

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
            <input type='email' className='emailTextArea' placeholder='Email' value={email} onChange={(e) => handleEmailChange(e)}></input>
            <input type='password' className='passwordTextArea' placeholder='Password' value={password} onChange={(e) => handlePasswordChange(e)}></input>
            
            <div className='loginButtonDiv'>
              <button className='modalLoginButton' onClick={() => {
                login();
                onLogin();
                }}> Login </button>
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
