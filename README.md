# 🎙️ Hệ thống Tạo Biên Bản Cuộc Họp AI

Ứng dụng web AI tạo biên bản cuộc họp từ file audio sử dụng OpenAI Speech-to-Text và GPT. Hệ thống bao gồm backend FastAPI và frontend ReactJS với UI/UX phù hợp chính phủ.

## 🌟 Tính năng chính

- **🎵 Upload Audio**: Hỗ trợ nhiều định dạng audio (mp3, wav, m4a, mp4, webm, flac)
- **🤖 Speech-to-Text**: Chuyển đổi giọng nói thành văn bản bằng OpenAI Whisper
- **📋 AI Summary**: Tóm tắt thông minh thành biên bản có cấu trúc
- **⚡ Real-time Processing**: Theo dõi tiến trình xử lý real-time
- **💾 Export**: Sao chép và tải xuống biên bản
- **📱 Responsive**: Tương thích mọi thiết bị

## 🏗️ Kiến trúc hệ thống

```
meeting-summary-system/
├── backend/                    # FastAPI Backend
│   ├── src/meeting_summary/
│   │   ├── api/               # API layer (Controllers, Schemas)
│   │   ├── application/       # Business logic (Services)
│   │   ├── domain/           # Domain models & exceptions
│   │   ├── infrastructure/   # External services (OpenAI, Storage)
│   │   └── config/          # Configuration
│   └── main.py              # Entry point
├── frontend/                  # React TypeScript Frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API clients
│   │   └── types/         # TypeScript types
│   └── public/            # Static assets
└── README.md             # Hướng dẫn này
```

## 🚀 Cài đặt và chạy

### Yêu cầu hệ thống
- Python 3.10+ (khuyến khích dùng Conda)
- Node.js 16+
- OpenAI API Key

### 1. Backend Setup

#### Option A: Sử dụng Conda (Khuyến nghị)

**Cách 1: Setup tự động**
```bash
# Di chuyển vào thư mục backend
cd backend

# Chạy script setup tự động
chmod +x setup_conda.sh && ./setup_conda.sh  # Linux/Mac
# hoặc setup_conda.bat                        # Windows

# Activate environment và chạy
conda activate meeting-summary
python main.py
```

**Cách 2: Setup thủ công**
```bash
# Tạo conda environment với Python 3.10
conda create -n meeting-summary python=3.10 -y
conda activate meeting-summary

# Di chuyển vào thư mục backend
cd backend

# Cài đặt dependencies
pip install -r requirements.txt
# hoặc sử dụng conda environment file
# conda env create -f environment.yml

# Tạo file .env và cấu hình OpenAI API key
# (Sao chép từ .env.example nếu có)

# Chạy server
python main.py
# hoặc uvicorn main:app --reload
```

#### Option B: Sử dụng Poetry
```bash
# Di chuyển vào thư mục backend
cd backend

# Cài đặt dependencies với poetry
poetry install
poetry shell

# Cấu hình environment variables
cp .env.example .env
# Chỉnh sửa .env với OpenAI API key của bạn

# Chạy server
python main.py
# hoặc uvicorn main:app --reload
```

#### Option C: Sử dụng pip thông thường
```bash
# Di chuyển vào thư mục backend
cd backend

# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc venv\Scripts\activate  # Windows

# Cài đặt dependencies
pip install -r requirements.txt

# Cấu hình environment variables
cp .env.example .env
# Chỉnh sửa .env với OpenAI API key của bạn

# Chạy server
python main.py
```

Backend sẽ chạy tại: http://localhost:8000

### 2. Frontend Setup

```bash
# Di chuyển vào thư mục frontend
cd frontend

# Cài đặt dependencies
npm install

# Chạy development server
npm start
```

Frontend sẽ chạy tại: http://localhost:3000

## ⚙️ Cấu hình

