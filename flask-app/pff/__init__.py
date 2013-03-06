from flask import Flask
import settings

app = Flask('pff')
app.config.from_object('pff.settings')

import views

