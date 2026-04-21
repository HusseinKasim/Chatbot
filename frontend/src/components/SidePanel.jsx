import { useState } from 'react'
import '../App.css'

export default function SidePanel({isOpen, children}) {
  return(
    <>
      <div className={isOpen ? 'sidePanelOpen' : 'sidePanelClose'}>
        {children}
      </div>
    </>
  )
}
