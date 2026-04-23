import { useState } from 'react'
import '../App.css'

export default function ToggleSidePanelButton({isOpen, onClick}) {
  return(
    <>
    <button className={isOpen ? 'toggleSidePanelButton open' : 'toggleSidePanelButton close'} onClick={onClick}>
      <img src='/assets/sidepanel.png'/>
    </button>
    </>
  )
}
