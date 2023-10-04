# :shield: ML-Based WAF and Query Analyzer
---
<div align="center">
  <img src="https://raw.githubusercontent.com/thealper2/AISECLAB-cyber-inspector/main/website/static/logo.png" width="320" height="320" >
</div>
<br/>
<i>Bu çalışma, aiseclab.org bünyesinde <b>cyber-inspector</b> ekibi projesi olarak geliştirilmiştir.</i>

# :shield: Amaç
---

* Makine öğrenmesi modellerini kullarak WAF isteklerini zararlı ve zararsız olarak sınıflandırılacaktır. Kullanılan veri setine ulaşmak için [bu bağlantıya](https://github.com/faizann24/Fwaf-Machine-Learning-driven-Web-Application-Firewall) tıklayabilirsiniz.
<br/>

# :shield: Ekip Üyeleri
---

1. [Alper KARACA](https://github.com/thealper2)
2. [Oudoum Ali HOUMED](https://github.com/OudoumAlihoumed)
3. [Zeynep GÜNEY](https://github.com/zeynepguney)
4. [Oğuz Kortun](https://github.com/OguzKortun)
<br/>

# :shield: Gerekli Kütüphaneler

* Kullanılan kütüphaneler ve versiyon bilgileri aşağıda belirtilmiştir.

```shell
Flask==3.0.0
Flask_Login==0.6.2
Flask_SocketIO==5.3.6
flask_sqlalchemy==3.1.1
matplotlib==3.8.0
nltk==3.8.1
numpy==1.23.1
pandas==1.5.3
Pillow==9.5.0
Pillow==9.0.1
Pillow==10.0.1
scikit_learn==1.2.2
seaborn==0.13.0
SQLAlchemy==2.0.21
Werkzeug==3.0.0
wordcloud==1.9.2
```
<br/>

# :shield: Kurulum
---

* Gerekli paketleri kurduktan sonra uygulamayı kullanmaya başlayabilirsiniz.

```python3
pip install -r requirements.txt
# Ana uygulamayı çalıştırmak için
python3 main.py
# Fake api'yi çalıştırmak için
python3 api.py
```
<br/>

# :shield: Modeller
---

* Problemi çözmek için LogisticRegression, RandomForest, DecisionTree ve XGB modelleri kullanılmıştır. Kullanılam modellere ait veriler aşağıda belirtilmiştir.

| Model | Training Time | Train Accuracy | Test Accuracy | F1-Score | Precision Score | Recall Score |
| ----- | ------------- | -------------- | ------------- | -------- | --------------- | ------------ |
| LogisticRegression | 9.63s | 0.9300 | 0.9296 | 0.9264 | 0.9703 | 0.8864 |  
| RandomForestClassifier | 300.30s | 0.9693 | 0.9684 | 0.9676 | 0.9925 | 0.9439 | 
| DecisionTreeClassifier | 16.59s | 0.9693 | 0.9683 | 0.9674 | 0.9928 | 0.9434 | 
| XGBClassifier | 7.17s | 0.9622 | 0.9618 | 0.9609 | 0.9860 | 0.9369 | 
