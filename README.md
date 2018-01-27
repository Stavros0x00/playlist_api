### TODO: Organize it better and add more comments

## Install on linux server

### Basic configurations
    export LANGUAGE=en_US.UTF-8
    export LANG=en_US.UTF-8
    export LC_ALL=en_US.UTF-8
    locale-gen en_US.UTF-8
    dpkg-reconfigure locales

    adduser {YOUR CHOISE OF NAME}
    usermod -aG sudo {YOUR CHOISE OF NAME}

    sudo apt-get install -y ufw
    sudo ufw allow ssh
    sudo ufw allow http
    sudo ufw allow 443/tcp
    sudo ufw --force enable
    sudo ufw status


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
    sudo apt-get install python3-pip
    pip3 install pipenv
    cd /home/playlist_api
    pipenv install
    pipenv install uwsgi



### Postgress

    sudo apt-get update
    sudo apt-get install postgresql postgresql-contrib

    sudo -i -u postgres
    createdb playlist_api

### Elasticsearch

    sudo apt-get update
    # Install java
    sudo apt-get install default-jre
    sudo add-apt-repository ppa:webupd8team/java
    sudo apt-get update
    sudo apt-get install oracle-java8-installer
    sudo apt-get update
    # Current elastic
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.1.2.deb
    sudo dpkg -i elasticsearch-6.1.2.deb
    sudo systemctl enable elasticsearch.service
    # Test
    curl -X GET 'http://localhost:9200'
    # if error check memory of server
    sudo service elasticsearch status
    nano /etc/elasticsearch/jvm.options
    Change or play with the storage https://stackoverflow.com/questions/31677563/connection-refused-error-on-elastic-search:
        -Xms128m
        -Xmx128m



### Security



# Env keys in an .env file
    # Create .env file in /home/playlist_api/ with the env variables below

    * FLASK_APP=run.py
    * SECRET_KEY=
    * DATABASE_URL=postgresql://postgres:{YOUR POSTGRES PASS}@localhost/playlist_api
    * ELASTICSEARCH_URI=http://localhost:9200
    * SENTRY_KEY= (optional)
    * SPOTIPY_CLIENT_ID=
    * SPOTIPY_CLIENT_SECRET=