from flask import Flask, jsonify, request, abort
import csv
import pandas as pd
import numpy as np
from scipy.spatial import cKDTree

app = Flask(__name__)

data_sd1 = pd.read_csv('ConUS_SD1.csv')
data_sds = pd.read_csv('ConUS_SDS.csv')

# Dictionary mapping the file names to their respective DataFrame
combined_data = pd.concat([data_sd1, data_sds], ignore_index=True)



def idw_interpolation(x, z, xi, k=12, p=3):
    # Ensure there are no NaN values in the input data
    valid_mask = ~np.isnan(z)
    x = x[valid_mask]
    z = z[valid_mask]

    # Check if enough neighbors are available
    if k > len(z):
        raise ValueError("Requested more neighbors than available data points.")

    # Create a KDTree for fast spatial searching
    tree = cKDTree(x)

    # Find the indices of the k nearest neighbors
    distances, indices = tree.query(xi, k=k)

    # Handle the case where distance is zero (query point coincides with a data point)
    with np.errstate(divide='ignore'):
        weights = 1.0 / np.power(distances, p)
        # Inf weights occur where distances are zero. Set them to a high number (instead of Inf)
        weights[distances == 0] = 1e10

    # Normalize weights to sum to one
    weight_sums = np.sum(weights, axis=1)
    valid_weights_mask = weight_sums > 0
    weights[valid_weights_mask] /= weight_sums[valid_weights_mask][:, None]

    # If all weight sums are zero, return NaN
    if not np.any(valid_weights_mask):
        return np.array([np.nan])

    # Multiply the weights for each interpolated point by all observed Z-values
    zi = np.sum(weights * z[indices], axis=1)

    # Return only valid zi or NaN if not valid
    zi[~valid_weights_mask] = np.nan
    return zi



def get_interpolated_value(latitude, longitude, site_class, value_prefix, data):
    # Dynamically creating the column name based on the site class and value prefix (SDS or SD1)
    value_column = f'{value_prefix}_{site_class}' if f'{value_prefix}_{site_class}' in data.columns else f'{value_prefix}_Default'

    if value_column not in data.columns:
        raise ValueError(f"Site class column {value_column} does not exist in the data.")

    # Extract the relevant column values
    values = data[value_column].values

    # Extract the latitude and longitude for interpolation
    coords = data[['Latitude', 'Longitude']].values

    # Perform IDW interpolation
    interpolated_value = idw_interpolation(
        x=coords,
        z=values,
        xi=np.array([[latitude, longitude]]),
        k=12,  # considering the 12 nearest neighbors
        p=2    # power parameter, commonly 2 is used as it is the inverse-square law
    )

    # Since we expect one value, extract the single value from the array
    return interpolated_value[0]





@app.route('/search_csv', methods=['GET'])
def search_csv():
    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)
    site_class = request.args.get('siteClass')

    if latitude is None or longitude is None or site_class is None:
        abort(400, description="Invalid request: Parameters 'latitude', 'longitude', and 'siteClass' are required.")

    try:
        # Perform the interpolation for both SDS and SD1 using the combined data
        interpolated_sds = get_interpolated_value(latitude, longitude, site_class, 'SDS', combined_data)
        interpolated_sd1 = get_interpolated_value(latitude, longitude, site_class, 'SD1', combined_data)

        # Round the interpolated values and construct the result
        result = {
            'Latitude': latitude,
            'Longitude': longitude,
            'SDS': round(interpolated_sds, 2),
            'SD1': round(interpolated_sd1, 2),
            'SiteClass': site_class
        }
        return jsonify(result)

    except ValueError as e:
        abort(400, description=str(e))
    except Exception as e:
        abort(500, description=str(e))

if __name__ == '__main__':
    app.run(debug=True)
