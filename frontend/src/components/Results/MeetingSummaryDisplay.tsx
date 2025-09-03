import React, { useState } from 'react';
import { 
  Typography, 
  Button, 
  Divider,
  message 
} from 'antd';
import { MeetingSummaryResponse } from '../../types/api';

const { Title, Text, Paragraph } = Typography;

interface MeetingSummaryDisplayProps {
  summary: MeetingSummaryResponse;
}

const MeetingSummaryDisplay: React.FC<MeetingSummaryDisplayProps> = ({ summary }) => {
  const [copiedSection, setCopiedSection] = useState<string | null>(null);

  const copyToClipboard = async (text: string, section: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedSection(section);
      message.success(`Đã sao chép ${section}`);
      setTimeout(() => setCopiedSection(null), 2000);
    } catch (error) {
      message.error('Không thể sao chép văn bản');
    }
  };

  const downloadAsText = () => {
    const content = `
BIÊN BẢN CUỘC HỌP
==================

Thời gian xử lý: ${new Date(summary.processed_at).toLocaleString('vi-VN')}
Thời lượng cuộc họp: ${summary.meeting_duration || 'Không xác định'}

TÓM TẮT
-------
${summary.summary}

ĐIỂM CHÍNH
----------
${summary.key_points.map((point, index) => `${index + 1}. ${point}`).join('\n')}

CÔNG VIỆC CẦN THỰC HIỆN
-----------------------
${summary.action_items.map((item, index) => `${index + 1}. ${item}`).join('\n')}

NGƯỜI THAM GIA
--------------
${summary.participants.length > 0 ? summary.participants.join(', ') : 'Không xác định'}

---
Được tạo bởi Hệ thống Tạo Biên Bản Cuộc Họp AI
`;

    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `bien-ban-cuoc-hop-${summary.task_id.slice(0, 8)}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    message.success('Đã tải xuống biên bản cuộc họp');
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('vi-VN');
  };

  return (
    <div className="meeting-summary-display" style={{ 
      maxWidth: '800px', 
      margin: '0 auto',
      background: '#ffffff',
      padding: '40px',
      borderRadius: '8px',
      boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
      fontFamily: '"Times New Roman", Times, serif',
      color: '#000000'
    }}>
      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: '40px', borderBottom: '3px double #333', paddingBottom: '20px' }}>
        <Title level={1} style={{ 
          margin: 0, 
          fontSize: '24px', 
          fontWeight: 'bold',
          textTransform: 'uppercase',
          letterSpacing: '2px',
          color: '#000000',
          fontFamily: '"Times New Roman", Times, serif'
        }}>
          BIÊN BẢN CUỘC HỌP
        </Title>
      </div>

      {/* Actions Bar */}
      <div style={{ textAlign: 'right', marginBottom: '30px' }}>
        <Button 
          type="default" 
          onClick={downloadAsText}
          size="small"
          style={{ marginRight: '8px', color: '#000000', fontFamily: '"Times New Roman", Times, serif' }}
        >
          Tải xuống
        </Button>
        <Button 
          type="text" 
          size="small"
          onClick={() => copyToClipboard(
            `BIÊN BẢN CUỘC HỌP\n\n` +
            `Thời gian xử lý: ${formatDate(summary.processed_at)}\n` +
            `${summary.meeting_duration ? `Thời lượng cuộc họp: ${summary.meeting_duration}\n` : ''}` +
            `ID: ${summary.task_id.slice(0, 8)}\n\n` +
            `## TÓM TẮT\n\n${summary.summary}\n\n` +
            `## ĐIỂM CHÍNH\n\n${summary.key_points.map((point, index) => `${index + 1}. ${point}`).join('\n')}\n\n` +
            `## CÔNG VIỆC CẦN THỰC HIỆN\n\n${summary.action_items.map((item, index) => `${index + 1}. ${item}`).join('\n')}\n\n` +
            `${summary.participants.length > 0 ? `## NGƯỜI THAM GIA\n\n${summary.participants.join(', ')}\n\n` : ''}`,
            'toàn bộ biên bản'
          )}
          style={{ 
            color: '#000000',
            fontFamily: '"Times New Roman", Times, serif'
          }}
        >
          {copiedSection === 'toàn bộ biên bản' ? 'Đã sao chép' : 'Sao chép toàn bộ'}
        </Button>
      </div>

      {/* Metadata */}
      <div style={{ marginBottom: '30px', fontSize: '14px', color: '#000000', fontFamily: '"Times New Roman", Times, serif' }}>
        <div style={{ marginBottom: '8px' }}>
          <strong>Thời gian xử lý:</strong> {formatDate(summary.processed_at)}
        </div>
        {summary.meeting_duration && (
          <div style={{ marginBottom: '8px' }}>
            <strong>Thời lượng cuộc họp:</strong> {summary.meeting_duration}
          </div>
        )}
        <div style={{ marginBottom: '8px' }}>
          <strong>ID:</strong> {summary.task_id.slice(0, 8)}
        </div>
      </div>

      <Divider style={{ margin: '30px 0', borderColor: '#333' }} />

      {/* Summary Section */}
      <div style={{ marginBottom: '40px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <Title level={2} style={{ 
            margin: 0, 
            fontSize: '18px', 
            fontWeight: 'bold',
            textTransform: 'uppercase',
            borderBottom: '2px solid #333',
            paddingBottom: '4px',
            color: '#000000',
            fontFamily: '"Times New Roman", Times, serif'
          }}>
            TÓM TẮT
          </Title>
          <Button 
            type="text" 
            size="small"
            onClick={() => copyToClipboard(summary.summary, 'tóm tắt')}
            style={{ 
              color: '#000000',
              fontSize: '12px',
              fontFamily: '"Times New Roman", Times, serif'
            }}
          >
            {copiedSection === 'tóm tắt' ? 'Đã sao chép' : 'Sao chép'}
          </Button>
        </div>
        <Paragraph style={{ 
          fontSize: '15px', 
          lineHeight: '1.8', 
          textAlign: 'justify',
          textIndent: '2em',
          marginBottom: 0,
          color: '#000000',
          fontFamily: '"Times New Roman", Times, serif'
        }}>
          {summary.summary}
        </Paragraph>
      </div>

      {/* Key Points */}
      <div style={{ marginBottom: '40px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <Title level={2} style={{ 
            margin: 0, 
            fontSize: '18px', 
            fontWeight: 'bold',
            textTransform: 'uppercase',
            borderBottom: '2px solid #333',
            paddingBottom: '4px',
            color: '#000000',
            fontFamily: '"Times New Roman", Times, serif'
          }}>
            ĐIỂM CHÍNH
          </Title>
          <Button 
            type="text" 
            size="small"
            onClick={() => copyToClipboard(summary.key_points.map((point, index) => `${index + 1}. ${point}`).join('\n'), 'điểm chính')}
            style={{ 
              color: '#000000',
              fontSize: '12px',
              fontFamily: '"Times New Roman", Times, serif'
            }}
          >
            {copiedSection === 'điểm chính' ? 'Đã sao chép' : 'Sao chép'}
          </Button>
        </div>
        <div>
          {summary.key_points.map((item, index) => (
            <div key={index} style={{ 
              marginBottom: '12px', 
              fontSize: '15px', 
              lineHeight: '1.6',
              display: 'flex',
              alignItems: 'flex-start'
            }}>
              <span style={{ 
                minWidth: '24px', 
                fontWeight: 'bold',
                marginRight: '8px',
                color: '#000000',
                fontFamily: '"Times New Roman", Times, serif'
              }}>
                {index + 1}.
              </span>
              <span style={{ textAlign: 'justify', color: '#000000', fontFamily: '"Times New Roman", Times, serif' }}>{item}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Action Items */}
      <div style={{ marginBottom: '40px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <Title level={2} style={{ 
            margin: 0, 
            fontSize: '18px', 
            fontWeight: 'bold',
            textTransform: 'uppercase',
            borderBottom: '2px solid #333',
            paddingBottom: '4px',
            color: '#000000',
            fontFamily: '"Times New Roman", Times, serif'
          }}>
            CÔNG VIỆC CẦN THỰC HIỆN
          </Title>
          <Button 
            type="text" 
            size="small"
            onClick={() => copyToClipboard(summary.action_items.map((item, index) => `${index + 1}. ${item}`).join('\n'), 'công việc')}
            style={{ 
              color: '#000000',
              fontSize: '12px',
              fontFamily: '"Times New Roman", Times, serif'
            }}
          >
            {copiedSection === 'công việc' ? 'Đã sao chép' : 'Sao chép'}
          </Button>
        </div>
        <div>
          {summary.action_items.map((item, index) => (
            <div key={index} style={{ 
              marginBottom: '12px', 
              fontSize: '15px', 
              lineHeight: '1.6',
              display: 'flex',
              alignItems: 'flex-start'
            }}>
              <span style={{ 
                minWidth: '24px', 
                fontWeight: 'bold',
                marginRight: '8px',
                color: '#000000',
                fontFamily: '"Times New Roman", Times, serif'
              }}>
                {index + 1}.
              </span>
              <span style={{ textAlign: 'justify', color: '#000000', fontFamily: '"Times New Roman", Times, serif' }}>{item}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Participants */}
      {summary.participants.length > 0 && (
        <div style={{ marginBottom: '40px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <Title level={2} style={{ 
              margin: 0, 
              fontSize: '18px', 
              fontWeight: 'bold',
              textTransform: 'uppercase',
              borderBottom: '2px solid #333',
              paddingBottom: '4px',
              color: '#000000',
              fontFamily: '"Times New Roman", Times, serif'
            }}>
              NGƯỜI THAM GIA
            </Title>
            <Button 
              type="text" 
              size="small"
              onClick={() => copyToClipboard(summary.participants.join(', '), 'người tham gia')}
              style={{ 
                color: '#000000',
                fontSize: '12px',
                fontFamily: '"Times New Roman", Times, serif'
              }}
            >
              {copiedSection === 'người tham gia' ? 'Đã sao chép' : 'Sao chép'}
            </Button>
          </div>
          <Paragraph style={{ 
            fontSize: '15px', 
            lineHeight: '1.6',
            textAlign: 'justify',
            color: '#000000',
            fontFamily: '"Times New Roman", Times, serif'
          }}>
            {summary.participants.join(', ')}
          </Paragraph>
        </div>
      )}

      {/* Transcription Section */}
      {summary.transcription && (
        <div style={{ marginBottom: '40px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <Title level={2} style={{ 
              margin: 0, 
              fontSize: '18px', 
              fontWeight: 'bold',
              textTransform: 'uppercase',
              borderBottom: '2px solid #333',
              paddingBottom: '4px',
              color: '#000000',
              fontFamily: '"Times New Roman", Times, serif'
            }}>
              NỘI DUNG TRÍCH XUẤT
              {summary.transcription_language && (
                <span style={{ 
                  fontSize: '12px', 
                  fontWeight: 'normal',
                  marginLeft: '8px',
                  color: '#000000',
                  fontFamily: '"Times New Roman", Times, serif'
                }}>
                  ({summary.transcription_language.toUpperCase()})
                </span>
              )}
            </Title>
            <Button 
              type="text" 
              size="small"
              onClick={() => copyToClipboard(summary.transcription || '', 'nội dung trích xuất')}
              style={{ 
                color: '#000000',
                fontSize: '12px',
                fontFamily: '"Times New Roman", Times, serif'
              }}
            >
              {copiedSection === 'nội dung trích xuất' ? 'Đã sao chép' : 'Sao chép'}
            </Button>
          </div>
          <div style={{ 
            background: '#f8f9fa',
            border: '1px solid #e9ecef',
            padding: '20px',
            borderRadius: '4px',
            maxHeight: '400px',
            overflow: 'auto'
          }}>
            <Text style={{ 
              whiteSpace: 'pre-wrap', 
              wordBreak: 'break-word',
              lineHeight: '1.6',
              fontSize: '14px',
              fontFamily: '"Times New Roman", Times, serif',
              color: '#000000'
            }}>
              {summary.transcription || ''}
            </Text>
          </div>
        </div>
      )}

      {/* Footer */}
      <Divider style={{ margin: '40px 0 20px 0', borderColor: '#333' }} />
      <div style={{ textAlign: 'center', fontSize: '12px', color: '#000000', fontStyle: 'italic', fontFamily: '"Times New Roman", Times, serif' }}>
        Được tạo bởi Hệ thống Tạo Biên Bản Cuộc Họp AI
      </div>
    </div>
  );
};

export default MeetingSummaryDisplay;
