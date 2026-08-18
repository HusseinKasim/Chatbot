import { useRef, useContext } from 'react';
import AuthContext from '../context/AuthContext.jsx';
import '../App.css';

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
      <button className='uploadButton' onClick={handleButtonClick}>
        <img src='../assets/upload.png' alt='Upload'/>
      </button>

      <input ref={fileInputRef} type='file' style={{display: 'none'}} onChange={handleFileChange}/>
    </>
  )
}
