import pandas as pd
import xarray as xr

# Load the CSV file
file_path = '1km_by_1km - Sheet1.csv'
data = pd.read_csv(file_path)

# Rename the columns to something more meaningful
data.columns = ['lat', 'lon', 'variable1', 'variable2', 'variable3']

# Convert the DataFrame to an xarray Dataset
ds = xr.Dataset(
    {
        'variable1': (['lat', 'lon'], data.pivot(index='lat', columns='lon', values='variable1').values),
        'variable2': (['lat', 'lon'], data.pivot(index='lat', columns='lon', values='variable2').values),
        'variable3': (['lat', 'lon'], data.pivot(index='lat', columns='lon', values='variable3').values),
    },
    coords={
        'lat': data['lat'].unique(),
        'lon': data['lon'].unique()
    }
)

# Save the Dataset to a NetCDF file
ds.to_netcdf('output.nc')

