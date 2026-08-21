import deleteIcon from '/assets/delete.png';
import { Button } from '@/components/ui/button';

export default function UserChat({title, onClick, onDelete}) {
  return(
    <>
    <div className='flex items-center w-full gap-0.5'>
      <Button variant='ghost' className='flex-1 min-w-0 justify-start px-2 mb-[5px] hover:bg-[#5f9ea0]' onClick={onClick}>
        <span className='w-full min-w-0 truncate text-left'> {title} </span>
      </Button>
      
      <Button variant='ghost' size='icon' onClick={onDelete}>
        <img className='h-[15px] w-[15px]' src={deleteIcon}/>
      </Button>
    </div>
    </>
  )
}

 