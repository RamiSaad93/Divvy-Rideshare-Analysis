# Divvy Bike-Share 2023 — Data Engineering and Exploratory Data Analysis

## Overview

This project analyzes **Divvy bike-share activity in Chicago during 2023**.

The project covers the complete workflow from raw data ingestion and cloud storage through data cleaning, feature engineering, weather enrichment, validation, and exploratory data analysis.

More than **5.6 million rides** are analyzed to understand how Divvy usage changes according to:

- Time of year
- Day of week
- Hour of day
- Membership type
- Bike type
- Ride duration
- Weather conditions
- Station-to-station routes

The project also establishes a reproducible AWS-based data pipeline that separates raw and processed data from the analytical notebooks.

The current version of the project focuses on **data preparation and exploratory analysis**.  
Machine-learning-based station demand prediction is planned as the next stage of the project.

---

# Project Objectives

The main objectives are to:

1. Build a reproducible ingestion pipeline for the 2023 Divvy trip data.
2. Store raw project data in AWS S3 rather than inside the Git repository.
3. Combine the monthly Divvy datasets into one analytical dataset.
4. Examine and clean invalid or inconsistent ride records.
5. Engineer useful temporal and ride-level features.
6. Enrich the Divvy data with daily Chicago weather information.
7. Validate the final processed dataset.
8. Analyze overall Divvy usage patterns.
9. Compare member and casual ride behavior.
10. Investigate bike-type usage and ride duration.
11. Examine the relationship between weather and daily demand.
12. Analyze station activity, routes, same-station trips, and directional station flow.
13. Prepare the analytical foundation for future machine-learning work.

---

# Data Sources

## Divvy Trip Data

The primary dataset is the official Divvy historical trip dataset:

https://divvy-tripdata.s3.amazonaws.com/index.html

The analysis uses all twelve monthly datasets for **2023**.

The monthly source files are ingested into the project's private AWS S3 raw-data layer using:

```text
src/ingest_divvy.py
```

---

## Weather Data

Daily Chicago weather information is retrieved from the **Open-Meteo API** during the data-preparation workflow.

The weather variables added to the Divvy dataset include:

- Mean temperature
- Minimum temperature
- Maximum temperature
- Precipitation
- Rainfall
- Snowfall
- Maximum wind speed

Weather observations are daily measurements and are merged with the ride data by date.

---

# Project Architecture

The project uses **AWS S3** as the primary storage layer for raw and processed data.

```text
Official Divvy Public Data
          |
          v
   src/ingest_divvy.py
          |
          v
   AWS S3 Raw Layer
          |
          v
01_data_preparation.ipynb
          |
          |-- Load and combine monthly data
          |-- Data-quality examination
          |-- Data cleaning
          |-- Feature engineering
          |-- Weather enrichment
          |-- Validation
          |
          v
 AWS S3 Processed Layer
          |
          |-- divvy_2023_processed.parquet
          |
          v
 02_divvy_analysis.ipynb
          |
          |-- Overall ridership
          |-- Temporal patterns
          |-- Member vs casual analysis
          |-- Bike-type analysis
          |-- Weather analysis
          |-- Station and route analysis
          |
          v
      Key Insights
```

This structure keeps large datasets outside GitHub while keeping the project code and notebooks reproducible.

---

# Repository Structure

