
# https://www.earthinversion.com/utilities/reading-NetCDF4-data-in-python/

import netCDF4
import numpy as np

f = netCDF4.Dataset('./KMDS__OPER_P___10M_OBS_L2_202107160000.nc')
print ('DATASET:', f)

# <class 'netCDF4._netCDF4.Dataset'>
# root group (NETCDF4 data model, file format HDF5):
#     featureType: timeSeries
#     Conventions: CF-1.4
#     title: KMDS__OPER_P___10M_OBS_L2
#     institution: Royal Netherlands Meteorological Institute (KNMI)
#     source: Royal Netherlands Meteorological Institute (KNMI)
#     history: File created from KMDS ASCII file. 
#     references: http://data.knmi.nl
#     comment: Please note: no data has been found for the following variables: ts1, ts2
#     dimensions(sizes): station(52), time(1)
#     variables(dimensions): <class 'str'> station(station), float64 time(time), <class 'str'> stationname(station), float64 lat(station), float64 lon(station), float64 height(station), float64 dd(station, time), float64 ff(station, time), float64 gff(station, time), float64 ta(station, time), float64 rh(station, time), float64 pp(station, time), float64 zm(station, time), float64 D1H(station, time), float64 dr(station, time), float64 hc(station, time), float64 hc1(station, time), float64 hc2(station, time), float64 hc3(station, time), float64 nc(station, time), float64 nc1(station, time), float64 nc2(station, time), float64 nc3(station, time), float64 pg(station, time), float64 pr(station, time), float64 qg(station, time), float64 R12H(station, time), float64 R1H(station, time), float64 R24H(station, time), float64 R6H(station, time), float64 rg(station, time), float64 ss(station, time), float64 td(station, time), float64 tgn(station, time), float64 Tgn12(station, time), float64 Tgn14(station, time), float64 Tgn6(station, time), float64 tn(station, time), float64 Tn12(station, time), float64 Tn14(station, time), float64 Tn6(station, time), float64 tx(station, time), float64 Tx12(station, time), float64 Tx24(station, time), float64 Tx6(station, time), float64 ww(station, time), float64 pwc(station, time), float64 ww-10(station, time), float64 ts1(station, time), float64 ts2(station, time), |S1 iso_dataset(), |S1 product(), |S1 projection()
#     groups: 

print('KEYS:', f.variables.keys()) 

# dict_keys(['station', 'time', 'stationname', 'lat', 'lon', 'height', 'dd', 'ff', 'gff', 'ta', 'rh', 'pp', 'zm', 'D1H', 'dr', 'hc', 'hc1', 'hc2', 'hc3', 'nc', 'nc1', 'nc2', 'nc3', 'pg', 'pr', 'qg', 'R12H', 'R1H', 'R24H', 'R6H', 'rg', 'ss', 'td', 'tgn', 'Tgn12', 'Tgn14', 'Tgn6', 'tn', 'Tn12', 'Tn14', 'Tn6', 'tx', 'Tx12', 'Tx24', 'Tx6', 'ww', 'pwc', 'ww-10', 'ts1', 'ts2', 'iso_dataset', 'product', 'projection'])

station_class = f.variables['station'] # station variable
print('STATION:', station_class)

# <class 'netCDF4._netCDF4.Variable'>
# vlen station(station)
#     long_name: Station id
#     cf_role: timeseries_id
# vlen data type: <class 'str'>
# unlimited dimensions: 
# current shape = (52,)

time_class = f.variables['time']
print('TIME:', time_class)

# TIME: <class 'netCDF4._netCDF4.Variable'>
# float64 time(time)
#     long_name: time of measurement
#     standard_name: time
#     units: seconds since 1950-01-01 00:00:00
# unlimited dimensions: 
# current shape = (1,)
# filling on, default _FillValue of 9.969209968386869e+36 used

lat_class,lon_class = f.variables['lat'], f.variables['lon']
print('LAT:',lat_class)
print('LON',lon_class)

# LAT: <class 'netCDF4._netCDF4.Variable'>
# float64 lat(station)
#     long_name: station  latitude
#     standard_name: latitude
#     units: degrees_north
# unlimited dimensions: 
# current shape = (52,)
# filling on, default _FillValue of 9.969209968386869e+36 used
# LON <class 'netCDF4._netCDF4.Variable'>
# float64 lon(station)
#     long_name: station longitude
#     standard_name: longitude
#     units: degrees_east
# unlimited dimensions: 
# current shape = (52,)
# filling on, default _FillValue of 9.969209968386869e+36 used

for d in f.dimensions.items():
  print('DIMENSIONS:', d)

#  ('station', <class 'netCDF4._netCDF4.Dimension'>: name = 'station', size = 52)
#  ('time', <class 'netCDF4._netCDF4.Dimension'>: name = 'time', size = 1)

stationname = f.variables['stationname'][:]
print('STATIONNAME:',stationname)

