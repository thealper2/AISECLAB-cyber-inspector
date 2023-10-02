import pandas as pd
import numpy as np
import os
import pickle
import json
from website.preprocess import preprocess
from website.functions import *
from flask_login import login_required, current_user
from flask import Blueprint, render_template, jsonify, request, send_file, redirect, url_for
from .models import Query, User
from . import db

views = Blueprint("views", __name__)

@views.route("/")
def index():
    return render_template("index.html")

@views.route("/docs")
def docs():
    return render_template("docs.html")

@views.route("/dashboard")
@login_required
def dashboard():
    total_0 = 0
    total_1 = 0

    for i in range(len(current_user.queries)):
        if "0.0" == current_user.queries[i].label:
            total_0 += 1
        elif "1.0" == current_user.queries[i].label:
            total_1 += 1
    
    total = total_0 + total_1
    if total > 0: 
        save_path = "website/static/reports/"

        label = np.array(["benign", "malicious"])
        values = np.array([total_0, total_1])
        colors = ["blue", "red"]

        plt.figure(figsize=(5, 5))
        plt.bar(label, values, color=colors)
        plt.title("Total Queries per Category")
        plt.savefig(save_path + "db_total.png")
        
        plt.figure(figsize=(5, 5))
        plt.pie(values, labels=label)
        plt.title("Total Queries per Category")
        plt.savefig(save_path + "db_total2.png")

        return render_template("dashboard.html", user=current_user, is_zero=False)

    else:
        return render_template("dashboard.html", user=current_user, is_zero=True)

@views.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file.filename != "":
            file_path = os.path.join("website/uploads", uploaded_file.filename)
            uploaded_file.save(file_path)

            model = pickle.load(open("website/models/logreg.pkl", "rb"))
            ss = pickle.load(open("website/models/ss.pkl", "rb"))
            
            test_df = pd.read_csv(file_path, names=["query"])
            test_df = test_df.head(10)
            test_df["query"] = test_df["query"].apply(clear_first_char)
            result_df = preprocess(test_df)
            X = result_df.drop(["query", "url_tokenized", "url_stemmed", "extension", "parameters"], axis=1)
            X_scaled = ss.transform(X)
            result = model.predict(X_scaled)
            for i in range(len(result_df)):
                result_df.loc[i, "label"] = result[i]
                query_text = result_df.loc[i, "query"]
                label = result_df.loc[i, "label"]
                new_query = Query(query_text=query_text, label=label, user_id=current_user.id)
                db.session.add(new_query)
                db.session.commit()

            if not os.path.isdir(f"website/static/reports/{uploaded_file.filename[:-4]}"):
                os.makedirs(f"website/static/reports/{uploaded_file.filename[:-4]}")
                
            save_path = f"website/static/reports/{uploaded_file.filename[:-4]}/"
            result_df.to_csv(f"{save_path}{uploaded_file.filename[:-4]}_preprocessed.csv")

            # EDA
            features = ['is_xss', 'is_lfi', 'is_oci', 'is_sqli', 'url_len',
                        'semicolon_count', 'underscore_count', 'questionmark_count',
                        'equal_count', 'and_count', 'or_count', 'dot_count', 'at_count',
                        'subdir_count', 'query_len', 'param_count', 'total_digits_url',
                        'total_letter_url', 'total_digits_domain', 'total_letter_domain', 
                        'total_digits_path', 'total_letter_path', 'has_extension', 'has_parameter']

            eda(result_df=result_df, save_path=save_path, features=features)

            images = os.listdir(save_path)
            image = [os.path.join(file) for file in images if file.endswith(".png")] 

            return render_template("statistics.html", user=current_user, selected=True, df=result_df, folder=f"{uploaded_file.filename[:-4]}")

    return render_template("upload.html", user=current_user)

@views.route("/delete-query", methods=["POST"])
def delete_query():
    qu = json.loads(request.data)
    queryId = qu["id"]
    qu = Query.query.get(queryId)
    if qu:
        if qu.user_id == current_user.id:
            db.session.delete(qu)
            db.session.commit()

    return jsonify({})

@views.route("/download_csv/<filename>", methods=["GET"])
@login_required
def download_csv(filename):
    folder_path = os.path.join("static/reports", filename[:-4])
    csv_file_path = os.path.join(folder_path, f"{filename[:-4]}_preprocessed.csv")
    return send_file(csv_file_path, as_attachment=True, download_name=f"{filename[:-4]}_preprocessed.csv")

@views.route("/database")
@login_required
def database():
    return render_template("database.html", user=current_user)

@views.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        new_username = request.form["username"]
        new_email = request.form["email"]

        user = User.query.filter_by(id=current_user.id).first()
        user.username = new_username
        user.email = new_email
        db.session.commit()
        return redirect(url_for("views.profile"))


    return render_template("profile.html", user=current_user)

@views.route("/statistics", methods=["GET", "POST"])
@login_required
def statistics():
    folders = [folder for folder in os.listdir("website/static/reports") if os.path.isdir(os.path.join("website/static/reports", folder))]
    if request.method == "POST":
        selected_folder = request.form["folder"]
        return render_template("statistics.html", user=current_user, selected=True, folder=selected_folder, folders=folders)

    return render_template("statistics.html", user=current_user, selected=False, folders=folders)

@views.route("/report")
@login_required
def report():
    return render_template("report.html", user=current_user)

def eda(result_df, save_path, features):
    pie_chart(df=result_df, save_path=save_path + "pie_chart.png")
    
    cn_1 = Counter()
    cn_0 = Counter()

    for text, phishing in zip(result_df.url_stemmed.values, result_df.label.values):
        for word in text.split():
            if phishing == 1:
                cn_1[word] += 1
            else:
                cn_0[word] += 1
                
    most_common_1 = cn_1.most_common(5)
    most_common_0 = cn_0.most_common(5)

    word_freq(freq_top=most_common_0, LABEL="TOP 5 WORDS - BENIGN", save_path=save_path + "0_top_words.png")
    word_freq(freq_top=most_common_1, LABEL="TOP 5 WORDS - MALICIOUS", save_path=save_path + "1_top_words.png")

    print_wordcloud(dict_top=most_common_0, LABEL="TOP 5 WORDS - BENIGN", save_path=save_path + "0_wc.png")
    print_wordcloud(dict_top=most_common_1, LABEL="TOP 5 WORDS - MALICIOUS", save_path=save_path + "1_wc.png")

    cn_ext_1 = Counter()
    cn_ext_0 = Counter()

    for text, phishing in zip(result_df.extension.values, result_df.label.values):
        for word in text.split():
            if phishing == 1:
                cn_ext_1[word] += 1
            else:
                cn_ext_0[word] += 1
            
    most_common_ext_1 = cn_ext_1.most_common(5)
    most_common_ext_0 = cn_ext_0.most_common(5)

    word_freq(freq_top=most_common_ext_0, LABEL="TOP 5 EXTENSIONS - BENIGN", save_path=save_path + "0_top_extensions.png")
    word_freq(freq_top=most_common_ext_1, LABEL="TOP 5 EXTENSIONS - MALICIOUS", save_path=save_path + "1_top_extensions.png")
    
    get_histplot_central_tendency(df=result_df, features=features, label=0, save_path=save_path)
    get_histplot_central_tendency(df=result_df, features=features, label=1, save_path=save_path)
