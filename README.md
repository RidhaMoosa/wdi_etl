# WDI ETL Pipeline

A comprehensive ETL (Extract, Transform, Load) pipeline for processing World Development Indicators (WDI) data from the World Bank API. This project automates the collection, processing, and storage of global development analytics data.

## Overview

This project provides an automated system for:
- **Extracting** development indicator data from World Bank APIs
- **Transforming** raw CSV/ZIP files into clean, structured datasets
- **Loading** processed data into both Parquet files and SQLite database
- **Cataloging** datasets with metadata for easy discovery and analysis

The pipeline processes 16 key development indicators including GDP, employment, health, education, and social metrics across 266 countries and regions.

## Features

- **Automated Data Extraction**: Downloads data from World Bank API endpoints
- **Smart Data Processing**: Handles both ZIP and direct CSV downloads
- **Data Transformation**: Cleans column names, removes empty rows/columns
- **Multiple Storage Formats**: Saves data as Parquet files and SQLite database
- **Data Catalog**: Generates YAML catalog with dataset metadata and schema information
- **Analysis Ready**: Includes Jupyter notebook for data exploration

## Project Structure

```
wdi_etl/
├── global_dev_analytics/
│   ├── config/
│   │   └── sources.yaml          # Data source configurations
│   ├── data/
│   │   ├── raw/                  # Downloaded ZIP/CSV files
│   │   └── processed/            # Cleaned Parquet files
│   ├── data_catalog/
│   │   └── catalog.yaml          # Dataset metadata catalog
│   ├── db/
│   │   └── global_dev.db         # SQLite database
│   ├── notebooks/
│   │   └── db_explore.ipynb      # Data exploration notebook
│   ├── src/
│   │   ├── etl.py               # Main ETL pipeline
│   │   ├── load_to_db.py        # Database loading script
│   │   └── build_catalog.py     # Catalog generation script
│   ├── requirements.txt
│   └── README.md
└── README.md
```

## Data Sources

The pipeline processes 16 World Development Indicators:

**Economic Indicators:**
- GDP (current US$)
- GDP per capita (current US$)
- GNI per capita, Atlas method
- Labor force, total
- Unemployment rate
- Employment to population ratio (15+)

**Health & Social Indicators:**
- Life expectancy at birth
- Health expenditure per capita
- HIV prevalence
- Immunization coverage (DPT)
- Poverty headcount ratio ($2.15/day)

**Infrastructure & Education:**
- Access to electricity
- Basic drinking water access
- Managed sanitation services
- School enrollment, secondary
- Government education expenditure

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/wdi_etl.git
cd wdi_etl/global_dev_analytics
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Run Complete ETL Pipeline

Execute the full pipeline to download, process, and store all data:

```bash
# Navigate to the global_dev_analytics directory
cd global_dev_analytics

# Run ETL pipeline
python src/etl.py

# Load data to SQLite database
python src/load_to_db.py

# Generate data catalog
python src/build_catalog.py
```

### Individual Components

**Extract and Transform Data:**
```bash
python src/etl.py
```
This downloads raw data and creates cleaned Parquet files in `data/processed/`.

**Load to Database:**
```bash
python src/load_to_db.py
```
Creates SQLite database with all processed datasets.

**Build Data Catalog:**
```bash
python src/build_catalog.py
```
Generates metadata catalog describing all datasets.

### Data Exploration

Use the provided Jupyter notebook for analysis:
```bash
jupyter notebook notebooks/db_explore.ipynb
```

The notebook provides:
- Database table exploration
- Sample data visualization
- Missing value analysis
- Summary statistics

## Configuration

Data sources are configured in `config/sources.yaml`. Each source includes:
- `name`: Dataset identifier
- `url`: World Bank API endpoint
- `description`: Human-readable description
- `extract`: Boolean flag to enable/disable processing

Example configuration:
```yaml
sources:
  - name: gdp_current_usd
    url: "http://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=csv"
    type: "csv"
    description: "GDP (current US$)"
    extract: true
```

## Output Data

**Processed Files:**
- `data/processed/*.parquet` - Clean datasets in Parquet format
- `db/global_dev.db` - SQLite database with all indicators
- `data_catalog/catalog.yaml` - Dataset metadata and schema

**Data Schema:**
Each dataset contains:
- `country_name` - Country/region name
- `country_code` - ISO country code
- `indicator_name` - Full indicator description
- `indicator_code` - World Bank indicator code
- Year columns (varies by indicator) - Numeric values

## Dependencies

- `pandas` - Data manipulation and analysis
- `requests` - HTTP requests for data download
- `pyyaml` - YAML configuration parsing
- `sqlalchemy` - Database operations
- `pyarrow` - Parquet file support
- `streamlit` - Web app framework (optional)
- `openpyxl` - Excel file support

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Data Source Attribution

Data sourced from the World Bank Open Data initiative:
- World Bank Open Data: https://data.worldbank.org/
- World Development Indicators: https://datatopics.worldbank.org/world-development-indicators/

## Contact

For questions or support, please open an issue on GitHub.
