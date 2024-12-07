from flask import Flask, request, redirect, url_for, render_template
import os
from datetime import datetime, date

app = Flask(__name__)
from app import app

if __name__ == '__main__':
    app.run(debug=True)
