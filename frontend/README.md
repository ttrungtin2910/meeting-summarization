# Meeting Summary Frontend

Frontend React TypeScript cho ứng dụng AI tạo biên bản cuộc họp từ file audio.

## Tính năng

- **UI/UX Chính phủ**: Thiết kế với tone màu và phong cách phù hợp với các cơ quan chính phủ
- **Upload Audio**: Drag & drop hoặc click để chọn file audio
- **Real-time Status**: Theo dõi tiến trình xử lý real-time
- **Kết quả Có cấu trúc**: Hiển thị biên bản cuộc họp với các section rõ ràng
- **Responsive Design**: Tương thích với mọi thiết bị
- **Copy & Download**: Sao chép nội dung hoặc tải xuống biên bản

## Công nghệ sử dụng

- **React 18** với TypeScript
- **Ant Design** cho UI components
- **Axios** cho API calls
- **React Router** cho routing
- **CSS-in-JS** với custom styling

## Cấu trúc Project

```
frontend/
├── public/
│   └── index.html              # HTML template
├── src/
│   ├── components/             # React components
│   │   ├── Layout/             # Header, Footer
│   │   ├── Upload/             # Audio uploader
│   │   └── Results/            # Status và summary display
│   ├── pages/                  # Page components
│   │   └── HomePage.tsx        # Main page
│   ├── services/               # API services
│   │   └── api.ts              # API client
│   ├── types/                  # TypeScript types
│   │   └── api.ts              # API response types
│   ├── App.tsx                 # Main app component
│   ├── index.tsx              # Entry point
│   └── index.css              # Global styles
├── package.json               # Dependencies
└── tsconfig.json             # TypeScript config
```

## Cài đặt và chạy

### Yêu cầu
- Node.js 16+
- npm hoặc yarn

### Cài đặt
```bash
# Cài đặt dependencies
npm install

# Hoặc với yarn
yarn install
```

### Chạy development server
```bash
npm start
# hoặc
yarn start
```

Ứng dụng sẽ chạy tại: http://localhost:3000

### Build production
```bash
npm run build
# hoặc
yarn build
```

## Cấu hình

### Environment Variables
Tạo file `.env` trong thư mục frontend:

```bash
# API URL (optional, mặc định: http://localhost:8000)
REACT_APP_API_URL=http://localhost:8000
```

### Proxy Configuration
File `package.json` đã được cấu hình proxy để redirect API calls đến backend:
```json
"proxy": "http://localhost:8000"
```

## Tính năng UI/UX

### Màu sắc chính phủ
- **Primary**: #1f5f8b (Deep Blue)
- **Secondary**: #28a745 (Green)
- **Background**: Gradient từ #e8f5e8 đến #f0f8ff
- **Cards**: White với shadow và border radius

### Components chính

#### AudioUploader
- Drag & drop area
- File validation (format, size)
- Progress indicator
- Error handling

#### ProcessingStatus
- Real-time status updates
- Timeline visualization
- Progress bars
- Error messages

#### MeetingSummaryDisplay
- Structured layout cho biên bản
- Collapsible sections
- Copy to clipboard
- Download functionality

### Responsive Design
- Mobile-first approach
- Breakpoints: 480px, 768px, 1200px
- Adaptive grid layout
- Touch-friendly interfaces

## API Integration

### Endpoints được sử dụng
- `POST /api/v1/process-audio` - Upload và xử lý đồng bộ
- `POST /api/v1/upload-audio` - Upload bất đồng bộ
- `GET /api/v1/tasks/{id}/status` - Lấy trạng thái
- `GET /api/v1/tasks/{id}/summary` - Lấy kết quả

### Error Handling
- Network errors
- API errors với status codes
- User-friendly error messages
- Retry mechanisms

## Customization

### Thay đổi theme colors
Chỉnh sửa trong `src/index.tsx`:
```typescript
const theme = {
  token: {
    colorPrimary: '#1f5f8b',
    colorSuccess: '#28a745',
    // ...
  },
};
```

### Thay đổi UI text
Tất cả text đều được hardcode để dễ customization. Có thể chuyển sang i18n nếu cần đa ngôn ngữ.

### Upload limits
Cấu hình trong `AudioUploader.tsx`:
```typescript
const maxSize = 25 * 1024 * 1024; // 25MB
const supportedFormats = ['mp3', 'wav', 'm4a', 'mp4', 'webm', 'flac'];
```

## Performance

### Optimizations
- Code splitting với React.lazy (nếu cần)
- Memoization cho expensive components
- Debounced API calls
- Efficient re-renders với proper keys

### Bundle size
- Ant Design tree shaking
- TypeScript compilation optimizations
- CSS minification

## Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Development Tips

### Hot Reload
Development server hỗ trợ hot reload cho rapid development.

### TypeScript
Strict mode enabled cho type safety. Tất cả API responses đều có proper typing.

### Debugging
- React DevTools
- Redux DevTools (nếu thêm state management)
- Network tab cho API debugging
