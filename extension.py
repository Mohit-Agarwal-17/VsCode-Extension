import pandas as pd
import re

column_names = ['term', 'start_time', 'end_time', 'duration', 'action']
#Enter location of raw file
df = pd.read_csv('recordings.csv', header=None, names=column_names)

df['start_time'] = pd.to_datetime(df['start_time'])
df['end_time'] = pd.to_datetime(df['end_time'])

df['backspace'] = 0
df['suggestion'] = 0

for i in range(len(df)):
    if df.loc[i, 'action'] in ['enter', 'semicolon']:
        for j in range(i - 1, -1, -1):
            if df.loc[j, 'action'] == 'backspace':
                df.at[i, 'backspace'] = 1  
            elif df.loc[j, 'action'] == 'suggestion':
                df.at[i, 'suggestion'] = 1
            if df.loc[j, 'action'] in ['enter', 'semicolon']:
                break
            
def remove_symbols(text):
    return re.sub(r'[^a-zA-Z0-9]', '', text)

for i in range(len(df)):
    if df.loc[i, 'action'] == 'suggestion':
        suggestion_term = df.loc[i, 'term']
        
        if '(' in suggestion_term or ')' in suggestion_term:
            continue
        
        print(f"Suggestion: {suggestion_term}")
        cleaned_suggestion = remove_symbols(suggestion_term)
        
        for j in range(i + 1, len(df)):
            if df.loc[j, 'action'] in ['enter', 'semicolon']:
                enter_term = df.loc[j, 'term']
                enter_words = enter_term.split()
                
                print(f"Original enter term: {enter_term}")
                
                updated_enter_term = ""
                for word in enter_words:
                    cleaned_word = remove_symbols(word)
                    print(f"Checking cleaned word: {cleaned_word}")
                    
                    if cleaned_word.lower() in cleaned_suggestion.lower():
                        print(f"Match found for: {cleaned_word} in {cleaned_suggestion}")
                        
                        match = re.search(re.escape(cleaned_word), cleaned_suggestion, re.IGNORECASE)
                        if match:
                            start, end = match.span()
                            before = suggestion_term[:start]
                            after = suggestion_term[end:]
                            updated_word = before + word + after
                            cleaned_suggestion = remove_symbols(updated_word)  # Update cleaned suggestion
                            suggestion_term = updated_word
                            print(f"Updated suggestion term: {suggestion_term}")
                            
                        updated_enter_term += updated_word + " "
                    else:
                        updated_enter_term += word + " "
                
                final_term = updated_enter_term.strip()
                df.loc[j, 'term'] = final_term
                print(f"Final updated suggestion term: {df.loc[i, 'term']}")
                
                break


df = df[df['action'].isin(['enter', 'semicolon'])]

total_lines = len(df)
total_backspace = len(df[df['backspace'] == 1])
total_suggestion = len(df[df['suggestion'] == 1])

summary_rows = [
    ['Total lines:', total_lines, '', '', '',"",""],
    ['Backspace is used:', total_backspace, '', '', '','',''],
    ['Suggestion is used:', total_suggestion, '', '', '','','']
]

summary_df = pd.DataFrame(summary_rows, columns=df.columns)

final_df = pd.concat([df, summary_df], ignore_index=True)

output_path = 'final_cleaned.csv'
final_df.to_csv(output_path, index=False)

print(f"Updated CSV file saved to {output_path}")
