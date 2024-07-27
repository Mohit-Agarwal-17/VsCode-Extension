import pandas as pd
import re

# Read the CSV file and set column names
column_names = ['term', 'start_time', 'end_time', 'duration', 'action']
df = pd.read_csv('c_recordings.csv', header=None, names=column_names)

# Convert start_time and end_time to datetime
df['start_time'] = pd.to_datetime(df['start_time'])
df['end_time'] = pd.to_datetime(df['end_time'])

# Initialize new columns with default values of 0
df['backspace'] = 0
df['suggestion'] = 0
df['copied'] = 0

for i in range(len(df)):
    if df.loc[i, 'action'] in ['enter', 'semicolon']:
        # Iterate backwards from the current 'enter' or 'semicolon' action
        for j in range(i - 1, -1, -1):
            if df.loc[j, 'action'] == 'backspace':
                df.at[i, 'backspace'] = 1
                break  # Stop searching once a backspace is found
            elif df.loc[j, 'action'] == 'suggestion':
                df.at[i, 'suggestion'] = 1
            elif df.loc[j, 'action'] == 'copied':
                df.at[i, 'copied'] = 1
            # Stop checking if we encounter another 'enter' or 'semicolon' action
            if df.loc[j, 'action'] in ['enter', 'semicolon']:
                break
            
# Iterate through the DataFrame to update the new columns
for i in range(len(df) - 1):
    if df.loc[i, 'action'] == 'suggestion':
        suggestion_term = df.loc[i, 'term']
        
        # Continue if the suggestion contains parentheses
        if '(' in suggestion_term or ')' in suggestion_term:
            continue
        
        next_row = i + 1
        if df.loc[next_row, 'action'] in ['enter', 'semicolon']:
            enter_term = df.loc[next_row, 'term']
            enter_words = enter_term.split()  # Split enter term into words
            
            print(f"Suggestion: {suggestion_term}")
            # Replace any part of enter_term that matches part of suggestion_term using regex
            for word in enter_words:
                print(f"Checking word: {word}")
                # Use regex to find if part of the word matches the suggestion term
                # Use re.IGNORECASE to make the search case-insensitive
                if re.search(re.escape(suggestion_term), word, re.IGNORECASE):
                    # Replace the matching part with the suggestion term in a case-insensitive manner
                    df.loc[next_row, 'term'] = re.sub(re.escape(word), suggestion_term, df.loc[next_row, 'term'], flags=re.IGNORECASE)
                    print(f"Updated enter term: {df.loc[next_row, 'term']}")

# Keep only rows where action is 'enter' or 'semicolon'
df = df[df['action'].isin(['enter', 'semicolon'])]

# Save the updated DataFrame to a new CSV file
output_path = 'clean_c_file9.csv'
df.to_csv(output_path, index=False)

print(f"Updated CSV file saved to {output_path}")
