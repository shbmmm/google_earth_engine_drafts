import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from netCDF4 import Dataset

# Load the NetCDF file
filename = 'detection_results_with_vehicles.nc'  # Path to the NetCDF file
nc = Dataset(filename)

# Extract the required variables
latitudes = nc.variables['lat'][:]
longitudes = nc.variables['lon'][:]
cars_2 = nc.variables['cars_2'][:]

# Plotting
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': ccrs.PlateCarree()})

# Set extents for the plot
extent = [longitudes.min(), longitudes.max(), latitudes.min(), latitudes.max()]

# Function to plot the points
def plot_points(ax, lons, lats, values, title, label):
    ax.set_extent(extent)
    ax.add_feature(cfeature.OCEAN, zorder=0)
    ax.add_feature(cfeature.LAND, zorder=0)
    ax.add_feature(cfeature.COASTLINE, zorder=1)
    ax.add_feature(cfeature.BORDERS, linestyle=':', zorder=1)
    ax.add_feature(cfeature.LAKES, alpha=0.5, zorder=1)
    ax.add_feature(cfeature.RIVERS, zorder=1)
    # Adjust the size of the points based on the values
    sizes = 100 + (values / values.max() * 1000)  # Scale the sizes for better visibility
    scatter = ax.scatter(lons, lats, s=sizes, color='b', alpha=0.6, transform=ccrs.PlateCarree(), zorder=2)
    ax.set_title(title, fontsize=10, pad=20)
    ax.set_xlabel('Longitude', fontsize=10)
    ax.set_ylabel('Latitude', fontsize=10)
    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='black', alpha=0.5, linestyle='--')
    gl.right_labels = False
    gl.top_labels = False
    gl.left_labels = True
    gl.bottom_labels = True
    gl.xlocator = plt.MaxNLocator(nbins=5)
    gl.ylocator = plt.MaxNLocator(nbins=5)

# Plot for cars_2
plot_points(ax, longitudes, latitudes, cars_2, 'Vehicles Detected (Cars + Buses)', 'Number of Vehicles')

# Improve the appearance of the plot
plt.tight_layout(rect=[0, 0.1, 1, 0.95])
plt.show()

