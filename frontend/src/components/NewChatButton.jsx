import { Button } from '@/components/ui/button';

export default function NewChatButton({isOpen, onClick}) {
  return(
    <>  
      <Button className={`flex items-center bg-none border-none p-0 gap-2 mt-2.5 ${isOpen ? 'mr-[100px]' : 'justify-start mr-[5px] mb-2.5 w-full'}`} onClick={onClick}>
        <img className='w-[30px]' src='/assets/add.png'/>
        {
          isOpen ? <>
            New Chat
          </>
          :
          <>
          </>
        }
      </Button>
    </>
  )
}
