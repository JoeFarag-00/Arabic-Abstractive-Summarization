import os
import re
import json
import camel_tools
import nltk
import pickle
import pandas as pd
from pathlib import Path
import qalsadi.lemmatizer
from camel_tools.ner import NERecognizer
from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.utils.dediac import dediac_ar, dediac_bw

lemmer = qalsadi.lemmatizer.Lemmatizer()
df = pd.read_json('Datasets//AIC Val//ds.jsonl', lines=True)

pass_pg_path = 'Debug/Token Tracking/Passed_Tokens/passed_paragraphs.txt'
pass_sum_path = 'Debug/Token Tracking/Passed_Tokens/passed_summaries.txt'

removed_pg_path = 'Debug/Token Tracking/Removed_Tokens/removed_paragraphs.txt'
removed_sum_path = 'Debug/Token Tracking/Removed_Tokens/removed_summaries.txt'

processed_records_path = "Debug/Preprocessed Dataset/Processed_Dataset.csv"
processed_records_Qalpath = "Debug/Preprocessed Dataset/QalProcessed_Dataset.csv"

with open(Path("Preprocessing//Stopwords//Stopwords_List_SoftF.txt"), "r", encoding="utf-8") as f:
    arabic_stopwords = set(f.read().splitlines())

class Preprocessor():
    
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

    def Normalize_Numbers(text, type):
        if type == 1:
            text = re.sub('[0-9]', lambda match: chr(int(match.group(0)) + 1632), text)
        elif type == 2:
            text = re.sub('[١٢٣٤٥٦٧٨٩٠]', lambda match: str(ord(match.group(0)) - 1632), text)
        elif type == 3:
            text = re.sub('[0-9٠١٢٣٤٥٦٧٨٩]', '', text)
        return text

    def Normalize(text):
        text = re.sub("[إأٱآا]", "ا", text)
        text = re.sub("ى", "ي", text)
        text = re.sub("ؤ", "ء", text)
        text = re.sub("ئ", "ء", text)
        text = re.sub("ة", "ه", text)
        text = re.sub("[:“،؟!()»«{}؛]","", text)
        text = re.sub("%", "", text)
        text = re.sub('[٠١٢٣٤٥٦٧٨٩0123456789]', '', text)

        return text
    
    def Preprocess_Qalsadi(text):
        #Not done Library bug issue
        Ftokens = []
        sw = ["،",".",",","؛","ء","ءَ","آ","(",")","!",":","=","-",'"']
        tokens = Preprocessor.DeDiacritics(text)
        lemmatized_tokens = lemmer.lemmatize_text(tokens, return_pos=True)

        for token in lemmatized_tokens:
            if isinstance(token, tuple):
                word, tag = token
                if tag != 'stopword' and token not in sw:
                    Ftokens.append(word)
            else:
                if token != 'stopword' and token not in sw:
                    Ftokens.append(token)

        processed_text = ''.join(Ftokens)
        return processed_text
    
    def Default_Preprocess(text):
        # tokens = Preprocessor.Normalize_Numbers(text, 1)
        tokens = Preprocessor.DeDiacritics(text)
        tokens = Preprocessor.Tokenize(tokens)
        tokens, rm_tokens = Preprocessor.Remove_SW(tokens, arabic_stopwords)
        tokens = Preprocessor.Lemmatize(tokens)
        return tokens,rm_tokens

    def Save_Passed(word, output):
        with open(output, 'a', encoding='utf-8') as file:
            file.write(word + '\n')
            
    def Save_Removed(word, output):
        with open(output, 'a', encoding='utf-8') as file:
            file.write(word + '\n')


open(pass_pg_path, 'w').close()
open(pass_sum_path, 'w').close()

open(removed_pg_path, 'w').close()
open(removed_sum_path, 'w').close()

processed_data = []
Final_Paragraphs = []
Final_Summaries = []
preprocessed_qalsadi = []
final_records_ct = 0

for index, row in df.iterrows():
    
    preprocessed_Paragraph, removed_Paragraph = Preprocessor.Default_Preprocess(row['paragraph'])
    # preprocessed_Summary, removed_Summary = Preprocessor.Default_Preprocess(row['summary'])
    
    processed_data.append({'paragraph': ' '.join(preprocessed_Paragraph), 'summary': row['summary']})

    Final_Paragraphs.append(preprocessed_Paragraph)
    
    Final_Summaries.append(row['summary'])
    
    for word in preprocessed_Paragraph:
        Preprocessor.Save_Passed(word, pass_pg_path)

    for word in removed_Paragraph:
        Preprocessor.Save_Removed(word, removed_pg_path)
        
    # for word in preprocessed_Summary:
    #     Preprocessor.Save_Passed(word, pass_sum_path)

    # for word in removed_Summary:
    #     Preprocessor.Save_Removed(word, removed_sum_path)
        
    final_records_ct+=1

processed_df = pd.DataFrame(processed_data)
processed_df.to_csv(processed_records_path, index=False)
print("Processed Dataset Records: ", final_records_ct)

# processed_df = pd.DataFrame(preprocessed_qalsadi)
# processed_df.to_csv(processed_records_Qalpath, index=False)

with open('Debug/Primary/Processed_Paragraphs.pkl', 'wb') as f:
    pickle.dump(Final_Paragraphs, f)

with open('Debug/Primary/Processed_Summaries.pkl', 'wb') as f:
    pickle.dump(Final_Summaries, f)
