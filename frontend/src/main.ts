// src/main.ts
import ReactDOM from 'react-dom/client';
import App from './App'; // Use relative path './App'

const rootElement = document.getElementById('root');

if (!rootElement) {
  throw new Error("Root element with ID 'root' not found in the DOM.");
}

const root = ReactDOM.createRoot(rootElement);
root.render(<App />);
