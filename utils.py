import math


# from OSM Slippy Tile definitions & https://github.com/Caged/tile-stitch
def latlon2tile(lat, lon, zoom):
    lat_radians = lat * math.pi / 180.0
    n = 1 << zoom
    return (
        n * ((lon + 180.0) / 360.0),
        n * (1 - (math.log(math.tan(lat_radians) + 1 / math.cos(lat_radians)) / math.pi)) / 2.0
    )


def tile2latlon(tx, ty, zoom):
    n = 1 << zoom
    lat_radians = math.atan(math.sinh(math.pi * (1.0 - 2.0 * ty / n)))
    lat = lat_radians * 180 / math.pi
    lon = 360 * tx / n - 180.0
    return (lat, lon)


def webmercator2tile(wx, wy, zoom):
    n = 1 << zoom
    tx = n * (wx / 40075016.68 + 0.5)
    ty = n * (0.5 - wy / 40075016.68)
    return (tx, ty)


def tile2webmercator(tx, ty, zoom):
    n = 1 << zoom
    wx = (tx / n - 0.5) * 40075016.68
    wy = (0.5 - ty / n) * 40075016.68
    return (wx, wy)


def tileres4webmercator(zoom):
    n = 1 << zoom
    return 40075016.68/n


def latlon2webmercator(lat, lon):
    wx = lon * 20037508.34 / 180
    wy = math.log(math.tan((90 + lat)*math.pi / 360))/(math.pi / 180)
    wy = wy * 20037508.34 / 180
    return (wx, wy)


def webmercator2latlon(wx, wy):
    # [12727039.383734727, 3579066.6894065146] vs [114.32894001591471, 30.58574800385281]
    lon = wx / 20037508.34 * 180
    lat = wy / 20037508.34 * 180
    lat = 180 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180)) - math.pi / 2)
    return (lat, lon)

