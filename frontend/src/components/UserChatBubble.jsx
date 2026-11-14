import { memo } from "react"

function UserChatBubble({value}) {
  return(
    <>
    <div className='text-base bg-[var(--color-user-message)] rounded-[20px] border-none py-[11px] px-[15px] break-words text-[var(--color-text)]'>{value}</div>
    </>
  )
}

export default memo(UserChatBubble);
