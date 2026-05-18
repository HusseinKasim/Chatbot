import { useState, useContext } from 'react'
import '../App.css'
import AuthContext from '../context/AuthContext.jsx'

export default function LogoutButton({onLogout}) {
  const { logout } = useContext(AuthContext);

  return(
    <>  
      <button className='logoutButton' onClick={() => {
        logout();
        onLogout();
      }}>
        Logout
      </button>
    </>
  )
}
