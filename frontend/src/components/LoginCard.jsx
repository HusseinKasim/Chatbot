import { useState, useContext } from 'react';
import AuthContext from '../context/AuthContext.jsx';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardAction, CardContent, CardHeader, CardFooter, CardTitle } from './ui/card.jsx';

export default function LoginCard({onRegister, onClose, onLogin, onLoginClose}) {
  const { login, email, password, handleEmailChange, handlePasswordChange } = useContext(AuthContext);
  const [ loginLoading, setLoginLoading ] = useState(false);

  return(
    <>
    <div className='fixed inset-0 z-50 flex items-center justify-center bg-black/50'>
      <Card className='flex w-full max-w-sm bg-[#F4F1EC]'>
        <CardHeader className='relative'>
          <CardTitle className=' flex justify-center text-[var(--color-modal-text)] text-lg text-bold'>
            Login
          </CardTitle>
          <CardAction>
            <Button className='absolute bottom-[15px] right-[5px] text-[var(--color-modal-text)] text-lg font-semibold rounded-[10px]' onClick={onClose}>
              X
            </Button>
          </CardAction>
        </CardHeader>

        <CardContent>
          <div className='flex flex-col gap-2.5 px-5'>
            <Input type='email' className='bg-[var(--color-modal-textarea)] text-[var(--color-modal-text)] h-[35px] border-none' placeholder='Email' value={email} onChange={(e) => handleEmailChange(e)} />
            <Input type='password' className='bg-[var(--color-modal-textarea)] text-[var(--color-modal-text)] h-[35px] border-none' placeholder='Password' value={password} onChange={(e) => handlePasswordChange(e)} />
          </div>
          
          <div className='flex justify-center'>
            { loginLoading ? 
                <>
                <div className='pt-[10px]'></div>
                </> : <>
                <Button className='text-[#F1F3F4] border-none rounded-[5px] mt-[20px] bg-[var(--color-buttons)] hover:bg-[var(--color-buttons-hover)]' onClick={async () => {
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
        </CardContent>

        <CardFooter className='mt-[-15px]'>
          <div className='flex justify-center items-center'>
            <p className='text-[var(--color-modal-text)]'> Not registered yet? </p>
            <Button variant='ghost' className='text-[var(--color-modal-auth-button)] pl-[5px] text-md hover:text-[var(--color-modal-auth-button-hover)]' onClick={onRegister}> Register now!</Button>
          </div>
        </CardFooter>
      </Card>
    </div>
    </>
  )
}
