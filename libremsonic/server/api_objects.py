"""
WARNING: AUTOGENERATED FILE
This file was generated by the api_object_generator.py script. Do
not modify this file directly, rather modify the script or run it on
a new API version.
"""

from datetime import datetime
from typing import List
from enum import Enum
from libremsonic.server.api_object import APIObject


class AlbumInfo(APIObject):
    notes: List[str]
    musicBrainzId: List[str]
    lastFmUrl: List[str]
    smallImageUrl: List[str]
    mediumImageUrl: List[str]
    largeImageUrl: List[str]
    value: str


class AverageRating(APIObject, float):
    pass


class MediaType(APIObject, Enum):
    MUSIC = 'music'
    PODCAST = 'podcast'
    AUDIOBOOK = 'audiobook'
    VIDEO = 'video'


class UserRating(APIObject, int):
    pass


class Child(APIObject):
    id: str
    value: str
    parent: str
    isDir: bool
    title: str
    album: str
    artist: str
    track: int
    year: int
    genre: str
    coverArt: str
    size: int
    contentType: str
    suffix: str
    transcodedContentType: str
    transcodedSuffix: str
    duration: int
    bitRate: int
    path: str
    isVideo: bool
    userRating: UserRating
    averageRating: AverageRating
    playCount: int
    discNumber: int
    created: datetime
    starred: datetime
    albumId: str
    artistId: str
    type: MediaType
    bookmarkPosition: int
    originalWidth: int
    originalHeight: int


class AlbumList(APIObject):
    album: List[Child]
    value: str


class AlbumID3(APIObject):
    id: str
    value: str
    name: str
    artist: str
    artistId: str
    coverArt: str
    songCount: int
    duration: int
    playCount: int
    created: datetime
    starred: datetime
    year: int
    genre: str


class AlbumList2(APIObject):
    album: List[AlbumID3]
    value: str


class AlbumWithSongsID3(APIObject):
    song: List[Child]
    value: str
    id: str
    name: str
    artist: str
    artistId: str
    coverArt: str
    songCount: int
    duration: int
    playCount: int
    created: datetime
    starred: datetime
    year: int
    genre: str


class Artist(APIObject):
    id: str
    value: str
    name: str
    artistImageUrl: str
    starred: datetime
    userRating: UserRating
    averageRating: AverageRating


class ArtistInfoBase(APIObject):
    biography: List[str]
    musicBrainzId: List[str]
    lastFmUrl: List[str]
    smallImageUrl: List[str]
    mediumImageUrl: List[str]
    largeImageUrl: List[str]
    value: str


class ArtistInfo(APIObject):
    similarArtist: List[Artist]
    value: str
    biography: List[str]
    musicBrainzId: List[str]
    lastFmUrl: List[str]
    smallImageUrl: List[str]
    mediumImageUrl: List[str]
    largeImageUrl: List[str]


class ArtistID3(APIObject):
    id: str
    value: str
    name: str
    coverArt: str
    artistImageUrl: str
    albumCount: int
    starred: datetime


class ArtistInfo2(APIObject):
    similarArtist: List[ArtistID3]
    value: str
    biography: List[str]
    musicBrainzId: List[str]
    lastFmUrl: List[str]
    smallImageUrl: List[str]
    mediumImageUrl: List[str]
    largeImageUrl: List[str]


class ArtistWithAlbumsID3(APIObject):
    album: List[AlbumID3]
    value: str
    id: str
    name: str
    coverArt: str
    artistImageUrl: str
    albumCount: int
    starred: datetime


class IndexID3(APIObject):
    artist: List[ArtistID3]
    value: str
    name: str


class ArtistsID3(APIObject):
    index: List[IndexID3]
    value: str
    ignoredArticles: str


class Bookmark(APIObject):
    entry: List[Child]
    value: str
    position: int
    username: str
    comment: str
    created: datetime
    changed: datetime


class Bookmarks(APIObject):
    bookmark: List[Bookmark]
    value: str


class ChatMessage(APIObject):
    username: str
    value: str
    time: int
    message: str


class ChatMessages(APIObject):
    chatMessage: List[ChatMessage]
    value: str


