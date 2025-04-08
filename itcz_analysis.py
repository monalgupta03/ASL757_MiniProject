import xarray as xr
import numpy as np
import pandas as pd

def compute_itcz_latitudes(filepath):
    ds = xr.open_dataset(filepath, decode_times=True)
    pr = ds['pr'].where(ds['pr'] != -9999.9)

    # Checking time
    if not np.issubdtype(pr['time'].dtype, np.datetime64):
        pr['time'] = pd.date_range(start="2010-01-01", periods=12, freq='MS')

    # Adding month as coordinate
    pr = pr.assign_coords(month=pr['time'].dt.month)

    # Defining DJF and JJA seasons
    djf = pr.where(pr['month'].isin([12, 1, 2]), drop=True)
    jja = pr.where(pr['month'].isin([6, 7, 8]), drop=True)

    # Computing zonal and seasonal mean
    djf_mean = djf.mean(dim=['time', 'lon'], skipna=True)
    jja_mean = jja.mean(dim=['time', 'lon'], skipna=True)

    # Getting latitude values
    lat = pr['lat']
    lon = ds['lon']

    # Finding ITCZ latitude as lat of max rainfall
    djf_itcz_lat = lat[djf_mean.argmax(dim='lat')].item()
    jja_itcz_lat = lat[jja_mean.argmax(dim='lat')].item()

    print(" DJF ITCZ Latitude:", djf_itcz_lat)
    print(" JJA ITCZ Latitude:", jja_itcz_lat)
    print(lon.values)

    return djf_mean, jja_mean, lat, lon, djf_itcz_lat, jja_itcz_lat


compute_itcz_latitudes("pr_Amon_TRMM_201001-201012.nc")