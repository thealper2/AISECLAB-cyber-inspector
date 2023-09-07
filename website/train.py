import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

df = pd.read_csv("preprocessed.csv")
X = df.drop(["query", "label", "url_tokenized", "url_stemmed", "extension", "parameters"], axis=1)
y = df["label"]

ss = StandardScaler()
X_scaled = ss.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

logreg = LogisticRegression()
logreg.fit(X_train, y_train)

pred_train = logreg.predict(X_train)
pred_test = logreg.predict(X_test)

train_score = accuracy_score(y_train, pred_train)
print("[+] Train Score:", train_score)

test_score = accuracy_score(y_test, pred_test)
print("[+] Test Score:", test_score)

pickle.dump(logreg, open("models/logreg.pkl", "wb"))
pickle.dump(ss, open("models/logreg_ss.pkl", "wb"))
