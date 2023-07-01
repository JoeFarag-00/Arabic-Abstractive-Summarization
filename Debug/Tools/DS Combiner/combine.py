import pandas as pd

def combine_csv_files(file1, file2, output_file):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    combined_data = pd.concat([df1, df2], axis=0, ignore_index=True)

    combined_data.to_csv(output_file, index=False)

file1 = 'Datasets/Primary Datasets/BBC Arabic/ModDataset1.csv'
file2 = 'Datasets/Primary Datasets/BBC Arabic/ModDataset2.csv'

output_file = 'Debug/Tools/DS Combiner/Combined Dataset/ModCombined1919.csv'

combine_csv_files(file1, file2, output_file)
