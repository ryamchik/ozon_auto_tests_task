import pytest
import time
from steps.DogDownloader import DogDownloader
from steps.YaUploader import YaUploader
from utils.name_splitter import split_name


@pytest.mark.parametrize('breed', ['doberman', 'bulldog', 'collie'])
def test_proverka_upload_dog(breed, request):
    dog_client = DogDownloader(breed)
    yandex_client = YaUploader(request)
    folder_name = 'test_folder'
    sub_breeds = dog_client.get_sub_breeds()
    urls = dog_client.get_urls(sub_breeds)
    yandex_client.delete_folder(folder_name)
    time.sleep(2)  # добавлен таймер, для ожидания полного удаления папки
    yandex_client.create_folder(folder_name)
    for url in urls:
        yandex_client.upload_photos_to_yd(folder_name, url, split_name(url))
    time.sleep(2)  # добавлен таймер для ожидания добавления всех файлов в папку
    response = yandex_client.get_folder(folder_name)
    assert response.status_code == 200, response.reason
    assert response.json()['type'] == "dir", "Тип ответа не совпал"
    assert response.json()['name'] == "test_folder", f"Наименование директории: {folder_name} не совпадает"
    answer_check = 1 if len(sub_breeds) == 0 else len(sub_breeds)
    assert len(response.json()['_embedded']['items']) == answer_check, "Кол-во фото не совпадает с кол-вом пород"
    for item in response.json()['_embedded']['items']:
        assert item['type'] == 'file', "Тип файла не совпал"
        assert item['name'].startswith(breed), f"Наименование файла не совпадает с {breed}"
