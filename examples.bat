--poly ./task1/poly.geojson --zoom 11 --url http://stamen-tiles-a.a.ssl.fastly.net/terrain-background/{z}/{x}/{y}.png --out-dir ./task1/tiles
--dir ./task1/tiles --out-file ./task1/out/out.png

--poly ./task2/poly.geojson --zoom 12 --url https://a.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png --out-dir ./task2/tiles
--dir ./task2/tiles --out-file ./task2/out/out.png


--dir ./task2/10/tiles --dst-file ./task2/10/out/10-geo.tif
