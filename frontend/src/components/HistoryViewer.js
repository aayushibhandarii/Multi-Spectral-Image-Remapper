import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000';

function HistoryViewer({ historyKey }) {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await axios.get(`${API_URL}/history`);
        setHistory(response.data);
      } catch (err) {
        console.error('Could not fetch processing history.');
      }
    };
    fetchHistory();
  }, [historyKey]); // Re-fetches when historyKey is updated after a new process

  return (
    <div className="module">
      <h2>4. Processing History Log (P0.4)</h2>
      <ul className="history-list">
        {history.length > 0 ? (
          history.slice(0, 5).map((item, index) => ( // Show latest 5
            <li key={index} className={`history-item ${item.status.toLowerCase()}`}>
              <span>{new Date(item.timestamp).toLocaleTimeString()}</span>
              <span>{item.filename}</span>
              <span>{item.status}</span>
            </li>
          ))
        ) : (
          <p>No processing history yet.</p>
        )}
      </ul>
    </div>
  );
}

export default HistoryViewer;