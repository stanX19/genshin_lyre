import re
import subprocess
import Paths
import classes
import os
import difflib
import json
import utils


def edit_using_notepad(text: str, dir_path=Paths.test_path, name="temporary editor.txt") -> str:
    path = os.path.join(dir_path, name)

    with open(path, 'w+') as file:
        file.write(text)

    try:
        subprocess.run([Paths.notepad_path, path], check=True)
    except subprocess.CalledProcessError as e:
        print("Error opening the file:", e)
        return text

    with open(path, 'r') as file:
        edited_text = file.read()

    try:
        os.remove(path)
    except OSError:
        pass

    return edited_text


def split_keys(text: str) -> list:
    pattern = r'\(([^)]+)\)|([A-Z])'
    keys = [m[0] if m[0] else m[1] for m in re.findall(pattern, text)]
    return keys


def longest_equal(old, new):
    if new in old:
        return [[old.find(new), old.find(new) + len(new), 0, len(new)]]

    data = [[[]] * (len(old) + 1) for _ in range(len(new) + 1)]  # data[new][old] = [[start_idx, end_idx]] + conseq
    count = [[[]] * (len(old) + 1) for _ in range(len(new) + 1)]  # count[new][old] = char_count [int]

    for new_idx in range(len(new) - 1, -1, -1):
        data[new_idx][len(old)] = data[new_idx + 1][0]
        count[new_idx][len(old)] = count[new_idx + 1][0]
        for old_idx in range(len(old) - 1, -1, -1):
            if not new[new_idx] == old[old_idx]:
                data[new_idx][old_idx] = data[new_idx][old_idx + 1]
                count[new_idx][old_idx] = count[new_idx][old_idx + 1]
                continue

            i, j = new_idx, old_idx
            while i < len(new) and j < len(old) and new[i] == old[j]:
                i += 1
                j += 1

            char_count = sorted([i - new_idx] + count[i][j], reverse=True)
            if char_count >= count[new_idx][old_idx + 1]:
                count[new_idx][old_idx] = char_count
                data[new_idx][old_idx] = [[old_idx, j, new_idx, i]] + data[i][j]
            else:
                count[new_idx][old_idx] = count[new_idx][old_idx + 1]
                data[new_idx][old_idx] = data[new_idx][old_idx + 1]

    return data[0][0]


def generate_opcodes(old, new):
    lcs_data = longest_equal(old, new)
    opcodes = []

    old_idx = 0

    for start_old, end_old, start_new, end_new in lcs_data:
        if old_idx < start_old:
            opcodes.append(('delete', old_idx, start_old))

        opcodes.append(('equal', start_old, end_old))
        old_idx = end_old

    if old_idx < len(old):
        opcodes.append(('delete', old_idx, len(old)))

    return opcodes


def find_removed_keys(original_score: str, opcodes) -> list[int]:
    # matcher = difflib.SequenceMatcher(None, original_score, edited_score)

    cur_idx = 0
    removed_keys_indices = []

    for op in opcodes:  # matcher.get_opcodes():
        print(op)
        involved_keys = split_keys(original_score[op[1]: op[2]])
        if op[0] == 'delete':
            for idx in range(len(involved_keys)):
                removed_keys_indices.append(cur_idx + idx)
        cur_idx += len(involved_keys)

    return removed_keys_indices


def remove_keys_by_index(score_list, to_remove):
    to_remove_set = set(to_remove)
    filtered_list = []

    key_idx = 0
    continue_idx = len(score_list)

    # first valid element lookup
    for idx, val in enumerate(score_list):
        if isinstance(val, str):
            if key_idx not in to_remove_set:
                filtered_list.append(val)
                continue_idx = idx + 1
                key_idx += 1
                break
            else:
                key_idx += 1

    # remaining valid element
    for idx, val in enumerate(score_list[continue_idx:]):
        if isinstance(val, str):
            if key_idx not in to_remove_set:
                filtered_list.append(val)
            key_idx += 1
        elif isinstance(val, float):
            if filtered_list:
                if isinstance(filtered_list[-1], str):
                    filtered_list.append(val)
                elif isinstance(filtered_list[-1], float):
                    filtered_list[-1] += val

    if filtered_list and isinstance(filtered_list[-1], float):
        filtered_list.pop(-1)

    return filtered_list


def save_changes(nightly_song: classes.Nightly, new_score_list: list):
    with open(nightly_song.path, encoding="utf-8") as f:
        json_data = json.load(f)

    KEYS = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
    NOTES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    KN = dict(zip(KEYS, NOTES))

    nightly_song.score_list = new_score_list

    notes = []
    cum_time = 100
    for val in new_score_list:
        if isinstance(val, float):
            cum_time += val * 1000
        if isinstance(val, str):
            for key in val:
                notes.append([KN[key], cum_time, "1"])

    json_data[0]["notes"] = notes
    with open(nightly_song.path, "w+", encoding="utf-8") as f:
        json.dump(json_data, f)


def edit_recorded_json(nightly_song: classes.Nightly) -> bool:
    """True: something has changed
       False: no changes applied"""

    if nightly_song.is_composed:
        return False

    raw_keys = nightly_song.raw_keys
    original_score = "\n".join(raw_keys.split("\n", 1)[1:])  # remove first row, (beat xxx)

    name = nightly_song.name + " (Only delete, Do not insert).txt"
    edited_score = edit_using_notepad(original_score, name=name)

    if edited_score == original_score:
        return False
    opcodes = generate_opcodes(original_score, edited_score)
    to_remove = find_removed_keys(original_score, opcodes)
    new_score_list = remove_keys_by_index(nightly_song.score_list, to_remove)

    save_changes(nightly_song, new_score_list)
    return True


def interactable_edit_recorded_json(nightly_song: classes.Nightly):
    if nightly_song.is_composed:
        print(f"{nightly_song.name} is not in recorded format")
        return

    print("    Detected type Nightly recorded, starting designated editor")
    print("    Started notepad, the saved edits will directly reflect onto the actual file\
(close the notepad to proceed)")

    raw_keys = nightly_song.raw_keys
    original_score = "\n".join(raw_keys.split("\n", 1)[1:])  # remove first row, (beat xxx)

    name = nightly_song.name + " (Only delete, Do not insert).txt"
    edited_score = edit_using_notepad(original_score, name=name)

    if edited_score == original_score:
        print("        No changes made")
        return

    opcodes = generate_opcodes(original_score, edited_score)
    to_remove = find_removed_keys(original_score, opcodes)
    new_score_list = remove_keys_by_index(nightly_song.score_list, to_remove)

    print(utils.score_list_to_score(new_score_list))
    print(f"changes:")
    for op in opcodes:
        print(f"    {op}")
    confirmed = utils.get_confirmation()

    if confirmed:
        save_changes(nightly_song, new_score_list)
        print(f"    Changes saved to {nightly_song.name}")
    else:
        print("    Changes discarded")


def main():
    path = utils.fileopenbox(title="Open", msg="Select files to be imported", default=Paths.downloads_path+'\\\\', multiple=True)[0]
    song = classes.Nightly(path, path)
    interactable_edit_recorded_json(song)


if __name__ == '__main__':
    main()
