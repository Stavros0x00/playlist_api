### TODO: Organize it better and add more comments

## Install on linux server

### Basic configurations
    apt-get update
    apt-get upgrade
    export LANGUAGE=en_US.UTF-8
    export LANG=en_US.UTF-8
    export LC_ALL=en_US.UTF-8
    locale-gen en_US.UTF-8
    dpkg-reconfigure locales

    adduser playlistapi
    usermod -aG sudo playlistapi
    su - playlistapi

    sudo apt-get install -y ufw
    sudo ufw allow ssh
    sudo ufw allow http
    sudo ufw allow 443/tcp
    sudo ufw --force enable
    sudo ufw status



### Postgress

    sudo apt-get update
    sudo apt-get install postgresql postgresql-contrib

    sudo -i -u postgres
    createdb playlist_api
    psql
    alter user postgres password '<YOUR POSTGRES PASS>';
    \q
    exit

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
    sudo nano /etc/elasticsearch/elasticsearch.yml
    Change network.host: 0.0.0.0
    sudo systemctl enable elasticsearch.service
    sudo systemctl start elasticsearch
    # Test
    curl -X GET 'http://localhost:9200'
    # if error check memory of server
    sudo service elasticsearch status
    sudo nano /etc/elasticsearch/jvm.options
    Change or play with the storage https://stackoverflow.com/questions/31677563/connection-refused-error-on-elastic-search:
        -Xms1g --> -Xms128m
        -Xms1g --> -Xmx128m
    sudo systemctl restart elasticsearch



### Project
    # Git
    cd /home/playlistapi
    git clone https://github.com/Stavros0x00/playlist_api.git

    # Install python 3.6:
    sudo add-apt-repository ppa:jonathonf/python-3.6
    sudo apt-get update
    sudo apt-get install python3.6
    sudo apt-get install python3.6-dev

    #  Install pipenv
    sudo apt-get install python3-pip
    pip3 install pipenv
    cd /home/playlistapi/playlist_api
    pipenv install
    # pipenv install uwsgi

    # Env keys in an .env file
    # Create .env file in /home/playlist_api/ with the env variables below

    * FLASK_APP=run.py
    * SECRET_KEY=
    * DATABASE_URL=postgresql://postgres:{YOUR POSTGRES PASS}@localhost:5432/playlist_api
    * ELASTICSEARCH_URI=http://localhost:9200
    * SENTRY_KEY= (optional)
    * SPOTIPY_CLIENT_ID=
    * SPOTIPY_CLIENT_SECRET=
    pipenv shell
    flask db upgrade
    python scripts/crawl_playlists.py
    python scripts/sync_db_elastic.py

    touch playlist_api.sock
    touch uwsgi.log
    echo '[uwsgi]
        module = run:app

        master = true
        processes = 5

        socket = playlist_api.sock
        chmod-socket = 660
        vacuum = true
        logto = /home/playlistapi/playlist_api/uwsgi.log
        for-readline = /home/playlistapi/playlist_api/.env
          env = %(_)
        endfor =

        die-on-term = true' > playlist_api.ini
        enable-threads = true

    sudo nano /etc/systemd/system/playlist_api.service
    copy # This needs to have guide for the venv directory
    [Unit]
    Description=uWSGI instance to serve myproject
    After=network.target

    [Service]
    User=playlistapi
    Group=www-data
    WorkingDirectory=/home/playlistapi/playlist_api
    Environment="PATH=/home/playlistapi/.local/share/virtualenvs/playlist_api-KjQVwPM-/bin"
    ExecStart=/home/playlistapi/.local/share/virtualenvs/playlist_api-KjQVwPM-/bin/uwsgi --ini playlist_api.ini

    [Install]
    WantedBy=multi-user.target

    sudo systemctl start playlist_api
    sudo systemctl enable playlist_api

    sudo systemctl restart playlist_api

### Nginx
    sudo apt-get update
    sudo apt-get install python3-pip python3-dev nginx

    sudo nano /etc/nginx/sites-available/playlist_api

    server {
        listen 80;
        server_name server_domain_or_IP;
        location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/playlistapi/playlist_api/playlist_api.sock;
    }

    }
    sudo ln -s /etc/nginx/sites-available/playlist_api /etc/nginx/sites-enabled
    sudo nginx -t
    sudo systemctl restart nginx
    sudo ufw allow 'Nginx Full'



### Security



