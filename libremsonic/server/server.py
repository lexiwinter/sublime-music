import math
from deprecated import deprecated
from typing import Any, Optional, Dict, List, Union, Iterator
from datetime import datetime

import requests

from .api_objects import (
    AlbumInfo,
    AlbumList,
    AlbumList2,
    AlbumWithSongsID3,
    ArtistInfo,
    ArtistsID3,
    ArtistWithAlbumsID3,
    Child,
    Directory,
    Genres,
    Indexes,
    License,
    MusicFolders,
    NowPlaying,
    Playlists,
    PlaylistWithSongs,
    Response,
    SearchResult,
    SearchResult2,
    SearchResult3,
    Starred,
    Starred2,
    Songs,
    VideoInfo,
)


class Server:
    """Defines a *Sonic server."""

    def __init__(self, name: str, hostname: str, username: str, password: str):
        # TODO handle these optionals better.
        self.name: str = name
        self.hostname: str = hostname
        self.username: str = username
        self.password: str = password

    def _get_params(self) -> Dict[str, str]:
        """See Subsonic API Introduction for details."""
        return dict(
            u=self.username,
            p=self.password,
            c='LibremSonic',
            f='json',
            v='1.15.0',
        )

    def _make_url(self, endpoint: str) -> str:
        return f'{self.hostname}/rest/{endpoint}.view'

    def _subsonic_error_to_exception(self, error):
        return Exception(f'{error.code}: {error.message}')

    def _post(self, url, **params) -> Response:
        """
        Make a post to a *Sonic REST API. Handle all types of errors including
        *Sonic ``<error>`` responses.

        :returns: a Response containing all of the data of the
            response, deserialized
        :raises Exception: needs some work TODO
        """
        params = {**self._get_params(), **params}
        result = requests.post(url, data=params)
        # TODO make better
        if result.status_code != 200:
            raise Exception(f'Fail! {result.status_code}')

        subsonic_response = result.json()['subsonic-response']

        # TODO make better
        if not subsonic_response:
            raise Exception('Fail!')

        # Debug
        # TODO: logging
        print(subsonic_response)

        response = Response.from_json(subsonic_response)

        # Check for an error and if it exists, raise it.
        if response.get('error'):
            raise self._subsonic_error_to_exception(response.error)

        return response

    def _stream(self, url, **params) -> Iterator[Any]:
        """
        Stream a file.
        """
        params = {**self._get_params(), **params}
        result = requests.post(url, data=params, stream=True)
        # TODO make better
        if result.status_code != 200:
            raise Exception(f'Fail! {result.status_code}')

        content_type = result.headers.get('Content-Type', '')

        if 'application/json' in content_type:
            # Error occurred
            subsonic_response = result.json()['subsonic-response']

            # TODO make better
            if not subsonic_response:
                raise Exception('Fail!')

            response = Response.from_json(subsonic_response)
            raise self._subsonic_error_to_exception(response.error)
        else:
            return result.iter_content(chunk_size=1024)

    def ping(self) -> Response:
        """
        Used to test connectivity with the server.
        """
        return self._post(self._make_url('ping'))

    def get_license(self) -> License:
        """
        Get details about the software license.
        """
        result = self._post(self._make_url('getLicense'))
        return result.license

    def get_music_folders(self) -> MusicFolders:
        """
        Returns all configured top-level music folders.
        """
        result = self._post(self._make_url('getMusicFolders'))
        return result.musicFolders

    def get_indexes(
            self,
            music_folder_id: int = None,
            if_modified_since: int = None,
    ) -> Indexes:
        """
        Returns an indexed structure of all artists.

        :param music_folder_id: If specified, only return artists in the music
            folder with the given ID. See ``getMusicFolders``.
        :param if_modified_since: If specified, only return a result if the
            artist collection has changed since the given time (in milliseconds
            since 1 Jan 1970).
        """
        result = self._post(self._make_url('getIndexes'),
                            musicFolderId=music_folder_id,
                            ifModifiedSince=if_modified_since)
        return result.indexes

    def get_music_directory(self, dir_id) -> Directory:
        """
        Returns a listing of all files in a music directory. Typically used
        to get list of albums for an artist, or list of songs for an album.

        :param dir_id: A string which uniquely identifies the music folder.
            Obtained by calls to ``getIndexes`` or ``getMusicDirectory``.
        """
        result = self._post(self._make_url('getMusicDirectory'),
                            id=str(dir_id))
        return result.directory

    def get_genres(self) -> Genres:
        """
        Returns all genres.
        """
        result = self._post(self._make_url('getGenres'))
        return result.genres

    def get_artists(self, music_folder_id: int = None) -> ArtistsID3:
        """
        Similar to getIndexes, but organizes music according to ID3 tags.

        :param music_folder_id: If specified, only return artists in the music
            folder with the given ID. See ``getMusicFolders``.
        """
        result = self._post(self._make_url('getArtists'),
                            musicFolderId=music_folder_id)
        return result.artists

    def get_artist(self, artist_id: int) -> ArtistWithAlbumsID3:
        """
        Returns details for an artist, including a list of albums. This method
        organizes music according to ID3 tags.

        :param artist_id: The artist ID.
        """
        result = self._post(self._make_url('getArtist'), id=artist_id)
        return result.artist

    def get_album(self, album_id: int) -> AlbumWithSongsID3:
        """
        Returns details for an album, including a list of songs. This method
        organizes music according to ID3 tags.

        :param album_id: The album ID.
        """
        result = self._post(self._make_url('getAlbum'), id=album_id)
        return result.album

    def get_song(self, song_id: int) -> Child:
        """
        Returns details for a song.

        :param song_id: The song ID.
        """
        result = self._post(self._make_url('getSong'), id=song_id)
        return result.song

    def get_videos(self) -> Optional[List[Child]]:
        """
        Returns all video files.
        """
        result = self._post(self._make_url('getVideos'))
        return result.videos.video

    def get_video_info(self, video_id: int) -> Optional[VideoInfo]:
        """
        Returns details for a video, including information about available
        audio tracks, subtitles (captions) and conversions.

        :param video_id: The video ID.
        """
        result = self._post(self._make_url('getVideoInfo'), id=video_id)
        return result.videoInfo

    def get_artist_info(
            self,
            id: int,
            count: int = None,
            include_not_present: bool = None,
    ) -> Optional[ArtistInfo]:
        """
        Returns artist info with biography, image URLs and similar artists,
        using data from last.fm.

        :param id: The artist, album, or song ID.
        :param count: Max number of similar artists to return. Defaults to 20,
            according to API Spec.
        :param include_not_present: Whether to return artists that are not
            present in the media library. Defaults to false according to API
            Spec.
        """
        result = self._post(
            self._make_url('getArtistInfo'),
            id=id,
            count=count,
            includeNotPresent=include_not_present,
        )
        return result.artistInfo

    def get_artist_info2(
            self,
            id: int,
            count: int = None,
            include_not_present: bool = None,
    ) -> Optional[ArtistInfo]:
        """
        Similar to getArtistInfo, but organizes music according to ID3 tags.

        :param id: The artist, album, or song ID.
        :param count: Max number of similar artists to return. Defaults to 20,
            according to API Spec.
        :param include_not_present: Whether to return artists that are not
            present in the media library. Defaults to false according to API
            Spec.
        """
        result = self._post(
            self._make_url('getArtistInfo2'),
            id=id,
            count=count,
            includeNotPresent=include_not_present,
        )
        return result.artistInfo

    def get_album_info(self, id: int) -> Optional[AlbumInfo]:
        """
        Returns album notes, image URLs etc, using data from last.fm.

        :param id: The album or song ID.
        """
        result = self._post(self._make_url('getAlbumInfo'), id=id)
        return result.albumInfo

    def get_album_info2(self, id: int) -> Optional[AlbumInfo]:
        """
        Similar to getAlbumInfo, but organizes music according to ID3 tags.

        :param id: The album or song ID.
        """
        result = self._post(self._make_url('getAlbumInfo2'), id=id)
        return result.albumInfo

    def get_similar_songs(self, id: int, count: int = None) -> List[Child]:
        """
        Returns a random collection of songs from the given artist and similar
        artists, using data from last.fm. Typically used for artist radio
        features.

        :param id: The artist, album or song ID.
        :param count: Max number of songs to return. Defaults to 50 according
            to API Spec.
        """
        result = self._post(
            self._make_url('getSimilarSongs'),
            id=id,
            count=count,
        )
        return result.similarSongs.song

    def get_similar_songs2(self, id: int, count: int = None) -> List[Child]:
        """
        Similar to getSimilarSongs, but organizes music according to ID3 tags.

        :param id: The artist, album or song ID.
        :param count: Max number of songs to return. Defaults to 50 according
            to API Spec.
        """
        result = self._post(
            self._make_url('getSimilarSongs2'),
            id=id,
            count=count,
        )
        return result.similarSongs2.song

    def get_top_songs(self, artist: str, count: int = None) -> List[Child]:
        """
        Returns top songs for the given artist, using data from last.fm.

        :param id: The artist name.
        :param count: Max number of songs to return. Defaults to 50 according
            to API Spec.
        """
        result = self._post(
            self._make_url('getTopSongs'),
            artist=artist,
            count=count,
        )
        return result.topSongs.song

    def get_album_list(
            self,
            type: str,
            size: int = None,
            offset: int = None,
            from_year: int = None,
            to_year: int = None,
            genre: str = None,
            music_folder_id: int = None,
    ) -> AlbumList:
        """
        Returns a list of random, newest, highest rated etc. albums. Similar to
        the album lists on the home page of the Subsonic web interface.

        :param type: The list type. Must be one of the following: ``random``,
            ``newest``, ``highest``, ``frequent``, ``recent``. Since 1.8.0 you
            can also use ``alphabeticalByName`` or ``alphabeticalByArtist`` to
            page through all albums alphabetically, and ``starred`` to retrieve
            starred albums.  Since 1.10.1 you can use ``byYear`` and
            ``byGenre`` to list albums in a given year range or genre.
        :param size: The number of albums to return. Max 500. Deafult is 10
            according to API Spec.
        :param offset: The list offset. Useful if you for example want to page
            through the list of newest albums. Default is 0 according to API
            Spec.
        :param from_year: Required if ``type`` is ``byYear``. The first year in
            the range. If ``fromYear > toYear`` a reverse chronological list is
            returned.
        :param to_year: Required if ``type`` is ``byYear``. The last year in
            the range.
        :param genre: Required if ``type`` is ``byGenre``. The name of the
            genre, e.g., "Rock".
        :param music_folder_id: (Since 1.11.0) Only return albums in the music
            folder with the given ID. See ``getMusicFolders``.
        """
        result = self._post(
            self._make_url('getAlbumList'),
            type=type,
            size=size,
            offset=offset,
            fromYear=from_year,
            toYear=to_year,
            genre=genre,
            musicFolderId=music_folder_id,
        )
        return result.albumList

    def get_album_list2(
            self,
            type: str,
            size: int = None,
            offset: int = None,
            from_year: int = None,
            to_year: int = None,
            genre: str = None,
            music_folder_id: int = None,
    ) -> AlbumList2:
        """
        Similar to getAlbumList, but organizes music according to ID3 tags.

        :param type: The list type. Must be one of the following: ``random``,
            ``newest``, ``frequent``, ``recent``, ``starred``,
            ``alphabeticalByName`` or ``alphabeticalByArtist``. Since 1.10.1
            you can use ``byYear`` and ``byGenre`` to list albums in a given
            year range or genre.
        :param size: The number of albums to return. Max 500. Deafult is 10
            according to API Spec.
        :param offset: The list offset. Useful if you for example want to page
            through the list of newest albums. Default is 0 according to API
            Spec.
        :param from_year: Required if ``type`` is ``byYear``. The first year in
            the range. If ``fromYear > toYear`` a reverse chronological list is
            returned.
        :param to_year: Required if ``type`` is ``byYear``. The last year in
            the range.
        :param genre: Required if ``type`` is ``byGenre``. The name of the
            genre, e.g., "Rock".
        :param music_folder_id: (Since 1.11.0) Only return albums in the music
            folder with the given ID. See ``getMusicFolders``.
        """
        result = self._post(
            self._make_url('getAlbumList2'),
            type=type,
            size=size,
            offset=offset,
            fromYear=from_year,
            toYear=to_year,
            genre=genre,
            musicFolderId=music_folder_id,
        )
        return result.albumList2

    def get_random_songs(
            self,
            size: int = None,
            genre: str = None,
            from_year: str = None,
            to_year: str = None,
            music_folder_id: int = None,
    ) -> Songs:
        """
        Returns random songs matching the given criteria.

        :param size: The maximum number of songs to return. Max 500. Defaults
            to 10 according to API Spec.
        :param genre: Only returns songs belonging to this genre.
        :param from_year: Only return songs published after or in this year.
        :param to_year: Only return songs published before or in this year.
        :param music_folder_id: Only return albums in the music folder with the
            given ID. See ``getMusicFolders``.
        """
        result = self._post(
            self._make_url('getRandomSongs'),
            size=size,
            genre=genre,
            fromYear=from_year,
            toYear=to_year,
            musicFolderId=music_folder_id,
        )
        return result.randomSongs

    def get_songs_by_genre(
            self,
            genre: str,
            count: int = None,
            offset: int = None,
            music_folder_id: int = None,
    ) -> Songs:
        """
        Returns songs in a given genre.

        :param genre: Only returns songs belonging to this genre.
        :param count: The maximum number of songs to return. Max 500. Defaults
            to 10 according to API Spec.
        :param offset: The offset. Useful if you want to page through the songs
            in a genre.
        :param music_folder_id: (Since 1.12.0) Only return albums in the music
            folder with the given ID. See ``getMusicFolders``.
        """
        result = self._post(
            self._make_url('getSongsByGenre'),
            genre=genre,
            count=count,
            offset=offset,
            musicFolderId=music_folder_id,
        )
        return result.songsByGenre

    def get_now_playing(self) -> NowPlaying:
        """
        Returns what is currently being played by all users. Takes no extra
        parameters.
        """
        result = self._post(self._make_url('getNowPlaying'))
        return result.nowPlaying

    def get_starred(self, music_folder_id: int = None) -> Starred:
        """
        Returns starred songs, albums and artists.

        :param music_folder_id: (Since 1.12.0) Only return results from the
            music folder with the given ID. See ``getMusicFolders``.
        """
        result = self._post(self._make_url('getStarred'))
        return result.starred

    def get_starred2(self, music_folder_id: int = None) -> Starred2:
        """
        Similar to getStarred, but organizes music according to ID3 tags.

        :param music_folder_id: (Since 1.12.0) Only return results from the
            music folder with the given ID. See ``getMusicFolders``.
        """
        result = self._post(self._make_url('getStarred2'))
        return result.starred2

    @deprecated(version='1.4.0', reason='You should use search2 instead.')
    def search(
            self,
            artist: str = None,
            album: str = None,
            title: str = None,
            any: str = None,
            count: int = None,
            offset: int = None,
            newer_than: datetime = None,
    ) -> SearchResult:
        """
        Returns a listing of files matching the given search criteria. Supports
        paging through the result.

        :param artist: Artist to search for.
        :param album: Album to searh for.
        :param title: Song title to search for.
        :param any: Searches all fields.
        :param count: Maximum number of results to return.
        :param offset: Search result offset. Used for paging.
        :param newer_than: Only return matches that are newer than this.
        """
        result = self._post(
            self._make_url('search'),
            artist=artist,
            album=album,
            title=title,
            any=any,
            count=count,
            offset=offset,
            newerThan=math.floor(newer_than.timestamp() *
                                 1000) if newer_than else None,
        )
        return result.searchResult

    def search2(
            self,
            query: str,
            artist_count: int = None,
            artist_offset: int = None,
            album_count: int = None,
            album_offset: int = None,
            song_count: int = None,
            song_offset: int = None,
            music_folder_id: int = None,
    ) -> SearchResult2:
        """
        Returns albums, artists and songs matching the given search criteria.
        Supports paging through the result.

        :param query: Search query.
        :param artist_count: Maximum number of artists to return. Defaults to
            20 according to API Spec.
        :param artist_offset: Search result offset for artists. Used for
            paging. Defualts to 0 according to API Spec.
        :param album_count: Maximum number of albums to return. Defaults to 20
            according to API Spec.
        :param album_offset: Search result offset for albums. Used for paging.
            Defualts to 0 according to API Spec.
        :param song_count: Maximum number of songs to return. Defaults to 20
            according to API Spec.
        :param song_offset: Search result offset for songs. Used for paging.
            Defualts to 0 according to API Spec.
        :param music_folder_id: (Since 1.12.0) Only return results from the
            music folder with the given ID. See ``getMusicFolders``.
        """
        result = self._post(
            self._make_url('search2'),
            query=query,
            artistCount=artist_count,
            artistOffset=artist_offset,
            albumCount=album_count,
            albumOffset=album_offset,
            songCount=song_count,
            songOffset=song_offset,
            musicFolderId=music_folder_id,
        )
        return result.searchResult2

    def search3(
            self,
            query: str,
            artist_count: int = None,
            artist_offset: int = None,
            album_count: int = None,
            album_offset: int = None,
            song_count: int = None,
            song_offset: int = None,
            music_folder_id: int = None,
    ) -> SearchResult3:
        """
        Similar to search2, but organizes music according to ID3 tags.

        :param query: Search query.
        :param artist_count: Maximum number of artists to return. Defaults to
            20 according to API Spec.
        :param artist_offset: Search result offset for artists. Used for
            paging. Defualts to 0 according to API Spec.
        :param album_count: Maximum number of albums to return. Defaults to 20
            according to API Spec.
        :param album_offset: Search result offset for albums. Used for paging.
            Defualts to 0 according to API Spec.
        :param song_count: Maximum number of songs to return. Defaults to 20
            according to API Spec.
        :param song_offset: Search result offset for songs. Used for paging.
            Defualts to 0 according to API Spec.
        :param music_folder_id: (Since 1.12.0) Only return results from the
            music folder with the given ID. See ``getMusicFolders``.
        """
        result = self._post(
            self._make_url('search3'),
            query=query,
            artistCount=artist_count,
            artistOffset=artist_offset,
            albumCount=album_count,
            albumOffset=album_offset,
            songCount=song_count,
            songOffset=song_offset,
            musicFolderId=music_folder_id,
        )
        return result.searchResult3

    def get_playlists(self, username: str = None) -> Playlists:
        """
        Returns all playlists a user is allowed to play.

        :param username: (Since 1.8.0) If specified, return playlists for this
            user rather than for the authenticated user. The authenticated user
            must have admin role if this parameter is used.
        """
        result = self._post(self._make_url('getPlaylists'), username=username)
        return result.playlists

    def get_playlist(self, id: int = None) -> PlaylistWithSongs:
        """
        Returns a listing of files in a saved playlist.

        :param username: ID of the playlist to return, as obtained by
            ``getPlaylists``.
        """
        result = self._post(self._make_url('getPlaylist'), id=id)
        return result.playlist

    def create_playlist(
            self,
            playlist_id: int = None,
            name: str = None,
            song_id: Union[int, List[int]] = None,
    ) -> Union[PlaylistWithSongs, Response]:
        """
        Creates (or updates) a playlist.

        :param playlist_id: The playlist ID. Required if updating.
        :param name: The human-readable name of the playlist. Required if
            creating.
        :param song_id: ID(s) of a song in the playlist. Can be a single ID or
            a list of IDs.
        """
        result = self._post(
            self._make_url('createPlaylist'),
            playlistId=playlist_id,
            name=name,
            songId=song_id,
        )

        if result.playlist:
            return result.playlist
        else:
            return result

    def update_playlist(
            self,
            playlist_id: int,
            name: str = None,
            comment: str = None,
            public: bool = None,
            song_id_to_add: Union[int, List[int]] = None,
            song_index_to_remove: Union[int, List[int]] = None,
    ) -> Response:
        """
        Updates a playlist. Only the owner of a playlist is allowed to update
        it.

        :param playlist_id: The playlist ID. Required if updating.
        :param name: The human-readable name of the playlist.
        :param comment: The playlist comment.
        :param public: ``true`` if the playlist should be visible to all users,
            ``false`` otherwise.
        :param song_id_to_add: Add this song with this ID to the playlist.
            Multiple parameters allowed.
        :param song_id_to_remove: Remove the song at this position in the
            playlist. Multiple parameters allowed.
        """
        return self._post(
            self._make_url('updatePlaylist'),
            playlistId=playlist_id,
            name=name,
            comment=comment,
            public=public,
            songIdToAdd=song_id_to_add,
            songIdToRemove=song_index_to_remove,
        )

    def delete_playlist(self, id: int) -> Response:
        """
        Deletes a saved playlist
        """
        return self._post(self._make_url('deletePlaylist'), id=id)

    def stream(
            self,
            id: str,
            max_bit_rate: int = None,
            format: str = None,
            time_offset: int = None,
            size: int = None,
            estimate_content_length: bool = False,
            converted: bool = False,
    ):
        """
        Streams a given file.

        :param id: A string which uniquely identifies the file to stream.
            Obtained by calls to ``getMusicDirectory``.
        :param maxBitRate: (Since 1.2.0) If specified, the server will attempt
            to limit the bitrate to this value, in kilobits per second. If set
            to zero, no limit is imposed.
        :param format: (Since 1.6.0) Specifies the preferred target format
            (e.g., "mp3" or "flv") in case there are multiple applicable
            transcodings. Starting with 1.9.0 you can use the special value
            "raw" to disable transcoding.
        :param timeOffset: Only applicable to video streaming. If specified,
            start streaming at the given offset (in seconds) into the video.
            Typically used to implement video skipping.
        :param size: (Since 1.6.0) Only applicable to video streaming.
            Requested video size specified as WxH, for instance "640x480".
        :param estimateContentLength: (Since 1.8.0). If set to ``True``, the
            *Content-Length* HTTP header will be set to an estimated value for
            transcoded or downsampled media. Defaults to False according to the
            API Spec.
        :param converted: (Since 1.14.0) Only applicable to video streaming.
            Subsonic can optimize videos for streaming by converting them to
            MP4. If a conversion exists for the video in question, then setting
            this parameter to ``True`` will cause the converted video to be
            returned instead of the original. Defaults to False according to
            the API Spec.
        """
        # TODO make this a decent object
        return self._stream(
            self._make_url('stream'),
            id=id,
            maxBitRate=max_bit_rate,
            format=format,
            timeOffset=time_offset,
            size=size,
            estimateContentLength=estimate_content_length,
            converted=converted,
        )

    def download(self, id: str):
        """
        Downloads a given media file. Similar to stream, but this method
        returns the original media data without transcoding or downsampling.

        :param id: A string which uniquely identifies the file to stream.
            Obtained by calls to ``getMusicDirectory``.
        """
        # TODO make this a decent object
        return self._post(self._make_url('stream'), id=id)
