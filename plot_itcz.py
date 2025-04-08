from itcz_analysis import compute_itcz_latitudes
import matplotlib.pyplot as plt

djf_mean, jja_mean, lat, lon, djf_lat, jja_lat = compute_itcz_latitudes("pr_Amon_TRMM_201001-201012.nc")

def plot_itcz(mean_precip, lat, season, itcz_lat):
    plt.figure(figsize=(8, 4))
    plt.plot(lat, mean_precip, label=f'{season} Mean Precipitation')
    plt.axvline(itcz_lat, color='red', linestyle='--', label=f'{season} ITCZ Latitude')

    y_pos = max(mean_precip) * 0
    plt.text(itcz_lat + 0.5, y_pos, f"{itcz_lat:.2f}°", color='red', fontsize=10, verticalalignment='center', bbox=dict(facecolor='white', alpha=0.7, edgecolor='red'))

    plt.title(f"{season} ITCZ Position")
    plt.xlabel("Latitude")
    plt.ylabel("Precipitation (mm)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

print(" DJF ITCZ Latitude:", djf_lat)
print(" JJA ITCZ Latitude:", jja_lat)
plot_itcz(djf_mean, lat, "DJF", djf_lat)
plot_itcz(jja_mean, lat, "JJA", jja_lat)
