import unittest

from jellydown.utils import format_music_label, music_filename


class MusicUtilsTests(unittest.TestCase):
    def test_music_filename_uses_track_metadata_and_original_extension(self):
        item = {
            "Name": 'Song: Name?',
            "Album": "Best / Album",
            "AlbumArtist": "Artist",
            "IndexNumber": 3,
            "MediaSources": [{"Path": "/music/track.flac"}],
        }

        self.assertEqual(
            music_filename(item),
            "Artist - Best Album - 03 - Song Name.flac",
        )

    def test_music_filename_falls_back_when_metadata_missing(self):
        item = {
            "Name": "Untitled",
            "MediaSources": [{"Container": "mp3"}],
        }

        self.assertEqual(
            music_filename(item),
            "Unknown Artist - Unknown Album - Untitled.mp3",
        )

    def test_format_music_label_includes_artist_album_and_track(self):
        item = {
            "Name": "Track",
            "Album": "Album",
            "Artists": ["Artist"],
            "IndexNumber": 7,
        }

        self.assertEqual(format_music_label(item), "Artist / Album / 07 - Track")


if __name__ == "__main__":
    unittest.main()
