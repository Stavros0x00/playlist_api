## Install on linux server

    export LANGUAGE=en_US.UTF-8
    export LANG=en_US.UTF-8
    export LC_ALL=en_US.UTF-8
    locale-gen en_US.UTF-8
    dpkg-reconfigure locales


### uWSGI and Nginx
    sudo apt-get update
    sudo apt-get install python3-pip python3-dev nginx



### Project
    # Git
    cd /home
    git clone https://github.com/Stavros0x00/playlist_api.git

    # Install python 3.6:
    sudo add-apt-repository ppa:jonathonf/python-3.6
    sudo apt-get update
    sudo apt-get install python3.6

    #  Install pipenv
    apt install python3-pip
    pip3 install pipenv
    cd /home/playlist_api
    pipenv install



### Postgress

    sudo apt-get update
    sudo apt-get install postgresql postgresql-contrib

    sudo -i -u postgres
    createdb playlist_api

### Elasticsearch

    sudo apt-get update


### Security



# Env keys in an .env file
    * FLASK_APP=run.py
    * SECRET_KEY
    * DATABASE_URL
    * ELASTICSEARCH_URI
    * SENTRY_KEY (optional)
    * SPOTIPY_CLIENT_ID
    * SPOTIPY_CLIENT_SECRETexport LANGUAGE=en_US.UTF-8