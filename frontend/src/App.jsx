import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [toi, setToi] = useState([]);
  const [et, setEt] = useState([]);
  const [bt, setBt] = useState([]);
  const [ht, setHt] = useState([]);
  const base = import.meta.env.VITE_API_BASE_URL;

  useEffect(()=>{
    fetch(`${base}/headlines/timesofindia`)
    .then(res=>res.json())
    .then(data=>setToi(data.headlines));

    fetch(`${base}/headlines/economictimes`)
      .then(res => res.json())
      .then(data => setEt(data.headlines));

    fetch(`${base}/headlines/businesstoday`)
      .then(res => res.json())
      .then(data => setBt(data.headlines));

    fetch(`${base}/headlines/thehindus`)
       .then(res=>res.json())
       .then(data=> setHt(data.headlines));
  }, []);


  const renderHeadlines=(source, headlines) => (
    <div className="bg-white rounded-2xl shadow-xl p-6 my-4 flex-1 min-w-[350px] max-w-[400px] transition-transform transform hover:scale-[1.02] hover:shadow-2xl border border-gray-200">
      <h2 className="text-2xl font-extrabold mb-4 text-center text-blue-800 tracking-tight border-b pb-2">{source}</h2>
      <ul className="list-disc ml-5 space-y-3">
        {headlines.map((item, i) => (
          <li key={i}>
            <a href={item.url} target="_blank" rel="noopener noreferrer" className="text-gray-700 hover:text-blue-600 hover:underline transition duration-300 ease-in-out">
              {item.title}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );

  return (
    <>
      <div className='min-h-screen bg-gradient-to-br from-blue-300 via-white to-blue-100 py-12 px-4'>
        <h1 className="text-4xl font-black mb-12 text-center text-blue-900 drop-shadow-lg tracking-tight font-serif">NewsScope</h1>
        <div className="flex flex-col md:flex-row md:justify-center md:items-start gap-10 max-w-7xl mx-auto px-2">
        {renderHeadlines("Times of India", toi)}
        {renderHeadlines("Economic Times", et)}
        {renderHeadlines("Business Today", bt)}
        {renderHeadlines("The Hindus", ht)}
      </div>
      </div>
    </>
  )
}

export default App
