import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy.ndimage import gaussian_filter

def compute_seasonal_itcz(filename):
    ds = xr.open_dataset(filename)

    pr = ds['pr']
    lat = ds['lat'].values
    lon = ds['lon'].values
    time = ds['time']

    # Handling missing values
    pr = pr.where(pr != -9999.9)

    # Assigning months
    months = np.tile(np.arange(1, 13), pr.sizes['time'] // 12)
    pr.coords['month'] = ('time', months)

    # Extracting DJF and JJA
    djf = pr.sel(time=pr['month'].isin([12, 1, 2]))
    jja = pr.sel(time=pr['month'].isin([6, 7, 8]))

    # Taking mean
    djf_mean = djf.mean(dim='time', skipna=True).values
    jja_mean = jja.mean(dim='time', skipna=True).values

    # Smoothening data
    djf_smoothed = gaussian_filter(djf_mean, sigma=1.5)
    jja_smoothed = gaussian_filter(jja_mean, sigma=1.5)

    # Restricting ITCZ detection to latitudes between -20° and 20°
    lat_mask = (lat >= -20) & (lat <= 20)
    lat_subset = lat[lat_mask]

    djf_smoothed_sub = djf_smoothed[lat_mask, :]
    jja_smoothed_sub = jja_smoothed[lat_mask, :]

    djf_itcz_idx = np.nanargmax(djf_smoothed_sub, axis=0)
    jja_itcz_idx = np.nanargmax(jja_smoothed_sub, axis=0)

    djf_itcz = lat_subset[djf_itcz_idx]
    jja_itcz = lat_subset[jja_itcz_idx]

    # Shifting longitudes from 0–360 to -180–180 (for better map view)
    lon_shifted = np.where(lon > 180, lon - 360, lon)
    sort_idx = np.argsort(lon_shifted)

    # Applying sorting to all longitude-dependent arrays
    lon_sorted = lon_shifted[sort_idx]
    djf_smoothed = djf_smoothed[:, sort_idx]
    jja_smoothed = jja_smoothed[:, sort_idx]
    djf_itcz = djf_itcz[sort_idx]
    jja_itcz = jja_itcz[sort_idx]

    return lon_sorted, lat, djf_smoothed, jja_smoothed, djf_itcz, jja_itcz

def plot_itcz_map(lon, lat, rainfall, itcz_latitudes, season):
    fig = plt.figure(figsize=(13, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    levels = np.linspace(np.nanmin(rainfall), np.nanmax(rainfall), 30)
    mesh = ax.contourf(lon, lat, rainfall, levels=levels, transform=ccrs.PlateCarree(), cmap='Blues', extend='both')
    plt.colorbar(mesh, ax=ax, orientation='vertical', label='Precipitation (mm)')

    ax.plot(lon, itcz_latitudes, color='red', linewidth=2, label='ITCZ')
    ax.axhline(0, color='black', linestyle='--', linewidth=1, label='Equator')

    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.set_title(f'{season} ITCZ Position and Rainfall')
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_xticks(np.arange(-180, 181, 30), crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(-30, 31, 10), crs=ccrs.PlateCarree())
    ax.gridlines(draw_labels=True)
    ax.legend()

    plt.tight_layout()
    plt.show()

filename = "pr_Amon_TRMM_201001-201012.nc"

lon, lat, djf_mean, jja_mean, djf_itcz, jja_itcz = compute_seasonal_itcz(filename)

plot_itcz_map(lon, lat, djf_mean, djf_itcz, "DJF (Winter)")
plot_itcz_map(lon, lat, jja_mean, jja_itcz, "JJA (Summer)")
