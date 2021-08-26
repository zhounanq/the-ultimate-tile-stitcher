import os
import argparse
import glob
from PIL import Image
from osgeo import gdal, osr

from utils import tile2webmercator, tileres4webmercator

web_mercator_proj = "PROJCS[\"WGS_1984_Web_Mercator_Auxiliary_Sphere\"," \
                    "GEOGCS[\"GCS_WGS_1984\"," \
                    "DATUM[\"D_WGS_1984\"," \
                    "SPHEROID[\"WGS_1984\",6378137.0,298.257223563]]," \
                    "PRIMEM[\"Greenwich\",0.0]," \
                    "UNIT[\"Degree\",0.017453292519943295]]," \
                    "PROJECTION[\"Mercator_Auxiliary_Sphere\"]," \
                    "PARAMETER[\"False_Easting\",0.0]," \
                    "PARAMETER[\"False_Northing\",0.0]," \
                    "PARAMETER[\"Central_Meridian\",0.0]," \
                    "PARAMETER[\"Standard_Parallel_1\",0.0]," \
                    "PARAMETER[\"Auxiliary_Sphere_Type\",0.0]," \
                    "UNIT[\"Meter\",1.0]]"


def set_spatialref(img_path, geotransform, proj):

    image_ds = gdal.Open(img_path, gdal.GA_Update)
    if not image_ds:
        print("Fail to open image {}".format(img_path))
        return False
    if proj:
        print("Projection is {}".format(proj))
    if geotransform:
        print("Origin = ({}, {})".format(geotransform[0], geotransform[3]))
        print("Pixel Size = ({}, {})".format(geotransform[1], geotransform[5]))

    image_ds.SetProjection(proj)
    image_ds.SetGeoTransform(geotransform)
    image_ds.FlushCache()

    print("### Copy spatial reference over")
    return True


def parse_args():
    parser = argparse.ArgumentParser(description='stitch tiles scraped by scraper.py')
    parser.add_argument('--dir', required=True, type=str,
                        help='directory containing times, saved in {zoom}_{X}_{Y} form')
    parser.add_argument('--dst-file', required=True, type=str, help='output filename')
    opts = parser.parse_args()
    return opts


def main():
    opts = parse_args()
    search_path = os.path.join(opts.dir, '*_*_*.png')

    filepaths = glob.glob(search_path)

    if len(filepaths) == 0:
        print('No files found')
        raise SystemExit

    def xyz(filepath):
        base = os.path.splitext(os.path.basename(filepath))[0]
        z, x, y = base.split('_')
        return int(x), int(y), int(z)

    xyzs = list(map(xyz, filepaths))
    x_min, y_min = min(map(lambda x_y: x_y[0], xyzs)), min(map(lambda x_y: x_y[1], xyzs))
    x_max, y_max = max(map(lambda x_y: x_y[0], xyzs)), max(map(lambda x_y: x_y[1], xyzs))
    zoom = xyzs[0][2]

    tile_w, tile_h = Image.open(filepaths[0]).size
    geo_x_0, geo_y_0 = tile2webmercator(x_min, y_min, zoom)
    res_x = tileres4webmercator(zoom) / tile_w
    res_y = tileres4webmercator(zoom) / tile_w
    print("[0]:{}\n[1]:{}\n[3]:{}\n[5]:{}".format(geo_x_0, res_x, geo_y_0, res_y))

    # sr = osr.SpatialReference()
    # sr.SetWellKnownGeogCS('WGS84')
    # sr.ImportFromEPSG(3857)
    # proj_wkt = sr.ExportToWkt()

    geotransform = [0]*6
    geotransform[0], geotransform[3] = geo_x_0, geo_y_0
    geotransform[1], geotransform[5] = res_x, -res_y
    geotransform[2], geotransform[4] = 0, 0

    set_spatialref(opts.dst_file, geotransform, web_mercator_proj)


if __name__ == '__main__':
    main()

