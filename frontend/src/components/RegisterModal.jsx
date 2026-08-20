import { useState, useContext } from 'react';
import '../App.css';
import AuthContext from '../context/AuthContext.jsx';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export default function RegisterModal({onLogin, onClose}) {
  const { firstName, lastName, email, password, handleFirstNameChange, handleLastNameChange, handleEmailChange, handlePasswordChange, register } = useContext(AuthContext);
  const [ registerLoading, setRegisterLoading ] = useState(false);

  return(
    <> 
    <div className='modalBackdrop'>
      <div className='registerModalContainer'>
        <div className='relative flex justify-center items-center'>
          <label className='text-black text-lg text-bold mt-[20px]'> Register </label>
          <Button className='absolute top-[5px] right-[5px] text-black text-lg font-semibold border-none bg-none rounded-[10px]' onClick={onClose}> X </Button> 
        </div>

        <div className='modalBody'>
          <div className='loginComponents'>
            <div className='flex flex-row gap-[22px]'>
                <Input type='text' className='bg-[#d3d3d3] text-black h-[35px] border-none pl-[10px]' placeholder='First Name' value={firstName} onChange={(e) => handleFirstNameChange(e)} />
                <Input type='text' className='bg-[#d3d3d3] text-black h-[35px] border-none pl-[10px]' placeholder='Last Name' value={lastName} onChange={(e) => handleLastNameChange(e)} />
            </div>
            <Input type='email' className='bg-[#d3d3d3] text-black h-[35px] border-none pl-[10px]' placeholder='Email' value={email} onChange={(e) => handleEmailChange(e)} />
            <Input type='password' className='bg-[#d3d3d3] text-black h-[35px] border-none pl-[10px]' placeholder='Password' value={password} onChange={(e) => handlePasswordChange(e)} />
            
            <div className='self-center pt-[10px]'>
              { registerLoading ? 
                <>
                <div className = 'loginLoadingDiv'></div>
                </> : <>
                <Button className='mt-[5px] pl-[20px] pr-[20px] text-black border-black rounded-[5px] bg-[#508991]' onClick={async () => {
                  setRegisterLoading(true);
                  const success = await register();
                  if(success){
                    console.log('Registration successful!');
                  }
                  setRegisterLoading(false);
                }}> Register </Button>
                </>
              }
            </div>
        </div>

         <div className='flex justify-center items-center mt-[10px]'>
          <p className='text-black'> Already have an account? </p>
          <Button className='bg-none border-none text-blue-500 pl-[5px] text-md' onClick={onLogin}> Login now!</Button>
         </div>
        </div>
      </div>
    </div>
    </>
  )
}
