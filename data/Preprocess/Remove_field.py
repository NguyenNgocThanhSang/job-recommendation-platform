import json
import os
# Read the JSON file

base_dir = os.getcwd()
json_path = os.path.abspath(os.path.join(base_dir, "CareerViet_Official_Cleaned.json"))

input_file = json_path  # Replace with the actual input file name

json_path_1 = os.path.abspath(os.path.join(base_dir, "jobs.json"))
output_file = json_path_1 # Replace with the desired output file name

with open(input_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract the required fields for each object in the list
output_data = [
    {
        "job_title": job.get("job_title"),
        "fields": job.get("en_fields")
    }
    for job in data
]

# Write the extracted fields to a new JSON file
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(output_data, file, ensure_ascii=False, indent=4)

print(f"Filtered data saved to {output_file}")