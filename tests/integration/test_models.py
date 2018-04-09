# Test models functions

from api import db
from api.models import Track, Playlist, PlaylistToTrack


def test_track_to_dict(app):
    track = Track(spotify_id='3y4ztntXFUI9PYwIcOLbMX',
                  artist='The Bones of J.R. Jones',
                  name="St. James' bed")
    db.session.add(track)
    db.session.commit()

    track_info = track.to_dict()
    assert 'spotify_id' in track_info
    assert 'artist' in track_info
    assert 'name' in track_info
    assert 'preview_url' in track_info
    assert 'lastfm_tags' in track_info


def test_track_get_neighbors(app):
    track1 = Track(spotify_id='07HF5tFmwh6ahN93JC6LmE',
                  artist='Kyuss',
                  name='Space Cadet')
    db.session.add(track1)
    db.session.commit()
    track2 = Track(spotify_id='6QgjcU0zLnzq5OrUoSZ3OK',
                   artist='Portugal. The Man',
                   name='Feel It Still')
    db.session.add(track2)
    db.session.commit()
    track3 = Track(spotify_id='1i8oOEZKBzaxnEmcZYAYCQ',
                   artist='Frenic',
                   name='Travel Alone')
    db.session.add(track3)
    db.session.commit()

    playlist = Playlist(spotify_id='testrandom123',
                        playlist_user='testrandomuser')
    db.session.add(playlist)
    db.session.commit()

    tracks = [track1, track2, track3]
    for index, track in enumerate(tracks):
        playlist_to_track = PlaylistToTrack(order_in_playlist=index)
        playlist_to_track.track = track
        with db.session.no_autoflush:
            playlist.tracks.append(playlist_to_track)
        db.session.commit()

    neighbors = track2.get_neighbors()
    assert neighbors[0].spotify_id == track1.spotify_id
    assert neighbors[1].spotify_id == track3.spotify_id
