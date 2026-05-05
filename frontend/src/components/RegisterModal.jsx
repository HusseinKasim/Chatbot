import { useState } from 'react'
import '../App.css'

export default function RegisterModal({onLogin, onClose}) {
  return(
    <> 
      <div className='registerModalContainer'>
        <div className='modalHeader'>
          <label className='loginTitle'> Register </label>
          <button className='closeButton' onClick={onClose}> X </button> 
        </div>

        <div className='modalBody'>
          <div className='loginComponents'>
            <div className='names'>
                <input type='email' className='firstName' placeholder='First Name'></input>
                <input type='email' className='lastName' placeholder='Last Name'></input>
            </div>
            <input type='email' className='emailTextArea' placeholder='Email'></input>
            <input type='password' className='passwordTextArea' placeholder='Password'></input>
            
            <div className='loginButtonDiv'>
              <button className='modalLoginButton'> Register </button>
            </div>
        </div>

         <div className='actions'>
          <p className='registerText'> Already have an account? </p>
          <button className='registerButton' onClick={onLogin}> Login now!</button>
         </div>

        </div>
      </div>
    </>
  )
}
