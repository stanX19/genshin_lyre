try:
    from ...classes import *
    from ...utils import *
except ImportError:
    from classes import *
    from utils import *

def print_stats(no):
    """print stats of a given song index"""
    FILE = list(Songs.songs.values())[no]
    song_name = list(Songs.songs)[no]

    if isinstance(FILE, old_music_score):
        if type(FILE) == music_score:
            score_list = key_list_to_score_list(FILE.keys)
            song_length = sum([length for length in score_list if isinstance(length,float)])
            if song_length >= 60:
                song_length = f"{math.floor(song_length / 60)}m {round(song_length % 60)}s"
            else:
                song_length = f"{round(song_length)}s"
        else:
            score_list = key_list_to_score_list([i for key in FILE.keys for i in [key,"-"]])
            song_length = sum([length for length in score_list if isinstance(length, float)])
            if song_length >= 60:
                song_length = f"{math.floor(song_length / 60)}m {round(song_length % 60)}s"
            else:
                song_length = f"{round(song_length)}s"

        print(f"""    STATS FOR {song_name}:
      TYPE      : txt score
      LENGTH    : {song_length}
      KEY NODES : {len(FILE.key_nodes)}
      CLASS     : {type(FILE).__name__}
      SAVED AS  : {song_name}.txt
    """)
    elif isinstance(FILE, Midi):
        print(FILE)
    elif isinstance(FILE, Nightly):
        print(FILE)