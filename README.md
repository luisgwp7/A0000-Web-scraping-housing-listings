# A0000-Web-scraping-housing-listings

## Introduction
This project is designed to gather information from prominent housing listing websites, both for sale and for rent. It utilizes Selenium as the principal tool for web scraping. In addition to Selenium, the program follows best practices for scraping, including implementing random time intervals and deleting temporary files created during the process.
Nowadays, the scrapers can retrieve more than 200 entries from each of the three principal websites, providing a comprehensive dataset for housing listings.

### Key Features:
- Web scraping of housing listings from major websites.
- Use of Selenium for efficient and dynamic data extraction.
- Implementation of best practices, such as random time intervals and cleaning up temporary files.

### Usage Scenario:
If you have a keen interest in the housing market and want to identify areas with high demand or untapped opportunities, this tool is your ideal companion for obtaining valuable data. The scrapers are designed to extract over 85% of the general data, providing a reliable and comprehensive source of information.

#### Key Benefits:
- **Strategic Insights:** Identify areas where housing offers are agglomerated or scarce, helping you make informed business decisions.
- **Market Trends:** Stay updated on the latest trends in the housing market by analyzing data from prominent websites.
- **Data Reliability:** With our scraping techniques, you can trust the accuracy and completeness of the extracted data.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Contact Information](#contact-information)


## Installation
You need to download all the project. Including the .bat file, which is used for deleting the temporal data. 

## Usage

### 1. Change the Directories Section:

- In the folder of **\_\_SCRAPERS\_\_**, you will find 2 folders ("BUILDINGS" and "Lotes"). Just focus on BUILDINGS. Now, there are another three folders (CC, FR, and ML), each of them corresponds to a different page. According to this, if you just want ML page data, make changes to this file.

- Now, the changes that you need to make are simple. You just need to change the directory paths in the .py file named directories. Don't worry; you can find it in the following path: *__C:\ Users \ {your_user} \ {your_folder_to_save_the_project} \ SCRAPERS \ BUILDINGS \ FR \ FR \ directories.py__*

Taking this into account, you just need to change your username and the folder that you use. In this python file, you are going to find three important paths: the master directory (the directory you use to save the data), the driver directory (where you save the Selenium driver required for this program), and finally, the directory of the .bat file, that deletes the temporal files on your machine.

### 2. Run!

- Now, you can use the Jupyter notebooks that are really simple. For this step, you need to understand that this program, at first, catches the data from the front pages, where you only have the main information, but not the most relevant if you want to dive deeper, such as the geographic information in this case.

You need to use, at first, the notebooks that have the FRONT, for used and rent. When those scrapers end, you can then run the INT notebooks for used and rent. If you want to run them simultaneously, go ahead. I recommend running Q1 and Q2 first, then Q3 and Q4 for each operation. But if you have different machines, then maybe you can run all of them simultaneously. The time execution could vary, but normally it takes just one week or less to get all the information.

### 3. Possible Future Issues

- Something that you may encounter is that the driver could change; in this case, the scraper is not going to work. Just look for the latest version of drivers for testing. This program uses the Chrome driver. You can find the latest versions [here](https://chromedriver.chromium.org/downloads) or [here](https://googlechromelabs.github.io/chrome-for-testing/).


## Contact Information
[linkedin](https://www.linkedin.com/in/luis-gwp7/)
[X](https://twitter.com/luis_gwp)

