# View functions for every api endpoint

from api import app


@app.route('/api/v1/songs', methods=['GET'])
def songs():
    return "songs"
