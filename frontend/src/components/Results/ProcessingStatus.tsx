import React from 'react';
import { Card, Progress, Timeline, Typography, Space, Spin, Tag } from 'antd';
import { 
  ClockCircleOutlined, 
  SoundOutlined, 
  FileTextOutlined, 
  CheckCircleOutlined,
  ExclamationCircleOutlined,
  LoadingOutlined 
} from '@ant-design/icons';
import { ProcessingStatusResponse, ProcessingStatus as ProcessingStatusType } from '../../types/api';

const { Title, Text } = Typography;

interface ProcessingStatusProps {
  status: ProcessingStatusResponse;
  isLoading?: boolean;
}

const ProcessingStatus: React.FC<ProcessingStatusProps> = ({ status, isLoading }) => {
  const getStatusColor = (currentStatus: ProcessingStatusType) => {
    switch (currentStatus) {
      case 'pending':
        return '#faad14';
      case 'uploading':
        return '#1890ff';
      case 'transcribing':
        return '#722ed1';
      case 'summarizing':
        return '#13c2c2';
      case 'completed':
        return '#52c41a';
      case 'failed':
        return '#ff4d4f';
      default:
        return '#d9d9d9';
    }
  };

  const getStatusText = (currentStatus: ProcessingStatusType) => {
    switch (currentStatus) {
      case 'pending':
        return 'Đang chờ xử lý';
      case 'uploading':
        return 'Đang tải lên';
      case 'transcribing':
        return 'Đang chuyển đổi giọng nói';
      case 'summarizing':
        return 'Đang tạo biên bản';
      case 'completed':
        return 'Hoàn thành';
      case 'failed':
        return 'Xử lý thất bại';
      default:
        return 'Không xác định';
    }
  };

  const getTimelineItems = () => {
    const statuses: ProcessingStatusType[] = ['uploading', 'transcribing', 'summarizing', 'completed'];
    const statusLabels = [
      'Tải lên file audio',
      'Chuyển đổi giọng nói thành văn bản',
      'Tạo biên bản cuộc họp',
      'Hoàn thành xử lý'
    ];
    const statusIcons = [
      <SoundOutlined />,
      <FileTextOutlined />,
      <FileTextOutlined />,
      <CheckCircleOutlined />
    ];

    return statuses.map((stepStatus, index) => {
      let color = '#d9d9d9';
      let icon = statusIcons[index];

      if (status.status === 'failed') {
        // For failed status, highlight first step in red
        color = index === 0 ? '#ff4d4f' : '#d9d9d9';
        icon = index === 0 ? <ExclamationCircleOutlined /> : icon;
      } else {
        const currentIndex = statuses.indexOf(status.status);
        
        if (currentIndex >= 0) {
          // Valid status in our timeline
          if (index < currentIndex) {
            // Completed steps
            color = '#52c41a';
          } else if (index === currentIndex) {
            // Current step
            color = getStatusColor(status.status);
            if (stepStatus !== 'completed') {
              icon = <LoadingOutlined spin />;
            }
          }
          // Future steps remain gray (default)
        } else if (status.status === 'pending') {
          // Pending status - all steps are gray
          color = '#d9d9d9';
        }
      }

      return {
        color,
        dot: React.cloneElement(icon, { style: { fontSize: '16px' } }),
        children: (
          <div>
            <Text strong style={{ color: color === '#d9d9d9' ? '#999' : '#333' }}>
              {statusLabels[index]}
            </Text>
            {index === statuses.indexOf(status.status) && status.status !== 'completed' && (
              <div style={{ marginTop: '4px' }}>
                <Progress 
                  percent={status.progress} 
                  size="small" 
                  strokeColor={color}
                  showInfo={false}
                />
              </div>
            )}
          </div>
        ),
      };
    });
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('vi-VN');
  };

  return (
    <Card 
      className="gov-card"
      title={
        <Space>
          <ClockCircleOutlined style={{ color: '#1f5f8b' }} />
          <Title level={4} style={{ margin: 0, color: '#1f5f8b' }}>
            Trạng thái xử lý
          </Title>
        </Space>
      }
      style={{ marginBottom: '24px' }}
    >
      <Space direction="vertical" style={{ width: '100%' }} size="large">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <Text strong>Mã tác vụ: </Text>
            <Text code>{status.task_id}</Text>
          </div>
          <Tag 
            color={getStatusColor(status.status)}
            style={{ 
              fontSize: '12px', 
              fontWeight: 600,
              padding: '4px 12px',
              borderRadius: '12px'
            }}
          >
            {getStatusText(status.status).toUpperCase()}
          </Tag>
        </div>

        <div>
          <Title level={5} style={{ marginBottom: '16px', color: '#333' }}>
            Tiến trình xử lý
          </Title>
          <Timeline items={getTimelineItems()} />
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: '#666' }}>
          <span>Bắt đầu: {formatDate(status.created_at)}</span>
          <span>Cập nhật: {formatDate(status.updated_at)}</span>
        </div>

        {status.status === 'failed' && status.message && (
          <div style={{ 
            background: '#fff2f0', 
            border: '1px solid #ffccc7',
            borderRadius: '8px',
            padding: '12px'
          }}>
            <Text type="danger">
              <ExclamationCircleOutlined style={{ marginRight: '8px' }} />
              Lỗi: {status.message}
            </Text>
          </div>
        )}

        {isLoading && (
          <div style={{ textAlign: 'center', padding: '20px' }}>
            <Spin size="large" />
            <div style={{ marginTop: '12px' }}>
              <Text type="secondary">Đang cập nhật trạng thái...</Text>
            </div>
          </div>
        )}
      </Space>
    </Card>
  );
};

export default ProcessingStatus;