```text
Final_Project/
│
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   │
│   └── processed/
│       └── .gitkeep
│
├── notebooks/
│   ├── 01_data_preparation.ipynb
│   └── 02_divvy_analysis.ipynb
│
├── src/
│   └── ingest_divvy.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

The actual raw and processed datasets are intentionally excluded from GitHub.

They are stored in AWS S3.

---

## Notebooks

### `01_data_preparation.ipynb`

Prepares the 2023 Divvy dataset by combining the monthly files, examining and cleaning data-quality issues, creating analytical features, adding daily weather information, validating the results, and exporting the final processed dataset to AWS S3 as Parquet.

### `02_divvy_analysis.ipynb`

Uses the processed dataset to explore overall ridership, temporal patterns, membership behavior, bike types, ride duration, weather relationships, station activity, routes, same-station trips, and station-flow imbalance.

---

# Key Findings and Conclusions

The 2023 Divvy analysis revealed clear differences in ridership according to time, membership type, weather, bike type, and station usage.

## 1. Overall Ridership

Divvy recorded **5,625,723 cleaned rides** during 2023, with an average ride duration of approximately **14.85 minutes**.

Members accounted for most activity:

- **Member rides:** 3,600,664 — **64.00%**
- **Casual rides:** 2,025,059 — **36.00%**

Members therefore generated almost two-thirds of all Divvy rides during the year.

---

## 2. Ridership Is Strongly Seasonal

Seasonality was one of the clearest patterns in the dataset.

- **Summer:** 39.53% of annual rides
- **Winter:** 10.56% of annual rides

Summer therefore accounted for almost four times as much activity as winter.

This seasonal pattern was also reflected in the weather analysis, particularly the strong relationship between temperature and daily ridership.

---

## 3. Weekday and Weekend Demand Differ More in Timing Than in Daily Volume

Although **71.56% of all rides occurred on weekdays**, this is partly explained by the fact that there are five weekdays compared with only two weekend days.

When average rides per day were compared, weekday and weekend volumes were relatively similar.

The larger difference was in the **shape and timing of demand**:

- Weekdays showed pronounced morning and evening peaks.
- Weekend demand was distributed more broadly through the daytime.
- The strongest overall demand occurred around **17:00**.

This means that the distinction between weekday and weekend usage is not simply about total ride volume, but also about **when rides occur and which types of riders generate them**.

---

## 4. Member and Casual Rides Show Different Usage Patterns

Member and casual rides differed consistently across multiple parts of the analysis.

### Member rides tended to show:

- Greater concentration during weekdays
- Stronger morning and evening peak-hour patterns
- More regular activity throughout the year
- Shorter average ride durations

### Casual rides tended to show:

- Greater weekend concentration
- Stronger seasonal variation
- More daytime and afternoon activity
- Longer average ride durations
- Greater sensitivity to adverse weather
- Much higher rates of same-station trips

Average ride duration was:

| Membership Type | Average Ride Duration |
|---|---:|
| Member | 12.04 minutes |
| Casual | 19.84 minutes |

Casual rides therefore lasted substantially longer on average.

These patterns are consistent with different types of travel behavior, but the dataset does not contain trip-purpose information, so commuting, recreation, or tourism cannot be confirmed directly.

---

## 5. Bike Usage Is Relatively Balanced, but Ride Duration Differs

The original Divvy dataset contains three bike categories:

| Bike Type | Share of Rides |
|---|---:|
| Electric bike | 51.55% |
| Classic bike | 47.11% |
| Docked bike | 1.34% |

Electric and classic bikes therefore accounted for almost all rides, with neither type overwhelmingly dominating usage.

The stronger difference appeared in **ride duration**.

Classic-bike rides generally lasted longer than electric-bike rides, particularly among casual rides.

This suggests that bike type may be more closely associated with **how long rides last** than with large differences in overall usage share.

---

## 6. Weather Is Strongly Associated With Daily Ridership

Weather showed clear relationships with daily Divvy demand.

### Temperature

Mean daily temperature showed the strongest weather relationship:

**r = 0.874**

The relationship was also strong within both membership groups:

- Member rides: **r = 0.834**
- Casual rides: **r = 0.824**

Higher-temperature days were therefore generally associated with substantially higher ride demand.

### Rain

Average daily ridership was approximately **7.5% lower on rainy days** than on dry days.

The difference was:

- Member rides: approximately **5.63% lower**
- Casual rides: approximately **10.63% lower**

### Snow

Snow days showed much lower ridership than days without snowfall:

- Member rides: approximately **55.00% lower**
- Casual rides: approximately **77.21% lower**

### Wind

Maximum daily wind speed showed a moderate negative correlation with daily ridership:

**r = -0.362**

Overall, temperature had the strongest observed weather relationship, while rain, snow, and stronger winds were associated with lower ridership.

Casual demand showed larger differences under rainy and snowy conditions than member demand, suggesting that casual ridership is more sensitive to adverse precipitation conditions.

These relationships should be interpreted as associations rather than isolated causal effects because weather variables are also related to season and to one another.

---

## 7. Member and Casual Riders Use the Station Network Differently

Station usage differed substantially between membership groups.

Only one station appeared in both groups' top-ten starting-station rankings:

**Wells St & Concord Ln**

The differences were also visible in the most frequently used station-to-station routes.

Casual rides were more strongly concentrated around several lakefront, central-city, and recreational locations, while member rides showed a different set of high-activity stations and routes.

This indicates that the two membership groups do not simply differ in when they ride; they also differ considerably in **where their trips occur**.

---

## 8. Major Stations Often Function as Both Origins and Destinations

Both start and end station information was available for approximately **75.46% of rides**, providing more than **4.2 million trips** for complete route analysis.

The busiest station for both departures and arrivals was:

**Streeter Dr & Grand Ave**

with:

- **61,832 departures**
- **62,992 arrivals**

Nine of the ten busiest departure stations also appeared among the ten busiest arrival stations.

This indicates that the highest-activity stations generally serve as both major origins and major destinations within the network.

---

## 9. Same-Station Trips Are Much More Common Among Casual Rides

Same-station trips represented **4.51%** of rides with valid start and end station information.

However, the difference between membership groups was large:

| Membership Type | Same-Station Trip Share |
|---|---:|
| Member | 2.52% |
| Casual | 8.13% |

Same-station trips were therefore more than **three times as common among casual rides**.

This is one of the clearest behavioral differences between member and casual station usage.

---

## 10. Station Activity and Directional Flow Are Different Characteristics

Some stations showed substantial differences between the number of departures and arrivals.

For example:

- **Columbus Dr & Randolph St:** 3,492 more departures than arrivals
- **DuSable Lake Shore Dr & North Blvd:** 3,388 more arrivals than departures

At the same time, some very busy stations maintained relatively balanced flows.

This shows that:

> **High station activity and directional imbalance are separate characteristics of station usage.**

A station can be extremely busy without having a large arrival/departure imbalance, while another station may have lower total activity but a much stronger directional pattern.

Because station capacity, bike availability, dock availability, and operational rebalancing information are not included in the dataset, these imbalances cannot by themselves be interpreted as evidence that a station requires rebalancing.

---

## Overall Conclusion

The analysis shows that Divvy demand during 2023 was shaped by several interacting factors:

- **Time of year**
- **Day of week**
- **Time of day**
- **Membership type**
- **Weather**
- **Bike type**
- **Station location**
- **Station and route patternss**

Members generally showed more regular weekday and peak-hour behavior, while casual rides were more seasonal, more weekend-oriented, longer in duration, more sensitive to adverse weather, and considerably more likely to begin and end at the same station.

Weather, particularly temperature, showed a strong relationship with daily ride demand, while station and route analysis demonstrated that demand also varies substantially across the Divvy network.

Together, these findings provide the analytical foundation for the next stage of the project: **predicting daily departure demand at individual Divvy stations using temporal, weather, station, and historical-demand features.**

---

# Limitations

Several limitations should be considered when interpreting the results.

### No Rider Identifier

The dataset contains individual trips rather than individual users.

Therefore, it is possible to compare **member rides and casual rides**, but not the number or behavior of unique riders.

### Missing Station Information

Some rides do not contain complete start or end station information.

Station and route analyses therefore use only records where the required station fields are available.

### Trip Purpose Is Unknown

The dataset does not indicate why a trip was taken.

Patterns that resemble commuting, recreation, or tourism should therefore be interpreted as possible explanations rather than confirmed trip purposes.

### Weather Results Are Associations

Weather variables are related to each other and to season.

The analysis therefore identifies statistical relationships rather than isolated causal effects.

### No Station Capacity or Rebalancing Information

Station capacity, dock availability, bike availability, and operational rebalancing data are not available.

Arrival/departure imbalance alone cannot determine whether operational intervention is required.

### Single Year

The current project analyzes only 2023.

Including multiple years could help determine whether the observed patterns remain stable over time.

---

# Technologies Used

## Programming and Analysis

- Python
- pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

## Data Engineering

- AWS S3
- boto3
- PyArrow
- Parquet

## External Data

- Divvy public trip dataset
- Open-Meteo weather API

## Version Control

- Git
- GitHub

---

# Environment Setup

Clone the repository:

```bash
git clone https://github.com/RamiSaad93/Divvy-Rideshare-Analysis
cd Final_Project
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

