"""
OpenAI Prompts for Meeting Summary System
"""

MEETING_SUMMARY_PROMPT = """
Bạn là một chuyên gia tạo biên bản cuộc họp. Hãy phân tích nội dung cuộc họp sau đây và tạo biên bản theo format JSON chính xác:

NỘI DUNG CUỘC HỌP:
{transcription}

YÊU CẦU:
1. Tóm tắt nội dung chính của cuộc họp một cách súc tích và rõ ràng
2. Liệt kê các điểm chính (key_points) được thảo luận
3. Xác định các công việc cần thực hiện (action_items) với người phụ trách (nếu có)
4. Nhận diện người tham gia cuộc họp (participants) dựa trên giọng nói và ngữ cảnh
5. Ước tính thời lượng cuộc họp (meeting_duration) nếu có thể

ĐỊNH DẠNG TRÍCH XUẤT:
{{
  "summary": "Tóm tắt tổng quan cuộc họp...",
  "key_points": [
    "Điểm chính thứ nhất được thảo luận",
    "Điểm chính thứ hai được thảo luận",
    "..."
  ],
  "action_items": [
    "Công việc 1: Mô tả công việc - Người phụ trách (nếu có)",
    "Công việc 2: Mô tả công việc - Người phụ trách (nếu có)",
    "..."
  ],
  "participants": [
    "Tên/vai trò người tham gia 1",
    "Tên/vai trò người tham gia 2",
    "..."
  ],
  "meeting_duration": "XX phút" hoặc "X giờ Y phút"
}}

LƯU Ý:
- Sử dụng tiếng Việt cho tất cả nội dung
- Giữ tính chính xác và khách quan
- Nếu không đủ thông tin cho một trường nào đó, hãy để array rỗng []
- Đảm bảo JSON format chính xác
- Tập trung vào thông tin quan trọng và hữu ích

Hãy tạo biên bản cuộc họp theo format JSON đã yêu cầu.
"""

TRANSCRIPTION_QUALITY_CHECK_PROMPT = """
Đánh giá chất lượng transcription này và đưa ra nhận xét ngắn gọn:

TRANSCRIPTION:
{transcription}

Hãy đánh giá:
1. Độ rõ ràng của nội dung
2. Tính hoàn chỉnh
3. Chất lượng âm thanh (dự đoán)
4. Khả năng tạo biên bản chất lượng

Trả lời ngắn gọn (1-2 câu) bằng tiếng Việt.
"""

MEETING_TYPE_DETECTION_PROMPT = """
Phân tích loại cuộc họp dựa trên nội dung:

{transcription}

Xác định:
1. Loại cuộc họp (họp công việc, họp dự án, họp định kỳ, họp khẩn cấp, etc.)
2. Mức độ trang trọng (chính thức/không chính thức)
3. Quy mô (họp nhỏ/họp lớn)

Trả lời ngắn gọn bằng tiếng Việt.
"""
