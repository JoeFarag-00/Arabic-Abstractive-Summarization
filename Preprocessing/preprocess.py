import os
import re
import json
import camel_tools
import nltk
import pandas as pd
from pathlib import Path

from camel_tools.tokenizers.word import simple_word_tokenize


df = pd.read_json('Dataset/AIC Val/ds.jsonl', lines=True)

with open(Path("Preprocessing/Stopwords/Stopwords_List.txt"), "r", encoding="utf-8") as f:
    arabic_stopwords = set(f.read().splitlines())

def Tokenize(text):
    return simple_word_tokenize(text)

def Lemmatize(tokens):
    lemmatizer = camel_tools.utils.lemmatize.Lemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]

def Remove_SW(tokens, stopwords):
    return [token for token in tokens if token not in stopwords]

def Remove_SW_Camel(tokens, stopwords):
    return [token for token in tokens if token not in stopwords]

def preprocess(text):
    tokens = Tokenize(text)
    # tokens = Remove_SW(tokens, stopwords)
    # tokens = Lemmatize(tokens)
    return tokens

def save(word ,output):
    with open(output, 'a', encoding='utf-8') as file:
        file.write(word + '\n')

paragraphs_output_file = 'Debug/Passed_Tokens/preprocessed_paragraphs.txt'
summaries_output_file = 'Debug/Passed_Tokens/preprocessed_summaries.txt'

open(paragraphs_output_file, 'w').close()
open(summaries_output_file, 'w').close()
    
for index, row in df.iterrows():
    
    preprocessed_Paragraph = preprocess(row['paragraph'])
    preprocessed_Summary = preprocess(row['summary'])
    
    for word in preprocessed_Paragraph:
        save(word, paragraphs_output_file)
        
    for word in preprocessed_Summary:
        save(word, summaries_output_file)