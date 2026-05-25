import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [data, setData] = useState({ speed: 0, battery: 100, tire_pressure: 0 });
  const [alerts, setAlerts] = useState([]);

  // Fetch data from our FastAPI backend every 1 second
  useEffect(() => {
    const fetchData = async () => {
      try {
        const statusRes = await fetch('http://127.0.0.1:8000/vehicle/status');
        const statusData = await statusRes.json();
        setData(statusData);

        const alertRes = await fetch('http://127.0.0.1:8000/vehicle/alerts');
        const alertData = await alertRes.json();
        setAlerts(alertData.alerts);
      } catch (err) {
        console.error("Connection to STLA Backend failed", err);
      }
    };

    const interval = setInterval(fetchData, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="dashboard-container">
      <header>
        <h1>STLA SMARTCOCKPIT</h1>
        <div className="vin">VIN: STLA-JEEP-2026-PROTOTYPE</div>
      </header>

      <div className="grid">
        <div className="card gauge">
          <h2>SPEED</h2>
          <div className="value">{data.speed}</div>
          <div className="unit">KM/H</div>
        </div>

        <div className="card gauge">
          <h2>BATTERY</h2>
          <div className={`value ${data.battery < 20 ? 'critical' : ''}`}>
            {Math.round(data.battery)}%
          </div>
          <div className="battery-bar">
            <div className="fill" style={{ width: `${data.battery}%` }}></div>
          </div>
        </div>

        <div className="card gauge">
          <h2>TIRE PRESSURE</h2>
          <div className="value">{data.tire_pressure}</div>
          <div className="unit">PSI</div>
        </div>
      </div>

      <div className="alerts-section">
        {alerts.length > 0 ? (
          alerts.map((msg, i) => <div key={i} className="alert-banner">{msg}</div>)
        ) : (
          <div className="system-ok">SYSTEMS OPTIMAL</div>
        )}
      </div>
    </div>
  )
}

export default App