#! /usr/local/bin/python
#-*- coding: utf-8 -*-
import requests
import re
import lxml
import json
from datetime import datetime
from time import time
import getpass
from bs4 import BeautifulSoup as bs
from requests.utils import dict_from_cookiejar, cookiejar_from_dict
__AUTHOR__ = 'lc4t0.0@gmail.com'


def get_tiles_per_edge(zoom):
    if zoom > 15:
        zoom = 15
    elif zoom < 3:
        zoom = 3
    else:
        pass
    return [1, 1, 1, 40, 40, 80, 80, 320, 1000, 2000, 2000, 4000, 8000, 16000, 16000, 32000][zoom]


def lng2tile(lng, tpe): # w
  return int((lng + 180) / 360 * tpe);

def lat2tile(lat, tpe): # j
    return int((1 - math.log(math.tan(lat * math.pi / 180) + 1 / math.cos(lat * math.pi / 180)) / math.pi) / 2 * tpe)

def tile2lng(x, tpe):
    return x / tpe * 360 - 180;

def tile2lat(y, tpe):
    n = math.pi - 2 * math.pi * y / tpe;
    return 180 / math.pi * math.atan(0.5 * (math.exp(n) - math.exp(-n)));


class IntelMap:
    r = requests.Session()
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8',
        'content-type': 'application/json; charset=UTF-8',
        'origin': 'https://www.ingress.com',
        'referer': 'https://www.ingress.com/intel',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    }
    data_base = {
        'v': '',
    }
    proxy = {
        'http': 'socks5://127.0.0.1:1080',
        'https': 'socks5://127.0.0.1:1080',
    }
    def __init__(self, cookie, username, password):
        self.username = username
        self.password = password
        self.login(cookie, username, password)

    def login(self, cookie, username, password):
        try:
            self.cookie_dict = {k.strip():v for k,v in re.findall(r'(.*?)=(.*?);', cookie)}
            s = requests.Session()
            s.cookies = cookiejar_from_dict(self.cookie_dict)
            test = s.get('https://www.ingress.com/intel', proxies=self.proxy)
            self.data_base['v'] = re.findall('/jsc/gen_dashboard_([\d\w]+).js"', test.text)[0]
            self.r = s
            print('cookies success')
        except IndexError:
            print('login with username password')
            _ = self.r.get('https://www.ingress.com/intel', proxies=self.proxy)
            login_url = re.findall('"(https://www\.google\.com/accounts/ServiceLogin.+?)"', _.text)[0]
            _ = self.r.get(login_url, proxies=self.proxy)
            username_xhr_url = 'https://accounts.google.com/accountLoginInfoXhr'
            headers = {
                'accept':'*/*',
                'accept-encoding':'gzip, deflate, br',
                'accept-language':'en-US,en;q=0.8',
                'content-type':'application/x-www-form-urlencoded',
                'origin': 'https://accounts.google.com',
                'referer' :'https://accounts.google.com/ServiceLogin?service=ah&passive=true&continue=https%3A%2F%2Fappengine.google.com%2F_ah%2Fconflogin%3Fcontinue%3Dhttps%3A%2F%2Fwww.ingress.com%2Fintel&ltmpl=gm&shdf=ChMLEgZhaG5hbWUaB0luZ3Jlc3MMEgJhaCIUDxXHTvPWkR39qgc9Ntp6RlMnsagoATIUG3HUffbxSU31LjICBdNoinuaikg',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            }
            html = bs(_.text, 'lxml')
            if len(username) == 0:
                username = input('username:')
                self.username = username
                password = getpass.getpass('password:')
                self.password = password

            data = {
                'Email' : username,
            }
            for i in html.form.select('input'):
                try:
                    if i['name'] == 'Page':
                        data.update({'Page': i['value']})
                    elif i['name'] == 'service':
                        data.update({'service': i['value']})
                    elif i['name'] == 'ltmpl':
                        data.update({'ltmpl': i['value']})
                    elif i['name'] == 'continue':
                        data.update({'continue': i['value']})
                    elif i['name'] == 'gxf':
                        data.update({'gxf': i['value']})
                    elif i['name'] == 'GALX':
                        data.update({'GALX': i['value']})
                    elif i['name'] == 'shdf':
                        data.update({'shdf': i['value']})
                    elif i['name'] == '_utf8':
                        data.update({'_utf8': i['value']})
                    elif i['name'] == 'bgresponse':
                        data.update({'bgresponse': i['value']})
                    else:
                        pass
                except KeyError:
                    pass
            _ = self.r.post(username_xhr_url, data=data, proxies=self.proxy, headers=headers)
            password_url = 'https://accounts.google.com/signin/challenge/sl/password'
            data.update({'Page': 'PasswordSeparationSignIn'})
            data.update({'identifiertoken': ''})
            data.update({'identifiertoken_audio': ''})
            data.update({'identifier-captcha-input': ''})
            data.update({'Passwd': password})
            data.update({'PersistentCookie': 'yes'})
            _ = self.r.post(password_url, headers=headers, data=data, proxies=self.proxy)
            self.data_base['v'] = re.findall('/jsc/gen_dashboard_([\d\w]+).js"', _.text)[0]

        self.cookie_dict = dict_from_cookiejar(self.r.cookies)
        self.headers.update({'x-csrftoken': self.cookie_dict['csrftoken']})


    def get_game_score(self):
        data = self.data_base
        data = json.dumps(data)
        _ = self.r.post('https://www.ingress.com/r/getGameScore', data=data, headers=self.headers, proxies=self.proxy)
        print(_.text)
        return json.loads(_.text)

    def get_entities(self, tilenames):
        _ = {
          "tileKeys": tilenames,    # ['15_25238_13124_8_8_100']
        }
        data = self.data_base
        data.update(_)
        data = json.dumps(data)
        _ = self.r.post('https://www.ingress.com/r/getEntities', data=data, headers=self.headers, proxies=self.proxy)
        return json.loads(_.text)

    def get_portal_details(self, guid):
        _ = {
          "guid": guid, # 3e2bcc15c58d486fae24e2ade2bf7327.16
        }
        data = self.data_base
        data.update(_)
        data = json.dumps(data)
        _ = self.r.post('https://www.ingress.com/r/getPortalDetails', data=data, headers=self.headers, proxies=self.proxy)
        return json.loads(_.text)

    def get_plexts(self, min_lng, max_lng, min_lat, max_lat, tab='all', maxTimestampMs=-1, minTimestampMs=0, ascendingTimestampOrder=True):
        if minTimestampMs == 0:
            minTimestampMs = int(time()*1000)
        data = self.data_base
        data.update({
            'ascendingTimestampOrder': ascendingTimestampOrder,
            'maxLatE6': max_lat,
            'minLatE6': min_lat,
            'maxLngE6': max_lng,
            'minLngE6': min_lng,
            'maxTimestampMs': maxTimestampMs,
            'minTimestampMs': minTimestampMs,
            'tab': tab,
        })
        data = json.dumps(data)
        _ = self.r.post('https://www.ingress.com/r/getPlexts', headers=self.headers, data=data, proxies=self.proxy)
        return json.loads(_.text)

    def send_plexts(self, lat, lng, message, tab='faction'):
        data = self.data_base
        data.update({
            'latE6': lat,
            'lngE6': lng,
            'message': message,
            'tab': tab,
        })
        data = json.dumps(data)
        _ = self.r.post('https://www.ingress.com/r/sendPlext', headers=self.headers, data=data, proxies=self.proxy)
        return json.loads(_.text)

    def get_region_score_details(self, lat, lng):
        data = self.data_base
        data.update({
            'latE6': lat,   # 30420109, 104938641
            'lngE6': lng,
        })
        data = json.dumps(data)
        _ = self.r.post('https://www.ingress.com/r/getRegionScoreDetails', headers=self.headers, data=data, proxies=self.proxy)
        return json.loads(_.text)

    def get_redeem_reward(self, passcode):
        data = self.data_base
        data.update({
            'passcode': passcode,
        })
        data = json.dumps(data)
        _ = self.r.post('https://www.ingress.com/r/redeemReward', headers=self.headers, data=data, proxies=self.proxy)
        return json.loads(_.text)

    def get_send_invite_email(self, email):
        data = self.data_base
        data.update({
            'inviteeEmailAddress': email,
        })
        data = json.dumps(data)
        _ = self.r.post('https://www.ingress.com/r/sendInviteEmail', headers=self.headers, data=data, proxies=self.proxy)
        return json.loads(_.text)

