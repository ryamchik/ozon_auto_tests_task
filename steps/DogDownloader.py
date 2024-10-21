import requests

class DogDownloader:
    def __init__(self, breed):
        self.breed = breed
        self.sub_breeds = []
        self.url=f"https://dog.ceo/api/breed/{breed}"

    def get_sub_breeds(self):
        res = requests.get(f'{self.url}/list')
        return res.json().get('message', [])

    def get_urls(self, sub_breeds):
        url_images = []
        if len(sub_breeds) > 0:
            for sub_breed in sub_breeds:
                response = requests.get(f"{self.url}/{sub_breed}/images/random")
                assert response.status_code == 200, response.reason
                sub_breed_urls = response.json().get('message')
                url_images.append(sub_breed_urls)
        else:
            url_images.append(requests.get(f"{self.url}/images/random").json().get('message'))
        return url_images