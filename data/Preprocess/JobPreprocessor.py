import pandas as pd
import os

from sentence_transformers import SentenceTransformer

class JobPreprocessor():
    def __init__(self) -> None:
        self.embedding_model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")
        
    def saveDataframeToJSON(self, df, output_path):
        df.to_json(output_path, orient="records", indent=4, force_ascii=False)
        print('Wrote dataframe to {}.'.format(output_path))
        
    def mergeJobDatasets(self, jobs_paths, output_path=None):
        dfs = []
        
        for path in jobs_paths:
            df = pd.read_json(path, encoding="utf-8")
            dfs.append(df)
            
        merged_df = pd.concat(dfs, ignore_index=True)
        
        if output_path is not None:
            self.saveDataframeToJSON(df=merged_df, output_path=output_path)
        
        return merged_df
        
    def encodeJobsRequirements(self, jobs_path, output_path=None):
        job_df = pd.read_json(jobs_path, encoding="utf-8")
        
        def encodeJobRequirements(job):
            # if job['requirements_language'] != 'en':
            #     requirements = job['en_requirements']
            # else:
            requirements = job['requirements']                
            encoded_requirements = self.embedding_model.encode(requirements)
            print('Encoded job {}'.format(job['job_title']))
            return encoded_requirements
        
        job_df['req_vector'] = job_df.apply(encodeJobRequirements, axis=1)
        
        if output_path is not None:
            self.saveDataframeToJSON(df=job_df, output_path=output_path)
        
        return job_df

        
if __name__ == '__main__':
    base_dir = os.getcwd()
    json_path = os.path.abspath(os.path.join(base_dir, "careerviet.json"))
    paths = json_path
    json_path = os.path.abspath(os.path.join(base_dir, "encoded_jobs.json"))
    encoded_path = json_path
    
    job_preprocessor = JobPreprocessor()
    
   
    job_preprocessor.encodeJobsRequirements(jobs_path=paths, output_path=encoded_path)