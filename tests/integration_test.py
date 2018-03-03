import requests
import filecmp
from file_storage.Minifile import Minifile

based_uri = "http://0.0.0.0:5000/minifilebox/api/v1/files"

file_1 = 'image1.jpg'
file_2 = 'image2.jpg'
file_3 = 'image3.jpg'


file_db = {}


def upload_file(file_name):
    files = {'file': (file_name, open(file_name, 'rb'))}
    response = requests.request("POST", based_uri + '/upload', files=files)

    # Validating response
    assert response.status_code == 200

    minifile = Minifile().from_json(response.json())
    #print("UPLOAD FILE %s - %s" % (file_name, minifile.to_json()))

    assert minifile.file_id
    assert minifile.file_name == file_name

    return minifile


def download_file(file_id, new_file_name):
    url = based_uri + "/download/" + file_id

    headers = {
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers)
    assert response.status_code == 200

    open(new_file_name, 'wb').write(response.content)
    #print("DOWNLOADED FILE %s" % file_id)


def delete_file(file_id):
    url = based_uri + "/delete/" + file_id

    headers = {
        'cache-control': "no-cache",
    }

    response = requests.request("DELETE", url, headers=headers)
    assert response.status_code == 200

    minifile = Minifile().from_json(response.json())
    #print('DELETE FILE %s - %s' % (file_id, minifile.to_json()))

    return minifile


def list_files():
    headers = {
        'cache-control': "no-cache",
    }

    response = requests.request("GET", based_uri, headers=headers)
    #print(response.json())

    # Validating response
    assert response.status_code == 200

    l = response.json()
    #print('LIST FILE: %s' % l)
    return [Minifile().from_json(s) for s in l]


print("Test %s running" % __file__)

# Check if no files exists
assert len(list_files()) == 0

# Upload one file
minifile = upload_file(file_1)
file_db[minifile.file_name] = minifile

# Upload second file
minifile = upload_file(file_2)
file_db[minifile.file_name] = minifile

# Upload third file
minifile = upload_file(file_3)
file_db[minifile.file_name] = minifile

# Getting list of files
file_list = list_files()

# Validating if all the files are returned
for file in file_list:
    assert file.file_name in file_db


# download file: let take one file
new_file_1 = 'new_' + file_1

download_file(file_db[file_1].file_id, new_file_1)
assert filecmp.cmp(file_1, new_file_1)

# download file: let take one file
new_file_2 = 'new_' + file_2

download_file(file_db[file_2].file_id, new_file_2)
assert filecmp.cmp(file_2, new_file_2)

# download file: let take one file
new_file_3 = 'new_' + file_3

download_file(file_db[file_3].file_id, new_file_3)
assert filecmp.cmp(file_3, new_file_3)

# delete all files
for mf in file_db.values():
    minifile = delete_file(mf.file_id)
    assert minifile == mf

# Check if no files exists
assert len(list_files()) == 0

print("Test %s OK" %__file__)
