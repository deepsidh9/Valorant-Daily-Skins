import ssl
import requests
from collections import OrderedDict
import re
from requests.adapters import HTTPAdapter
from urllib3 import PoolManager


class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1_2)


class ValorantAPI(object):

    def __init__(self, username, password, region):
        self.username = username
        self.password = password
        self.region = region
        self.authenticate()
        self.all_skins = self.get_skins()
        self.player_store = self.get_player_store()
    
    def mount_session(self):

        self.headers = OrderedDict({
            'User-Agent': 'RiotClient/43.0.1.4195386.4190634 rso-auth (Windows;10;;Professional, x64)'
        })

        self.session = requests.session()
        self.session.mount(
            'https://auth.riotgames.com/api/v1/authorization', SSLAdapter())
        self.session.headers = self.headers

        data = {
            'client_id': 'play-valorant-web-prod',
            'nonce': '1',
            'redirect_uri': 'https://playvalorant.com/opt_in',
            'response_type': 'token id_token',
        }
        r = self.session.post(f'https://auth.riotgames.com/api/v1/authorization', json=data,
                              headers=self.headers)
        self.validate_request(r, "Session Mount")

    def get_access_token(self):
        data = {
            'type': 'auth',
            'username': self.username,
            'password': self.password
        }
        r = self.session.put(
            f'https://auth.riotgames.com/api/v1/authorization', json=data, headers=self.headers)
        self.validate_request(r, "Access Token")
        pattern = re.compile(
            'access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
        data = pattern.findall(r.json()['response']['parameters']['uri'])[0]
        self.access_token = data[0]

    def get_entitlements_token(self):

        self.headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': "entitlements.auth.riotgames.com",
            'User-Agent': 'RiotClient/43.0.1.4195386.4190634 rso-auth (Windows;10;;Professional, x64)',
            'Authorization': f'Bearer {self.access_token}',
        }
        r = self.session.post(
            'https://entitlements.auth.riotgames.com/api/token/v1', headers=self.headers, json={})
        self.validate_request(r, "Entitlment Token")
        self.entitlements_token = r.json()['entitlements_token']

    def get_user_info(self):
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': "auth.riotgames.com",
            'User-Agent': 'RiotClient/43.0.1.4195386.4190634 rso-auth (Windows;10;;Professional, x64)',
            'Authorization': f'Bearer {self.access_token}',
        }

        r = self.session.post('https://auth.riotgames.com/userinfo',
                              headers=self.headers, json={})
        self.validate_request(r, "User Info Space")
        self.user_id = r.json()['sub']
        self.headers['X-Riot-Entitlements-JWT'] = self.entitlements_token
        del self.headers['Host']
        self.session.close()

    def authenticate(self):
        self.mount_session()
        self.get_access_token()
        self.get_entitlements_token()
        self.get_user_info()

    def get_skins(self):
        all_skins = requests.get(
            "https://valorant-api.com/v1/weapons/skins").json()["data"]
        flat_skins = []
        for skin in all_skins:
            if 'chromas' in skin:
                for chroma in skin['chromas']:
                    flat_skins.append(chroma)
            if 'levels' in skin:
                for level in skin['levels']:
                    if level != None:
                        flat_skins.append(level)
        return flat_skins

    def get_player_store(self):
        r = requests.get(
            f'https://pd.{self.region}.a.pvp.net/store/v2/storefront/{self.user_id}', headers=self.headers)
        
        self.validate_request(r, "Player Store Space")
        jsonData = r.json()
        store_skins = jsonData['SkinsPanelLayout']['SingleItemOffers']
        final_result = [
            skin for skin in self.all_skins if skin['uuid'] in store_skins]
        return final_result

    def validate_request(self, request, origin):
        if request.status_code!= 200:
            raise Exception("Something didn't work in "+origin)
        if "error" in request.json():
            raise Exception("Something didn't work in "+origin +
                            " because :"+request.json()['error'])
