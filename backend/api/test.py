import os
import json

# Lấy thư mục hiện tại
base_dir = os.getcwd()

# Xây dựng đường dẫn tới data/jobs.json
data_dir = os.path.join(base_dir, "..", "data", "jobs.json")
# data_dir = os.path.abspath(data_dir)  # Chuyển đường dẫn thành tuyệt đối
print(f"Path to jobs.json: {data_dir}")

# Kiểm tra nếu file tồn tại
if os.path.exists(data_dir):
    print("File exists!")
    
    # Đọc dữ liệu từ file jobs.json
    with open(data_dir, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)  # Parse nội dung JSON
            print("Data in jobs.json:")
            print(json.dumps(data, indent=4, ensure_ascii=False))  # In dữ liệu theo định dạng dễ đọc
        except json.JSONDecodeError as e:
            print(f"Error reading JSON: {e}")
else:
    print("File not found!")
