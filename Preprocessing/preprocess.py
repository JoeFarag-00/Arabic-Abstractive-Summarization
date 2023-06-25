import os
import re
import json
import camel_tools
import nltk
import pandas as pd
from pathlib import Path
import qalsadi.lemmatizer
from camel_tools.ner import NERecognizer
from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.utils.dediac import dediac_ar, dediac_bw

lemmer = qalsadi.lemmatizer.Lemmatizer()
df = pd.read_json('Dataset//AIC Val//ds.jsonl', lines=True)

with open(Path("Preprocessing//Stopwords//Stopwords_List_HF.txt"), "r", encoding="utf-8") as f:
    arabic_stopwords = set(f.read().splitlines())
# print(df)

def Tokenize(text):
    return simple_word_tokenize(text)

def Lemmatize(text):
   return lemmer.lemmatize_text(' '.join(text))

def DeDiacritics(text):
    return dediac_ar(text)

def Remove_SW(tokens, stopwords):
    removed_tokens = []
    passed_tokens = []
    for token in tokens:
        if token in stopwords:
            removed_tokens.append(token)
        else:
            passed_tokens.append(token)
 
    return passed_tokens, removed_tokens

def Remove_SW_Camel(tokens, stopwords):
    return [token for token in tokens if token not in stopwords]

def Preprocess_Qalsadi(text):
    #TBD REQUIRES IMPLEMENTATION
    pass

def Preprocess(text):
    tokens = DeDiacritics(text)
    tokens = Tokenize(tokens)
    tokens, rm_tokens = Remove_SW(tokens, arabic_stopwords)
    tokens = Lemmatize(tokens)
    return tokens,rm_tokens

def Save_Passed(word, output):
    with open(output, 'a', encoding='utf-8') as file:
        file.write(word + '\n')
        
def Save_Removed(word, output):
    with open(output, 'a', encoding='utf-8') as file:
        file.write(word + '\n')

pass_pg_path = 'Debug/Token Tracking/Passed_Tokens/passed_paragraphs.txt'
pass_sum_path = 'Debug/Token Tracking/Passed_Tokens/passed_summaries.txt'

removed_pg_path = 'Debug/Token Tracking/Removed_Tokens/removed_paragraphs.txt'
removed_sum_path = 'Debug/Token Tracking/Removed_Tokens/removed_summaries.txt'

processed_records = "Debug/Processed Dataset/Processed_Dataset.csv"

open(pass_pg_path, 'w').close()
open(pass_sum_path, 'w').close()

open(removed_pg_path, 'w').close()
open(removed_sum_path, 'w').close()

processed_data = []
final_records_ct = 0
for index, row in df.iterrows():
    
    preprocessed_Paragraph, removed_Paragraph = Preprocess(row['paragraph'])
    preprocessed_Summary, removed_Summary = Preprocess(row['summary'])
    
    processed_data.append({'Paragraph': ' '.join(preprocessed_Paragraph), 'Summary': ' '.join(preprocessed_Summary)})
    
    for word in preprocessed_Paragraph:
        Save_Passed(word, pass_pg_path)

    for word in removed_Paragraph:
        Save_Removed(word, removed_pg_path)
        
    for word in preprocessed_Summary:
        Save_Passed(word, pass_sum_path)

    for word in removed_Summary:
        Save_Removed(word, removed_sum_path)
        
    final_records_ct+=1

processed_df = pd.DataFrame(processed_data)
processed_df.to_csv(processed_records, index=False)
print("Processed Dataset Records: ", final_records_ct)