import json

def merge_json_files(input_files, output_file):
    # Initialize an empty list to store merged data
    merged_data = []

    # Loop through each file and load the data
    for file in input_files:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            merged_data.extend(data)  # Append the data to the merged list

    # Write the merged data to a new JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)

    print(f"All files have been successfully merged into {output_file}.")

if __name__ == '__main__':
    # File names
    input_files = [
        "/home/phan/Workspace/job-recommendation-platform/data/CareerViet/CareerViet_jobs_1.json",
        "/home/phan/Workspace/job-recommendation-platform/data/CareerViet/CareerViet_jobs_2.json",
        "/home/phan/Workspace/job-recommendation-platform/data/CareerViet/CareerViet_jobs_3.json",
        "/home/phan/Workspace/job-recommendation-platform/data/CareerViet/CareerViet_jobs_4.json",
        "/home/phan/Workspace/job-recommendation-platform/data/CareerViet/CareerViet_jobs_5.json",
        "/home/phan/Workspace/job-recommendation-platform/data/CareerViet/CareerViet_jobs_6.json",
    ]
    output_file = "/home/phan/Workspace/job-recommendation-platform/data/CareerViet/CareerViet_Official.json"

    # Call the function to merge JSON files
    merge_json_files(input_files, output_file)
