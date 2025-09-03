# 🚀 Hướng dẫn Deploy và Chạy Hệ thống

## ✅ **Tất cả lỗi đã được sửa!**

### 🐛 **Lỗi đã khắc phục:**
1. ✅ **FastAPI Dependency Injection Error** - Fixed
2. ✅ **TypeScript Type Errors** - Fixed  
3. ✅ **File Upload "read of closed file" Error** - Fixed

## 🚀 **Cách chạy hệ thống**

### **Bước 1: Setup Backend với Conda**

```bash
# 1. Tạo conda environment
conda create -n meeting-summary python=3.10 -y
conda activate meeting-summary

# 2. Cài đặt dependencies
cd backend
pip install -r requirements.txt

# 3. Tạo file .env
OPENAI_API_KEY=your_actual_openai_api_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# 4. Test và chạy backend
python test_startup.py   # Kiểm tra import và setup
python test_file_upload.py  # Kiểm tra file upload
python main.py           # Chạy server
```

**Backend sẽ chạy tại:** http://localhost:8000

### **Bước 2: Setup Frontend**

```bash
# Mở terminal mới
cd frontend
npm install
npm start
```

**Frontend sẽ chạy tại:** http://localhost:3000

## 🎯 **Kiểm tra hoạt động**

### **Backend Health Check**
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Test endpoint: `curl http://localhost:8000/docs`

### **Frontend Health Check**
- Giao diện: http://localhost:3000
- Kiểm tra console không có errors
- Test upload file (dùng file mp3 nhỏ để test)

## 🔧 **Troubleshooting**

### **1. Backend Issues**

**Lỗi OpenAI API:**
```bash
# Kiểm tra API key
python -c "import os; print('OPENAI_API_KEY:', os.getenv('OPENAI_API_KEY', 'NOT_SET'))"
```

**Lỗi Dependencies:**
```bash
conda activate meeting-summary
pip install --upgrade pip
pip install -r requirements.txt
```

**Lỗi File Upload:**
```bash
# Test file upload functionality
python test_file_upload.py
```

### **2. Frontend Issues**

**Build Errors:**
```bash
npm run build
# Sẽ show chi tiết lỗi TypeScript nếu có
```

**Runtime Errors:**
- Mở Developer Tools (F12)
- Kiểm tra Console tab
- Kiểm tra Network tab cho API calls

### **3. CORS Issues**

Nếu frontend không kết nối được backend:

**Backend (.env):**
```bash
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001
```

**Frontend (package.json):**
```json
"proxy": "http://localhost:8000"
```

## 📱 **Sử dụng ứng dụng**

### **Workflow chuẩn:**
1. 📁 **Upload file audio** (mp3, wav, m4a, mp4, webm, flac)
2. ⏳ **Chờ xử lý** (real-time progress tracking)
3. 📋 **Xem biên bản** cuộc họp có cấu trúc
4. 💾 **Copy/Download** kết quả

### **File types supported:**
- **Formats**: mp3, wav, m4a, mp4, webm, flac
- **Max size**: 25MB
- **Language**: Tiếng Việt (configurable)

### **Processing modes:**
- **Sync** (< 10MB): Xử lý ngay lập tức
- **Async** (> 10MB): Upload → Polling → Result

## 🎛️ **Configuration**

### **Backend Config (backend/.env):**
```bash
# OpenAI
OPENAI_API_KEY=sk-...
WHISPER_MODEL=whisper-1
CHAT_MODEL=gpt-4o-mini
LANGUAGE=vi

# Server
ALLOWED_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO

# JWT (if needed)
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
```

### **Frontend Config (frontend/.env):**
```bash
REACT_APP_API_URL=http://localhost:8000
```

## 📊 **Performance Tips**

### **Backend:**
- Sử dụng SSD cho temp file storage
- Tăng RAM nếu xử lý nhiều file cùng lúc
- Monitor CPU usage với OpenAI API calls

### **Frontend:**
- Clear browser cache nếu có issues
- Use Chrome/Firefox/Edge (modern browsers)
- Disable ad blockers nếu có API issues

## 🔒 **Security Notes**

### **Production Deployment:**
1. **Environment Variables**: Không commit `.env` files
2. **CORS**: Restrict `ALLOWED_ORIGINS` cho production
3. **File Upload**: Validate file types và size limits
4. **API Keys**: Rotate OpenAI keys định kỳ
5. **HTTPS**: Sử dụng SSL certificates

### **File Cleanup:**
- Temp files tự động cleanup sau processing
- Monitor disk space trong `/tmp` directory
- Log rotation để tránh disk full

## 🌐 **Production Deployment**

### **Backend (Docker):**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Frontend (Static):**
```bash
npm run build
# Deploy build/ folder to static hosting
# (Netlify, Vercel, AWS S3, etc.)
```

---

**🎉 Hệ thống đã sẵn sàng sử dụng! Chúc bạn thành công với demo AI meeting summary!**
