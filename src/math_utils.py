

def round_if_int(num):
    if int(num) == num:
        return int(num)
    return round(num, 2)
