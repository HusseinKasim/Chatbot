import { useState } from 'react'
import '../App.css'

export default function LoginModal({onClose}) {
  return(
    <> 
      <div className='modalContainer'>
        <div className='modalHeader'>
          <label className='loginTitle'> Login </label>
          <button className='closeButton' onClick={onClose}> X </button> 
        </div>

        <div className='modalBody'>
          <div className='loginComponents'>
            <input type='email' className='emailTextArea' placeholder='Email'></input>
            <input type='password' className='passwordTextArea' placeholder='Password'></input>
            
            <div className='loginButtonDiv'>
              <button className='modalLoginButton'> Login </button>
            </div>
        </div>

         <div className='actions'>
          <p className='registerText'> Not registered yet? </p>
          <button className='registerButton'> Register now!</button>
         </div>

        </div>
      </div>
    </>
  )
}
