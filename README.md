# BiciMAD Data Processing and Analysis

The **Open Data Portal of EMT Madrid** offers abundant information about transportation and mobility within the city, including data on the use of the city council's electric bike service, **BiciMAD**. This project provides tools to scrape, process, and analyze BiciMAD usage data, focusing on trips starting from **June 2021** onward.

## Dataset Overview

The dataset can be accessed on the EMT Madrid Open Data Portal:  
[https://opendata.emtmadrid.es/Home](https://opendata.emtmadrid.es/Home)  

Direct link to the BiciMAD data:  
[https://opendata.emtmadrid.es/Datos-estaticos/Datos-generales-(1)](https://opendata.emtmadrid.es/Datos-estaticos/Datos-generales-(1))  

The data consists of monthly usage records available as compressed ZIP files. Each ZIP file contains a CSV file with detailed trip information.  

### Naming Convention

The CSV files follow this naming format: `trips_YY_MM_monthName.csv`

- `YY`: Year (e.g., 21 for 2021)  
- `MM`: Month (e.g., 06 for June)  
- `monthName`: Name of the month in English  

⚠️ **Note:** The file for October 2021 contains errors and is excluded from this project.

---

## Data Fields (Metadata)

Each CSV file includes the following fields:  

- **`date` (Date):** The date of the trip.  
- **`idbike` (Bike ID):** Unique identifier of the bike used in the trip.  
- **`fleet` (Fleet):** The fleet to which the bike belongs.  
- **`trip_minutes` (Trip Duration in Minutes):** Total duration of the trip.  
- **`geolocation_unlock` (Unlock Geolocation):** Geographic coordinates of the trip's start location.  
- **`address_unlock` (Unlock Address):** Postal address where the bike was unlocked.  
- **`unlock_date` (Unlock Date and Time):** Exact timestamp when the trip started.  
- **`locktype` (Lock Type):** Bike's status before the trip (e.g., docked or freely locked).  
- **`unlocktype` (Unlock Type):** Bike's status after the trip started.  
- **`geolocation_lock` (Lock Geolocation):** Geographic coordinates of the trip's end location.  
- **`address_lock` (Lock Address):** Postal address where the bike was locked.  
- **`lock_date` (Lock Date and Time):** Exact timestamp when the trip ended.  
- **`station_unlock` (Unlock Station Number):** Station number where the bike was docked before the trip (if applicable).  
- **`dock_unlock` (Unlock Dock):** Dock number at the station before the trip (if applicable).  
- **`unlock_station_name` (Unlock Station Name):** Name of the station where the bike was docked before the trip (if applicable).  
- **`station_lock` (Lock Station Number):** Station number where the bike was docked after the trip (if applicable).  
- **`dock_lock` (Lock Dock):** Dock number at the station after the trip (if applicable).  
- **`lock_station_name` (Lock Station Name):** Name of the station where the bike was docked after the trip (if applicable).  

---

## Features

This project provides:  
- **Web Scraping Tools:** Automates the downloading of BiciMAD data directly from the Open Data Portal.  
- **Data Processing Pipelines:** Tools to clean, filter, and transform raw data into a usable format.  
- **Analysis Utilities:** Functions to generate insights, including trip statistics and fleet usage patterns.  

---

## Installation

1. Clone this repository:  
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
    ```bash
    cd bicimad-data
    ```
3. Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```