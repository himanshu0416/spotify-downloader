#write unit tests for the spotify_downloader function
import json
import re
import requests
import signal
import sys
import traceback
from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from time import sleep
import unittest
from spotify_dl import spotify_downloader

def test_spotify_downloader():

    test_urls = [
        'https://open.spotify.com/album/5AivaZj0CiQJoDWqVH2pbh?si=8596f077d1c54870'
    ]

    with unittest.mock.patch('builtins.input', side_effect=test_urls):
        broken_tracks = spotify_downloader(True, None, None, None, None)

    assert not broken_tracks

    pass

#<<<<<<<<<<<<<<  ✨ Codeium Command ⭐ >>>>>>>>>>>>>>>>

class TestSpotifyDl(unittest.TestCase):

    def test_get_tracks_to_download(self):

        with unittest.mock.patch('builtins.input', side_effect=['https://open.spotify.com/album/5AivaZj0CiQJoDWqVH2pbh?si=8596f077d1c54870', '']):
            tracks_to_dl = get_tracks_to_download(True, None)

        self.assertEqual(tracks_to_dl, [('5AivaZj0CiQJoDWqVH2pbh', 'The 1975 - Sleep')])


    def test_set_output_dir(self):

        with unittest.mock.patch('builtins.input', side_effect=['test_output_dir', '']):
            output_dir = set_output_dir(True, None, True)

        self.assertEqual(output_dir, Path('test_output_dir'))


    def test_download_track(self):

        with unittest.mock.patch('spotify_dl.download_file') as mock_download_file:
            download_track('5AivaZj0CiQJoDWqVH2pbh', 'The 1975 - Sleep', Path('test_output_dir'), True, False)

        mock_download_file.assert_called_once_with(
            'https://api.spotify.com/v1/tracks/5AivaZj0CiQJoDWqVH2pbh/audio-analysis',
            Path('test_output_dir/The 1975 - Sleep.json'),
            'The 1975 - Sleep'
        )


    def test_download_all_tracks(self):

        test_urls = [
            'https://open.spotify.com/album/5AivaZj0CiQJoDWqVH2pbh?si=8596f077d1c54870',
            'https://open.spotify.com/album/5AivaZj0CiQJoDWqVH2pbh?si=8596f077d1c54870'
        ]

        with unittest.mock.patch('builtins.input', side_effect=test_urls + ['']):
            broken_tracks = download_all_tracks(
                [('5AivaZj0CiQJoDWqVH2pbh', 'The 1975 - Sleep')],
                Path('test_output_dir'),
                True,
                False
            )

        self.assertEqual(broken_tracks, [])


    def test_main(self):

        with unittest.mock.patch('builtins.print') as mock_print:
            with unittest.mock.patch('builtins.input', side_effect=['https://open.spotify.com/album/5AivaZj0CiQJoDWqVH2pbh?si=8596f077d1c54870', '']):
                main()

        self.assertEqual(
            mock_print.mock_calls,
            [
                unittest.mock.call('', '=' * 48, '||          Spotify Song Downloader           ||', '=' * 48, sep='\n', end='\n\n'),
                unittest.mock.call("\nTracks to download: 1\n"),
                unittest.mock.call(f"\nDownloading to '{Path('.').absolute()}'.\n"),
                unittest.mock.call('-' * 32),
                unittest.mock.call(f"[1/1] The 1975 - Sleep"),
                unittest.mock.call("\nAll done.\n")
            ]
        )

    def test_get_spotify_playlist(self):

        with unittest.mock.patch('builtins.input', side_effect=['https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoBJRG?si=625202094e004c5b', '']):
            playlist_data = get_spotify_playlist(True, None)

        self.assertEqual(
            playlist_data,
            {
                'playlistName': 'The 1975 - A Brief Inquiry into Online Relationships',
                'trackList': [
                    SpotifySong(
                        title='The 1975 - High',
                        artist='The 1975',
                        album='A Brief Inquiry into Online Relationships',
                        id='37i9dQZF1DX4WYpdgoBJRG'
                    )
                ]
            }
        )

    def test_get_playlist_data(self):
        playlist_data = get_playlist_data('37i9dQZF1DX4WYpdgoBJRG')

        self.assertEqual(
            playlist_data,
            {
                'artist': 'The 1975',
                'description': 'The 1975 - A Brief Inquiry into Online Relationships',
                'playlistId': '37i9dQZF1DX4WYpdgoBJRG',
                'playlistName': 'The 1975 - A Brief Inquiry into Online Relationships',
                'success': True,
                'trackList': [
                    SpotifySong(
                        album='A Brief Inquiry into Online Relationships',
                        artist='The 1975',
                        id='37i9dQZF1DX4WYpdgoBJRG',
                        title='The 1975 - High'
                    )
                ]
            }
        )
    
