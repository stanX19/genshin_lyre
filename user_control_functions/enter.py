try:
    from .. import utils
except ImportError:
    import utils

raw = ""
split = []
no = None
float = 0.0
isnumeric = False

def set_raw(txt:str):
    global raw, split, no, float, isnumeric
    raw = txt
    split = txt.split()
    no = utils.first_int(txt)
    float = utils.first_float(txt)
    isnumeric = txt.isnumeric()
