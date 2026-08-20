import { useState, useContext } from 'react';
import AuthContext from '../context/AuthContext.jsx';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export default function LoginModal({onRegister, onClose, onLogin, onLoginClose}) {
  const { login, email, password, handleEmailChange, handlePasswordChange } = useContext(AuthContext);
  const [ loginLoading, setLoginLoading ] = useState(false);

  return(
    <> 
    <div className='modalBackdrop'>
      <div className='loginModalContainer'>
        <div className='relative flex justify-center items-center'>
          <label className='text-black text-lg text-bold mt-[20px]'> Login </label>
          <Button className='absolute top-[5px] right-[5px] text-black text-lg font-semibold border-none bg-none rounded-[10px]' onClick={onClose}> X </Button> 
        </div>

        <div className='modalBody'>
          <div className='flex flex-col gap-2.5 mt-[35px] px-5'>
            <Input type='email' className='bg-[#d3d3d3] text-black h-[35px] border-none pl-[10px]' placeholder='Email' value={email} onChange={(e) => handleEmailChange(e)} />
            <Input type='password' className='bg-[#d3d3d3] text-black h-[35px] border-none pl-[10px]' placeholder='Password' value={password} onChange={(e) => handlePasswordChange(e)} />
            
            <div className='self-center pt-[10px]'>
              { loginLoading ? 
                <>
                <div className = 'loginLoadingDiv'></div>
                </> : <>
                <Button className='mt-[5px] pl-[20px] pr-[20px] text-black border-black rounded-[5px] bg-[#508991]' onClick={async () => {
                  setLoginLoading(true);
                  const success = await login();
                  if(success){
                    onLogin();
                    onLoginClose(); 
                  }
                  setLoginLoading(false);
                }}> Login </Button>
                </>
              }
            </div>
        </div>

         <div className='flex justify-center items-center mt-[10px]'>
          <p className='text-black'> Not registered yet? </p>
          <Button className='bg-none border-none text-blue-500 pl-[5px] text-md' onClick={onRegister}> Register now!</Button>
         </div>

        </div>
      </div>
    </div>
    </>
  )
}
