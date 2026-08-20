import { useRef, useContext } from 'react';
import AuthContext from '../context/AuthContext.jsx';
import { Button } from '@/components/ui/button.jsx';
import { Input } from '@/components/ui/input';

export default function UploadButton({onFileSelect}) {
  const { user } = useContext(AuthContext);
  const fileInputRef = useRef(null);

  function handleButtonClick(){
    fileInputRef.current.click();
  }

  function handleFileChange(e) {
    const file = e.target.files[0];

    if(file){
      onFileSelect(file);
    }
  }
  
  if(!user) {
    return null;
  }
    return(
    <>  
      <Button className='absolute left-[15px] top-1/2 -translate-y-1/2 border-none p-0 bg-none' onClick={handleButtonClick}>
        <img className='w-[25px]' src='../assets/upload.png' alt='Upload'/>
      </Button>

      <Input className='hidden' ref={fileInputRef} type='file' onChange={handleFileChange} />
    </>
  )
}
