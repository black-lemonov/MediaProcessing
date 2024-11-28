
def get_pixel(x, y, tg):
    if (x >= 0 and y <= 0 and tg < -2.414) or (x <= 0 and y <= 0 and tg > 2.414):
        return 0
    elif x >= 0 and y <= 0 and tg < -0.414:
        return 1
    elif (x >= 0 and y <= 0 and tg > -0.414) or (x >= 0 and y >= 0 and tg < 0.414):
        return 2
    elif x >= 0 and y >= 0 and tg < 2.414:
        return 3
    elif (x >= 0 and y >= 0 and tg > 2.414) or (x <= 0 and y >= 0 and tg < -2.414):
        return 4
    elif x <= 0 and y >= 0 and tg < -0.414:
        return 5
    elif (x <= 0 and y >= 0 and tg > -0.414) or (x <= 0 and y <= 0 and tg < 0.414):
        return 6
    elif x <= 0 and y <= 0 and tg < 2.414:
        return 7