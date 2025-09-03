import React, { useState, useEffect } from 'react';
import { Row, Col, Typography, Card, Alert, Button, Spin } from 'antd';
import { 
  SoundOutlined, 
  FileTextOutlined, 
  RobotOutlined, 
  CheckCircleOutlined,
  ReloadOutlined 
} from '@ant-design/icons';
import AudioUploader from '../components/Upload/AudioUploader';
import ProcessingStatus from '../components/Results/ProcessingStatus';
import MeetingSummaryDisplay from '../components/Results/MeetingSummaryDisplay';
import TranscriptionDisplay from '../components/Results/TranscriptionDisplay';
import { audioAPI } from '../services/api';
import { 
  MeetingSummaryResponse, 
  ProcessingStatusResponse,
  TranscriptionResponse
} from '../types/api';

const { Title, Paragraph } = Typography;

const HomePage: React.FC = () => {
  const [currentTaskId, setCurrentTaskId] = useState<string | null>(null);
  const [processingStatus, setProcessingStatus] = useState<ProcessingStatusResponse | null>(null);
  const [transcriptionResult, setTranscriptionResult] = useState<TranscriptionResponse | null>(null);
  const [meetingSummary, setMeetingSummary] = useState<MeetingSummaryResponse | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isCreatingSummary, setIsCreatingSummary] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isLoadingStatus, setIsLoadingStatus] = useState(false);

  const pollInterval = 3000; // 3 seconds

  // Poll for status updates
  useEffect(() => {
    let intervalId: NodeJS.Timeout;

    if (currentTaskId && isProcessing) {
      intervalId = setInterval(async () => {
        try {
          setIsLoadingStatus(true);
          const status = await audioAPI.getTaskStatus(currentTaskId);
          setProcessingStatus(status);

          if (status.status === 'completed') {
            // Get the summary
            const summary = await audioAPI.getMeetingSummary(currentTaskId);
            setMeetingSummary(summary);
            setIsProcessing(false);
          } else if (status.status === 'failed') {
            setError(status.message || 'Xử lý thất bại');
            setIsProcessing(false);
          }
        } catch (error: any) {
          console.error('Error polling status:', error);
          // Don't stop polling for temporary network errors
        } finally {
          setIsLoadingStatus(false);
        }
      }, pollInterval);
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [currentTaskId, isProcessing]);

  const handleFileSelect = async (file: File) => {
    setError(null);
    setTranscriptionResult(null);
    setMeetingSummary(null);
    setProcessingStatus(null);
    setIsProcessing(true);

    try {
      // Always use transcription-only first
      const transcription = await audioAPI.transcribeAudio(file);
      setTranscriptionResult(transcription);
      setCurrentTaskId(transcription.task_id);
      setIsProcessing(false);
    } catch (error: any) {
      console.error('Error processing file:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Có lỗi xảy ra khi xử lý file';
      setError(errorMessage);
      setIsProcessing(false);
    }
  };

  const handleCreateSummary = async () => {
    if (!currentTaskId) return;
    
    setError(null);
    setIsCreatingSummary(true);

    try {
      const summary = await audioAPI.createSummaryFromTranscription(currentTaskId);
      setMeetingSummary(summary);
    } catch (error: any) {
      console.error('Error creating summary:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'Có lỗi xảy ra khi tạo biên bản';
      setError(errorMessage);
    } finally {
      setIsCreatingSummary(false);
    }
  };

  const handleReset = () => {
    setCurrentTaskId(null);
    setProcessingStatus(null);
    setTranscriptionResult(null);
    setMeetingSummary(null);
    setIsProcessing(false);
    setIsCreatingSummary(false);
    setError(null);
    setIsLoadingStatus(false);
  };

  const features = [
    {
      icon: <SoundOutlined />,
      title: 'Chuyển đổi giọng nói',
      description: 'Sử dụng công nghệ AI tiên tiến của OpenAI Whisper để chuyển đổi audio thành văn bản với độ chính xác cao.'
    },
    {
      icon: <RobotOutlined />,
      title: 'Tóm tắt thông minh',
      description: 'AI phân tích nội dung cuộc họp và tạo ra biên bản có cấu trúc với các điểm chính và công việc cần thực hiện.'
    },
    {
      icon: <FileTextOutlined />,
      title: 'Biên bản chuyên nghiệp',
      description: 'Tạo ra biên bản cuộc họp theo định dạng chuẩn, phù hợp với yêu cầu công sở và doanh nghiệp.'
    }
  ];

  return (
    <div className="homepage">
      {/* Hero Section */}
      <div className="hero-section">
        <div className="main-container">
          <Title level={1} className="hero-title">
            Hệ thống Tạo Biên Bản Cuộc Họp
          </Title>
          <Paragraph className="hero-subtitle">
            Chuyển đổi file audio cuộc họp thành biên bản có cấu trúc bằng công nghệ AI tiên tiến. 
            Tiết kiệm thời gian và nâng cao hiệu quả công việc.
          </Paragraph>
        </div>
      </div>

      <div className="main-container">
        {/* Features Section */}
        <div className="features-section">
          <Row gutter={[24, 24]} className="features-grid">
            {features.map((feature, index) => (
              <Col xs={24} md={8} key={index}>
                <Card className="feature-card">
                  <div className="feature-icon">{feature.icon}</div>
                  <Title level={4} className="feature-title">
                    {feature.title}
                  </Title>
                  <Paragraph className="feature-description">
                    {feature.description}
                  </Paragraph>
                </Card>
              </Col>
            ))}
          </Row>
        </div>

        {/* Upload Section */}
        <div className="upload-section">
          <AudioUploader 
            onFileSelect={handleFileSelect}
            isProcessing={isProcessing}
            progress={processingStatus?.progress || 0}
          />

          {/* Error Display */}
          {error && (
            <Alert
              message="Lỗi xử lý"
              description={error}
              type="error"
              showIcon
              closable
              onClose={() => setError(null)}
              style={{ marginBottom: '24px' }}
              action={
                <Button size="small" onClick={handleReset}>
                  Thử lại
                </Button>
              }
            />
          )}

          {/* Processing Status */}
          {processingStatus && (
            <ProcessingStatus 
              status={processingStatus} 
              isLoading={isLoadingStatus}
            />
          )}

          {/* Transcription Results */}
          {transcriptionResult && !meetingSummary && (
            <div className="transcription-section fade-in">
              <TranscriptionDisplay 
                transcription={transcriptionResult}
                onCreateSummary={handleCreateSummary}
                isCreatingSummary={isCreatingSummary}
              />
            </div>
          )}

          {/* Meeting Summary Results */}
          {meetingSummary && (
            <div className="results-section fade-in">
              <div style={{ textAlign: 'center', marginBottom: '24px' }}>
                <CheckCircleOutlined 
                  style={{ 
                    fontSize: '48px', 
                    color: '#52c41a',
                    marginBottom: '16px'
                  }} 
                />
                <Title level={2} style={{ color: '#52c41a', margin: 0 }}>
                  Xử lý hoàn tất!
                </Title>
                <Paragraph style={{ fontSize: '16px', color: '#666', marginTop: '8px' }}>
                  Biên bản cuộc họp đã được tạo thành công
                </Paragraph>
              </div>

              <MeetingSummaryDisplay summary={meetingSummary} />

              <div style={{ textAlign: 'center', marginTop: '24px' }}>
                <Button 
                  type="primary" 
                  icon={<ReloadOutlined />}
                  size="large"
                  onClick={handleReset}
                  style={{
                    background: 'linear-gradient(135deg, #1f5f8b 0%, #28a745 100%)',
                    border: 'none',
                    borderRadius: '8px',
                    padding: '0 32px',
                    height: '44px',
                    fontSize: '16px',
                  }}
                >
                  Xử lý file mới
                </Button>
              </div>
            </div>
          )}

          {/* Processing Animation */}
          {isProcessing && !processingStatus && (
            <div className="processing-animation">
              <Spin size="large" />
              <div style={{ marginTop: '16px' }}>
                <Title level={4} style={{ color: '#1f5f8b' }}>
                  Đang xử lý file audio...
                </Title>
                <Paragraph type="secondary">
                  Quá trình này có thể mất vài phút tùy thuộc vào kích thước file
                </Paragraph>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default HomePage;
