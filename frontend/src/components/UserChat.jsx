import deleteIcon from '/assets/delete.png';
import { Button } from '@/components/ui/button';

export default function UserChat({isOpen, title, onClick, onDelete}) {
  return(
    <>
    <div className='flex items-center w-full bg-none border-none p-0 gap-0.5'>
      <Button className='flex-1 min-w-0 bg-none border-none mb-[5px] overflow-hidden' onClick={onClick}>
        <div className='w-full min-w-0 truncate' title={title}>
          {title}
        </div>
      </Button>
      
      <Button className='bg-none border-none' onClick={onDelete}>
        <img className='h-[15px] w-[15px]' src={deleteIcon}/>
      </Button>

    </div>
    </>
  )
}

 