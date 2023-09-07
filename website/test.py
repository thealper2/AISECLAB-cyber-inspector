import numpy as np
import pandas as pd
import pickle
from nltk.tokenize import RegexpTokenizer
from nltk.stem import SnowballStemmer
from website.preprocess import preprocess

columns = ['query', 'is_xss', 'is_lfi', 'is_oci', 'is_sqli', 'url_len',
       'semicolon_count', 'underscore_count', 'questionmark_count',
       'equal_count', 'and_count', 'or_count', 'dot_count', 'at_count',
       'subdir_count', 'query_len', 'param_count', 'total_digits_url',
       'total_letter_url', 'url_tokenized', 'url_stemmed', 'total_digits_domain', 'total_letter_domain', 
       'total_digits_path', 'total_letter_path', 'has_extension', 'extension', 'has_parameter', 'parameters']

test1 = 'hrttz9fj.dll?<script>document.cookie="testtbjy=7334;"</script>' # 1
test2 = 'index.php?option=com_mailto&tmpl=component&link=aHR0cDovL2FkdmVudHVyZ' # 1
test3 = 'nba/player/_/id/3457/brandon-rush' # 0
test4 = '?q=anthony-hamilton-soulife' # 0
test5 = 'site/relationship_detail.php?name=Martin-Brodeur&celebid=12150&relid=11371' # 0

test_df = pd.DataFrame(columns=columns)

model = pickle.load(open("website/models/logreg.pkl", "rb"))
ss = pickle.load(open("website/models/logreg_ss.pkl", "rb"))

test_df.loc[0, "query"] = test1
test_df.loc[1, "query"] = test2
test_df.loc[2, "query"] = test3
test_df.loc[3, "query"] = test4
test_df.loc[4, "query"] = test5

stemmer = SnowballStemmer("english")
tokenizer = RegexpTokenizer(r"[A-Za-z]+")

test_df = preprocess(test_df)
print(test_df.shape)
test_df.to_csv("website/uploads/test.csv")
dropped = test_df.drop(["query", "url_tokenized", "url_stemmed", "extension", "parameters"], axis=1)
dropped_scaled = ss.transform(dropped)
print(model.predict(dropped_scaled))
