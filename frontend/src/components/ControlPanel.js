import React, { useState } from 'react';

// These configurations represent the "AI Models and Palettes"
const MODELS = {
  hubble: { name: 'Hubble Palette (SHO)', red_channel: 2, green_channel: 0, blue_channel: 1 },
  natural: { name: 'Natural Color (RGB)', red_channel: 0, green_channel: 1, blue_channel: 2 },
  custom: { name: 'Custom BGR', red_channel: 2, green_channel: 1, blue_channel: 0 },
};

function ControlPanel({ onColorize, isLoading }) {
  const [selectedPalette, setSelectedPalette] = useState('natural');

  const handleColorizeClick = () => {
    onColorize({ palette: selectedPalette });
  };

  return (
    <div className="module">
      <h2>2. Configure & Run</h2>
      <div>
        <label>Color Palette:</label>
        <select value={selectedPalette} onChange={(e) => setSelectedPalette(e.target.value)}>
          {Object.entries(MODELS).map(([key, value]) => (
            <option key={key} value={key}>{value.name}</option>
          ))}
        </select>
      </div>
      <button onClick={handleColorizeClick} disabled={isLoading}>
        {isLoading ? 'Processing...' : 'Colorize Image'}
      </button>
    </div>
  );
}

export default ControlPanel;