import { useState } from 'react'
import '../App.css'

export default function LogoutButton() {

    async function handleLogout() 
    {
      const response = await fetch('/api/logout', {
      method: 'POST',
      credentials: 'include'
      })

      console.log("Logged out");
  }
  return(
    <>  
      <button className='logoutButton' onClick={handleLogout}>
        Logout
      </button>
    </>
  )
}
