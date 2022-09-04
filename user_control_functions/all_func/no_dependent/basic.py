try:
    from ....srcs import *
    from ....classes import *
    from ....play_song import play_song
    from ... import helper
    from ... import enter
except ImportError:
    from srcs import *
    from classes import *
    from play_song import play_song
    import helper
    import enter

def edit_order():
    """order"""
    result = controller.order.edit(enter)
    if result == 0:
        print("exited editing\n")
    else:
        print()
        controller.song_list.refresh()

def export():
    """export"""
    if enter.no is None:
        index = input("Song index of song?: ")
        enter.no = get_song_index(index)
    if enter.no is None:
        print("Invalid index")
        return
    try:
        selected_song = list(Songs.songs.values())[enter.no]
        controller.export.export_as_nightly(selected_song)
    except IndexError:
        print("Invalid index")

def print_stats():
    """stats, info, data"""
    if enter.no is None:
        index = input("Song index of song?: ")
        enter.no = get_song_index(index)
    if enter.no is None:
        return
    try:
        print_stats(enter.no)
    except IndexError:
        print("Invalid index")

def print_txt_score():
    """txt, key, score"""
    no_result = False
    if enter.no is None:
        temp = input("song name or song index? ")
        enter.no = get_song_index(temp)  # returns int or None ONLY
        if enter.no is None:
            no_result = True
            print("invalid song name or index :(\n")

    if enter.no is not None and not no_result:  # no_result is used here as a local variable
        if enter.no <= len(Songs.songs):
            selected_song = list(Songs.songs.values())[enter.no - 1]
            if isinstance(selected_song, old_music_score):
                if type(selected_song) == old_music_score:
                    keys = [i for keys in selected_song.keys for i in [keys, "-"]]
                else:
                    keys = selected_song.keys
                raw_keys = score_list_to_score(key_list_to_score_list(keys))
            else:
                raw_keys = selected_song.score
            if "raw" in enter:
                pass
            else:
                spaced_key = "\n".join(
                    [i.replace("-", " ").strip() for i in raw_keys.splitlines()])
                if "space" in enter:
                    raw_keys = spaced_key
                else:
                    stripped_key = " ".join([i for i in spaced_key.split(" ") if i and "BEAT" not in i])
                    raw_keys = stripped_key
                    print("you can try: [space key] or [raw key]")

            print(f"\n>>>{list(Songs.songs.keys())[enter.no - 1].capitalize()}<<<")
            print(raw_keys)

            if 'txt' in enter:
                if os.path.exists(f"{Paths.score_path}\\{list(Songs.songs.keys())[enter.no - 1]}.txt"):
                    os.startfile(f"{Paths.score_path}\\{list(Songs.songs.keys())[enter.no - 1]}.txt")
                else:
                    if input(
                            f"'{list(Songs.songs.keys())[enter.no - 1]}' is a midi file, start anyways? (Y/n): ").lower() in [
                        "yes", 'y']:
                        os.startfile(f"{Paths.mid_path}\\{list(Songs.songs.keys())[enter.no - 1]}.mid")
        else:
            print(f"""    song index is out of range, maximum index is {len(Songs.songs)}""")

def __new_midi__():
    """midi"""
    if 'new' in enter:
        helper.new_midi()
    else:
        os.startfile(Paths.mid_path)

def __test_session__():
    """test, new, edit"""
    NEW = True  # if not 'test' in enter / if 'new' in enter or 'edit' in enter

    if enter.no != [] and int(enter.no[0]) <= len(Songs.songs.keys()) and "edit" in enter:
        selected_song = list(Songs.songs.values())[int(enter.no[0]) - 1]
        NAME = enter.no[0]
        TEST_SCORE = selected_song.score
        if type(selected_song) == old_music_score:
            TEST_SCORE = "-".join(selected_song.raw_key_list)

        print("switched to test session, any changes here wont affect the original song")
        print(
            "if you want to access this test score again, just enter 'test' followed by its file number to open it\n")
    else:
        if "test" in enter:
            NAME = enter.raw.replace("test", "").strip()
            NEW = False
        else:
            NAME = ""
        TEST_SCORE = ""
    helper.test_session(NAME, TEST_SCORE, NEW)

