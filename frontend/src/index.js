import React from 'react';
import ReactDOM from 'react-dom/client';
import './App.css'; // Importing your main CSS file
import App from './App';

// Find the root element from your index.html
const rootElement = document.getElementById('root');

// Create a React root to render the application
const root = ReactDOM.createRoot(rootElement);

// Render the main App component
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);