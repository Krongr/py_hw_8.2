from pprint import pprint
import requests


def get_token_from_file(file_name='ya_token.txt') -> str:
    """Возвращает авторизационный токен сохраненный в отдельном файле 'file_name'."""
    with open(file_name, 'rt', encoding='utf-8') as file:
        return file.read().strip()


class YaDiskUploader:

    def __init__(self, token):
        self.token = token

    def create_headers(self) -> dict:
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def get_upload_link(self, ya_disk_file_path) -> dict:
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.create_headers()        
        params = {"path": ya_disk_file_path, "overwrite": "true"}
        return requests.get(upload_url, headers=headers, params=params).json()

    def upload_file_to_disk(self, local_file_path, filename, ya_disk_file_path):
        href = self.get_upload_link(ya_disk_file_path).get("href")
        response = requests.put(href, data=open(local_file_path + filename, 'rb'))
        response.raise_for_status()
        if response.status_code:
            print("Success")


if __name__ == '__main__':
    local_file_path = 'D:\\!for_upload\\'

    uploader = YaDiskUploader(get_token_from_file())

    uploader.upload_file_to_disk(local_file_path, 'test.txt', 'netology_hw/test.txt')
