import json

# Đường dẫn tới tệp JSON
file_path = 'CareerViet_Official_No_en_fields.json'

# Đọc dữ liệu từ tệp JSON
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Xóa trường 'en_fields' khỏi từng mục
for job in data:
    if 'job_site' in job:
        del job['job_site']

# Lưu dữ liệu đã chỉnh sửa vào tệp mới
output_path = 'CareerViet_Official.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Xem trước dữ liệu đã chỉnh sửa (tùy chọn)
print(json.dumps(data[:5], ensure_ascii=False, indent=2))  # Hiển thị 5 mục đầu tiên
