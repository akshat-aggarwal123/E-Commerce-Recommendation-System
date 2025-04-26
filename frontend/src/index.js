import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles.css'; // Import global styles
import App from './App'; // Import the main App component

// Create a root for the React app
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render the App component
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);