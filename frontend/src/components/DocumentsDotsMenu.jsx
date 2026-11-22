import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuGroup, DropdownMenuItem } from "./ui/dropdown-menu"
import { Button } from '@/components/ui/button';

export default function DocumentsDotsMenu({onClickRename, onClickDelete}) {
  return(
    <>
    <DropdownMenu className='absolute'>
    <DropdownMenuTrigger render={<Button><img className='h-[20px] w-[20px]' src='/assets/three-dots.png'/></Button>}/>
    <DropdownMenuContent className='overflow-hidden p-0 text-[var(--color-text)] bg-[var(--color-buttons)]'>
        <DropdownMenuGroup>
            <DropdownMenuItem className='rounded-none hover:bg-[var(--color-buttons-hover)]' onClick={onClickDelete}>
                Delete
            </DropdownMenuItem>
        </DropdownMenuGroup>
    </DropdownMenuContent>
    </DropdownMenu>
    </>
  )
}

 