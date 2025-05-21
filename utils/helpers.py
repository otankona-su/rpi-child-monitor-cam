# utils/helpers.py

def parse_resolution(res_str):
    """
    解像度文字列 "WxH" を (W, H) のタプルに変換
    """
    w, h = res_str.split("x")
    return int(w), int(h)

