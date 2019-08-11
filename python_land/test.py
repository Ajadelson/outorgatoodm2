"""Utilizando rasterio"""

import rasterio
import numpy as np
import geopandas as gpd
import glob
import pyproj
import matplotlib
import matplotlib.pyplot as plt
from rasterio.merge import merge
from rasterio.plot import show

class Fun():
    def __init__(self):
        self.rasters = glob.glob("Alagoas/Mapa/*.tif")

        self.mosaic = []
        for item in self.rasters:
            self.src = rasterio.open(item)
            self.mosaic.append(self.src)

        self.mosaic, self.out_trans = merge(self.mosaic)
        #show(self.mosaic)

    def mostrar(self):
        show(self.mosaic, cmap='terrain')

        out_meta = self.src.meta.copy()
        out_meta.update({"driver":"GTiff", "height":self.mosaic.shape[1],
        "width":self.mosaic.shape[2], "transform": self.out_trans,
        "crs":"+proj=utm +zone=23 +ellps=GRS80 +units=m +no_defs"})

        with rasterio.open("new.tif", "w",**out_meta) as dest:
            dest.write(self.mosaic)

    def abrir(self):
        window = rasterio.windows.Window(1024,1024,self.mosaic.shape[2],self.mosaic.shape[1])
        with rasterio.open("new.tif") as src:
            subset = src.read(1,window=window)

        plt.figure(figsize=(15,10))
        plt.imshow(subset, cmap='terrain')
        plt.colorbar(shrink=0.5)
        plt.show()
