#!/bin/bash

# Script setup conda environment cho Meeting Summary Backend
echo "🚀 Setting up Meeting Summary Backend with Conda..."

# Tạo conda environment
echo "📦 Creating conda environment 'meeting-summary' with Python 3.10..."
conda create -n meeting-summary python=3.10 -y

# Activate environment
echo "⚡ Activating conda environment..."
source activate meeting-summary

# Cài đặt dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Tạo .env file từ template
echo "⚙️ Setting up environment variables..."
if [ ! -f .env ]; then
    cat > .env << EOL
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# JWT Configuration  
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256

# API Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Optional: Logging Configuration
LOG_LEVEL=INFO
EOL
    echo "✅ Created .env file. Please update OPENAI_API_KEY with your actual key."
else
    echo "ℹ️ .env file already exists. Skipping creation."
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. conda activate meeting-summary"
echo "2. Edit .env file and add your OpenAI API key"
echo "3. python main.py"
echo ""
echo "🌐 Backend will be available at: http://localhost:8000"
echo "📖 API docs will be available at: http://localhost:8000/docs"
