"""Manipulação com os arquivos Landsat"""

import rasterio
import numpy as np
import geopandas as gpd
import glob
import pyproj
import matplotlib
import matplotlib.pyplot as plt
from rasterio.merge import merge
from rasterio.plot import show

class Sat():
    def __init__(self):
        self.arquivos = glob.glob("Landsat-Al/*.TIF")
        self.arquivos2 = glob.glob("Landsat-Al-antes/*.TIF")

        self.arquivos.sort()
        self.arquivos2.sort()

        self.redband = self.arquivos[3]
        self.near_infrared = self.arquivos[4]
        self.redband2 = self.arquivos2[3]
        self.near_infrared2 = self.arquivos2[4]
        self.band1 = self.arquivos[0]
        self.band2 = self.arquivos[1]
        self.band3 = self.arquivos[2]
        self.band6 = self.arquivos[5]
        self.band7 = self.arquivos[6]
        self.band8 = self.arquivos[7]
        self.band9 = self.arquivos[8]
        self.band_bqa = self.arquivos[9]

        with rasterio.open(self.band1) as src:
            profile_b1 = src.profile
            self.b1 = src.read(1, out_shape=(1, int(src.height), int(src.width)))

        with rasterio.open(self.band2) as src:
            profile_b2 = src.profile
            self.b2 = src.read(1, out_shape=(1, int(src.height), int(src.width)))

        with rasterio.open(self.band3) as src:
            profile_b3 = src.profile
            self.b3 = src.read(1, out_shape=(1, int(src.height), int(src.width)))

        with rasterio.open(self.redband) as src:
            profile_red = src.profile
            self.b4 = src.read(1, out_shape=(1, int(src.height), int(src.width)))

        with rasterio.open(self.near_infrared) as src:
            profile_nir = src.profile
            self.b5 = src.read(1, out_shape=(1, int(src.height), int(src.width)))

        with rasterio.open(self.band6) as src:
            profile_b6 = src.profile
            self.b6 = src.read(1, out_shape=(1, int(src.height), int(src.width)))

        with rasterio.open(self.band6) as src:
            profile_b6 = src.profile
            self.b6 = src.read(1, out_shape=(1, int(src.height), int(src.width)))

        with rasterio.open(self.band7) as src:
            profile_b7 = src.profile
            self.b7 = src.read(1, out_shape=(1, int(src.height), int(src.width)))

        with rasterio.open(self.band8) as src:
            profile_b8 = src.profile
            self.b8 = src.read(1, out_shape=(1, int(src.height), int(src.width)))

        with rasterio.open(self.band9) as src:
            profile_b9 = src.profile
            self.b9 = src.read(1, out_shape=(1, int(src.height), int(src.width)))

        with rasterio.open(self.band_bqa) as src:
            profile_bqa = src.profile
            self.bqa = src.read(1, out_shape=(1, int(src.height), int(src.width)))




        self.b1 = self.b1.astype('f4')
        self.b2 = self.b2.astype('f4')
        self.b3 = self.b3.astype('f4')
        self.b4 = self.b4.astype('f4')
        self.b5 = self.b5.astype('f4')
        self.b6 = self.b6.astype('f4')
        self.b7 = self.b7.astype('f4')
        self.b8 = self.b8.astype('f4')
        self.b9 = self.b9.astype('f4')
        self.bqa = self.bqa.astype('f4')


    def ndvi(self):
        """Vegetação saudavel"""
        with rasterio.open(self.redband) as src:
            profile_red = src.profile
            self.red = src.read(1, out_shape=(1, int(src.height), int(src.width)))

        with rasterio.open(self.near_infrared) as src:
            profile_nir = src.profile
            self.nir = src.read(1, out_shape=(1, int(src.height), int(src.width)))

        nir = self.nir.astype('f4')
        red = self.red.astype('f4')
        self.ndvi = (nir - red)/(nir + red)

        plt.imshow(self.ndvi, cmap='RdYlGn')
        plt.colorbar()
        plt.show()

    def subndvi(self):
        """Vegetação saudavel em decorrencia do tempo"""
        date = '18/04/2017'
        date2 = '15/05/2015'
        with rasterio.open(self.redband2) as src:
            profile_red = src.profile
            self.red2 = src.read(1, out_shape=(1, int(src.height), int(src.width)))

        with rasterio.open(self.near_infrared2) as src:
            profile_nir = src.profile
            self.nir2 = src.read(1, out_shape=(1, int(src.height), int(src.width)))

        nir2 = self.nir2.astype('f4')
        red2 = self.red2.astype('f4')
        self.ndvi2 = (nir2 - red2)/(nir2 + red2)

        with rasterio.open(self.redband) as src:
            profile_red = src.profile
            self.red = src.read(1, out_shape=(1, int(src.height), int(src.width)))

        with rasterio.open(self.near_infrared) as src:
            profile_nir = src.profile
            self.nir = src.read(1, out_shape=(1, int(src.height), int(src.width)))

        nir = self.nir.astype('f4')
        red = self.red.astype('f4')
        self.ndvi = (nir - red)/(nir + red)

        fig, axes = plt.subplots(1,3, figsize=(14,6), sharex=True, sharey=True)

        plt.sca(axes[0])
        plt.imshow(self.ndvi, cmap='RdYlGn', vmin=-1, vmax=1)
        plt.colorbar(shrink=0.5)
        plt.title('NDVI {}'.format(date))
        plt.xlabel('Column #')
        plt.ylabel('Row #')

        plt.sca(axes[1])
        plt.imshow(self.ndvi2, cmap='RdYlGn', vmin=-1, vmax=1)
        plt.colorbar(shrink=0.5)
        plt.title('NDVI {}'.format(date2))

        plt.sca(axes[2])
        plt.imshow(self.ndvi - self.ndvi2, cmap='bwr', vmin=-1, vmax=1)
        plt.colorbar(shrink=0.5)
        plt.title('Diff ({} - {})'.format(date2, date))
        plt.show()

    def rq(self):
        """Neosolo quartizarênico ortico"""

        #eutrofico
        self.rq1_e = -46.4206-228.4600*self.b1-125.9748*self.b2-14.8318*self.b3+199.3307*self.b4-254.0578*self.b5+403.4543*self.b7
        #álico
        self.rq1_a = -62.5108-241.7664*self.b1-274.8210*self.b2+39.6622*self.b3+264.4101*self.b4-286.0963*self.b5+437.0335*self.b7
        #hidromorfico alico
        self.rq3_a = -66.2576-282.5612*self.b1+303.8616*self.b2-345.5951*self.b3+244.5534*self.b4-380.9188*self.b5+584.1653*self.b7

        fig, axes = plt.subplots(1,3, figsize=(14,6), sharex=True, sharey=True)

        plt.sca(axes[0])
        plt.imshow(self.rq1_e, vmin=-1, vmax=1)
        plt.colorbar(shrink=0.5)
        plt.title('Neosolo quartizarênico ortico eutrofico')

        plt.sca(axes[1])
        plt.imshow(self.rq1_a, vmin=-1, vmax=1)
        plt.colorbar(shrink=0.5)
        plt.title('Neosolo quartizarênico ortico álico')

        plt.sca(axes[2])
        plt.imshow(self.rq3_a, vmin=-1, vmax=1)
        plt.colorbar(shrink=0.5)
        plt.title('Neosolo quartizarênico hidromorfico álico')
        plt.show()

    def lv1(self):
        """Latossolo Vermelho tipico argiloso"""

        #eutrofico
        self.lv1_e = -24.8406-37.1991*self.b1-351.8395*self.b2+105.4918*self.b3+314.4517*self.b4-173.1839*self.b5+122.8555*self.b7
        #distrofico
        self.lv1_d = -30.36133-121.7438*self.b1-268.5567*self.b2+114.4559*self.b3+191.6955*self.b4-184.76132*self.b5+250.3459*self.b7

        fig, axes = plt.subplots(1,2, figsize=(14,6), sharex=True, sharey=True)

        plt.sca(axes[0])
        plt.imshow(self.lv1_e, vmin=-1, vmax=1)
        plt.colorbar(shrink=0.5)
        plt.title('Latossolo Vermelho tipico argiloso eutrofico')

        plt.sca(axes[1])
        plt.imshow(self.lv1_d, vmin=-1, vmax=1)
        plt.colorbar(shrink=0.5)
        plt.title('Latossolo Vermelho tipico argiloso distrófico')
        plt.show()

    def lv2(self):
        """Latossolo Vermelho tipico medio-argiloso"""

        #eutrofico
        self.lv2_e = -27.9713-135.1567*self.b1-156.4192*self.b2+53.7164*self.b3+157.4458*self.b4-168.6005*self.b5+255.9643*self.b7
        #alico
        self.lv2_a = -36.9334-44.8428*self.b1-264.1166*self.b2+58.4441*self.b3+181.1672*self.b4-121.5379*self.b5+226.8691*self.b7

        fig, axes = plt.subplots(1,2, figsize=(14,6), sharex=True, sharey=True)

        plt.sca(axes[0])
        plt.imshow(self.lv2_e, vmin=-1, vmax=1)
        plt.colorbar(shrink=0.5)
        plt.title('Latossolo Vermelho tipico medio-argiloso eutrofico')

        plt.sca(axes[1])
        plt.imshow(self.lv2_a, vmin=-1, vmax=1)
        plt.colorbar(shrink=0.5)
        plt.title('Latossolo Vermelho tipico medio-argiloso álico')
        plt.show()

    def lv3(self):
        """Latossolo Vermelho tipico medio-arenoso"""

        #eutrofico
        self.lv3_e = -60.8654-250.7927*self.b1-54.8743*self.b2-165.4928*self.b3+241.5738*self.b4-325.1146*self.b5+539.7188*self.b7
        #alico
        self.lv3_a = -43.0196-201.2953*self.b1-253.7626*self.b2+27.9028*self.b3+293.4075*self.b4-292.2899*self.b5+370.9185*self.b7

        fig, axes = plt.subplots(1,2, figsize=(14,6), sharex=True, sharey=True)

        plt.sca(axes[0])
        plt.imshow(self.lv3_e, vmin=-1, vmax=1)
        plt.colorbar(shrink=0.5)
        plt.title('Latossolo Vermelho tipico medio-arenoso eutrofico')

        plt.sca(axes[1])
        plt.imshow(self.lv3_a, vmin=-1, vmax=1)
        plt.colorbar(shrink=0.5)
        plt.title('Latossolo Vermelho tipico medio-arenoso álico')
        plt.show()

    def lvdf1(self):
        """Latossolo Vermelho distroférrico argiloso"""

        #eutrofico
        self.lvdf1_e = -23.4650-60.7526*self.b1-464.4926*self.b2+285.0277*self.b3+211.8802*self.b4-37.1807*self.b5-11.8664*self.b7
        #alico
        self.lvdf1_a = -23.7360-88.3488*self.b1-436.8303*self.b2+226.8088*self.b3+308.7524*self.b4-160.9397*self.b5+64.7676*self.b7

        fig, axes = plt.subplots(1,2, figsize=(14,6), sharex=True, sharey=True)

        plt.sca(axes[0])
        plt.imshow(self.lvdf1_e, vmin=-1, vmax=1)
        plt.colorbar(shrink=0.5)
        plt.title('Latossolo Vermelho distroférrico argiloso eutrofico')

        plt.sca(axes[1])
        plt.imshow(self.lvdf1_a, vmin=-1, vmax=1)
        plt.colorbar(shrink=0.5)
        plt.title('Latossolo Vermelho distroférrico argiloso álico')
        plt.show()

    def lva2(self):
        """Latossolo Vermelho-Amarelo tipico medio-arenoso"""

        #alico
        self.lva2_a = -43.4150-187.4732*self.b1-181.3167*self.b2-25.1457*self.b3+238.1350*self.b4-271.5631*self.b5+402.0682*self.b7

        plt.imshow(self.lva2_a, vmin=-1, vmax=1)
        plt.colorbar(shrink=0.5)
        plt.title('Latossolo Vermelho-Amarelo tipico medio-arenoso álico')
        plt.show()

    def pva2(self):
        """Argissolo vermelho-amarelo medio-arenoso"""

        #eutrofico
        self.pva2_e = -33.0866-73.4533*self.b1-291.5132*self.b2-59.7143*self.b3+493.2500*self.b4-307.9804*self.b5+202.9670*self.b7
        #alico
        self.pva2_a = -71.5916-199.9395*self.b1-270.6843*self.b2-72.9379*self.b3+369.9924*self.b4-288.9663*self.b5+426.5647*self.b7

        fig, axes = plt.subplots(1,2, figsize=(14,6), sharex=True, sharey=True)

        plt.sca(axes[0])
        plt.imshow(self.pva2_e, vmin=-1, vmax=1)
        plt.colorbar(shrink=0.5)
        plt.title('Argissolo vermelho-amarelo medio-arenosoeutrofico')

        plt.sca(axes[1])
        plt.imshow(self.pva2_a, vmin=-1, vmax=1)
        plt.colorbar(shrink=0.5)
        plt.title('Argissolo vermelho-amarelo medio-arenoso alico')
        plt.show()

    def pva3(self):
        """argissolo Vermelho-amarelo abrupto argiloso"""

        #eutrofico
        self.pva3_e = -56.7563-128.6798*self.b1-158.5975*self.b2-252.4119*self.b3+504.0434*self.b4-434.6178*self.b5+486.5749*self.b7
        #alico
        self.pva3_a = -48.7805-282.8469*self.b1+183.4150*self.b2-288.1546*self.b3+170.9145*self.b4-327.1532*self.b5+561.8631*self.b7

        fig, axes = plt.subplots(1,2, figsize=(14,6), sharex=True, sharey=True)

        plt.sca(axes[0])
        plt.imshow(self.pva3_e, vmin=-1, vmax=1)
        plt.colorbar(shrink=0.5)
        plt.title('argissolo Vermelho-amarelo abrupto argiloso eutrofico')

        plt.sca(axes[1])
        plt.imshow(self.pva3_a, vmin=-1, vmax=1)
        plt.colorbar(shrink=0.5)
        plt.title('argissolo Vermelho-amarelo abrupto argiloso alico')
        plt.show()

    def nv1(self):
        """Nitossolo vermelho"""

        #eutrofico
        self.nv1_e = -20.9665-48.2103*self.b1-368.8835*self.b2+135.5378*self.b3+294.6483*self.b4-92.4371*self.b5+19.2430*self.b7
        #alico
        self.nv1_a = -13.4694-71.7484*self.b1-331.4813*self.b2+217.0301*self.b3+155.1439*self.b4-61.7458*self.b5+31.1940*self.b7

        fig, axes = plt.subplots(1,2, figsize=(14,6), sharex=True, sharey=True)

        plt.sca(axes[0])
        plt.imshow(self.nv1_e, vmin=-1, vmax=1)
        plt.colorbar(shrink=0.5)
        plt.title('Nitossolo vermelho eutrofico')

        plt.sca(axes[1])
        plt.imshow(self.nv1_a, vmin=-1, vmax=1)
        plt.colorbar(shrink=0.5)
        plt.title('Nitossolo vermelho álico')
        plt.show()

    def nv2(self):
        """Nitossolo Vermelho cambissolos associados"""

        #eutrofico
        self.nv2_e = -33.0766-50.0515*self.b1-385.3550*self.b2-143.9981*self.b3+294.7166*self.b4+48.4649*self.b5-63.3923*self.b7

        plt.imshow(self.nv2_e, vmin=-1, vmax=1)
        plt.colorbar(shrink=0.5)
        plt.title('Nitossolo Vermelho cambissolos associados')
        plt.show()
