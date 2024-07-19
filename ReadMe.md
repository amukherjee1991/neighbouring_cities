# Major Cities API

This project provides a FastAPI-based web service to list major cities (with a population of more than 1 million) and to get neighboring cities for a specified main city. The data is sourced from a CSV file.

## Features

- **/major_cities**: Returns a list of major cities with a population of more than 1 million.
- **/city/{main_city}**: Returns details of a specified major city, including its neighboring cities.

## Setup and Installation

1. **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the FastAPI server**:
    ```bash
    uvicorn app:app --reload
    ```

4. **Access the API**:
    - Major cities by state: `http://127.0.0.1:8000/{state}`
    - Major cities: `http://127.0.0.1:8000/major_cities`
    - Specific city details: `http://127.0.0.1:8000/city/{main_city}`


## Files

- **app.py**: Main application script.
- **uscities.csv**: CSV file containing city data.
- **requirements.txt**: List of dependencies.
- **README.md**: Project documentation.

## Dependencies

- fastapi
- pandas
- requests
- uvicorn

