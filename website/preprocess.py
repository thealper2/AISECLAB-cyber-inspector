import numpy as np
import pandas as pd
import urllib
import os
import re
import pickle
import nltk
import string
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from nltk.tokenize import RegexpTokenizer
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from collections import Counter
from PIL import Image
from website.functions import *

stemmer = SnowballStemmer("english")
tokenizer = RegexpTokenizer(r"[A-Za-z]+")

def preprocess(test_df):
    test_df["is_xss"] = test_df["query"].apply(xss_check)
    test_df["is_lfi"] = test_df["query"].apply(lfi_check)
    test_df["is_oci"] = test_df["query"].apply(command_injection_check)
    test_df["is_sqli"] = test_df["query"].apply(sql_injection_check)
    test_df["url_len"] = test_df["query"].apply(urllen)
    test_df["delim_count"] = test_df["query"].apply(delimitercount)
    test_df["dot_count"] = test_df["query"].apply(dotcount)
    test_df["at_count"] = test_df["query"].apply(atcount)
    test_df["subdir_count"] = test_df["query"].apply(subdircount)
    test_df["query_len"] = test_df["query"].apply(query_count)
    test_df["total_digits_url"] = test_df["query"].apply(total_digits_in_url)
    test_df["total_letter_url"] = test_df["query"].apply(total_letter_in_url)
    test_df["url_tokenized"] = test_df["query"].apply(lambda x: tokenizer.tokenize(x))
    test_df["url_stemmed"] = test_df["url_tokenized"].apply(stem_url)
    test_df["total_digits_domain"] = test_df["query"].apply(total_digits_domain)
    test_df["total_letter_domain"] = test_df["query"].apply(total_letter_domain)
    test_df["total_digits_path"] = test_df["query"].apply(total_digits_path)
    test_df["total_letter_path"] = test_df["query"].apply(total_letter_path)
    test_df["has_extension"] = test_df["query"].apply(has_extension)
    test_df["extension"] = test_df["query"].apply(find_extension)
    test_df["has_parameter"] = test_df["query"].apply(has_parameter)
    return test_df
