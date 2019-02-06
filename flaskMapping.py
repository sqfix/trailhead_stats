from flask import Flask
import requests
from lxml import html

app = Flask(__name__)


@app.route('/')
def index():    
    return get_user_info()


if __name__ == "__main__":
    app.run(debug=True)


def get_user_info():
    page = requests.get("https://trailhead.salesforce.com/en/me/00550000006xt96AAA")
    tree = html.fromstring(page.content)
    prices = tree.xpath('//span[@class="user-information__achievements-data"]/text()')
    return prices

