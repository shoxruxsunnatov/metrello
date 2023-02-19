import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()


class TrelloManager:
    trello_api_key = os.environ.get('TRELLO_KEY')
    trello_token = os.environ.get('TRELLO_TOKEN')

    def __init__(self, username):
        self.username = username

    @staticmethod
    def base_header():
        return {
            "Accept": "application/json"
        }

    @staticmethod
    def get_list_id_with_name(list_id, name):
        try:
            return [data.get('name') for data in list_id if name == data.get('name')][0]
        except Exception as e:
            print(e)

    @staticmethod
    def get_list_id_with_name_for_add_member(list_data, name):
        try:
            return [data.get("id") for data in list_data if data.get("name") == name][0]
        except Exception as e:
            print(e)

    def credentials(self):
        return {
            "key": self.trello_api_key,
            'token': self.trello_token
        }

    def get_member_id(self):
        url = f"https://api.trello.com/1/members/{self.username}"

        response = requests.request(
            'GET',
            url,
            headers=self.base_header(),
            params=self.credentials()
        )
        if response.status_code == 200:
            return json.loads(response.text)

    def get_board(self):

        url = f"https://api.trello.com/1/members/{self.username}/boards"

        response = requests.request(
            'GET',
            url,
            headers=self.base_header(),
            params=self.credentials()
        )
        if response.status_code == 200:
            return json.loads(response.text)


    def create_new_list(self, board_id, list_name):

        url = f"https://api.trello.com/1/boards/{board_id}/lists"

        response = requests.request(
            'POST',
            url,
            headers=self.base_header(),
            params={
                **self.credentials(),
                'name': list_name,
                'pos': 'top'
            }
        )
        if response.status_code == 200:
            return True


    def get_list_on_a_board(self, board_id):

        url = f'https://api.trello.com/1/boards/{board_id}/lists'

        response = requests.request(
            'GET',
            url,
            headers=self.base_header(),
            params=self.credentials()
        )

        if response.status_code == 200:
            return json.loads(response.text)

    def get_board_members(self, board_id):
        url = f"https://api.trello.com/1/boards/{board_id}/memberships"
        response = requests.request(
            "GET",
            url,
            headers=self.base_header(),
            params=self.credentials()
        )

        if response.status_code == 200:
            return json.loads(response.text)

    def get_cards_on_a_list(self, list_id):
        url = f"https://api.trello.com/1/lists/{list_id}/cards"

        response = requests.request(
            "GET",
            url,
            headers=self.base_header(),
            params=self.credentials()
        )
        if response.status_code == 200:
            return json.loads(response.text)

    def get_members_fullname_by_id_member(self, members_id):

        url = f"https://api.trello.com/1/members/{members_id}"

        response = requests.request(
            "GET",
            url,
            headers=self.base_header(),
            params=self.credentials()
        )

        if response.status_code == 200:
            return json.loads(response.text)

    def create_new_card(self, param):
        url = f'https://api.trello.com/1/cards'
        print(param)
        param.update(self.credentials())

        response = requests.request(
            "POST",
            url,
            headers=self.base_header(),
            params=param
        )
        if response.status_code == 200:
            return json.loads(response.text)
