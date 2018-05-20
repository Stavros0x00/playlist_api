.. Playlist Api documentation master file, created by
   sphinx-quickstart on Sat Jan 13 16:49:32 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Playlist Api's documentation!
========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



.. http:get:: /api/v1/search/tracks/

   The tracks in the database that matches the query. Max 10 tracks with
   the option to chose the number of results with the n argument. Results are ordered
   by relevance.

   **Example request**:

   .. sourcecode:: http

      GET /api/v1/search/tracks/?q=oasis&n=4 HTTP/1.1
      Host: example.com
      Accept: application/json

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      {
        "items": [
          {
            "artist": "Tarja",
            "id": 37237,
            "lastfm_tags": [
              "symphonic metal",
              "female vocalists",
              "Classical",
              "Tarja Turunen",
              "beautiful"
            ],
            "name": "Oasis",
            "preview_url": "https://p.scdn.co/mp3-preview/53a977d65842fa07f7b8081535e579852247d8de?cid=0c0bb28de56d49d3b925f9755a289113",
            "spotify_id": "5hGoIsMmOwF3EsDpp4nwws"
          },
          {
            "artist": "Oasis",
            "id": 10748,
            "lastfm_tags": [
              "britpop",
              "rock",
              "oasis",
              "acoustic",
              "british"
            ],
            "name": "Half The World Away",
            "preview_url": "https://p.scdn.co/mp3-preview/569431423cf0900a40238fb6989995da3ed4f1f2?cid=0c0bb28de56d49d3b925f9755a289113",
            "spotify_id": "6aM4E6WfuoDnPAgaKaZ5hM"
          },
          {
            "artist": "Oasis",
            "id": 16795,
            "lastfm_tags": [
              "britpop",
              "rock",
              "90s",
              "british",
              "oasis"
            ],
            "name": "Don't Look Back in Anger",
            "preview_url": "https://p.scdn.co/mp3-preview/8d5ecd081b86c19a0189462c2222687088a15ed1?cid=0c0bb28de56d49d3b925f9755a289113",
            "spotify_id": "698mT3CTx8JEnp7twwJrGG"
          },
          {
            "artist": "Oasis",
            "id": 16992,
            "lastfm_tags": [
              "rock",
              "britpop",
              "90s",
              "alternative",
              "oasis"
            ],
            "name": "Wonderwall",
            "preview_url": null,
            "spotify_id": "7JrUo70YjhU4S7flcJtK0k"
          }
        ]
      }



   :query q: track name, artist name or both
   :query n: Number of results. Max 10. Default 10.
   :reqheader Accept: application/json
   :resheader Content-Type: application/json
   :statuscode 200: no error
   :statuscode 400: bad request (e.g. wrong request accept type)
   :statuscode 429: exceeded rate limit of 5 requests per second

------------

.. http:get:: /api/v1/similar/

   The similar tracks in the database that matches the spotify id in the url argument. Max 10 tracks with
   the option to chose the number of results with the n argument. Results are ordered
   by score of similarity.

   **Example request**:

   .. sourcecode:: http

      GET /api/v1/similar/?spotify_id=30UTvW5IQWXmvdcZ1zbF6R&n=5 HTTP/1.1
      Host: example.com
      Accept: application/json

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: application/json

      {
        "items": [
          {
            "artist": "Boogie Down Productions",
            "id": 6007,
            "lastfm_tags": [
              "Hip-Hop",
              "Old School Hip Hop",
              "old school",
              "hip hop",
              "rap"
            ],
            "name": "The Bridge Is Over",
            "preview_url": "https://p.scdn.co/mp3-preview/04a97c7c1c8cc89293006d3f4e57aac4ccf824bd?cid=0c0bb28de56d49d3b925f9755a289113",
            "score": 2.7284167729011495,
            "spotify_id": "5jkjpSsMOfsxgdGScPZVq2"
          },
          {
            "artist": "Beastie Boys",
            "id": 6009,
            "lastfm_tags": [
              "Hip-Hop",
              "rap",
              "hip hop",
              "80s",
              "Beastie Boys"
            ],
            "name": "Shake Your Rump",
            "preview_url": null,
            "score": 2.7284167729011495,
            "spotify_id": "4RvprQhj7Ov1SFQ3HfO7FH"
          },
          {
            "artist": "Ice-T",
            "id": 6006,
            "lastfm_tags": [
              "Hip-Hop",
              "rap",
              "old school",
              "west coast",
              "80s"
            ],
            "name": "6 'N The Mornin'",
            "preview_url": "https://p.scdn.co/mp3-preview/0a4e9b835553a99d1b1a4934443fecc1d3a24dd2?cid=0c0bb28de56d49d3b925f9755a289113",
            "score": 1.3642083864505747,
            "spotify_id": "2cBOh97kgDenDOdtKhwU9O"
          },
          {
            "artist": "Schoolly D",
            "id": 6010,
            "lastfm_tags": [
              "hip hop",
              "breakbeat",
              "questions",
              "title is a full sentence",
              "cold case"
            ],
            "name": "P.S.K. 'What Does It Mean'?",
            "preview_url": "https://p.scdn.co/mp3-preview/7f2c402a4d8d53524f4b01a7db9dc41955461e92?cid=0c0bb28de56d49d3b925f9755a289113",
            "score": 1.3642083864505747,
            "spotify_id": "3StKzbpR9dRZB8epDx4KDW"
          }
        ],
        "playlist": {
          "spotify_id": "4PDd58PluSP0lnach9fXX3",
          "url": "https://open.spotify.com/user/6faqhxu4ww7isy9sr96j3o116/playlist/4PDd58PluSP0lnach9fXX3"
        },
        "seed_info": {
          "artist": "De La Soul",
          "id": 6008,
          "lastfm_tags": [
            "Hip-Hop",
            "hip hop",
            "old school",
            "rap",
            "80s"
          ],
          "name": "Me, Myself And I",
          "preview_url": null,
          "spotify_id": "30UTvW5IQWXmvdcZ1zbF6R"
        }
      }




   :query spotify_id: Spotify id of the track
   :query n: Number of results. Max 10. Default 10.
   :query with_spotify_seed: If with_spotify_seed arg specified, the api queries the spotify seed recommendation endpoint. If it finds tracks that we have in the database:

          1) Boosts score of possible common tracks from the graph suggestions
          2) Returns seed_spotify_recommendations items that we have in the database with a max of 20 tracks found.
   :query with_k_neighbors: If with_k_neighbors arg specified, the api queries the k_neighbors model created from spotify track features:

          1) Boosts score of possible common tracks from the graph suggestions
          2) Returns k_neighbors_recommendations items that we have in the database with a max of 20 tracks found.
   :reqheader Accept: application/json
   :resheader Content-Type: application/json
   :statuscode 200: no error
   :statuscode 400: bad request (e.g. wrong request accept type)
   :statuscode 429: exceeded rate limit of 5 requests per minute

.. Indices and tables
.. ==================
..
.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
