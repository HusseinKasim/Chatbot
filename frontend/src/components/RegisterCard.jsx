import { useState, useContext } from 'react';
import AuthContext from '../context/AuthContext.jsx';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardAction, CardContent, CardHeader, CardFooter, CardTitle } from './ui/card.jsx';

export default function RegisterCard({onLogin, onClose}) {
  const { firstName, lastName, email, password, handleFirstNameChange, handleLastNameChange, handleEmailChange, handlePasswordChange, register } = useContext(AuthContext);
  const [ registerLoading, setRegisterLoading ] = useState(false);

  return(
    <>
    <div className='fixed inset-0 z-50 flex items-center justify-center bg-black/50'>
      <Card className='flex w-full max-w-sm bg-[#F4F1EC]'>
        <CardHeader className='relative'>
          <CardTitle className=' flex justify-center text-[var(--color-modal-text)] text-lg text-bold'>
            Register
          </CardTitle>
          <CardAction>
            <Button className='absolute bottom-[15px] right-[5px] text-[var(--color-modal-text)] text-lg font-semibold rounded-[10px]' onClick={onClose}>
              X
            </Button>
          </CardAction>
        </CardHeader>

        <CardContent>
          <div className='flex flex-col gap-2.5 px-5'>
          <div className='grid grid-cols-2 gap-3'>
            <Input type='text' className='bg-[var(--color-modal-textarea)] text-[var(--color-modal-text)] h-[35px] border-none pl-[10px]' placeholder='First Name' value={firstName} onChange={(e) => handleFirstNameChange(e)} />
            <Input type='text' className='bg-[var(--color-modal-textarea)] text-[var(--color-modal-text)] h-[35px] border-none pl-[10px]' placeholder='Last Name' value={lastName} onChange={(e) => handleLastNameChange(e)} />
          </div>
            <Input type='email' className='bg-[var(--color-modal-textarea)] text-[var(--color-modal-text)] h-[35px] border-none pl-[10px]' placeholder='Email' value={email} onChange={(e) => handleEmailChange(e)} />   
            <Input type='password' className='bg-[var(--color-modal-textarea)] text-[var(--color-modal-text)] h-[35px] border-none pl-[10px]' placeholder='Password' value={password} onChange={(e) => handlePasswordChange(e)} />
          </div>
          
          <div className='flex justify-center'>
          { registerLoading ? 
                <>
                <div className='pt-[10px]'></div>
                </> : <>
                <Button className='mt-[15px] pl-[20px] pr-[20px] text-[var(--color-text)] border-none rounded-[5px] bg-[#508991] hover:bg-[#427780]' onClick={async () => {
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
        </CardContent>

        <CardFooter className='mt-[-15px]'>
          <div className='flex justify-center items-center'>
            <p className='text-[var(--color-modal-text)]'> Already have an account? </p>
            <Button variant='ghost' className='text-[var(--color-modal-auth-button)] pl-[5px] text-md hover:text-[var(--color-modal-auth-button-hover)]' onClick={onLogin}> Login now!</Button>
          </div>
        </CardFooter>
      </Card>
    </div>
    </>
  )
}
