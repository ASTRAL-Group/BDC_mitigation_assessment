import pandas as pd
import glob
import os

keep_columns = [
    'acc', 'acc_norm', 'flexible_extract', 'exact_match', 'doc_id'
]

input_path = 'output'
output_path = 'compressed_output'

def compress_file(input_path, output_path):
    df = pd.read_json(input_path, lines=False)
    keep_columns_here = keep_columns.copy()
    # remove columns that are not in the dataframe
    keep_columns_here = [col for col in keep_columns_here if col in df.columns]
    df = df[keep_columns_here]
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

for file in glob.glob(f'{input_path}/**/*.jsonl', recursive=True):
    output_file = file.replace(input_path, output_path).replace('.jsonl', '.csv')
    compress_file(file, output_file)