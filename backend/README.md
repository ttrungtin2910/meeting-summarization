# Meeting Summary Backend

Backend API cho ứng dụng AI tạo biên bản cuộc họp từ file audio sử dụng OpenAI Speech-to-Text.

## Tính năng

- **Upload Audio**: Hỗ trợ upload file audio (mp3, wav, m4a, mp4, webm, flac)
- **Speech-to-Text**: Chuyển đổi audio thành văn bản sử dụng OpenAI Whisper
- **Meeting Summary**: Tóm tắt văn bản thành biên bản cuộc họp có cấu trúc
- **Async Processing**: Xử lý bất đồng bộ với theo dõi trạng thái
- **Clean Architecture**: Cấu trúc code rõ ràng theo Clean Architecture

## Cấu trúc Project

```
backend/
├── src/meeting_summary/
│   ├── api/                    # API layer (Controllers, Schemas, Dependencies)
│   │   ├── v1/                 # API version 1
│   │   ├── schemas/            # Request/Response schemas
│   │   └── dependencies/       # Dependency injection
│   ├── application/            # Application layer (Services, Use cases)
│   │   └── services/           # Business logic services
│   ├── domain/                 # Domain layer (Models, Exceptions, Value objects)
│   │   ├── models/             # Domain models
│   │   └── exceptions/         # Domain exceptions
│   ├── infrastructure/         # Infrastructure layer (External services)
│   │   ├── openai_client/      # OpenAI integration
│   │   └── storage/            # File storage
│   └── config/                 # Configuration
├── main.py                     # Entry point
└── pyproject.toml             # Dependencies
```

## Cài đặt

1. **Cài đặt dependencies**:
   ```bash
   pip install -r requirements.txt
   # hoặc sử dụng poetry
   poetry install
   ```

2. **Cấu hình environment variables**:
   ```bash
   # Tạo file .env
   OPENAI_API_KEY=your_openai_api_key_here
   JWT_SECRET_KEY=your_jwt_secret_key_here
   JWT_ALGORITHM=HS256
   ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
   ```

3. **Chạy server**:
   ```bash
   python main.py
   # hoặc
   uvicorn main:app --reload
   ```

Server sẽ chạy tại: http://127.0.0.1:8000

## API Endpoints

### Upload và xử lý hoàn chỉnh
- `POST /api/v1/process-audio` - Upload và xử lý audio hoàn chỉnh (sync)

### Upload và xử lý bất đồng bộ
- `POST /api/v1/upload-audio` - Upload file audio
- `GET /api/v1/tasks/{task_id}/status` - Lấy trạng thái xử lý
- `GET /api/v1/tasks/{task_id}/transcription` - Lấy kết quả transcription
- `GET /api/v1/tasks/{task_id}/summary` - Lấy biên bản cuộc họp

### API Documentation
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Ví dụ sử dụng

### 1. Xử lý hoàn chỉnh (Đồng bộ)
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/process-audio" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@meeting.mp3"
```

### 2. Xử lý bất đồng bộ
```bash
# Upload file
curl -X POST "http://127.0.0.1:8000/api/v1/upload-audio" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@meeting.mp3"

# Kiểm tra trạng thái
curl "http://127.0.0.1:8000/api/v1/tasks/{task_id}/status"

# Lấy kết quả
curl "http://127.0.0.1:8000/api/v1/tasks/{task_id}/summary"
```

## Các file được hỗ trợ

- **Audio formats**: mp3, wav, m4a, mp4, webm, flac
- **Maximum size**: 25MB (theo giới hạn của OpenAI)
- **Language**: Tiếng Việt (có thể cấu hình)

## Development

### Cấu trúc Clean Architecture

1. **API Layer**: Chứa controllers, schemas, và dependencies
2. **Application Layer**: Chứa business logic và use cases
3. **Domain Layer**: Chứa domain models và business rules
4. **Infrastructure Layer**: Chứa implementations của external services

### Logging
Sử dụng `loguru` cho logging. Logs được ghi ra console và có thể cấu hình để ghi ra file.

### Error Handling
- Custom exceptions cho từng domain
- Proper HTTP status codes
- Structured error responses
