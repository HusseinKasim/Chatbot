import { useState, useContext } from 'react'
import '../App.css'
import AuthContext from '../context/AuthContext.jsx'

export default function LogoutButton() {
  const { logout } = useContext(AuthContext);

  return(
    <>  
      <button className='logoutButton' onClick={logout}>
        Logout
      </button>
    </>
  )
}
