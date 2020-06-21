# blog-nlp
Predicting author gender in a large blog corpus acquired here:
https://www.kaggle.com/rtatman/blog-authorship-corpus/

Preprocessing done with SpaCy, SymSpell, Gensim and NLTK in the clean.py file. Text preprocessing is probably the most technical part of NLP and I'm a fan of sticking the preprocessing step all into one neat script.
Predictor algorithm is XGBoost's "boosted random forest" method, sending out multiple "stumps" at each cycle and averaging their predictions.
/myapp contains an interactive bokeh app which was deployed to an AWS EC2 instance. 

You can find my deployed Bokeh app at http:// 18.216 dot 47.156:5006/main
Or my deployed Flask app at dockerp53 dot herokuapp dot com
