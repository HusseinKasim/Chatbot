import { Textarea } from "@/components/ui/textarea";

export default function UserTextArea({value, onChange, onKeyDown, isLoggedIn}) {
  return(
    <>
    <Textarea className={`w-full h-[55px] py-[17px] pr-[50px] ${ isLoggedIn ? 'pl-[60px]' : 'pl-[15px]' } md:text-lg rounded-[20px] border border-[#FFEEDD] resize-none overflow-hidden`} value={value} onChange={onChange} onKeyDown={onKeyDown} placeholder='Ask a question...' />
    </>
  )
}

