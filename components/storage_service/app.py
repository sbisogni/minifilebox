from flask import Flask


app = Flask(__name_)


@app.route(config.MINIFILEBOX_BASE_URI + '/files/upload', methods=['POST'])
def upload_file():
    """
    :return:
    """
    pass

