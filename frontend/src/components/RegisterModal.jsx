import { useState, useContext } from 'react'
import '../App.css'
import AuthContext from '../context/AuthContext.jsx'

export default function RegisterModal({onLogin, onClose}) {
  const { firstName, lastName, email, password, handleFirstNameChange, handleLastNameChange, handleEmailChange, handlePasswordChange, register } = useContext(AuthContext);
  const [ registerLoading, setRegisterLoading ] = useState(false);

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
                <input type='email' className='firstName' placeholder='First Name' value={firstName} onChange={(e) => handleFirstNameChange(e)}></input>
                <input type='email' className='lastName' placeholder='Last Name' value={lastName} onChange={(e) => handleLastNameChange(e)}></input>
            </div>
            <input type='email' className='emailTextArea' placeholder='Email' value={email} onChange={(e) => handleEmailChange(e)}></input>
            <input type='password' className='passwordTextArea' placeholder='Password' value={password} onChange={(e) => handlePasswordChange(e)}></input>
            
            <div className='loginButtonDiv'>
              { registerLoading ? 
                <>
                <div className = 'loginLoadingDiv'></div>
                </> : <>
                <button className='modalLoginButton' onClick={async () => {
                  setRegisterLoading(true);
                  const success = await register();
                  if(success){
                    console.log('Registration successful!');
                  }
                  setRegisterLoading(false);
                }}> Register </button>
                </>
              }
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
