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

stemmer = SnowballStemmer("english")
tokenizer = RegexpTokenizer(r"[A-Za-z]+")

def loadFile(name):
    directory = str(os.getcwd())
    filepath = os.path.join(directory, name)
    with open(filepath, "r") as f:
        data = f.readlines()

    data = list(set(data))
    result = []
    for d in data:
        d = str(urllib.parse.unqoute(d))
        result.append(d)

    return result

def clean_newline(column):
    return column[:-2]

def clear_first_char(column):
    if column.startswith("/"):
        return column[1:]
    else:
        return column

def xss_check(input_string):
    xss_pattern = re.compile(r'(<|>|&lt;|&gt;|script|alert|document\.|onload\=|onerror\=|eval\(|expression\(|prompt\(|confirm\()')
    if xss_pattern.search(input_string.split("/")[-1]):
        return 1
    else:
        return 0

def lfi_check(input_string):
    lfi_pattern = re.compile(r'(file\:\/\/|(\.\.\/)|(\.\.\\))')
    if "=" in input_string.split("/")[-1]:
        if lfi_pattern.search(input_string.split("/")[-1].split("=", 1)[1]):
            return 1
        else:
            return 0
    elif lfi_pattern.search(input_string.split("/")[-1]):
        return 1
    else:
        return 0

def command_injection_check(input_string):
    cmd_injection_pattern = re.compile(r'(;|\||`|\$\(|\$\{)')

    if cmd_injection_pattern.search(input_string):
        return 1
    else:
        return 0

def sql_injection_check(input_string):
    sql_injection_pattern = re.compile(r'(\b(SELECT|INSERT|UPDATE|DELETE|FROM|WHERE|AND|OR|UNION|ALL|EXEC|EXECUTE|DECLARE|CAST)\b)')

    if sql_injection_pattern.search(input_string):
        return 1
    else:
        return 0

def urllen(url):
    return len(url)

def delimitercount(url):
    return url.count(";") + url.count("_") + url.count("?") + url.count("=") + url.count("&") + url.count("|")

def dotcount(url):
    return url.count(".")

def atcount(url):
    return url.count("@")

def subdircount(url):
    return url.count("/")

def query_count(query):
    if "=" in query:
        return len(query.split("=")[1])
    else:
        return 0

def total_digits_in_url(url):
    total_digits = 0
    for text in list(map(str, "0123456789")):
        total_digits += url.lower().count(text)

    return total_digits

def total_letter_in_url(url):
    total_letter = 0
    for text in url:
        if text not in "0123456789":
            if text not in string.punctuation:
                total_letter += 1

    return total_letter

def stem_url(column):
    words = [stemmer.stem(word) for word in column]
    return " ".join(words)

def total_digits_domain(url):
    if "/" in url:
        path = url.split("/")[-1]
        dom = url.replace(path, "")
        return total_digits_in_url(dom)

    else:
        return 0

def total_digits_path(url):
    if "/" in url:
        path = url.split("/")[-1]
        return total_digits_in_url(path)
    else:
        return total_digits_in_url(url)

def total_letter_domain(url):
    if "/" in url:
        path = url.split("/")[-1]
        dom = url.replace(path, "")
        return total_letter_in_url(dom)
    else:
        return 0

def total_letter_path(url):
    if "/" in url:
        path = url.split("/")[-1]
        return total_letter_in_url(path)
    else:
        return total_letter_in_url(url)

def has_extension(column):
    if "." in column.split("/")[-1]:
        return 1
    else:
        return 0

def find_extension(column):
    text = column.split("/")[-1]
    if "." in text:
        if "?" in text:
            return text.split("?", 1)[0]
        else:
            return text.split(".", 1)[1]
    else:
        return ""

def has_parameter(column):
    if "?" in column.split("/")[-1]:
        return 1
    else:
        return 0

def word_freq(freq_top, LABEL, save_path):
    words = [word for word, _ in freq_top]
    counts = [count for _, count in freq_top]

    plt.figure(figsize=(20, 5))
    plt.bar(words, counts)
    plt.title(LABEL)
    plt.ylabel("Frequency")
    plt.xlabel("Words")
    plt.savefig(save_path)

def print_wordcloud(dict_top, LABEL, save_path):
    dict_top = dict(dict_top)
    wordcloud = WordCloud(width=350, height=350, background_color="white").generate_from_frequencies(dict_top)

    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.title(LABEL)
    plt.savefig(save_path)

def get_histplot_central_tendency(df, features, label, save_path):
    for feature in features:
        v_dist_1 = df[feature].values
        plt.figure()
        sns.histplot(v_dist_1, kde=True)

        mean = df[feature].mean()
        median = df[feature].median()
        #mode = df[feature].mode()

        plt.axvline(mean, color="r", linestyle="--", label="Mean")
        plt.axvline(median, color="g", linestyle="-", label="Median")
        #plt.axvline(mode, color="b", linestyle=":", label="Mode")
        plt.xlabel(f"count", fontsize=13, color="#333F4B")
        plt.ylabel(f"{feature}", fontsize=13, color="#333F4B")
        plt.legend()
        plt.grid(False)
        plt.title(f"Histogram for {feature} - {label}", fontsize=18)
        plt.plot(color="white", lw=3)
        plt.savefig(save_path + f"{label}_{feature}.png")

def pie_chart(df, save_path):
    plt.figure(figsize=(5, 5))
    positive = len(df[df["label"] == 0])
    negative = len(df[df["label"] == 1])
    pie_y = [positive, negative]
    pie_labels = ["benign", "malicious"]
    plt.pie(pie_y, labels=pie_labels, startangle=90, autopct="%.1f%%")
    plt.savefig(save_path)