import React from 'react';
import { Layout, Typography } from 'antd';
import { CopyrightOutlined, HeartFilled } from '@ant-design/icons';

const { Footer: AntFooter } = Layout;
const { Text } = Typography;

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <AntFooter 
      style={{
        textAlign: 'center',
        background: '#f0f2f5',
        borderTop: '1px solid #d9d9d9',
        padding: '20px 50px',
      }}
    >
      <div style={{ marginBottom: '8px' }}>
        <Text style={{ color: '#666', fontSize: '14px' }}>
          <CopyrightOutlined style={{ marginRight: '4px' }} />
          {currentYear} Hệ thống Tạo Biên Bản Cuộc Họp. 
          Phát triển với <HeartFilled style={{ color: '#ff4d4f', margin: '0 4px' }} /> 
          bằng công nghệ AI
        </Text>
      </div>
      
      <div>
        <Text style={{ color: '#999', fontSize: '12px' }}>
          Sử dụng OpenAI Whisper cho chuyển đổi giọng nói thành văn bản và GPT cho tóm tắt thông minh
        </Text>
      </div>
    </AntFooter>
  );
};

export default Footer;
