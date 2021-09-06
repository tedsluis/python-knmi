
# https://www.earthinversion.com/utilities/reading-NetCDF4-data-in-python/

import netCDF4
import numpy as np
import re
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys
from datetime import datetime, timedelta
from pathlib import Path
import requests
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel("INFO")

api_url = "https://api.dataplatform.knmi.nl/open-data"
api_version = "v1"


def get_data():
    # Parameters
    api_key = "eyJvcmciOiI1ZTU1NGUxOTI3NGE5NjAwMDEyYTNlYjEiLCJpZCI6ImNjOWE2YjM3ZjVhODQwMDZiMWIzZGIzZDRjYzVjODFiIiwiaCI6Im11cm11cjEyOCJ9"
    dataset_name = "Actuele10mindataKNMIstations"
    dataset_version = "2"

    # Use get file to retrieve a file from one hour ago.
    # Filename format for this dataset equals KMDS__OPER_P___10M_OBS_L2_YYYYMMDDHHMM.nc,
    # where the minutes are increased in steps of 10.
    timestamp_now = datetime.utcnow()
    timestamp_one_hour_ago = (
        timestamp_now
        - timedelta(hours=1)
        - timedelta(minutes=timestamp_now.minute % 10)
    )
    filename = (
        f"KMDS__OPER_P___10M_OBS_L2_{timestamp_one_hour_ago.strftime('%Y%m%d%H%M')}.nc"
    )

    logger.info(f"Current time: {timestamp_now}")
    logger.info(f"One hour ago: {timestamp_one_hour_ago}")
    logger.info(f"Dataset file to download: {filename}")

    endpoint = f"{api_url}/{api_version}/datasets/{dataset_name}/versions/{dataset_version}/files/{filename}/url"
    get_file_response = requests.get(endpoint, headers={"Authorization": api_key})

    if get_file_response.status_code != 200:
        logger.error("Unable to retrieve download url for file")
        logger.error(get_file_response.text)
        sys.exit(1)

    logger.info(
        f"Successfully retrieved temporary download URL for dataset file {filename}"
    )

    download_url = get_file_response.json().get("temporaryDownloadUrl")
    dataset_file_response = requests.get(download_url)

    # Write dataset file to disk
    p = Path(filename)
    p.write_bytes(dataset_file_response.content)

    logger.info(f"Successfully downloaded dataset file to {p}")

    # Check logging for deprecation
    if "X-KNMI-Deprecation" in get_file_response.headers:
        deprecation_message = get_file_response.headers.get("X-KNMI-Deprecation")
        logger.warning(f"Deprecation message: {deprecation_message}")

    return filename

_dataset_filename=get_data()


f = netCDF4.Dataset(_dataset_filename)
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
#     variables(dimensions): <class 'str'> station(station), float64 time(time), <class 'str'> stationname(station), float64 lat(station), float64 lon(station), 
# float64 height(station), float64 dd(station, time), float64 ff(station, time), float64 gff(station, time), float64 ta(station, time), float64 rh(station, time), 
# float64 pp(station, time), float64 zm(station, time), float64 D1H(station, time), float64 dr(station, time), float64 hc(station, time), float64 hc1(station, time), 
# float64 hc2(station, time), float64 hc3(station, time), float64 nc(station, time), float64 nc1(station, time), float64 nc2(station, time), float64 nc3(station, time), 
# float64 pg(station, time), float64 pr(station, time), float64 qg(station, time), float64 R12H(station, time), float64 R1H(station, time), float64 R24H(station, time), 
# float64 R6H(station, time), float64 rg(station, time), float64 ss(station, time), float64 td(station, time), float64 tgn(station, time), float64 Tgn12(station, time), 
# float64 Tgn14(station, time), float64 Tgn6(station, time), float64 tn(station, time), float64 Tn12(station, time), float64 Tn14(station, time), float64 Tn6(station, time), 
# float64 tx(station, time), float64 Tx12(station, time), float64 Tx24(station, time), float64 Tx6(station, time), float64 ww(station, time), float64 pwc(station, time), 
# float64 ww-10(station, time), float64 ts1(station, time), float64 ts2(station, time), |S1 iso_dataset(), |S1 product(), |S1 projection()
#     groups: 

print('KEYS:', f.variables.keys()) 

