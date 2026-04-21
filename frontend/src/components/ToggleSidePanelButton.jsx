import { useState } from 'react'
import '../App.css'

export default function ToggleSidePanelButton({isOpen, onClick}) {
  return(
    <>
    <button className={isOpen ? 'toggleSidePanelButtonOpen' : 'toggleSidePanelButtonClose'} onClick={onClick}>
      <img src='./assets/sidepanel.png'/>
    </button>
    </>
  )
}