# AWS Configuration

The project uses `boto3` to access the private AWS S3 data layer.

AWS credentials are **not included in the repository**.

To reproduce the complete pipeline, a valid AWS CLI profile with access to the required S3 bucket must be configured locally.

The AWS profile or S3 configuration may need to be adjusted when running the project in another environment.

---

# Running the Project

The intended execution order is:

```text
1. src/ingest_divvy.py
        ↓
2. notebooks/01_data_preparation.ipynb
        ↓
3. notebooks/02_divvy_analysis.ipynb
```

The ingestion script transfers the source files to AWS S3, the first notebook prepares the analytical dataset, and the second notebook performs the exploratory analysis.

---

# Data Storage

Large datasets are intentionally excluded from GitHub.

The project separates:

```text
Code / notebooks / documentation → GitHub
Raw and processed datasets       → AWS S3
```

The local `data/raw/` and `data/processed/` directories are retained only to document the intended repository structure.

---

# Project Status

### Completed

- Raw-data ingestion
- AWS S3 raw and processed data workflow
- Data cleaning and validation
- Feature engineering
- Weather enrichment
- Processed Parquet dataset
- Temporal analysis
- Member vs casual analysis
- Bike-type analysis
- Weather analysis
- Station analysis
- Route analysis
- Same-station analysis
- Arrival/departure flow analysis

---

# Future Work — Machine Learning

The next stage of the project will focus on predicting:

> **The number of rides departing from a Divvy station on a given day.**

The planned machine-learning dataset will use one observation per:

```text
station × date
```

Potential features include:

- Calendar and temporal information
- Weather conditions
- Station information
- Geographic information
- Historical station demand

Potential historical features may include previous-day demand, weekly lagged demand, and rolling averages.

The final feature set, station-selection strategy, train/test methodology, and model selection will be determined during the ML development stage while carefully avoiding future-data leakage.

The machine-learning work will be developed separately before being merged into the completed main project.