class GameAPI:
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Content-Encoding': 'gzip',
        'User-Agent': 'Nemesis (gzip)',
        'Accept-Encoding': 'gzip',
    }
    proxy = {
        'http': 'socks5://127.0.0.1:1080',
        'https': 'socks5://127.0.0.1:1080',
    }
    r = requests.Session()

    def __init__(self, language, token, auth, blob):
        self.headers.update({
            'Accept-Language': language,
            'X-XsrfToken': token,
            'Authorization': auth,
        })

    def set_blob(self, blob, timestamp):

        self.data_base = {
            'params': {
                'clientBasket': {
                    'clientBlob': blob,
                },
                'knobSyncTimestamp': int(timestamp),
            }
        }

    def get_game_score(self):
        url = 'https://m-dot-betaspike.appspot.com/rpc/playerUndecorated/getGameScore'
        data = {
                "params": []
                }
        data = json.dumps(data)
        _ = self.r.post(url, proxies=self.proxy, headers=self.headers, data=data)
        return json.loads(_.text)

    def get_objects_in_cells(self, lng, lat):
        data = self.data_base
        data['params'].update({
            "energyGlobGuids": [],
            "playerLocation": '%s,%s' % (hex(lng)[2:], hex(lat)[2:]),
            "dates": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        })
        # todo here

if __name__ == '__main__':
    pass
