import React, { useState, useEffect } from 'react'; // Import useEffect
import axios from 'axios';
import ControlPanel from './components/ControlPanel';
import ImageViewer from './components/ImageViewer';
import HistoryViewer from './components/HistoryViewer';
import './App.css';

const API_URL = 'http://127.0.0.1:5000';

function App() {
  const [redFile, setRedFile] = useState(null);
  const [greenFile, setGreenFile] = useState(null);
  const [blueFile, setBlueFile] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);
  const [metadata, setMetadata] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [historyKey, setHistoryKey] = useState(0);
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    document.body.classList.remove('light', 'dark');
    document.body.classList.add(theme);
  }, [theme]);

  const handleColorize = async (modelParams) => {
    if (!redFile || !greenFile || !blueFile) {
      setError('Please select a file for each color channel.');
      return;
    }
    setIsLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('red_file', redFile);
    formData.append('green_file', greenFile);
    formData.append('blue_file', blueFile);
    formData.append('palette', modelParams.palette);

    try {
      const response = await axios.post(`${API_URL}/colorize-layers`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setProcessedImage(response.data.imageData);
      setMetadata(response.data.metadata);
      setHistoryKey(prevKey => prevKey + 1);
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred during colorization.');
    } finally {
      setIsLoading(false);
    }
  };

  const toggleTheme = () => {
    setTheme(prevTheme => (prevTheme === 'light' ? 'dark' : 'light'));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Astro Image Colorizer 🔭</h1>
        <button onClick={toggleTheme} className="theme-toggle">
          Switch to {theme === 'light' ? 'Dark' : 'Light'} Mode
        </button>
      </header>
      <main>
        <div className="main-container">
          <div className="left-panel">
            <div className="module">
              <h2>1. Upload Layers</h2>
              <div>
                <label>Red Channel:</label>
                <input type="file" accept=".fits,.fit" onChange={(e) => setRedFile(e.target.files[0])} />
              </div>
              <div>
                <label>Green Channel:</label>
                <input type="file" accept=".fits,.fit" onChange={(e) => setGreenFile(e.target.files[0])} />
              </div>
              <div>
                <label>Blue Channel:</label>
                <input type="file" accept=".fits,.fit" onChange={(e) => setBlueFile(e.target.files[0])} />
              </div>
            </div>
            <ControlPanel onColorize={handleColorize} isLoading={isLoading} />
            {error && <p className="error">{error}</p>}
            <HistoryViewer historyKey={historyKey} />
          </div>
          <div className="right-panel">
            <ImageViewer imageUrl={processedImage} metadata={metadata} isLoading={isLoading} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;