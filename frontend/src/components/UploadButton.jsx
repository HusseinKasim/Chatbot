import { useRef, useState } from 'react'
import '../App.css'

export default function UploadButton({onFileSelect}) {
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
  
    return(
    <>  
      <button className='uploadButton' onClick={handleButtonClick}>
        <img src='/assets/upload.png' alt='Upload'/>
      </button>

      <input ref={fileInputRef} type='file' style={{display: 'none'}} onChange={handleFileChange}/>
    </>
  )
}
