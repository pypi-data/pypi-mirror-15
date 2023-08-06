from simplestruct import Struct, TypedField

class PlaylistSignature(Struct):
    playlist_id = TypedField(str)
    name = TypedField(str)
    length = TypedField(int)
    author = TypedField(str)
    thumbnail = TypedField(str)
    first_video_id = TypedField(str)

    @property
    def url(self):
        return 'https://www.youtube.com/playlist?list=' + self.playlist_id

    @property
    def first_video_url(self):
        return 'https://www.youtube.com/watch?v={0}&list={1}'.format(self.first_video_id, self.playlist_id)
