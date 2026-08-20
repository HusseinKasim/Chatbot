import { useContext } from 'react';
import AuthContext from '../context/AuthContext.jsx';
import { Button } from '@/components/ui/button';

export default function LogoutButton({onLogout}) {
  const { logout } = useContext(AuthContext);

  return(
    <>  
      <Button className='flex justify-center w-[calc(100%-40px)] mx-5 mb-5 mt-auto box-border overflow-hidden bg-[#508991]' onClick={() => {
        logout();
        onLogout();
      }}>
        Logout
      </Button>
    </>
  )
}
