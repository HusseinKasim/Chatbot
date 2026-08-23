import deleteIcon from '/assets/delete.png';
import { Button } from '@/components/ui/button';

export default function UserChat({title, onClick, onDelete, isSelected}) {
  return(
    <>
    <div className='flex items-center w-full gap-0.5 pt-[5px]'>
      <Button variant='ghost' className={`flex-1 min-w-0 justify-start pl-[20px] pr-[15px] mb-[5px] hover:bg-[var(--color-chats-hover)] ${isSelected ? 'bg-[var(--sidebar-accent)]' : ''}`} onClick={onClick}>
        <span className='w-full min-w-0 truncate text-left'> {title} </span>
      </Button>
      
      <Button variant='ghost' className='hover:bg-[var(--color-chats-hover)]' size='icon' onClick={onDelete}>
        <img className='h-[15px] w-[15px]' src={deleteIcon}/>
      </Button>
    </div>
    </>
  )
}

 