import { Button } from '@/components/ui/button';

export default function LoginButton({isOpen, onClick}) {
  return(
    <>  
      <Button className='flex justify-center w-[calc(100%-40px)] mx-5 mb-5 mt-auto box-border overflow-hidden bg-[#508991]' onClick={onClick}>
        Login
      </Button>
    </>
  )
}
