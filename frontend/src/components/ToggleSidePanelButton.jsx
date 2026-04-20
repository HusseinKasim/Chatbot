import { useState } from 'react'
import '../App.css'

export default function ToggleSidePanelButton({onClick}) {
  return(
    <>
      <button className='toggleSidePanelButton' onClick={onClick}>Toggle Sidepanel </button>
    </>
  )
}
