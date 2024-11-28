
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
    

def get_neighbours(x, y, angle: int) -> tuple[tuple[int, int], tuple[int, int]]:
    if angle == 0 or angle == 4:
        neighbour1 = (y - 1, x)
        neighbour2 = (y + 1, x)
    elif angle == 1 or angle == 5:
        neighbour1 = (y - 1, x + 1)
        neighbour2 = (y + 1, x - 1)
    elif angle == 2 or angle == 6:
        neighbour1 = (y, x + 1)
        neighbour2 = (y, x - 1)
    elif angle == 3 or angle == 7:
        neighbour1 = (y + 1, x + 1)
        neighbour2 = (y - 1, x - 1)
    
    return neighbour1, neighbour2
