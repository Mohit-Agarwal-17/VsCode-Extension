import pandas as pd

column_names = ['term', 'start_time', 'end_time', 'duration', 'action']
df = pd.read_csv('1_recordings.csv', header=None, names=column_names)

df['start_time'] = pd.to_datetime(df['start_time'])
df['end_time'] = pd.to_datetime(df['end_time'])

for i in range(len(df) - 1):
    if df.loc[i, 'action'] == 'suggestion':
        suggestion_term = df.loc[i, 'term']
        
        if '(' in suggestion_term or ')' in suggestion_term:
            continue
        
        next_row = i + 1
        if df.loc[next_row, 'action'] in ['enter', 'semicolon']:
            enter_term = df.loc[next_row, 'term']
            
            first_char = enter_term[0]
            
            suggestion_part_length = len(suggestion_term)
            remaining_part = enter_term[suggestion_part_length:]
            
            combined_term = first_char + suggestion_term +" "+ remaining_part
            df.loc[next_row, 'term'] = combined_term

output_path = '16updated_file.csv'
df.to_csv(output_path, index=False)

print(f"Updated CSV file saved to {output_path}")
