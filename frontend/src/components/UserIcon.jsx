
export default function UserIcon({isOpen, firstName, lastName}) {
  return(
    <>
        <div className={`${isOpen ? 'grid grid-cols-[1fr_3fr] pl-[10px]' : 'flex justify-center'}`}>
          {
            isOpen ? <>
            <div className='flex justify-center items-center h-[50px] w-[50px] bg-[#5f9ea0] shadow-[0_10px_30px_rgba(0,0,0,0.2)] rounded-full self-center text-white'>{firstName[0]}{lastName[0]}</div>
            <div className='flex justify-center items-center text-lg text-white pr-[30px] truncate'>{firstName} {lastName}</div>
            </>
            :
            <>
            <div className='flex justify-center items-center h-[50px] w-[50px] bg-[#5f9ea0] shadow-[0_10px_30px_rgba(0,0,0,0.2)] rounded-full text-white'>{firstName[0]}{lastName[0]}</div>
            </>
          }       
        </div>
    </>
  )
}

 