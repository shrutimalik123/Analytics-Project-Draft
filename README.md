# Diabetes Hospital Readmission Data Analytics

This repository contains the code, data, and academic reports for a data analytics project exploring hospital readmission rates among diabetic patients. It was developed for the **ANLT 5010: Data Analytics** course.

## Project Overview

The goal of this project is to analyze clinical data to identify factors associated with hospital readmissions. The insights derived from this dataset can help healthcare providers improve patient outcomes and reduce unnecessary hospital returns.

## Repository Structure

- **Python Scripts**:
  - `data_profiling.py`: Script for exploring, cleaning, and visualizing the raw dataset.
  - `generate_report.py`: Script that programmatically generates a formatted Word document (`.docx`) report combining analytical findings and visualizations.
- **Datasets**:
  - `diabetes_raw.zip`: The original compressed raw data.
  - `diabetic_data.csv` / `diabetic_data_clean.csv`: The primary dataset (raw and cleaned versions).
  - `IDS_mapping.csv`: Mapping table for ID variables (e.g., admission source, discharge disposition).
- **Visualizations (`.png`)**: Various generated figures illustrating missing values, readmission distributions, age, medical specialties, and number of medications.
- **Course Documents**:
  - `Week1_Project_Proposal.docx`: The initial project proposal.
  - `Week5_Analytics_Report_Shruti_Malik.docx`: The generated midterm analytics report.
  - `Week7_Programming_Best_Practices.docx` (and `.pdf`): An executive summary on programming best practices for data analytics.

## Setup and Usage

### Prerequisites
The scripts require Python 3 and the following primary libraries:
- `pandas` and `numpy` (for data manipulation)
- `matplotlib` and `seaborn` (for data visualization)
- `python-docx` (for document generation)

You can install dependencies via pip:
```bash
pip install pandas numpy matplotlib seaborn python-docx
```

### Running the Code
1. **Data Profiling**: Run `data_profiling.py` to process the raw data and generate analytical visualizations.
   ```bash
   python data_profiling.py
   ```
2. **Report Generation**: Run `generate_report.py` to compile the generated figures and findings into a Microsoft Word document.
   ```bash
   python generate_report.py
   ```

## Author
Shruti Malik  
ANLT 5010: Data Analytics
