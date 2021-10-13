from flask import Flask
app = Flask(__name__)
app.secret_key = "secrets"

DATABASE = "recipes_v2"