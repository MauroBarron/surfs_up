#%%
##
##  Learning FLASK
##
# %%
# Dependencies
from flask import Flask
# %%
# Create a new Flask instance
app = Flask(__name__)
# %%
# Create a new Flask route runs function hello_world
@app.route('/')
def hello_world():
    return 'Hello All Big Monkeys of the World'