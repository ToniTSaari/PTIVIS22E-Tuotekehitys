def move(speedX, speedY, xy, map, width):
    yColl = xy[0] + width
    xColl = xy[1] + width
    yMap = map["y"]
    xMap = map["x"]
    if yMap[yColl] == True:
        xy[0] = yColl - speedY - width
    if xMap[xColl] == True:
        xy[1] = xColl - speedX - width
    return 