import pandas as pd

class DatasetFilter:
    def __init__(self, dataset_file):
        self.dataset_file = dataset_file
        self.data = pd.read_csv(dataset_file)
        self.previous_record_size = len(self.data)
        self.removed_records_count = 0

    def word_count(self, text):
        words = text.split()
        return len(words)

    def Filter_Texts(self, word_count_threshold):
        initial_size = len(self.data)
        self.data = self.data[self.data['text'].apply(self.word_count) > word_count_threshold]
        self.removed_records_count = initial_size - len(self.data)

    def Filter_Summaries(self, word_count_threshold):
        initial_size = len(self.data)
        self.data = self.data[self.data['summary'].apply(self.word_count) > word_count_threshold]
        self.removed_records_count = initial_size - len(self.data)

    def save_filtered_dataset(self, output_file):
        self.data.to_csv(output_file, index=False)

    def get_previous_record_size(self):
        return self.previous_record_size

    def get_removed_records_count(self):
        return self.removed_records_count

    def get_final_record_size(self):
        return len(self.data)


filter_instance = DatasetFilter('Datasets/Primary Datasets/BBC Arabic/ComBBC.csv')
word_count_threshold = 100

filter_instance.Filter_Texts(word_count_threshold)

previous_size = filter_instance.get_previous_record_size()
removed_count = filter_instance.get_removed_records_count()
final_size = filter_instance.get_final_record_size()

print(f"Previous record size: {previous_size}")
print(f"Removed records count: {removed_count}")
print(f"Final record size: {final_size}")

filter_instance.save_filtered_dataset('Debug/Tools/Word Count Filter/Filtered Dataset/Filtered_Dataset.csv')


filter_instance = DatasetFilter('Debug/Tools/Word Count Filter/Filtered Dataset/Filtered_Dataset.csv')
word_count_threshold = 20

filter_instance.Filter_Summaries(word_count_threshold)

previous_size = filter_instance.get_previous_record_size()
removed_count = filter_instance.get_removed_records_count()
final_size = filter_instance.get_final_record_size()

print(f"Previous record size: {previous_size}")
print(f"Removed records count: {removed_count}")
print(f"Final record size: {final_size}")

filter_instance.save_filtered_dataset('Debug/Tools/Word Count Filter/Filtered Dataset/Filtered_Dataset.csv')
