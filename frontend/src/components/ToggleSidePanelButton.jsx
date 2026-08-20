import { Button } from '@/components/ui/button';

export default function ToggleSidePanelButton({isOpen, onClick}) {
  return(
    <>
    <Button className={`bg-none border-none p-0 ${isOpen ? 'rotate-180' : ''}`} onClick={onClick}>
      <img className='w-[30px]' src='/assets/sidepanel.png'/>
    </Button>
    </>
  )
}
