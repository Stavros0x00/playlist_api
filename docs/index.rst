.. Playlist Api documentation master file, created by
   sphinx-quickstart on Sat Jan 13 16:49:32 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Playlist Api's documentation!
========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



.. http:get:: /users/(int:user_id)/posts/(tag)

   The posts tagged with `tag` that the user (`user_id`) wrote.

   **Example request**:

   .. sourcecode:: http

      GET /api/v1/search/songs?q=oasis&n=4 HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/javascript

      [
        {
          "post_id": 12345,
          "author_id": 123,
          "tags": ["server", "web"],
          "subject": "I tried Nginx"
        },
        {
          "post_id": 12346,
          "author_id": 123,
          "tags": ["html5", "standards", "web"],
          "subject": "We go to HTML 5"
        }
      ]

   :query sort: one of ``hit``, ``created-at``
   :query offset: offset number. default is 0
   :query limit: limit number. default is 30
   :reqheader Accept: the response content type depends on
                      :mailheader:`Accept` header
   :reqheader Authorization: optional OAuth token to authenticate
   :resheader Content-Type: this depends on :mailheader:`Accept`
                            header of request
   :statuscode 200: no error
   :statuscode 404: there's no user

.. Indices and tables
.. ==================
..
.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
