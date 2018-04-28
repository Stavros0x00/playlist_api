
### Basic configurations on linux server
    # Logged in as root

    # Update the system
    apt-get update
    apt-get upgrade

    # Config locale related settings (to remove locale warnings):
    export LANGUAGE=en_US.UTF-8
    export LANG=en_US.UTF-8
    export LC_ALL=en_US.UTF-8
    locale-gen en_US.UTF-8
    dpkg-reconfigure locales

    # Add, config new user and login as him
    adduser playlistapi
    usermod -aG sudo playlistapi
    su - playlistapi

    # Config firewall
    sudo apt-get install -y ufw
    sudo ufw allow ssh
    sudo ufw allow http
    sudo ufw allow 443/tcp
    sudo ufw --force enable
    sudo ufw status



### Install and Config Postgres
    # Update and install necessary software
    sudo apt-get update
    sudo apt-get install postgresql postgresql-contrib

    # Login as postgres and config the db. Then exit back to previous user
    sudo -i -u postgres
    createdb playlist_api
    createdb test_database # For testing reasons
    psql
    alter user postgres password 'YOUR POSTGRES PASS';
    \q
    exit

### Install and Config Elasticsearch

    # Install java related requirements
    sudo apt-get update
    sudo apt-get install default-jre
    sudo add-apt-repository ppa:webupd8team/java
    sudo apt-get update
    sudo apt-get install oracle-java8-installer
    sudo apt-get update

    # Download and Install current elastic (See current version here: https://www.elastic.co/downloads/elasticsearch )
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.2.3.deb
    sudo dpkg -i elasticsearch-6.2.3.deb

    # Config
    sudo nano /etc/elasticsearch/elasticsearch.yml
    Change: network.host: 0.0.0.0

    sudo systemctl enable elasticsearch.service
    sudo systemctl start elasticsearch

    # Test if it works. (If not see below)
    curl -X GET 'http://localhost:9200'

    # If error, check memory of the server. Change it to apropriate level following the steps below
    sudo service elasticsearch status
    sudo nano /etc/elasticsearch/jvm.options
    (Change the size of the storage https://stackoverflow.com/questions/31677563/connection-refused-error-on-elastic-search)
        e.g.
        -Xms1g --> -Xms128m
        -Xms1g --> -Xmx128m
    sudo systemctl restart elasticsearch


### Install and Config the Project
    # Clone the project from git
    cd /home/playlistapi
    git clone https://github.com/Stavros0x00/playlist_api.git

    # Install python 3.6 and related packages:
    sudo add-apt-repository ppa:jonathonf/python-3.6
    sudo apt-get update
    sudo apt-get install build-essential python3-dev python3.6 python3.6-dev python3-setuptools python-dev graphviz libgraphviz-dev pkg-config python-pygraphviz

    #  Install pipenv and needed python packages for the project
    sudo apt-get install python3-pip
    sudo pip3 install pipenv
    cd /home/playlistapi/playlist_api
    pipenv install

    # Needed Enviroment keys in an .env file
    # Create .env file in /home/playlistapi/playlist_api with the env variables below
    * FLASK_APP=run.py
    * SECRET_KEY=(YOUR APP SECRET KEY HERE)
    * DATABASE_URL=postgresql://postgres:{YOUR POSTGRES PASS}@localhost:5432/playlist_api
    * TEST_DATABASE_URL=postgresql://postgres:{YOUR POSTGRES PASS}@localhost:5432/test_database
    * ELASTICSEARCH_URI=http://localhost:9200
    * SENTRY_KEY= (optional)
    * SPOTIPY_CLIENT_ID=
    * SPOTIPY_CLIENT_SECRET=
    * LAST_FM_API_KEY=
    * LAST_FM_SHARED_SECRET=
    * MAIL_USERNAME=
    * MAIL_PASSWORD=

    # Run the virtual enviroment. And populate the database creating the schema and running the necessary scripts.
    pipenv shell
    flask db upgrade
    mkdir /home/playlistapi/playlist_api/api/pickled_files/
    python scripts/crawl_playlists.py
    python scripts/sync_db_elastic.py
    python scripts/track_features.py

    # Config uwsgi
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

    enable-threads = true
    die-on-term = true' > playlist_api.ini


    sudo nano /etc/systemd/system/playlist_api.service
    (Copy the below lines in the created file and save)
    (Where the lines for the virtual enviroment, replace with yours location)
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

### Install and Config the Nginx Server
    # Install nginx
    sudo apt-get update
    sudo apt-get install nginx

    # Config nginx
    sudo nano /etc/nginx/sites-available/playlist_api
    (Copy the below lines in the created file and save)
    (Replace the server_domain_or_IP with appropriate ip or hostname)
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



