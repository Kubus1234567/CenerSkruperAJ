from flask import request, render_template, redirect, url_for
from app import app
from app.models.opinion import Opinion
from app.models.shop import Shop
from app.forms import ShopForm
from os import listdir
import requests
import json

app.config['SECRET_KEY'] = "NotSoSecretKey"

@app.route('/')
@app.route('/index')
def index():
    return render_template('main.html.jinja')

@app.route('/extract', methods=['GET', 'POST'])
def extract():
    form = ShopForm()
    if request.method == 'POST' and form.validate_on_submit():
        shop = Shop(request.form['shopName'])
        # 403 when using default user-agent
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        respons = requests.get(shop.opinionsPageUrl(), headers=headers)
        if respons.status_code == 200:
            shop.extractShop()
            shop.exportShop()
            return redirect(url_for('shop', shopName=shop.shopName))
        else:
            form.shopName.errors.append("For given shopName there is no shop")
    return render_template('extract.html.jinja', form=form)

@app.route('/shop/<shopName>')
def shop(shopName):
    return render_template('shop.html.jinja', shopName=shopName)

@app.route('/shops')
def shops():
    shopsList = [x.split(".")[0] for x in listdir("app/opinions")]
    return render_template('shops.html.jinja', shopsList=shopsList)

@app.route('/author')
def author():
    return render_template('author.html.jinja')