# dict_keys(['station', 'time', 'stationname', 'lat', 'lon', 'height', 'dd', 'ff', 'gff', 'ta', 'rh', 'pp', 'zm', 
# 'D1H', 'dr', 'hc', 'hc1', 'hc2', 'hc3', 'nc', 'nc1', 'nc2', 'nc3', 'pg', 'pr', 'qg', 'R12H', 'R1H', 'R24H', 'R6H',
# 'rg', 'ss', 'td', 'tgn', 'Tgn12', 'Tgn14', 'Tgn6', 'tn', 'Tn12', 'Tn14', 'Tn6', 'tx', 'Tx12', 'Tx24', 'Tx6', 'ww', 
# 'pwc', 'ww-10', 'ts1', 'ts2', 'iso_dataset', 'product', 'projection'])

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

time = time_class[:]
# dtime = netCDF4.num2date(time_var[:],time_var.units)
print('time:',time)
print('netCDF4.num2date:',netCDF4.num2date(time_class[:],time_class.units))
#_dtime = netCDF4.num2date(time_class[:],time_class.units)
_datetime = netCDF4.num2date(time_class[0],time_class.units).strftime('%Y-%b-%d %H:%M')
print('num2date -> strftime:',_datetime)

# time: [2.2575456e+09]
# netCDF4.num2date: [cftime.DatetimeGregorian(2021, 7, 16, 0, 0, 0, 0, has_year_zero=False)]
# num2date -> strftime: 2021-Jul-16 00:00

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

_variables = f.variables.keys()
for _var in _variables:
  lijst=f.variables[_var][:]
  print('var',_var)
  if not re.match('(iso_dataset|product|projection)', _var):
    _lijst=" ".join(str(i) for i in lijst)
    print('\n|----',_var,'---->',f.variables[_var],'\n   >---->',_lijst,'>---|')

station_class = f.variables['station']
station = station_class[:]
print('STATION:',station)

tn = f.variables['tn'][:]
dd = f.variables['dd'][:]
ff = f.variables['ff'][:]
lon = f.variables['lon'][:]
lat = f.variables['lat'][:]

print('TN:', slice)

for _station in f.variables['station'][:]:
  _stationname = stationname[station == _station][0]
  _tn = tn[station == _station][0][0]
  _height = height[station == _station][0]
  _dd = dd[station == _station][0][0]
  _ff = ff[station == _station][0][0]
  _lon = lon[station == _station][0]
  _lat = lat[station == _station][0]
  print('stationname:', _stationname, 'tn:',_tn, 'height:',_height, 'dd:',_dd, 'ff:',_ff,'lon:',_lon, 'lat:',_lat)

_long_names={'key': 'value'}
_units={'key': 'value'}
_index_key={}
_key=0
for _variable in _variables:
  _index_key[_variable]=_key
  print('->>>>>>>>>>>>>>>',_variable, _key)
  _key+=1  
  if not re.match('(iso_dataset|product|projection|ts1|ts2)', _variable):
    _class = f.variables[_variable] # station variable
    _string=str(_class)
    _string=_string.replace('\n','#')
    _long_name = re.search('.*long_name:\s([^#]+)#.*', _string)
    if _long_name:
      _long_name=_long_name.group(1)
    else:
      _long_name=""
    _unit = re.search('.*units:\s([^#]+)#.*', _string)
    if _unit:
      _unit=_unit.group(1)
    else:
      _unit=""
    _long_names[_variable]=_long_name
    _units[_variable]=_unit
    print('long_name:',_long_name,'units:',_unit)

_cat={}
_cat['station info']=['station','time','lat','lon','height']
_cat['basics']=['ta','rh','pp','zm']
_cat['wind']=['dd','ff','gff']
_cat['wolken']=['hc','hc1','hc2','hc3','nc','nc1','nc2','nc3']
_cat['neerslag']=['D1H','dr','pg','pr','R12H','R1H','R24H','R6H','rg']
_cat['zon']=['qg','ss']
_cat['temperatuur']=['td','tgn','Tgn12','Tgn14','Tgn6','tn','Tn12','Tn14','Tn6','tx','Tx12','Tx24','Tx6']
_cat['weer code']=['ww','pwc','ww-10']

