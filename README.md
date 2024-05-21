
# 📊 Seismic Data Interpolation API

Welcome to the Seismic Data Interpolation API! This API allows you to interpolate seismic data values (SDS and SD1) at specific geographic coordinates using Inverse Distance Weighting (IDW).

## 🚀 Features

- 🌍 Interpolates seismic data based on latitude and longitude
- 🗃️ Supports multiple site classes (e.g., A, B, C, D, E)
- ⚡ Fast spatial queries using KDTree
- 🔍 Easy to use GET endpoint for data retrieval

## 📋 Requirements

- Python 3.7+
- Flask
- pandas
- numpy
- scipy

## 📦 Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/dev-nolant/seismic-data-interpolation-api.git
    cd seismic-data-interpolation-api
    ```

2. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Place your `ConUS_SD1.csv` and `ConUS_SDS.csv` files in the project directory.

## 🛠️ Usage

1. Run the Flask application:

    ```sh
    python app.py
    ```

2. Make a GET request to the `/search_csv` endpoint with the required parameters:

    ```sh
    curl "http://127.0.0.1:5000/search_csv?latitude=34.05&longitude=-118.25&siteClass=B"
    ```

    Example response:

    ```json
    {
        "Latitude": 34.05,
        "Longitude": -118.25,
        "SDS": 1.23,
        "SD1": 0.45,
        "SiteClass": "B"
    }
    ```

## 🧩 API Endpoint

### `/search_csv`

- **Method**: GET
- **Parameters**:
    - `latitude` (float): Latitude of the point of interest
    - `longitude` (float): Longitude of the point of interest
    - `siteClass` (string): Site class (e.g., A, B, C, D, E)
- **Response**:
    - `Latitude` (float): Latitude of the queried point
    - `Longitude` (float): Longitude of the queried point
    - `SDS` (float): Interpolated SDS value
    - `SD1` (float): Interpolated SD1 value
    - `SiteClass` (string): Site class used for interpolation

## ⚠️ Error Handling

- 400 Bad Request: Returned when required parameters are missing or invalid.
- 500 Internal Server Error: Returned when there is an unexpected error on the server side.

## 🤝 Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch-name`.
3. Make your changes and commit them: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-branch-name`.
5. Submit a pull request.

## 📄 License

This project is licensed under the Creative Commons Zero v1.0 Universal License.


Happy interpolating! 🎉
