import json
import pandas as pd
from sentence_transformers import SentenceTransformer
import os

class JobPreprocessor():
    def __init__(self) -> None:
        # Khởi tạo mô hình SentenceTransformer
        self.embedding_model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")
        
    def saveDataframeToJSON(self, df, output_path):
        """Lưu DataFrame thành tệp JSON."""
        df.to_json(output_path, orient="records", indent=4, force_ascii=False)
        print(f'Wrote dataframe to {output_path}.')
        
    def encodeJobFields(self, job_listings, output_path=None):
        """Mã hóa các trường công việc (fields) bằng SentenceTransformer."""
        # Tạo set chứa các trường công việc duy nhất
        unique_fields = set()
        for job in job_listings:
            fields = job.get('fields', [])
            for field in fields:
                unique_fields.add(field.strip())  # Xóa các ký tự trắng dư thừa
        
        print(f"Unique Fields Extracted: {unique_fields}")

        # Chuyển các trường công việc thành danh sách
        fields_list = list(unique_fields)
        
        # Mã hóa các trường công việc thành các vector (embeddings)
        embeddings = self.embedding_model.encode(fields_list)
        
        # Tạo danh sách kết quả chứa các trường công việc và vector tương ứng
        field_embeddings = []
        for field, embedding in zip(fields_list, embeddings):
            field_embeddings.append({
                "field": field,
                "field_vector": embedding.tolist()  # Chuyển tensor thành list để lưu vào JSON
            })
        
        # Chuyển kết quả thành DataFrame để dễ dàng thao tác (tùy chọn)
        df = pd.DataFrame(field_embeddings)
        print(df)

        # Lưu kết quả vào tệp JSON nếu có đường dẫn đầu ra
        if output_path is not None:
            self.saveDataframeToJSON(df=df, output_path=output_path)
        
        return df

if __name__ == '__main__':
    base_dir = os.getcwd()
    json_path = os.path.abspath(os.path.join(base_dir, "jobs.json"))
    output_json_path = os.path.abspath(os.path.join(base_dir, "encoded_fields.json"))
    
    # Đọc dữ liệu JSON từ tệp
    with open(json_path, 'r', encoding='utf-8') as file:
        job_listings = json.load(file)
    
    # Khởi tạo JobPreprocessor và mã hóa các trường công việc
    job_preprocessor = JobPreprocessor()
    job_preprocessor.encodeJobFields(job_listings=job_listings, output_path=output_json_path)
    
    print("Transformation complete. The 'fields_with_vectors.json' file has been created.")
