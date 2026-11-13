import { Button } from '@/components/ui/button';

export default function UserChat({title, onClick, children, isSelected}) {
  return(
    <>
    <div className='pt-[5px] pb-[5px]'>
      <div className='flex items-center w-full gap-0.5 rounded-4xl hover:bg-[var(--color-chats-hover)]'>
        <Button variant='ghost' className={`flex-1 min-w-0 justify-start pl-[20px] pr-[15px] hover:bg-transparent ${isSelected ? 'bg-[var(--sidebar-accent)]' : ''}`} onClick={onClick}>
          <span className='w-full min-w-0 truncate text-left'> {title} </span>
        </Button>
        {children}
      </div>
    </div>
    </>
  )
}

 