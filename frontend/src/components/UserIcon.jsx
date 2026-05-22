import { useState } from 'react'
import '../App.css'

export default function UserIcon({isOpen, firstName, lastName}) {
  return(
    <>
        <div className={`userIconContainer ${isOpen ? 'open' : 'close'}`}>
          {
            isOpen ? <>
            <div className='userIconImage'>{firstName[0]}{lastName[0]}</div>
            <div className='userName'>{firstName} {lastName}</div>
            </>
            :
            <>
            <div className='userIconImageCentered'>{firstName[0]}{lastName[0]}</div>
            </>
          }
            
        </div>
    </>
  )
}

 