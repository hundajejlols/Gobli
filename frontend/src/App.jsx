import { useState, useEffect } from 'react'
import axios from 'axios'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

function App() {
  const [items, setItems] = useState([])
  const [selectedItem, setSelectedItem] = useState(null)
  const [history, setHistory] = useState([])

  // Adres Twojego API (zmien na IP malinki, gdy przeniesiesz tam serwer)
  const API_URL = 'http://127.0.0.1:8000'

  // Pobierz liste przedmiotow przy starcie aplikacji
  useEffect(() => {
    axios.get(`${API_URL}/api/items`)
      .then(response => {
        setItems(response.data.tracked_items)
        if (response.data.tracked_items.length > 0) {
          setSelectedItem(response.data.tracked_items[0])
        }
      })
      .catch(error => console.error("Error fetching items:", error))
  }, [])

  // Pobierz historie cen, gdy zmieni sie wybrany przedmiot
  useEffect(() => {
    if (selectedItem) {
      axios.get(`${API_URL}/api/items/${selectedItem}/history`)
        .then(response => {
          // Recharts lubi dane poukladane chronologicznie, wiec odwracamy tablice
          const sortedData = response.data.history.reverse()
          setHistory(sortedData)
        })
        .catch(error => console.error("Error fetching history:", error))
    }
  }, [selectedItem])

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>Gobli Dashboard</h1>
      
      <div style={{ marginBottom: '20px' }}>
        <label style={{ marginRight: '10px' }}>Select Item ID: </label>
        <select 
          value={selectedItem || ''} 
          onChange={(e) => setSelectedItem(e.target.value)}
          style={{ padding: '5px' }}
        >
          {items.map(item => (
            <option key={item} value={item}>{item}</option>
          ))}
        </select>
      </div>

      <div style={{ width: '100%', height: 400 }}>
        {history.length > 0 ? (
          <ResponsiveContainer>
            <LineChart data={history} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="timestamp" />
              {/* API Blizzarda podaje ceny w miedziakach, dzielimy przez 10000 zeby miec Gold */}
              <YAxis tickFormatter={(value) => `${(value / 10000).toFixed(2)}g`} />
              <Tooltip formatter={(value) => `${(value / 10000).toFixed(2)} Gold`} />
              <Legend />
              <Line type="monotone" dataKey="min_price" name="Minimum Price" stroke="#8884d8" activeDot={{ r: 8 }} />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <p>Loading chart data...</p>
        )}
      </div>
    </div>
  )
}

export default App