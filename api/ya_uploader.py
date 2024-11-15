import requests


class YaUploader:
    def __init__(self, request):
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources'
        self.token = request.config.getoption("--token")
        self.headers = {'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        'Authorization': f'OAuth {self.token}'}

    def create_folder(self, path):
        requests.put(f'{self.url}?path={path}', headers=self.headers)

    def get_folder(self, name):
        return requests.get(f'{self.url}?path=/{name}', headers=self.headers)

    def upload_photos_to_yd(self, path, url_file, name):
        url = f"{self.url}/upload"
        params = {
            "path": f'/{path}/{name}',
            'url': url_file, "overwrite": "true"
        }
        requests.post(url, headers=self.headers, params=params)

    def delete_folder(self, name):
        requests.delete(f'{self.url}?path=/{name}', headers=self.headers)
