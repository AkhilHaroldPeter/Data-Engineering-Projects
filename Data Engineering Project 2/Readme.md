# Credit Card Transaction Analysis Project

## Overview
This project analyzes credit card transaction data sourced from Kaggle, focusing on consumer spending habits in India. The analysis provides insights into spending categories, budget allocation, and consumer behavior trends. It employs Python for data processing, SQL for database management, and the Cohere API for generating insights.

The project consists of a NiFi flow for orchestrating the data pipeline, multiple SQL scripts for data analysis, and Python scripts for generating outputs in various formats. The structured output is essential for report generation and decision-making.

## How the Project Works
1. **Data Download**: The project starts by downloading datasets from Kaggle using the `Kaggle_data_download.py` script.
2. **Data Loading**: The downloaded data is then loaded into a SQL database using the `Table_Creation_and_data_loading.py` script, which creates necessary tables and inserts data.
3. **SQL Analysis**: SQL scripts in the `sql/` directory are executed using the `sql_analysis.py` script to perform various analytical queries on the data.
4. **File Content Generation**: The `File_content_generator.py` script generates a comprehensive analysis of the spending data using the Cohere API.
5. **Output Generation**: Finally, various outputs (reports, documents) are generated using `Output_Generation.py`, `create_doc.py`, and `create_pdf.py`.

## Limitations
- **API Dependence**: The analysis relies on the Cohere API, which requires an active internet connection and API key.
- **Data Quality**: The insights are only as good as the input data. Inaccuracies in the transaction data may affect the results.
- **Performance**: As the dataset grows, the processing time for SQL queries may increase, impacting performance.

## Prerequisites
Before running the project, ensure you have the following software installed:

1. **Python 3.8 or higher**  
   - [Download Python](https://www.python.org/downloads/)
  
2. **SQL Server Management Studio (SSMS)**  
   - [Download SSMS](https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms)

3. **SQL Server (SQL Server 2019 or higher)**  
   - [Download SQL Server](https://www.microsoft.com/en-us/sql-server/sql-server-downloads)

4. **Apache NiFi**  
   - [Download Apache NiFi](https://nifi.apache.org/download.html)

5. **IDE (Integrated Development Environment)**  
   - [PyCharm](https://www.jetbrains.com/pycharm/download/)
   - [Jupyter Notebook](https://jupyter.org/install)

## Packages Used

To ensure all functionalities work correctly, install the following Python packages. You can do this via pip:

```bash
pip install cohere pandas numpy sqlalchemy pyodbc python-docx reportlab
```

#### Packages for Each Script
- convert_to_tuple_format.py: No additional packages required.
- create_doc.py: Requires ```python-docx``` for creating Word documents.
- create_pdf.py: Requires ```reportlab``` for generating PDF reports.
- File_content_generator.py: Requires ```cohere``` for generating insights from the Cohere API.
- get_latest_log_file.py: No additional packages required.
- Kaggle_data_download.py: Requires requests to interact with the ```Kaggle API```.
- Output_Generation.py: No additional packages required.
- read_sql_file.py: No additional packages required.
- setup_logging.py: No additional packages required.
- sql_analysis.py: Requires  ```pyodbc``` for SQL Server connectivity.
- Table_Creation_and_data_loading.py: Requires ```pyodbc``` for table creation and data loading.

## Project Structure

```
Data Engineering Project 2/
│
├── data/                           # Directory to store datasets or generated files
│   ├── input/                     # Input datasets (CSV, Excel, JSON, etc.)
│   ├── output/                    # Generated outputs in CSV, Excel, JSON, PDF, etc.
│   └── logs/                      # Directory for log files
│
├── sql/                           # Directory to store SQL scripts
│   ├── Average_Spend_Per_Transaction_by_Card_Type.sql
│   ├── Cumulative_Spend_by_City.sql
│   ├── Fastest_Growth_in_Spending.sql
│   ├── Highest_Spending_Gender.sql
│   ├── Spend_by_Gender_Across_Cities.sql
│   ├── Spend_Distribution_Across_Card_Types.sql
│   ├── Top_5_Expense_Categories.sql
│   ├── Weekend_vs_Weekday_Transaction_Patterns.sql
│   └── Year_over_Year_Spend_Growth.sql
│
├── config/                        # Directory for configuration files
│   ├── iconfig.ini                # Main config file with settings for outputs
│
├── scripts/                       # Directory to store all Python scripts
│   ├── file_content_generator.py  # File generator script
│   ├── create_doc.py              # Word document generation script
│   ├── create_pdf.py              # PDF generation script
│   ├── sql_analysis.py            # Main analysis script using SQL
│   ├── setup_logging.py            # Logging setup script
│   ├── read_sql_file.py           # Script to read SQL files for analysis
│   ├── output_generation.py        # Script for generating various output formats
│   ├── kaggle_data_download.py     # Script to download datasets from Kaggle
│   ├── table_creation_and_data_loading.py  # Script for creating tables and loading data
│   ├── get_latest_log_file.py      # Script to retrieve the latest log file
│   └── convert_to_tuple_format.py   # Script to convert data to tuple format
│ 
├── docs/                          # Documentation related files
│   ├── project_report.docx        # Final project report (can be dynamically generated)
│   └── README.md                  # Documentation for the project setup and usage
│
├── .gitignore                     # Git ignore file for hiding unwanted files in version control
└── README.md                      # General project documentation (overview, setup, etc.)
```

## Future Improvement Areas

Enhanced Data Visualization: Integrate libraries like Matplotlib or Seaborn for visual representation of data trends.

User Interface: Develop a web-based dashboard to present analysis results in real-time using frameworks like Flask or Django.

Automated Reporting: Automate report generation in various formats (PDF, Word) based on specific triggers or scheduled intervals. 

Data Quality Checks: Implement data validation and quality checks before processing to ensure data integrity.

Advanced Analytics: Utilize machine learning techniques to predict future spending trends based on historical data.

Error Handling: Improve error handling and logging mechanisms for better troubleshooting and maintenance.

Code Optimization: Regularly refactor code for better performance, especially in data processing scripts.

## Conclusion

This project serves as a comprehensive analysis tool for credit card transaction data, enabling deeper insights into consumer behavior. By following the setup instructions and ensuring all prerequisites are met, users can run the analysis smoothly and extend the project as needed.

```
Feel free to make any adjustments as necessary to better reflect your project specifics!
```