# STATIONNAME: ['D15-FA-1' 'P11-B' 'K14-FA-1C' 'A12-CPP' 'L9-FF-1' 'AWG-1' 'J6-A'
#  'HOORN-A' 'BUITENGAATS/BG-OHVS2' 'VOORSCHOTEN AWS' 'IJMUIDEN WP'
#  'TEXELHORS WP' 'DE KOOY VK' 'F3-FB-1' 'AMSTERDAM/SCHIPHOL AP' 'VLIELAND'
#  'WIJDENES WP' 'BERKHOUT AWS' 'TERSCHELLING HOORN AWS' 'WIJK AAN ZEE AWS'
#  'HOUTRIBDIJK WP' 'DE BILT AWS' 'STAVOREN AWS' 'LELYSTAD AP' 'LEEUWARDEN'
#  'MARKNESSE AWS' 'DEELEN' 'LAUWERSOOG AWS' 'HEINO AWS' 'HOOGEVEEN AWS'
#  'GRONINGEN AP EELDE' 'HUPSEL AWS' 'NIEUW BEERTA AWS' 'TWENTHE AWS'
#  'VLISSINGEN AWS' 'WESTDORPE AWS' 'WILHELMINADORP AWS'
#  'HOEK VAN HOLLAND AWS' 'WOENSDRECHT' 'ROTTERDAM GEULHAVEN'
#  'ROTTERDAM THE HAGUE AP' 'CABAUW TOWER AWS' 'GILZE RIJEN' 'HERWIJNEN AWS'
#  'EINDHOVEN AP' 'VOLKEL' 'ELL AWS' 'MAASTRICHT AACHEN AP' 'ARCEN AWS'
#  'JUANCHO E. YRAUSQUIN AIRPORT  SABA'
#  'F.D. ROOSEVELT AIRPORT ST. EUSTATIUS' 'FLAMINGO AIRPORT BONAIRE']

lat = f.variables['lat'][:]
print('LAT:',lat)

# LAT: [54.32566667 52.36       53.26944444 55.39916667 53.61444444 53.49166667
#  53.82413056 52.91805556 54.03694    52.139722   52.46224287 52.99501581
#  52.92686501 54.85388889 52.317222   53.24002666 52.63243067 52.6426969
#  53.39126595 52.50533389 52.64818731 52.0988218  52.89664391 52.45727049
#  53.22300049 52.70190239 52.05486178 53.4115811  52.43456176 52.7490564
#  53.12367621 52.06753427 53.19440957 52.27314817 51.44133406 51.22475751
#  51.52595651 51.99094192 51.44774449 51.89183091 51.96066736 51.96903112
#  51.56488902 51.85759384 51.44977246 51.65852838 51.1966999  50.90525626
#  51.49730626 17.6461111  17.4955556  12.13      ]

lon = f.variables['lon'][:]
print('LON:',lon)

# LON: [  2.93575      3.34166667   3.62777778   3.81027778   4.96027778
#    5.94166667   2.94527778   4.15027778   6.04167      4.436389
#    4.55490068   4.71987579   4.78114532   4.69611111   4.789722
#    4.92079071   5.17347397   4.97875724   5.34580109   4.60293006
#    5.40038813   5.17970586   5.3834789    5.5196324    5.75157389
#    5.88744617   5.87232255   6.19909945   6.25897703   6.57297011
#    6.584847     6.65672536   7.14932206   6.89087451   3.59582416
#    3.86096572   3.88353374   4.12184977   4.342014     4.31266383
#    4.44690051   4.9259217    4.93523863   5.14539892   5.37700393
#    5.70659467   5.76254472   5.76178349   6.19610678 -63.2208333
#  -62.9827778  -68.2758333 ]

station = station_class[:]
print('STATION SHAPE',station.shape)
print('STATION',station)

# STATION SHAPE (52,)
# STATION ['06201' '06203' '06204' '06205' '06207' '06208' '06211' '06212' '06214'
#  '06215' '06225' '06229' '06235' '06239' '06240' '06242' '06248' '06249'
#  '06251' '06257' '06258' '06260' '06267' '06269' '06270' '06273' '06275'
#  '06277' '06278' '06279' '06280' '06283' '06286' '06290' '06310' '06319'
#  '06323' '06330' '06340' '06343' '06344' '06348' '06350' '06356' '06370'
#  '06375' '06377' '06380' '06391' '78871' '78873' '78990']

height_class = f.variables['height']
height = height_class[:]
print('HEIGHT:',height)

# HEIGHT: [ 42.7   41.84  41.8   48.35  44.    40.5   45.7   50.9   42.46  -1.15
#    4.4    1.     1.22  50.6   -3.35  10.79   0.8   -2.4    0.73   8.5
#    7.25   1.9   -1.3   -3.66   1.22  -3.35  48.16   2.9    3.6   15.82
#    5.18  29.07  -0.2   34.75   8.03   1.68   1.65  11.86  19.2    3.5
#   -4.27  -0.71  14.94   0.66  22.56  21.95  30.   114.3   19.5   42.06
#   39.93   7.32]

slice = stationname[height > 40]
print('shape of temp slice: %s' % repr(slice.shape))
print('SLIDE STATIONNAME',slice)

# shape of temp slice: (13,)
# SLIDE STATIONNAME ['D15-FA-1' 'P11-B' 'K14-FA-1C' 'A12-CPP' 'L9-FF-1' 'AWG-1' 'J6-A'
#  'HOORN-A' 'BUITENGAATS/BG-OHVS2' 'F3-FB-1' 'DEELEN'

# extract lat/lon values (in degrees) to numpy arrays
latvals = lat[:] 
lonvals = lon[:]

# a function to find the index of the point closest pt
# (in squared distance) to give lat/lon value.
def getclosest_ij(lats,lons,latpt,lonpt):
  print('lats.shape',lats.shape)
  # find squared distance of every point on grid
  dist_sq = (lats-latpt)**2 + (lons-lonpt)**2
  print('dist_sq:',dist_sq)
  # 1D index of minimum dist_sq element
  minindex_flattened = dist_sq.argmin()
  print('dist_sq.argmin:',minindex_flattened)
  # Get 2D index for latvals and lonvals arrays from 1D index
  return np.unravel_index(minindex_flattened, lats.shape)

iy_min, ix_min = getclosest_ij(latvals, lonvals, 52, 5)
print(iy_min)
print(ix_min)