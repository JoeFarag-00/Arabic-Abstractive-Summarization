import pandas as pd

class DatasetFilter:
    
    def __init__(self, dataset_file):
        self.dataset_file = dataset_file
        self.data = pd.read_csv(dataset_file)
        self.initial_record_count = len(self.data)
    
    def Filter_Texts(self, min_word_count, max_word_count):
        previous_record_count = len(self.data)
        self.data = self.data[(self.data['text'].str.split().str.len() >= min_word_count) & (self.data['text'].str.split().str.len() <= max_word_count)]
        removed_records = previous_record_count - len(self.data)
        return removed_records, previous_record_count, len(self.data)
    
    def Filter_Summaries(self, min_word_count, max_word_count):
        previous_record_count = len(self.data)
        self.data = self.data[(self.data['summary'].str.split().str.len() >= min_word_count) & (self.data['summary'].str.split().str.len() <= max_word_count)]
        removed_records = previous_record_count - len(self.data)
        return removed_records, previous_record_count, len(self.data)
    
    def Generate_New_Dataset(self, output_file):
        self.data.to_csv(output_file, index=False)

dataset = DatasetFilter('Datasets/Primary Datasets/BBC Arabic/ComBBC.csv')
removed_text_records, prev_text_record_count, final_text_record_count = dataset.Filter_Texts(230, 430)
removed_summary_records, prev_summary_record_count, final_summary_record_count = dataset.Filter_Summaries(40, 150)

print("Text Records:")
print(f"Removed Records: {removed_text_records}")
print(f"Previous Record Count: {prev_text_record_count}")
print(f"Final Record Count: {final_text_record_count}")

print("\nSummary Records:")
print(f"Removed Records: {removed_summary_records}")
print(f"Previous Record Count: {prev_summary_record_count}")
print(f"Final Record Count: {final_summary_record_count}")

dataset.Generate_New_Dataset('Debug/Tools/Word Count Filter/Filtered Dataset/filtered_dataset.csv')
