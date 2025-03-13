import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Atlas from 'src/pages/Atlas'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Atlas />}/>
        <Route path='*' element={<Navigate to='/'/>}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App
