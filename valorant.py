import urllib.parse

import requests


class ValorantAPI(object):
    access_token = None
    cookies = None
    entitlements_token = None
    player_store = None

    def __init__(self, username, password, region, client_ip):
        self.username = username
        self.password = password
        self.region = region
        self.client_ip = client_ip

        self.cookies = self.get_cookies()

        self.access_token = self.get_access_token()

        self.entitlements_token = self.get_entitlements_token()

        self.user_info, self.game_name = self.get_user_info()

        self.all_skins = self.get_skins()

        self.player_store = self.get_player_store()

    def get_cookies(self):
        data = {
            'client_id': 'play-valorant-web-prod',
            'nonce': '1',
            'redirect_uri': 'https://playvalorant.com/',
            'response_type': 'token id_token',
            'scope': 'account openid',
        }
        headers = {
            'X-Forwarded-For': self.client_ip
        }
        r = requests.post(
            'https://auth.riotgames.com/api/v1/authorization', headers=headers, json=data)
        self.validate_request(r, "Cookie Space")
        cookies = r.cookies

        return cookies

    def get_access_token(self):
        data = {
            'type': 'auth',
            'username': self.username,
            'password': self.password
        }
        headers = {
            'X-Forwarded-For': self.client_ip
        }
        r = requests.put('https://auth.riotgames.com/api/v1/authorization',
                         headers=headers, json=data, cookies=self.cookies)
        self.validate_request(r, "Access Token Space")
        uri = r.json()['response']['parameters']['uri']
        jsonUri = urllib.parse.parse_qs(uri)

        access_token = jsonUri['https://playvalorant.com/#access_token'][0]

        return access_token

    def get_entitlements_token(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'X-Forwarded-For': self.client_ip
        }
        r = requests.post('https://entitlements.auth.riotgames.com/api/token/v1',
                          headers=headers, json={}, cookies=self.cookies)
        self.validate_request(r, "Entitlment Token Space")

        entitlements_token = r.json()['entitlements_token']

        return entitlements_token

    def get_user_info(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'X-Forwarded-For': self.client_ip
        }

        r = requests.post('https://auth.riotgames.com/userinfo',
                          headers=headers, json={}, cookies=self.cookies)
        self.validate_request(r, "User Info Space")
        jsonData = r.json()
        user_info = jsonData['sub']
        name = jsonData['acct']['game_name']
        tag = jsonData['acct']['tag_line']
        game_name = name + ' #' + tag

        return user_info, game_name

    def get_match_history(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'X-Riot-Entitlements-JWT': f'{self.entitlements_token}',
            'X-Forwarded-For': self.client_ip,
            'X-Riot-ClientPlatform': "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"
        }
        r = requests.get(
            f'https://pd.{self.region}.a.pvp.net/mmr/v1/players/{self.user_info}/competitiveupdates?startIndex=0&endIndex=20', headers=headers, cookies=self.cookies)

        jsonData = r.json()

        return jsonData

    def get_player_store(self):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'X-Riot-Entitlements-JWT': f'{self.entitlements_token}',
            'X-Forwarded-For': self.client_ip,
        }
        r = requests.get(
            f'https://pd.{self.region}.a.pvp.net/store/v2/storefront/{self.user_info}', headers=headers, cookies=self.cookies)
        self.validate_request(r, "Player Store Space")
        jsonData = r.json()
        store_skins = jsonData['SkinsPanelLayout']['SingleItemOffers']
        final_result = [
            skin for skin in self.all_skins if skin['uuid'] in store_skins]
        return final_result

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

    def validate_request(self, request, origin):
        if "error" in request.json():
            raise Exception("Something didn't work in "+origin +
                            " because :"+request.json()['error'])
