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

.. Indices and tables
.. ==================
..
.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
