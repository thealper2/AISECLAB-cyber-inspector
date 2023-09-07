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
    test_df["query"] = test_df["query"].apply(clear_first_char)
    test_df["is_xss"] = test_df["query"].apply(xss_check)
    test_df["is_lfi"] = test_df["query"].apply(lfi_check)
    test_df["is_oci"] = test_df["query"].apply(command_injection_check)
    test_df["is_sqli"] = test_df["query"].apply(sql_injection_check)
    test_df["url_len"] = test_df["query"].apply(urllen)
    test_df["semicolon_count"] = test_df["query"].apply(semicolon_count)
    test_df["underscore_count"] = test_df["query"].apply(underscore_count)
    test_df["questionmark_count"] = test_df["query"].apply(questionmark_count)
    test_df["equal_count"] = test_df["query"].apply(equal_count)
    test_df["and_count"] = test_df["query"].apply(and_count)
    test_df["or_count"] = test_df["query"].apply(or_count)
    test_df["dot_count"] = test_df["query"].apply(dotcount)
    test_df["at_count"] = test_df["query"].apply(atcount)
    test_df["subdir_count"] = test_df["query"].apply(subdircount)
    test_df["query_len"] = test_df["query"].apply(query_len)
    test_df["param_count"] = test_df["query"].apply(param_count)
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
    test_df["parameters"] = test_df["query"].apply(find_parameter_name)
    return test_df
