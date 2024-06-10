# Women's Premier League Data Scraping and Analysis Project

## Description
This project scrapes data from various EPL related websites, and transforms/stores this data in Azure Blob Storage and PostgreSQL databse, and automates the process using Github Actions. Lastly, it connects to PowerBI for EDA

## Table of Contents
- [Description](#description)
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
  - [Install Dependencies](#install-dependencies)
- [Usage](#usage)
  - [Step 1: Examine the Data Sources](#step-1-examine-the-data-sources)
  - [Step 2: Build the Web Scraping Script](#step-2-build-the-web-scraping-script)
  - [Step 3: Provision Blob Storage and Upload Data](#step-3-provision-blob-storage-and-upload-data)
  - [Step 4: Provision PostgreSQL Database and Upload Data](#step-4-provision-postgresql-database-and-upload-data)
  - [Step 5: Automate the Process with GitHub Actions](#step-5-automate-the-process-with-github-actions)
  - [Step 6: Connect Power BI for Exploratory Data Analysis](#step-6-connect-power-bi-for-exploratory-data-analysis)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)
- [Authors](#authors)
- [Contact](#contact)


### Prerequisites
- Python 3.9 or higher
- Azure account
- PostgreSQL database on Azure
- GitHub account

### Clone the Repository
```sh
git clone https://github.com/your_username/premier-league-data-scraping.git
cd premier-league-data-scraping

### Install Dependencies
```sh
pip install -r requirements.txt