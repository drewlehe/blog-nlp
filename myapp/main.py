from bokeh.models import Button, Paragraph, TextInput, WidgetBox
from bokeh.plotting import curdoc, show, figure
from clean import clean
from joblib import load
import json
import pandas as pd

model = load('pima.joblib.dat')
tfid = load('tfidf.pickle')

def update_data(event):
    data = str(textin.value)
    result = model.predict(tfid.transform([' '.join(clean(data))]))
    if int(result) == 1:
            pred_text = 'Male'
        else:
            pred_text = 'Female'
        output = {'prediction': pred_text}
    return output


textin = TextInput(title = "Submit Blog Post:")
button = Button(label="Submit", button_type="success")
button.on_click(update_data)
p = Paragraph(text="Price here")
box = WidgetBox(children = [textin, button, p])
curdoc().add_root(box)