### Backend Environment Variables
```bash
# .env file trong thư mục backend
OPENAI_API_KEY=your_openai_api_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Frontend Environment Variables
```bash
# .env file trong thư mục frontend (optional)
REACT_APP_API_URL=http://localhost:8000
```

## 📖 Sử dụng

1. **Truy cập ứng dụng**: Mở http://localhost:3000
2. **Upload audio**: Kéo thả hoặc click chọn file audio cuộc họp
3. **Xử lý**: Hệ thống sẽ tự động chuyển đổi và tóm tắt
4. **Xem kết quả**: Biên bản cuộc họp với cấu trúc rõ ràng
5. **Export**: Sao chép hoặc tải xuống biên bản

## 🔄 API Endpoints

### Xử lý đồng bộ (khuyến nghị cho file < 10MB)
```bash
POST /api/v1/process-audio
Content-Type: multipart/form-data
Body: file=audio_file
```

### Xử lý bất đồng bộ (cho file lớn)
```bash
# Upload
POST /api/v1/upload-audio

# Theo dõi trạng thái
GET /api/v1/tasks/{task_id}/status

# Lấy kết quả
GET /api/v1/tasks/{task_id}/summary
```

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🎨 UI/UX Design

### Màu sắc chính phủ
- **Primary**: #1f5f8b (Deep Blue) - Màu chủ đạo
- **Secondary**: #28a745 (Green) - Màu phụ
- **Background**: Gradient xanh nhạt
- **Cards**: Trắng với shadow tinh tế

### Tính năng UI
- **Drag & Drop**: Upload file dễ dàng
- **Progress Indicators**: Theo dõi tiến trình xử lý
- **Timeline**: Hiển thị các bước xử lý
- **Collapsible Sections**: Tổ chức nội dung gọn gàng
- **Copy to Clipboard**: Sao chép nhanh
- **Download**: Tải xuống file văn bản

## 🔧 Công nghệ sử dụng

### Backend
- **FastAPI**: Modern Python web framework
- **OpenAI**: Whisper (Speech-to-Text) & GPT (Summarization)
- **Pydantic**: Data validation
- **Loguru**: Logging
- **Clean Architecture**: Tổ chức code rõ ràng

### Frontend
- **React 18**: Modern React với hooks
- **TypeScript**: Type safety
- **Ant Design**: Professional UI components
- **Axios**: HTTP client
- **CSS-in-JS**: Custom styling

## 📁 File hỗ trợ

- **Audio formats**: mp3, wav, m4a, mp4, webm, flac
- **Maximum size**: 25MB (theo giới hạn OpenAI)
- **Language**: Tiếng Việt (có thể cấu hình)

## 🔍 Kiểm tra và debug

### Backend
```bash
# Kiểm tra API
curl -X POST "http://localhost:8000/api/v1/process-audio" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_audio.mp3"

# Xem logs
tail -f logs/app.log
```

### Frontend
- Mở Developer Tools
- Kiểm tra Network tab cho API calls
- Console tab cho errors

## 📦 Production Deployment

### Backend
```bash
# Build với Poetry
poetry build

# Hoặc sử dụng Docker
docker build -t meeting-summary-backend .
docker run -p 8000:8000 meeting-summary-backend
```

### Frontend
```bash
# Build production
npm run build

# Deploy static files
# Có thể sử dụng nginx, netlify, vercel, etc.
```

## 🤝 Đóng góp

1. Fork project
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Hỗ trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra [Issues](../../issues)
2. Tạo issue mới với thông tin chi tiết
3. Provide logs và error messages

## 🔮 Roadmap

- [ ] **Multi-language support**: Hỗ trợ nhiều ngôn ngữ
- [ ] **Voice activity detection**: Tự động phát hiện người nói
- [ ] **Integration với calendar**: Sync với lịch họp
- [ ] **Advanced analytics**: Thống kê và báo cáo
- [ ] **Mobile app**: Ứng dụng di động
- [ ] **Real-time collaboration**: Chỉnh sửa biên bản real-time

---

**Made with ❤️ using AI technology**
