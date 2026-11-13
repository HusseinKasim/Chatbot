import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuGroup, DropdownMenuItem } from "./ui/dropdown-menu"
import { Button } from '@/components/ui/button';

export default function DotsMenu({onClick}) {
  return(
    <>
    <DropdownMenu className='absolute'>
    <DropdownMenuTrigger render={<Button><img className='h-[20px] w-[20px]' src='/assets/three-dots.png'/></Button>}/>
    <DropdownMenuContent className='hover:bg-[var(--color-buttons-hover)] text-[var(--color-text)] bg-[var(--color-buttons)]'>
        <DropdownMenuGroup>
            <DropdownMenuItem onClick={onClick}>
                Delete
            </DropdownMenuItem>
        </DropdownMenuGroup>
    </DropdownMenuContent>
    </DropdownMenu>
    </>
  )
}

 