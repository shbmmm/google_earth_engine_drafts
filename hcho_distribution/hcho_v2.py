import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy.interpolate import griddata

# Load CSV file
filename = 'hcho_10by10_delhi.csv'  # Path to the uploaded file
data = pd.read_csv(filename)

# Extract columns
var1 = data.iloc[:, 2]
var2 = data.iloc[:, 3]
var3 = data.iloc[:, 4]
latitudes = data.iloc[:, 0]
longitudes = data.iloc[:, 1]

# Create a grid of points with higher resolution
lon_grid = np.linspace(longitudes.min(), longitudes.max(), 500)
lat_grid = np.linspace(latitudes.min(), latitudes.max(), 500)
lon_mesh, lat_mesh = np.meshgrid(lon_grid, lat_grid)

# Interpolate values onto the grid for var1, var2, and var3
grid_values_var1 = griddata((longitudes, latitudes), var1, (lon_mesh, lat_mesh), method='linear')
grid_values_var2 = griddata((longitudes, latitudes), var2, (lon_mesh, lat_mesh), method='linear')
grid_values_var3 = griddata((longitudes, latitudes), var3, (lon_mesh, lat_mesh), method='linear')

# Plotting
fig, axes = plt.subplots(1, 3, figsize=(20, 10), subplot_kw={'projection': ccrs.PlateCarree()})

# Set extents for all plots
extent = [longitudes.min(), longitudes.max(), latitudes.min(), latitudes.max()]

# Common function to plot each subplot
def plot_variable(ax, grid_values, title, label):
    ax.set_extent(extent)
    ax.add_feature(cfeature.OCEAN, zorder=0)
    ax.add_feature(cfeature.LAND, zorder=0)
    ax.add_feature(cfeature.COASTLINE, zorder=1)
    ax.add_feature(cfeature.BORDERS, linestyle=':', zorder=1)
    ax.add_feature(cfeature.LAKES, alpha=0.5, zorder=1)
    ax.add_feature(cfeature.RIVERS, zorder=1)
    num_levels = 50
    heatmap = ax.contourf(lon_mesh, lat_mesh, grid_values, levels=num_levels, transform=ccrs.PlateCarree(), cmap='jet', alpha=0.8, zorder=2)
    cbar = plt.colorbar(heatmap, ax=ax, orientation='horizontal', pad=0.15, aspect=50)
    cbar.set_label(label, fontsize=10)
    cbar.ax.tick_params(rotation=60)
    ax.set_title(title, fontsize=10, pad=20)
    ax.set_xlabel('Longitude', fontsize=3)
    ax.set_ylabel('Latitude', fontsize=3)
    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='black', alpha=0.5, linestyle='--')
    gl.right_labels = False
    gl.top_labels = True
    gl.left_labels = True
    gl.bottom_labels = False
    gl.xlocator = plt.MaxNLocator(nbins=5)
    gl.ylocator = plt.MaxNLocator(nbins=5)

# Plot for var1
plot_variable(axes[0], grid_values_var1, 'HCHO_slant_cnd', 'mol/m^2')

# Plot for var2
plot_variable(axes[1], grid_values_var2, 'tropospheric_HCHO_cnd', 'mol/m^2')

# Plot for var3
plot_variable(axes[2], grid_values_var3, 'tropospheric_HCHO_cnd_amf', 'mol/m^2')

# Improve the appearance of the plot
plt.tight_layout(rect=[0, 0.1, 1, 0.95])
plt.subplots_adjust(wspace=0.3)
plt.show()

