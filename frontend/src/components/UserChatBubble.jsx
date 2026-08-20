
export default function UserChatBubble({key, value}) {
  return(
    <>
    <div className='bg-[#343636] rounded-[20px] border-0 border-[#FFEEDD] py-[11px] px-[15px] break-words text-white' key={key}>{value}</div>
    </>
  )
}
