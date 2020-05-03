from bokeh.models import Button, Paragraph, TextInput, WidgetBox
from bokeh.plotting import curdoc, show, figure
from clean import clean
from joblib import load
from threading import Thread
from tornado.ioloop import IOLoop
from bokeh.embed import server_document
import pandas as pd
from flask import Flask, render_template
from flask_restful import reqparse, abort, Api, Resource
from bokeh.server.server import Server

model = load('xgbooster')
vocab = load('feature')

app = Flask(__name__)
api = Api(app)

from sklearn.feature_extraction.text import TfidfVectorizer
transformer = TfidfVectorizer(min_df=2, max_df=0.6, smooth_idf=True,
                              norm = 'l2', ngram_range=[1,2], max_features=125000,
                              decode_error="replace", vocabulary=vocab)
transformer.fit_transform(vocab)

def bkapp(doc):
    textin = TextInput(title = "Submit Blog Post:")
    button = Button(label="Submit", button_type="success")
    p = Paragraph(text="Blog entry here")
    def update_data(event):
        data = str(textin.value)
        vector = transformer.transform([' '.join(clean(data))])
        result = model.predict(vector)
        if int(result) == 1:
            pred_text = 'Male'
        else:
            pred_text = 'Female'
        output = {'prediction': pred_text}
        p.text = "{}".format(output)
        
    button.on_click(update_data)
    box = WidgetBox(children = [textin, button, p])
    doc.add_root(box)
    
        
@app.route('/', methods=['GET'])
def bkapp_page():
    script = server_document('http://localhost:5006/bkapp')
    return render_template("embed.html", script=script, template="Flask")


def bk_worker():
    server = Server({'/bkapp': bkapp}, io_loop=IOLoop(), allow_websocket_origin=["localhost:8000", "127.0.0.1:5006"])
    server.start()
    server.io_loop.start()

Thread(target=bk_worker).start()

if __name__ == '__main__':
    app.run(debug=True, port=8000)