def mapping_data(_variable):
    _lon, _lat, _value, _stationname = [], [], [], []
    for _station in f.variables['station'][:]:
      _values=f.variables[_variable][:]
      if re.match('(lat|lon|height|stationname|station|iso_dataset|product|projection)', _variable):
        _v=_values[station == _station][0]
      elif re.match('(time)', _variable):
        _v=_datetime
      else:
        _v=_values[station == _station][0][0]
      _value.append(_v)
      _sn=stationname[station == _station][0]
      for _afkorting in [' AWS',' VK',' AP',' WP']:
        _sn=_sn.replace(_afkorting,'')
      _stationname.append(_sn)
      _lon.append(lon[station == _station][0])
      _lat.append(lat[station == _station][0])
      print(_lon, _lat, _value)
    return _lon, _lat, _value, _stationname

def createmap(_variable):

    fig, ax = plt.subplots()
    _lon, _lat, _value, _stationname = mapping_data(_variable)
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html
    ax.scatter(_lon, _lat, s=1, edgecolors='red', linewidths=0.3, zorder=2)
    for i in range(len(_lon)):
        #ax.annotate(_stationname[i], xy=(_lon[i],_lat[i]+0.05))
    # for i in range(len(_stationname)):
        ax.annotate(str(_value[i])+'\n'+_stationname[i], xy=(_lon[i],_lat[i]),fontsize=2)
        # ax.annotate(_dd[i], xy=(_lon[i],_lat[i]), xytext=(_lon[i]+0.2,_lat[i]+0.1),arrowprops=dict(facecolor='black', shrink=0.1),)
    # for i in range(len(atlas_data)):
    #     ax.annotate(atlas_data[i][0], xy=(atlas_data[i][2],atlas_data[i][1]), xytext=(atlas_data[i][2],atlas_data[i][1]+0.1),arrowprops=dict(facecolor='black', shrink=0.01),)

    #ax.imshow(mpimg.imread('https://i.ibb.co/8xKy10y/Kaart-Nederland-grijs.png'), extent=(  3.2674058600277225, 7.222483905734761, 50.74706431634171, 53.54700518476279), aspect=1.5, zorder=1)
    ax.imshow(mpimg.imread('https://i.ibb.co/K7bTd8p/Kaart-Nederland-groen.png'), extent=(  3.2674058600277225, 7.222483905734761, 50.74706431634171, 53.54700518476279), aspect=1.5, zorder=1)
    _filename=_variable+'.png'
    #fig.savefig(_filename, dpi=fig.dpi)
    _title=_long_names[_variable]+' ('+_variable+')\n'+_units[_variable]
    ax.text(3.3,53.5, _title,fontsize=5, ha="left", va='top', color='.5')
    fig.savefig(_filename, dpi=400, bbox_inches = 'tight')
    #plt.show()

for _variable in _variables:
   if not re.match('(iso_dataset|product|projection|time|ts1|ts2)', _variable):
     print('_variable',_variable)
     createmap(_variable)

# _css='''    <style>
# .verticalTableHeader {
#   writing-mode: vertical-lr;

#   white-space: nowrap;
#   -webkit-writing-mode: vertical-lr;
#   -ms-writing-mode: vertical-lr;
#   height="300px";  
# }
# .mono {
#   font-family:monospace;
# }
#     </style>'''

