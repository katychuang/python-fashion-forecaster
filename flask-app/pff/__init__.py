from flask import Flask
import settings

app = Flask('frame')
app.config.from_object('frame.settings')

import views

