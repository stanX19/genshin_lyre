try:
    from ...classes import *
    from ...utils import *
except ImportError:
    from classes import *
    from utils import *

def print_stats(no):
    """No return, print stats of a given song index"""
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
        score_list = [val for val in FILE.to_score_list() if type(val) == float]
        total_length = sum(score_list)
        if total_length > 60:
            song_length = f"{math.floor(total_length / 60)}m {round(total_length % 60)}s"
        else:
            song_length = f"{round(total_length)}s"
        lowest_sharp, total_key = FILE.tune_to_C()
        percentage = round(lowest_sharp / total_key * 100, 1)
        if lowest_sharp > 0:
            suitability = f"lowest sharp is {lowest_sharp} out of {total_key} keys"
            if percentage > 0:
                suitability += f" -{percentage}%-, score may sound weird"
        else:
            suitability = "midi is tuned to C"
        print(f"""    STATS FOR {song_name}:
      TYPE        : Midi file
      SAVED AS    : {song_name}.mid
      LENGTH      : {song_length}
      SUITABILITY : {suitability}
    """)
    elif isinstance(FILE, Nightly):
        float_list = [val for val in FILE.score_list if type(val) == float]
        total_length = sum(float_list)
        if total_length > 60:
            song_length = f"{math.floor(total_length / 60)}m {round(total_length % 60)}s"
        else:
            song_length = f"{round(total_length)}s"
        print(f"""    STATS FOR {song_name}:
      TYPE        : nightly score
      SAVED AS    : {song_name}.json
      LENGTH      : {song_length}
            """)