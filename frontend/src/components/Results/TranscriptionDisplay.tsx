import React from 'react';
import { Card, Typography, Tag, Space, Button, Divider } from 'antd';
import { 
  SoundOutlined,
  ArrowRightOutlined,
  ClockCircleOutlined,
  PercentageOutlined
} from '@ant-design/icons';
import { TranscriptionResponse } from '../../types/api';

const { Title, Text, Paragraph } = Typography;

interface TranscriptionDisplayProps {
  transcription: TranscriptionResponse;
  onCreateSummary: () => void;
  isCreatingSummary?: boolean;
}

const TranscriptionDisplay: React.FC<TranscriptionDisplayProps> = ({
  transcription,
  onCreateSummary,
  isCreatingSummary = false
}) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('vi-VN');
  };

  const formatDuration = (seconds?: number) => {
    if (!seconds) return 'Không xác định';
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className="transcription-display">
      <Card 
        className="gov-card"
        title={
          <Space>
            <SoundOutlined style={{ color: '#1f5f8b' }} />
            <Title level={3} style={{ margin: 0, color: '#1f5f8b' }}>
              Kết quả Speech-to-Text
            </Title>
          </Space>
        }
      >
        {/* Metadata */}
        <div style={{ marginBottom: '20px' }}>
          <Space wrap size="middle">
            <Text type="secondary">
              <ClockCircleOutlined /> Xử lý lúc: {formatDate(transcription.processed_at)}
            </Text>
            
            {transcription.transcription_language && (
              <Tag color="blue">
                Ngôn ngữ: {transcription.transcription_language.toUpperCase()}
              </Tag>
            )}
            
            {transcription.audio_duration && (
              <Tag color="green">
                <ClockCircleOutlined /> Thời lượng: {formatDuration(transcription.audio_duration)}
              </Tag>
            )}
            
            {transcription.confidence && (
              <Tag color="orange">
                <PercentageOutlined /> Độ tin cậy: {Math.round(transcription.confidence * 100)}%
              </Tag>
            )}
          </Space>
        </div>

        <Divider />

        {/* Transcription Content */}
        <div style={{ marginBottom: '24px' }}>
          <Title level={4} style={{ color: '#1f5f8b', marginBottom: '16px' }}>
            Nội dung phiên âm:
          </Title>
          
          <Card 
            style={{ 
              background: '#f8f9fa',
              border: '1px solid #e9ecef',
              maxHeight: '400px',
              overflow: 'auto'
            }}
          >
            <Paragraph style={{ 
              whiteSpace: 'pre-wrap', 
              wordBreak: 'break-word',
              lineHeight: '1.8',
              fontSize: '15px',
              margin: 0,
              color: '#333'
            }}>
              {transcription.transcription}
            </Paragraph>
          </Card>
        </div>

        {/* Action Button */}
        <div style={{ textAlign: 'center', marginTop: '24px' }}>
          <Button 
            type="primary" 
            size="large"
            icon={<ArrowRightOutlined />}
            onClick={onCreateSummary}
            loading={isCreatingSummary}
            style={{
              background: 'linear-gradient(135deg, #1f5f8b 0%, #28a745 100%)',
              border: 'none',
              borderRadius: '8px',
              padding: '0 32px',
              height: '48px',
              fontSize: '16px',
              fontWeight: '500'
            }}
          >
            {isCreatingSummary ? 'Đang tạo biên bản...' : 'Tạo biên bản cuộc họp'}
          </Button>
          
          <div style={{ marginTop: '12px' }}>
            <Text type="secondary" style={{ fontSize: '14px' }}>
              Nhấn để AI phân tích và tạo biên bản cuộc họp từ nội dung phiên âm
            </Text>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default TranscriptionDisplay;
