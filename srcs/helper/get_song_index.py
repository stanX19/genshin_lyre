from classes import *

def get_song_index(txt: str):
    sorted_songs = list(Songs.songs)
    sorted_songs.sort(key=len)
    for song_name in sorted_songs:
        if song_name in txt:
            index = list(Songs.songs).index(song_name)
            return index

    index = first_int(txt)

    if isinstance(index, int):
        index -= 1
        return index
    return None