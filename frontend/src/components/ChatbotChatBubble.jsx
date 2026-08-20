
export default function ChatbotChatBubble({key, value}) {
  return(
    <>
    <div className='flex items-start w-3/4 h-auto p-2 rounded-[20px] resize-none overflow-hidden whitespace-pre-wrap break-words text-white' key={key}>{value}</div>
    </>
  )
}

 