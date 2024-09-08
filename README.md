# Web Scraping for Kabum and Amazon

This project performs web scraping of products from any category on the Kabum and Amazon websites. It searches through all the pages of the selected category and generates CSV and Excel files containing all the products found in that category.

## Description

The project utilizes **Selenium** to automate web browsing tasks and the **Pandas** library for managing data and generating CSV and Excel file outputs. It is designed to scrape product data and export it to both CSV and XLSX formats.

## Requirements

- **Python 3.12**
- **Windows OS**
- **WebDriver** (ChromeDriver): Required for Selenium to interact with the browser.

### Dependencies

- **Selenium**: For automating interactions with the web browser during the scraping process.
- **Pandas**: For data manipulation and generation of CSV and Excel files.
- **XlsxWriter**: Used by Pandas to export data to Excel format.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Conexao1/product-scraping.git
   cd kabum-scraping
2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
