import React, { useState, useCallback, useMemo } from 'react';
import { Upload, Button, message, Progress, Card, Space, Typography } from 'antd';
import { 
  UploadOutlined, 
  InboxOutlined, 
  AudioOutlined,
  DeleteOutlined,
  PlayCircleOutlined 
} from '@ant-design/icons';
import type { UploadProps, UploadFile, RcFile } from 'antd/es/upload';

const { Dragger } = Upload;
const { Text, Title } = Typography;

interface AudioUploaderProps {
  onFileSelect: (file: File) => void;
  isProcessing: boolean;
  progress: number;
}

const AudioUploader: React.FC<AudioUploaderProps> = ({
  onFileSelect,
  isProcessing,
  progress,
}) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [fileList, setFileList] = useState<UploadFile[]>([]);

  const supportedFormats = useMemo(() => ['mp3', 'wav', 'm4a', 'mp4', 'webm', 'flac'], []);
  const maxSize = 25 * 1024 * 1024; // 25MB

  const beforeUpload = useCallback((file: File) => {
    // Check file size
    if (file.size > maxSize) {
      message.error(`File quá lớn! Kích thước tối đa: 25MB`);
      return false;
    }

    // Check file format
    const fileExtension = file.name.split('.').pop()?.toLowerCase();
    if (!fileExtension || !supportedFormats.includes(fileExtension)) {
      message.error(
        `Định dạng file không được hỗ trợ! Hỗ trợ: ${supportedFormats.join(', ')}`
      );
      return false;
    }

    // Set selected file
    setSelectedFile(file);
    
    // Create proper UploadFile object
    const uploadFile: UploadFile = {
      uid: file.name + '-' + Date.now(),
      name: file.name,
      status: 'done',
      size: file.size,
      type: file.type,
      originFileObj: file as RcFile,
    };
    
    setFileList([uploadFile]);

    return false; // Prevent auto upload
  }, [maxSize, supportedFormats]);

  const handleRemove = useCallback(() => {
    setSelectedFile(null);
    setFileList([]);
  }, []);

  const handleProcess = useCallback(() => {
    if (selectedFile) {
      onFileSelect(selectedFile);
    }
  }, [selectedFile, onFileSelect]);

  const uploadProps: UploadProps = {
    name: 'audio',
    multiple: false,
    fileList,
    beforeUpload,
    onRemove: handleRemove,
    showUploadList: false,
    accept: supportedFormats.map(format => `.${format}`).join(','),
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  // Removed formatDuration as it's not currently used
  // Can be re-added later if needed for showing audio duration

  return (
    <div className="audio-uploader">
      <Card 
        className="gov-card"
        style={{ marginBottom: '24px' }}
      >
        <Title level={4} style={{ textAlign: 'center', marginBottom: '24px', color: '#1f5f8b' }}>
          <AudioOutlined style={{ marginRight: '8px' }} />
          Tải lên file audio cuộc họp
        </Title>

        {!selectedFile ? (
          <Dragger 
            {...uploadProps}
            className="upload-area"
            style={{
              padding: '40px 20px',
              background: '#fafafa',
              border: '2px dashed #d9d9d9',
              borderRadius: '12px',
            }}
          >
            <p className="ant-upload-drag-icon">
              <InboxOutlined style={{ fontSize: '48px', color: '#1f5f8b' }} />
            </p>
            <p className="ant-upload-text" style={{ fontSize: '18px', color: '#333' }}>
              Kéo thả file audio vào đây hoặc click để chọn
            </p>
            <p className="ant-upload-hint" style={{ color: '#666' }}>
              Hỗ trợ: {supportedFormats.join(', ').toUpperCase()} | Tối đa: 25MB
            </p>
          </Dragger>
        ) : (
          <div className="selected-file-info">
            <Card 
              size="small" 
              style={{ 
                background: '#f0f8ff', 
                border: '1px solid #1f5f8b',
                borderRadius: '8px'
              }}
            >
              <Space direction="vertical" style={{ width: '100%' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <Space>
                    <PlayCircleOutlined style={{ fontSize: '20px', color: '#1f5f8b' }} />
                    <div>
                      <Text strong style={{ color: '#1f5f8b' }}>{selectedFile.name}</Text>
                      <br />
                      <Text type="secondary" style={{ fontSize: '12px' }}>
                        {formatFileSize(selectedFile.size)}
                      </Text>
                    </div>
                  </Space>
                  
                  <Button 
                    type="text" 
                    icon={<DeleteOutlined />} 
                    onClick={handleRemove}
                    disabled={isProcessing}
                    danger
                  />
                </div>

                {isProcessing && (
                  <div>
                    <Progress 
                      percent={progress} 
                      size="small"
                      strokeColor="#1f5f8b"
                      showInfo={true}
                      format={(percent) => `${percent}%`}
                    />
                    <Text type="secondary" style={{ fontSize: '12px', marginTop: '4px', display: 'block' }}>
                      Đang xử lý file audio...
                    </Text>
                  </div>
                )}
              </Space>
            </Card>

            {!isProcessing && (
              <div style={{ textAlign: 'center', marginTop: '20px' }}>
                <Button 
                  type="primary" 
                  size="large"
                  icon={<UploadOutlined />}
                  onClick={handleProcess}
                  style={{
                    background: 'linear-gradient(135deg, #1f5f8b 0%, #28a745 100%)',
                    border: 'none',
                    borderRadius: '8px',
                    padding: '0 40px',
                    height: '48px',
                    fontSize: '16px',
                    fontWeight: 600,
                  }}
                >
                  Bắt đầu xử lý
                </Button>
              </div>
            )}
          </div>
        )}

        <div style={{ marginTop: '16px', textAlign: 'center' }}>
          <Text type="secondary" style={{ fontSize: '12px' }}>
            💡 Tip: File audio chất lượng cao sẽ cho kết quả transcription tốt hơn
          </Text>
        </div>
      </Card>
    </div>
  );
};

export default AudioUploader;
