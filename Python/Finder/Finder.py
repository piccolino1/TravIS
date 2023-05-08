import sys
import pandas as pd
import numpy as np


df = pd.read_csv('C:\\Users\\Dominik\\source\\repos\\piccolino1\\TravIS\\Python\\ChatGPT\\country_keywords.csv', encoding='latin-1', sep=';')
df.head()

new_df = df
new_df.head()
new_df.dropna(inplace=True)

blanks = []  # start with an empty list

col=['country','keywords','keywords climate','keywords food','keywords vegetation','keywords culture']
for i,col in new_df.iterrows():  # iterate over the DataFrame
    if type(col)==str:            # avoid NaN values
        if col.isspace():         # test 'review' for whitespace
            blanks.append(i)     # add matching index numbers to the list

new_df.drop(blanks, inplace=True)

new_df['keywords'] = new_df['keywords'].map(lambda x: x.lower().split(','))
new_df['keywords climate'] = new_df['keywords climate'].map(lambda x: x.lower().split(','))
new_df['keywords food'] = new_df['keywords food'].map(lambda x: x.lower().split(','))
new_df['keywords vegetation'] = new_df['keywords vegetation'].map(lambda x: x.lower().split(','))
new_df['keywords culture'] = new_df['keywords culture'].map(lambda x: x.lower().split(','))

new_df.head()

new_df['bag_of_words'] = ''
columns = new_df.columns
for index, row in df.iterrows():
    words = ''
    for col in columns:
            words = words + ' '.join(row[col])+ ' '
    new_df['bag_of_words'][index] = words
    
new_df.drop(columns = [col for col in df.columns if col != 'bag_of_words' and col != 'country'], inplace = True)

from sklearn.feature_extraction import text
vectorizer = text.TfidfVectorizer()

def cosine_sim(test1, test2):
    tfidf = vectorizer.fit_transform([test1, test2])
    result = ((tfidf * tfidf.T).A)[0,1]
    return result
    
def cosine_sim_df(df_data, keyword):
    col1 = 'bag_of_words'
    df_data[col1] = df_data[col1].str.replace(r'\d', '')
    
    df_data['cos_sim'] = 0
    df_data['cos_sim'] = df_data.apply(
        lambda x: cosine_sim(x[col1], keyword), axis=1)
    
    df_data = df_data.sort_values(by='cos_sim', ascending=False)
    return df_data

searchKeyword = ""
if(len(sys.argv) >= 2):
    searchKeyword = sys.argv[1]

new_df = cosine_sim_df(new_df, searchKeyword)
print(new_df.iloc[0]['country'])

