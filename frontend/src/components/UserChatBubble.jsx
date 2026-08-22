
export default function UserChatBubble({key, value}) {
  return(
    <>
    <div className='bg-[var(--color-user-message)] rounded-[20px] border-none py-[11px] px-[15px] break-words text-[var(--color-text)]' key={key}>{value}</div>
    </>
  )
}
