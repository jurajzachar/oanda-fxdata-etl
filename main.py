import logging
from flask import Flask
from oanda_filesystem import *
app = Flask(__name__)

@app.route("/healthcheck")
def healthcheck():
    return "healthy"

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

    # discover files in dir and dump them to db
    persistence = Persistence()
    fx_folder = '/oxygen/oanda-streams'
    for file in list_in_dir(fx_folder):
        logging.info("saving '%s' to the db", join(fx_folder, file))
        persistence.upsert_to_db(folder=fx_folder, filename=file)

    #dispose of persistent connection
    persistence.__del__()

    app.run(host='0.0.0.0', port=8080)