.. Playlist Api documentation master file, created by
   sphinx-quickstart on Sat Jan 13 16:49:32 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Playlist Api's documentation!
========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



.. http:get:: /api/v1/search/songs/

   The songs in the database that matches the query. Max 10 songs with
   the option to chose the number of results with the n argument. Results are ordered
   by relevance.

   **Example request**:

   .. sourcecode:: http

      GET /api/v1/search/songs/?q=oasis&n=4 HTTP/1.1
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
            "id": 23073,
            "name": "Oasis",
            "spotify_id": "5hGoIsMmOwF3EsDpp4nwws"
          },
          {
            "artist": "Oasis",
            "id": 14202,
            "name": "Champagne Supernova - Remastered",
            "spotify_id": "40bynawzslg9U7ACq07fAj"
          },
          {
            "artist": "Oasis",
            "id": 17552,
            "name": "Wonderwall",
            "spotify_id": "7JrUo70YjhU4S7flcJtK0k"
          },
          {
            "artist": "Oasis",
            "id": 20476,
            "name": "Live Forever",
            "spotify_id": "0ZyrgDl8C0Cq9Gt3nPxqvd"
          }
        ]
      }


   :query q: song name, artist name or both
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
