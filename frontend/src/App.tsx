import React from 'react'

export default function App() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Trend App — Frontend (Phase 1)</h1>
      <p>Backend will run at <code>{import.meta.env.VITE_API_BASE_URL}</code></p>
    </div>
  )
}
