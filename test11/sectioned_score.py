

def format(score:str,sep="--"):
    sectioned_score = score.replace("\n","").replace(" ",'-').split("/")
    new_score = ""
    for idx, section in enumerate(sectioned_score):
        section_bucket = []
        bucket = ""
        for key in section:
            if bucket:
                bucket+=key
                if key == ")":
                    section_bucket.append(bucket)
                    bucket = ""
            elif key == "(":
                bucket+=key
            elif key == "-":
                section_bucket.append('')
            else:
                section_bucket.append(key)
        if len(section_bucket) <= 4:
            section_bucket += [''] * (5 - len(section_bucket))
        else:
            section_bucket += [''] * (9 - len(section_bucket))
            # 9 instead of 8 because we are using .join() later, will need an extra character

        cur_sec_score = sep.join(section_bucket)
        if idx % 2 == 1 and cur_sec_score[-1] == "-":
                new_score += cur_sec_score[:-1] + "\n"
        else:
            new_score += cur_sec_score
    return new_score

def to_score_list(score:str, rest=0.25):
    sectioned_score = score.replace("\n","").replace(" ",'-').split("/")
    raw_sections = []
    for idx, section in enumerate(sectioned_score):
        section_bucket = []
        bucket = ""
        for key in section:
            if bucket:
                bucket+=key
                if key == ")":
                    section_bucket.append(bucket)
                    bucket = ""
            elif key == "(":
                bucket+=key
            elif key == "-":
                section_bucket.append('')
            else:
                section_bucket.append(key)

        raw_sections.append(section_bucket)


    print(raw_sections)
    score_list = [0.0]
    max_len = len(max(raw_sections, key=len))
    accum = 0.0
    for section in raw_sections:
        cur_len = len(section)
        if cur_len == 0:
            continue
        ratio = max_len // cur_len

        for note in section:
            if note:
                score_list.append(accum)
                score_list.append(note)
                accum = 0.0
            accum += ratio * rest
    while isinstance(score_list[0], float):
        score_list.pop(0)
    while isinstance(score_list[-1], float):
        score_list.pop(-1)
    return score_list


if __name__ == '__main__':
    fd = open(r"C:\Users\DELL\PycharmProjects\pythonProject\genshin_lyre\genshin_lyre\genshin_assets\test\test.txt")
    score = fd.read()
    print(to_score_list(score))
    fd.close()