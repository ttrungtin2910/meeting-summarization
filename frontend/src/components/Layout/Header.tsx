import React from 'react';
import { Layout, Typography } from 'antd';
import { SoundOutlined, BankOutlined } from '@ant-design/icons';

const { Header: AntHeader } = Layout;
const { Title } = Typography;

const Header: React.FC = () => {
  return (
    <AntHeader 
      style={{
        background: 'linear-gradient(135deg, #1f5f8b 0%, #28a745 100%)',
        padding: '0 50px',
        display: 'flex',
        alignItems: 'center',
        boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
        height: '80px',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <BankOutlined 
          style={{ 
            fontSize: '32px', 
            color: 'white',
            marginRight: '8px'
          }} 
        />
        <Title 
          level={3} 
          style={{ 
            color: 'white', 
            margin: 0, 
            fontSize: '24px',
            fontWeight: 600
          }}
        >
          Hệ thống Tạo Biên Bản Cuộc Họp
        </Title>
      </div>
      
      <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <SoundOutlined style={{ fontSize: '20px', color: 'white' }} />
        <span style={{ color: 'white', fontSize: '14px', fontWeight: 500 }}>
          Powered by AI
        </span>
      </div>
    </AntHeader>
  );
};

export default Header;
