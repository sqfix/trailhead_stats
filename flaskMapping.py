import datetime
import requests
import os
from flask import Flask, request
from lxml import html

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user_ids = request.json['user_ids']
        return get_user_info(str(user_ids))
    return 'Hello!'


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


def get_user_info(user_id):
    page = requests.get("https://trailhead.salesforce.com/en/me/" + user_id)
    print(user_id)
    tree = html.fromstring(page.content)
    badges = tree.xpath('//div[@class="user-information__achievements-data"]/text()')[0]
    points = tree.xpath('//div[@class="user-information__achievements-data"]/text()')[1]

    stats = str(UserStats(badges, points, datetime.date.today(), user_id))
    return str(stats)


class UserStats(object):
    def __init__(self, badges, points, date, trail_id):
        self.badges = badges
        self.points = points
        self.date = date
        self.trail_id = trail_id

    def __str__(self):
        return '{' + '"badges" : "' + self.badges + '", "points" : "' + self.points + '", "trail_id" : "' + self.trail_id + '"}'
