import time
import pytest
from api.dog_downloader import DogDownloader
from api.ya_uploader import YaUploader
from utils.name_splitter import split_name


@pytest.mark.parametrize('breed', ['doberman', 'bulldog', 'collie', 'spaniel'])
def test_proverka_upload_dog(breed, request):
    dog_client = DogDownloader(breed)
    yandex_client = YaUploader(request)
    folder_name = 'test_folder'
    sub_breeds = dog_client.get_sub_breeds()
    urls = dog_client.get_urls(sub_breeds)
    yandex_client.create_folder(folder_name)
    for url in urls:
        yandex_client.upload_photos_to_yd(folder_name, url, split_name(url))

    time.sleep(5)
    response = yandex_client.get_folder(folder_name)
    response_json = response.json()

    assert response.status_code == 200, response.reason
    assert response_json.get('type') == "dir", "Тип ответа не совпал"
    assert response_json.get('name') == "test_folder", \
        f"Наименование директории: {folder_name} не совпадает"
    answer_check = 1 if len(sub_breeds) == 0 else len(sub_breeds)
    items = response_json.get('_embedded').get('items')
    assert len(items) == answer_check, \
        "Кол-во фото не совпадает с кол-вом пород"
    for item in items:
        assert item.get('type') == 'file', "Тип файла не совпал"
        assert item.get('name').startswith(breed), \
            f"Наименование файла не совпадает с {breed}"

    yandex_client.delete_folder(folder_name)
