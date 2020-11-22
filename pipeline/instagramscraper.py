import requests
from datetime import datetime
from db.database import Database
from config import host, db, user, pw
import json


class Instagram:
    def __init__(self):
        self.session = None
        self.date = datetime.now()
        self.db = Database(host, db, user, pw)

    def load(self, session):
        self.session = session

    def login(self, username: str, password: str) -> dict:
        url = 'https://www.instagram.com/accounts/login/'
        login_url = 'https://www.instagram.com/accounts/login/ajax/'

        time = int(datetime.now().timestamp())

        response = requests.get(url)
        csrf = response.cookies['csrftoken']

        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        login_header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/77.0.3865.120 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            "x-csrftoken": csrf
        }

        login_response = requests.post(login_url, data=payload, headers=login_header)
        json_data = json.loads(login_response.text)

        print(json_data)

        if json_data["authenticated"]:
            cookies = login_response.cookies
            cookie_jar = cookies.get_dict()

            self.session = {
                "csrf_token": cookie_jar['csrftoken'],
                "session_id": cookie_jar['sessionid']
            }

            return self.session

        raise Exception(login_response.text)

    def get_html(self, username):
        url = f"https://www.instagram.com/{username}"

        cookies = {
            "sessionid": self.session['session_id'],
            "csrftoken": self.session['csrf_token']
        }

        response = requests.request("POST", url, cookies=cookies)

        return response.text

    def _number_converter(self, num):
        num = num.replace(" ", "").replace(",", "")
        try:
            if "k" in num:
                num = float(num.split("k")[0]) * 1000
            elif "m" in num:
                num = float(num.split("m")[0]) * 1000000
            else:
                num = float(num)
        except:
            num = -1

        return int(num)


    def _get_info(self, username):
        html = self.get_html(username)
        meta = html.split("meta content=")[1].split("See Instagram")[0]
        meta = meta.replace('"', '')

        # Follower count
        follower_count = self._number_converter(meta.split("Followers")[0])

        # Following
        following_count = self._number_converter(meta.split("Followers,")[1].split("Following")[0])

        # Posts
        posts = self._number_converter(meta.split(",", 1)[1].split(",")[-1].split("Posts")[0])

        name = str(html.split('name="description:"')[0].split('from ')[1].split('(')[0].strip())
        if len(name) > 300:
            name = ""

        return username, name, follower_count, following_count, posts

    def upload_record(self, username):
        username, name, follower_count, following_count, posts = self._get_info(username)
        record = [username, name, follower_count, following_count, posts, self.date]
        print(self.db.insert_ignore('social_media', record))


# reference: https://github.com/softcoder24/insta_share/blob/master/insta_share/instagram.py