class Directory(APIObject):
    child: List[Child]
    value: str
    id: str
    parent: str
    name: str
    starred: datetime
    userRating: UserRating
    averageRating: AverageRating
    playCount: int


class Error(APIObject):
    code: int
    value: str
    message: str


class Genre(APIObject):
    songCount: int
    value: str
    albumCount: int


class Genres(APIObject):
    genre: List[Genre]
    value: str


class Index(APIObject):
    artist: List[Artist]
    value: str
    name: str


class Indexes(APIObject):
    shortcut: List[Artist]
    index: List[Index]
    child: List[Child]
    value: str
    lastModified: int
    ignoredArticles: str


class InternetRadioStation(APIObject):
    id: str
    value: str
    name: str
    streamUrl: str
    homePageUrl: str


class InternetRadioStations(APIObject):
    internetRadioStation: List[InternetRadioStation]
    value: str


class JukeboxStatus(APIObject):
    currentIndex: int
    value: str
    playing: bool
    gain: float
    position: int


class JukeboxPlaylist(APIObject):
    entry: List[Child]
    value: str
    currentIndex: int
    playing: bool
    gain: float
    position: int


class License(APIObject):
    valid: bool
    value: str
    email: str
    licenseExpires: datetime
    trialExpires: datetime


class Lyrics(APIObject):
    artist: str
    value: str
    title: str


class MusicFolder(APIObject):
    id: int
    value: str
    name: str


class MusicFolders(APIObject):
    musicFolder: List[MusicFolder]
    value: str


class PodcastStatus(APIObject, Enum):
    NEW = 'new'
    DOWNLOADING = 'downloading'
    COMPLETED = 'completed'
    ERROR = 'error'
    DELETED = 'deleted'
    SKIPPED = 'skipped'


class PodcastEpisode(APIObject):
    streamId: str
    channelId: str
    description: str
    status: PodcastStatus
    publishDate: datetime
    value: str
    id: str
    parent: str
    isDir: bool
    title: str
    album: str
    artist: str
    track: int
    year: int
    genre: str
    coverArt: str
    size: int
    contentType: str
    suffix: str
    transcodedContentType: str
    transcodedSuffix: str
    duration: int
    bitRate: int
    path: str
    isVideo: bool
    userRating: UserRating
    averageRating: AverageRating
    playCount: int
    discNumber: int
    created: datetime
    starred: datetime
    albumId: str
    artistId: str
    type: MediaType
    bookmarkPosition: int
    originalWidth: int
    originalHeight: int


class NewestPodcasts(APIObject):
    episode: List[PodcastEpisode]
    value: str


class NowPlayingEntry(APIObject):
    username: str
    minutesAgo: int
    playerId: int
    playerName: str
    value: str
    id: str
    parent: str
    isDir: bool
    title: str
    album: str
    artist: str
    track: int
    year: int
    genre: str
    coverArt: str
    size: int
    contentType: str
    suffix: str
    transcodedContentType: str
    transcodedSuffix: str
    duration: int
    bitRate: int
    path: str
    isVideo: bool
    userRating: UserRating
    averageRating: AverageRating
    playCount: int
    discNumber: int
    created: datetime
    starred: datetime
    albumId: str
    artistId: str
    type: MediaType
    bookmarkPosition: int
    originalWidth: int
    originalHeight: int


class NowPlaying(APIObject):
    entry: List[NowPlayingEntry]
    value: str


class PlayQueue(APIObject):
    entry: List[Child]
    value: str
    current: int
    position: int
    username: str
    changed: datetime
    changedBy: str


class Playlist(APIObject):
    allowedUser: List[str]
    value: str
    id: str
    name: str
    comment: str
    owner: str
    public: bool
    songCount: int
    duration: int
    created: datetime
    changed: datetime
    coverArt: str


class PlaylistWithSongs(APIObject):
    entry: List[Child]
    value: str
    allowedUser: List[str]
    id: str
    name: str
    comment: str
    owner: str
    public: bool
    songCount: int
    duration: int
    created: datetime
    changed: datetime
    coverArt: str


class Playlists(APIObject):
    playlist: List[Playlist]
    value: str


