import pandas as pd

output_df = pd.read_csv('output_model_wiki_and_twitter.csv')

n = 500
print('Top', n, 'deletion rate:', output_df.head(n)['WasDeleted'].values.sum()/n)
print('Bottom', n, 'deletion rate:', output_df.tail(n)['WasDeleted'].values.sum()/n)