import { Button } from '@/components/ui/button'

export default function SendButton({onClick}) {
  return(
    <>  
      <Button className='absolute right-[15px] top-1/2 -translate-y-1/2 border-none p-0 hover:border-none' onClick={onClick}>
        <img className='w-[30px]' src='./assets/send.png'/>
      </Button>
    </>
  )
}
