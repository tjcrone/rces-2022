#!/usr/bin/env python

from datetime import datetime
import pandas as pd
from pydap.client import open_url
from pydap.cas.urs import setup_session
import xarray as xr

username = 'tjcrone'
password = 'cJ#*V&e0eLNJnCf!M42kYc'

# create file list
start_date = datetime(2000,6,1)
end_date = datetime(2019, 12, 31)
dates = pd.date_range(start_date, end_date, freq='d')
baseurl='https://measures.gesdisc.eosdis.nasa.gov/opendap/GPCP/GPCPDAY.3.1/{0}/GPCPDAY_L3_{1}_V3.1.nc4'
urls = [ baseurl.format(d.year, d.strftime("%Y%m%d")) for d in dates]

# function to get single dataset
def get_dataset(url):
    session = setup_session(username, password, check_url=url)
    pydap_ds = open_url(url, session=session, timeout=600)
    store = xr.backends.PydapDataStore(pydap_ds)
    return xr.open_dataset(store, drop_variables=['time_bnds', 'probability_liquid_precip'])

#loop through list of urls
ds_list = []
for i, url in enumerate(urls):
    filename = url.split('/')[-1]
    print(filename)
    try:
        ds = get_dataset(url)
        ds_list.append(ds)
    except:
        print(f'*** {filename} not found ***')
    if i==1:
        break

# concatenate and write
if len(ds_list)>1:
    gpcp = xr.concat(ds_list, dim='time').drop_vars('bnds')
    gpcp.to_netcdf('gpcp.nc')
