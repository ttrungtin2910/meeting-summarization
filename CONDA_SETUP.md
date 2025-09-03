# 🐍 Hướng dẫn Setup nhanh với Conda

Hướng dẫn chi tiết để setup hệ thống Meeting Summary với Conda environment Python 3.10.

## 🚀 Quick Start

### Bước 1: Setup Backend với Conda

```bash
# 1. Tạo và activate conda environment
conda create -n meeting-summary python=3.10 -y
conda activate meeting-summary

# 2. Di chuyển vào thư mục backend
cd backend

# 3. Cài đặt dependencies
pip install -r requirements.txt

# 4. Setup environment variables
# Tạo file .env với nội dung:
OPENAI_API_KEY=your_actual_openai_api_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# 5. Chạy backend
python main.py
```

### Bước 2: Setup Frontend

```bash
# Mở terminal mới và di chuyển vào thư mục frontend
cd frontend

# Cài đặt Node.js dependencies
npm install

# Chạy frontend
npm start
```

## 📋 Chi tiết Dependencies

### Backend Dependencies (đã cài với pip)
- **FastAPI**: Web framework hiện đại cho Python
- **OpenAI**: Client library cho OpenAI API (Whisper + GPT)
- **Uvicorn**: ASGI server để chạy FastAPI
- **Pydantic**: Data validation và serialization
- **Loguru**: Logging library dễ sử dụng

### Kiểm tra cài đặt thành công

```bash
# Trong conda environment meeting-summary
python -c "import fastapi, openai, uvicorn; print('✅ All dependencies installed successfully!')"
```

## 🔧 Các script tiện ích

### Auto Setup Script
Đã tạo sẵn script tự động setup:

**Linux/Mac:**
```bash
cd backend
chmod +x setup_conda.sh
./setup_conda.sh
```

**Windows:**
```cmd
cd backend
setup_conda.bat
```

### Alternative: Sử dụng conda environment file
```bash
# Tạo environment từ file YAML
conda env create -f backend/environment.yml
conda activate meeting-summary
```

## 🌐 Truy cập ứng dụng

Sau khi setup thành công:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## 🐛 Troubleshooting

### Lỗi thường gặp

1. **Conda environment không tìm thấy**
   ```bash
   conda info --envs  # Kiểm tra các environments
   conda activate meeting-summary
   ```

2. **OpenAI API key không hoạt động**
   - Kiểm tra file `.env` có đúng format không
   - Đảm bảo API key hợp lệ và có credit

3. **Port đã được sử dụng**
   ```bash
   # Thay đổi port backend
   uvicorn main:app --host 127.0.0.1 --port 8001
   
   # Thay đổi port frontend
   PORT=3001 npm start
   ```

4. **Lỗi cài đặt dependencies**
   ```bash
   # Cập nhật pip
   pip install --upgrade pip
   
   # Hoặc cài từng package
   pip install fastapi uvicorn openai pydantic loguru
   ```

### Kiểm tra health của services

```bash
# Kiểm tra backend
curl http://localhost:8000/docs

# Kiểm tra có thể upload file
curl -X POST "http://localhost:8000/api/v1/process-audio" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_audio.mp3"
```

## 💡 Tips cho Development

### Chạy backend ở development mode
```bash
conda activate meeting-summary
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Logging và debugging
- Logs sẽ hiển thị trực tiếp trên terminal
- Có thể thay đổi log level trong file `.env`: `LOG_LEVEL=DEBUG`

### Hot reload
- Backend: Tự động reload khi có thay đổi code (với `--reload`)
- Frontend: Tự động refresh browser khi có thay đổi

## 🔄 Commands hữu ích

```bash
# Activate environment nhanh
conda activate meeting-summary

# Deactivate environment
conda deactivate

# Xóa environment (nếu cần)
conda env remove -n meeting-summary

# Xem packages đã cài
conda list

# Export environment để chia sẻ
conda env export > environment.yml
```

---

**🎉 Chúc bạn setup thành công! Nếu có vấn đề gì, hãy kiểm tra lại từng bước hoặc tham khảo README.md chính.**
