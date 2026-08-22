
export default function UserIcon({isOpen, firstName, lastName}) {
  return(
    <>
        <div className={`${isOpen ? 'grid grid-cols-[1fr_4fr] pl-[30px]' : 'flex justify-center'}`}>
          {
            isOpen ? <>
            <div className='flex justify-center items-center h-[50px] w-[50px] bg-[var(--color-icon)] shadow-[0_10px_30px_rgba(0,0,0,0.2)] rounded-full self-center text-[var(--color-text)] '>{firstName[0]}{lastName[0]}</div>
            <div className='flex justify-center items-center text-lg text-[var(--color-text)] pr-[30px] truncate'>{firstName} {lastName}</div>
            </>
            :
            <>
            <div className='flex justify-center items-center h-[50px] w-[50px] bg-[var(--color-icon)] text-[var(--color-text)] shadow-[0_10px_30px_rgba(0,0,0,0.2)] rounded-full'>{firstName[0]}{lastName[0]}</div>
            </>
          }       
        </div>
    </>
  )
}

 