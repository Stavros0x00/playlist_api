from api import db


playlist_to_track = db.Table('playlist_to_track',
                             db.Column('playlist_id', db.Integer, db.ForeignKey('playlists.id'), primary_key=True),
                             db.Column('track_id', db.Integer, db.ForeignKey('tracks.id'), primary_key=True)
                             )

class Track(db.Model):
    __tablename__ = "tracks"
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(100), index=True, unique=True)
    musicbrainz_id = db.Column(db.String(100), index=True, unique=True)
    artist = db.Column(db.String(100), index=True)
    name = db.Column(db.String(100), index=True)

    playlists = db.relationship('Playlist', secondary=playlist_to_track,
                                backref=db.backref('tracks', lazy='dynamic'),
                                lazy='dynamic'
                                )

    def __repr__(self):
        return '<Song {} - {} - {}>'.format(self.spotify_id, self.artist, self.name)


class Playlist(db.Model):
    __tablename__ = "playlists"
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(100), index=True, unique=True)


    def __repr__(self):
        return '<Playlist {}>'.format(self.spotify_id)




