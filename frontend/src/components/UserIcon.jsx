import { useState } from 'react'
import '../App.css'

export default function UserIcon({firstName, lastName}) {
  return(
    <>
    <div className='userIconWrapper'>
        <div className='userIconContainer'>
            <div className='userIconImage'>{firstName[0]}{lastName[0]}</div>
            <div className='userName'>{firstName} {lastName}</div>
        </div>
    </div>
    </>
  )
}

 