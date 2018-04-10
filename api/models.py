# The models of the playlist api. With the help of the sqlalchemy ORM

from sqlalchemy import or_, String
from sqlalchemy.dialects.postgresql import ARRAY

from api import db
from api.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    """
    This mixin class is needed for injecting elastic searching
    functionality to the existing models when needed.
    Credit to chapter 16 of the flask mega tutorial:
    https://learn.miguelgrinberg.com/read/mega-tutorial/ch16.html#cid126

    """
    @classmethod
    def search(cls, expression, page=1, per_page=100):
        """
        The main elastic search method. We have to have the same names for index in elastic and table in db.
        I wont do pagination for now. For now use these default pagination numbers.
        """
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total  # The case is needed for keep the elastic search result score sorting

    @classmethod
    def before_commit(cls, session):
        """
        This method is needed for saving in a dict the change that will go under for
        every object in the session. This dict will be needed after the commit of the
        transaction. A time that the state of every object in the transaction will not be available.
        """
        session._changes = {
            'add': [obj for obj in session.new if isinstance(obj, cls)],
            'update': [obj for obj in session.dirty if isinstance(obj, cls)],
            'delete': [obj for obj in session.deleted if isinstance(obj, cls)]
        }

    @classmethod
    def after_commit(cls, session):
        """
        This method is needed for indexing the changes in the elastic search, right after
        commiting the changes in the db
        """
        for obj in session._changes['add']:
            add_to_index(cls.__tablename__, obj)
        for obj in session._changes['update']:
            add_to_index(cls.__tablename__, obj)
        for obj in session._changes['delete']:
            remove_from_index(cls.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        """
        This method is needed for reindexing every data in the db to the elasticsearh
        """
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


class Track(db.Model, SearchableMixin):
    """
    Creates the track python object representing a track from the database.
    """
    __tablename__ = "tracks"

    __searchable__ = ['artist', 'name']

    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(100), index=True, unique=True, nullable=False)
    musicbrainz_id = db.Column(db.String(100), index=True, unique=True)
    artist = db.Column(db.String(600), index=True, nullable=False)
    name = db.Column(db.String(300), index=True, nullable=False)
    preview_url = db.Column(db.String(600), index=True)
    lastfm_tags = db.Column(ARRAY(String))

    playlists = db.relationship("PlaylistToTrack", back_populates="track")

    def to_dict(self):
        """
        Rest api json representation of the track object
        """
        data = {
            'id': self.id,
            'artist': self.artist,
            'name': self.name,
            'spotify_id': self.spotify_id,
            'preview_url': self.preview_url,
            'lastfm_tags': self.lastfm_tags,
        }
        return data

    def get_neighbors(self):
        """
        Gets the previous and next tracks in playlists it belongs
        """
        neighbors = []
        playlists = self.playlists
        for playlist in playlists:
            order_in_playlist = playlist.order_in_playlist
            neighbors_in_the_playlist = db.session.query(PlaylistToTrack).filter(PlaylistToTrack.playlist_id == playlist.playlist_id,
                                                                                 or_(PlaylistToTrack.order_in_playlist == order_in_playlist - 1,
                                                                                     PlaylistToTrack.order_in_playlist == order_in_playlist + 1)).all()

            for neighbor in neighbors_in_the_playlist:
                neighbors.append(neighbor.track)
        return neighbors

    def __repr__(self):
        return '<Song {} - {} - {}>'.format(self.spotify_id, self.artist, self.name)


# Sqlalchemy event listeners for what to do before and after
# every transaction when quering the db related tracks table
db.event.listen(db.session, 'before_commit', Track.before_commit)
db.event.listen(db.session, 'after_commit', Track.after_commit)


class Playlist(db.Model):
    """
    Creates the playlist python object representing a playlist from the database.
    """
    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(100), index=True, unique=True, nullable=False)
    playlist_user = db.Column(db.String(200), index=True, nullable=False)
    tracks = db.relationship("PlaylistToTrack", back_populates="playlist")

    def __repr__(self):
        return '<Playlist {}>'.format(self.spotify_id)


class PlaylistToTrack(db.Model):
    """
    Creates the playlist to track association object with the corresponding order of the truck inside the playlist.
    """
    __tablename__ = "playlist_to_track"

    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), primary_key=True, autoincrement=False)
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), primary_key=True, autoincrement=False)
    order_in_playlist = db.Column(db.Integer)

    track = db.relationship(Track, back_populates="playlists")
    playlist = db.relationship(Playlist, back_populates="tracks")

    def __repr__(self):
        return '<PlaylistToTrack {}, {}, {}>'.format(self.playlist_id, self.track_id, self.order_in_playlist)
