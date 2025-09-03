import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout } from 'antd';
import Header from './components/Layout/Header';
import Footer from './components/Layout/Footer';
import HomePage from './pages/HomePage';
import './App.css';

const { Content } = Layout;

const App: React.FC = () => {
  return (
    <Router>
      <Layout className="app-layout">
        <Header />
        <Content className="app-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
          </Routes>
        </Content>
        <Footer />
      </Layout>
    </Router>
  );
};

export default App;
