import React from 'react';
import ReactDOM from 'react-dom/client';
import { ConfigProvider } from 'antd';
import viVN from 'antd/locale/vi_VN';
import App from './App';
import './index.css';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

// Theme config with government-friendly colors
const theme = {
  token: {
    colorPrimary: '#1f5f8b', // Deep blue for government
    colorSuccess: '#28a745', // Green
    colorWarning: '#ffc107', // Yellow
    colorError: '#dc3545', // Red
    borderRadius: 8,
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif',
  },
};

root.render(
  <React.StrictMode>
    <ConfigProvider 
      locale={viVN}
      theme={theme}
    >
      <App />
    </ConfigProvider>
  </React.StrictMode>
);