with open('index.html', 'w') as p:

  print('''
<html>
  <head>
    <style>
.verticalTableHeader {
  writing-mode: vertical-lr;

  white-space: nowrap;
  -webkit-writing-mode: vertical-lr;
  -ms-writing-mode: vertical-lr;
  height="300px";  
}
.mono {
  font-family:monospace;
}
    </style>
  </head>
  <body>''', file=p)
  # Knoppen alles of niets
  _show_button=''
  _hide_button=''
  _all_vars=[]
  for _category, _vars in _cat.items():
    _all_vars+=_vars
    for _var in _vars:
      _show_button+='''tf.extension('colsVisibility').showCol('''+str(_index_key[_var])+'''); '''
      _hide_button+='''tf.extension('colsVisibility').hideCol('''+str(_index_key[_var])+'''); '''
  _title=', '.join(_all_vars)+' (columns: '+", ".join(str(_index_key[i]) for i in _all_vars)+')'
  _show_button+='''">+ alles</button>'''
  _hide_button+='''">- niets</button>'''
  print('''<button class="mono" title="'''+'show: '+_title+'''" onclick="javascript: '''+_show_button, file=p)
  print('''<button class="mono" title="'''+'hide: '+_title+'''" onclick="javascript: '''+_hide_button, file=p)
  print('</br>', file=p)
  # categorieen
  for _category, _vars in _cat.items():
    _show_button=''
    _hide_button=''
    for _var in _vars:
      print('_category',_category,'_variable',_var)
      print('index_key',_index_key[_var])
      _show_button+='''tf.extension('colsVisibility').showCol('''+str(_index_key[_var])+'''); '''
      _hide_button+='''tf.extension('colsVisibility').hideCol('''+str(_index_key[_var])+'''); '''
    # show en hide knoppen  
    _title=', '.join(_vars)+' (columns: '+", ".join(str(_index_key[i]) for i in _vars)+')'
    _show_button+='''">+ '''+_category+'''</button>'''
    _hide_button+='''">- '''+_category+'''</button> >===> '''
    print('''<button class="mono" title="'''+'show: '+_title+'''" onclick="javascript: '''+_show_button, file=p)
    print('''<button class="mono" title="'''+'hide: '+_title+'''" onclick="javascript: '''+_hide_button, file=p)
    # toggle knoppen
    for _var in _vars:
      if not re.match('(iso_dataset|product|projection|ts1|ts2)', _var):
        _title='toggle:'+_long_names[_var]+' ('+_units[_var]+') (column: '+str(_index_key[_var])+')'
        print('''<button title="''',_title,'''" onclick="javascript: tf.extension('colsVisibility').toggleCol(''',_index_key[_var],''');">''',_var,'''</button>''', file=p)      
    print('</br>', file=p)
  # tabel
  print('    <table border="1" id="knmi">', file=p)
  print('      <tr>', file=p)
  # verticale kolom headers
  for _var in _variables:
    if not re.match('(iso_dataset|product|projection|ts1|ts2)', _var):
      _header=_long_names[_var]
      _unit=""
      if _units[_var] != "":
        _unit=' ('+_units[_var]+')'
        _header+=_unit
      print('        <th class="verticalTableHeader" title="'+_var+' '+_unit+' (column:'+str(_index_key[_var])+')">',_header,'</th>', file=p)
  print('      </tr>', file=p)
  # horizontale kolom headers
  print('      <tr>', file=p)
  for _var in _variables:
    if not re.match('(iso_dataset|product|projection|ts1|ts2)', _var):
      _unit=""
      if _units[_var] != "":
        _unit+=' ('+_units[_var]+')'
      print('        <th title="'+_long_names[_var]+_unit+' (column:'+str(_index_key[_var])+')">',_var,'</th>', file=p)
  print('      </tr>', file=p)

  for _station in f.variables['station'][:]:
    _stationname = stationname[station == _station][0]
    print('      <tr>', file=p)
    # tabel waarden
    for _var in _variables:
      if not re.match('(iso_dataset|product|projection|ts1|ts2)', _var):
        _values=f.variables[_var][:]
        if re.match('(lat|lon|height|stationname|station)', _var):
          _value=str(_values[station == _station][0])
        elif re.match('(time)', _var):
          _value=_datetime
        else:
          _value=str(_values[station == _station][0][0])
        _title=_stationname+':'+_var+' ('+_long_names[_var]+') :'+ _value+' '+ _units[_var]
        print('''        <td title="'''+_title+'''"><a href="'''+_var+'''.html">'''+_value+'''</a></td>''', file=p)
    print('      </tr>', file=p)
  print('    </table>', file=p)

  print('''
<script src="tablefilter/tablefilter.js"></script>

<script data-config>
var tfConfig = {
    base_path: 'tablefilter/',
    filters_row_index: 0,
    rows_counter: {
                text: 'Items: '
    },
    btn_reset: true,
    status_bar: true,
    extensions: [{
              name: 'colsVisibility',
              at_start: [0,1,3,4,5],
              text: 'Columns: ',
              public_toolbar_position: 'left',
              enable_tick_all: true
          }, {
              name: 'sort'
        }]
};
var tf = new TableFilter('knmi', tfConfig);
tf.init();
</script>
</body>
</html>''',file=p)
p.close()

for _variable in _variables:
  if not re.match('(iso_dataset|product|projection|ts1|ts2)', _variable):
    _image_name=_variable+'.png'
    _page_name=_variable+'.html'
    print('_image_name:',_image_name,'_page_name:',_page_name)
    with open(_page_name, 'w') as p:
      print('''
<html>
  <head>
    <style>
.mono {
  font-family:monospace;
}
    </style>
  </head>
  <body>
    <img src="'''+_image_name+'''" alt="">
  </body>''', file=p)
    p.close()