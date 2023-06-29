import pandas as pd

class DatasetStats:
    def __init__(self, dataset_file):
        self.dataset_file = dataset_file
        self.data = pd.read_csv(dataset_file)

    def calculate_word_count(self, text):
        words = text.split()
        return len(words)

    def get_stats(self):
        text_word_counts = self.data['text'].apply(self.calculate_word_count)
        summary_word_counts = self.data['summary'].apply(self.calculate_word_count)

        avg_text_word_count = text_word_counts.mean()
        max_text_word_count = text_word_counts.max()
        min_text_word_count = text_word_counts.min()

        avg_summary_word_count = summary_word_counts.mean()
        max_summary_word_count = summary_word_counts.max()
        min_summary_word_count = summary_word_counts.min()

        record_size = len(self.data)

        return {
            'Avg Text Word Count': avg_text_word_count,
            'Max Text Word Count': max_text_word_count,
            'Min Text Word Count': min_text_word_count,
            'Avg Summary Word Count': avg_summary_word_count,
            'Max Summary Word Count': max_summary_word_count,
            'Min Summary Word Count': min_summary_word_count,
            'Record Size': record_size
        }


stats_instance = DatasetStats('Datasets/Primary Datasets/BBC Arabic/FiltBBC.csv')

statistics = stats_instance.get_stats()

print("Text Statistics:")
print(f"Avg Text Word Count: {statistics['Avg Text Word Count']}")
print(f"Max Text Word Count: {statistics['Max Text Word Count']}")
print(f"Min Text Word Count: {statistics['Min Text Word Count']}")

print("Summary Statistics:")
print(f"Avg Summary Word Count: {statistics['Avg Summary Word Count']}")
print(f"Max Summary Word Count: {statistics['Max Summary Word Count']}")
print(f"Min Summary Word Count: {statistics['Min Summary Word Count']}")

print(f"Record Size: {statistics['Record Size']}")