class PodcastChannel(APIObject):
    episode: List[PodcastEpisode]
    value: str
    id: str
    url: str
    title: str
    description: str
    coverArt: str
    originalImageUrl: str
    status: PodcastStatus
    errorMessage: str


class Podcasts(APIObject):
    channel: List[PodcastChannel]
    value: str


class ResponseStatus(APIObject, Enum):
    OK = 'ok'
    FAILED = 'failed'


class ScanStatus(APIObject):
    scanning: bool
    value: str
    count: int


class SearchResult(APIObject):
    match: List[Child]
    value: str
    offset: int
    totalHits: int


class SearchResult2(APIObject):
    artist: List[Artist]
    album: List[Child]
    song: List[Child]
    value: str


class SearchResult3(APIObject):
    artist: List[ArtistID3]
    album: List[AlbumID3]
    song: List[Child]
    value: str


class Share(APIObject):
    entry: List[Child]
    value: str
    id: str
    url: str
    description: str
    username: str
    created: datetime
    expires: datetime
    lastVisited: datetime
    visitCount: int


class Shares(APIObject):
    share: List[Share]
    value: str


class SimilarSongs(APIObject):
    song: List[Child]
    value: str


class SimilarSongs2(APIObject):
    song: List[Child]
    value: str


class Songs(APIObject):
    song: List[Child]
    value: str


class Starred(APIObject):
    artist: List[Artist]
    album: List[Child]
    song: List[Child]
    value: str


class Starred2(APIObject):
    artist: List[ArtistID3]
    album: List[AlbumID3]
    song: List[Child]
    value: str


class TopSongs(APIObject):
    song: List[Child]
    value: str


class User(APIObject):
    folder: List[int]
    value: str
    username: str
    email: str
    scrobblingEnabled: bool
    maxBitRate: int
    adminRole: bool
    settingsRole: bool
    downloadRole: bool
    uploadRole: bool
    playlistRole: bool
    coverArtRole: bool
    commentRole: bool
    podcastRole: bool
    streamRole: bool
    jukeboxRole: bool
    shareRole: bool
    videoConversionRole: bool
    avatarLastChanged: datetime


class Users(APIObject):
    user: List[User]
    value: str


class Version(APIObject, str):
    pass


class AudioTrack(APIObject):
    id: str
    value: str
    name: str
    languageCode: str


class Captions(APIObject):
    id: str
    value: str
    name: str


class VideoConversion(APIObject):
    id: str
    value: str
    bitRate: int
    audioTrackId: int


class VideoInfo(APIObject):
    captions: List[Captions]
    audioTrack: List[AudioTrack]
    conversion: List[VideoConversion]
    value: str
    id: str


class Videos(APIObject):
    video: List[Child]
    value: str


class Response(APIObject):
    musicFolders: MusicFolders
    indexes: Indexes
    directory: Directory
    genres: Genres
    artists: ArtistsID3
    artist: ArtistWithAlbumsID3
    album: AlbumWithSongsID3
    song: Child
    videos: Videos
    videoInfo: VideoInfo
    nowPlaying: NowPlaying
    searchResult: SearchResult
    searchResult2: SearchResult2
    searchResult3: SearchResult3
    playlists: Playlists
    playlist: PlaylistWithSongs
    jukeboxStatus: JukeboxStatus
    jukeboxPlaylist: JukeboxPlaylist
    license: License
    users: Users
    user: User
    chatMessages: ChatMessages
    albumList: AlbumList
    albumList2: AlbumList2
    randomSongs: Songs
    songsByGenre: Songs
    lyrics: Lyrics
    podcasts: Podcasts
    newestPodcasts: NewestPodcasts
    internetRadioStations: InternetRadioStations
    bookmarks: Bookmarks
    playQueue: PlayQueue
    shares: Shares
    starred: Starred
    starred2: Starred2
    albumInfo: AlbumInfo
    artistInfo: ArtistInfo
    artistInfo2: ArtistInfo2
    similarSongs: SimilarSongs
    similarSongs2: SimilarSongs2
    topSongs: TopSongs
    scanStatus: ScanStatus
    error: Error
    value: str
    status: ResponseStatus
    version: Version
