import datetime
import requests
import json
import jsonpickle
from flask import Flask, request
from lxml import html

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        user_ids = request.json['user_ids']
        return get_user_info(str(user_ids))
    return ''


if __name__ == "__main__":
    app.run(debug=True)


def get_user_info(user_id):
    page = requests.get("https://trailhead.salesforce.com/en/me/" + user_id)
    print(user_id)
    tree = html.fromstring(page.content)
    badges = tree.xpath('//div[@class="user-information__achievements-data"]/text()')[0]
    points = tree.xpath('//div[@class="user-information__achievements-data"]/text()')[1]

    stats = str(UserStats(badges, points, datetime.date.today(), user_id))
    return json.dumps(stats)


class UserStats(object):
    def __init__(self, badges, points, date, trail_id):
        self.badges = badges
        self.points = points
        self.date = date
        self.trailId = trail_id
