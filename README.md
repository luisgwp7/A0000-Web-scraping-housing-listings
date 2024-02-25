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
- [Configuration](#configuration)
- [Contributing](#contributing)
- [Credits](#credits)
- [License](#license)
- [Contact Information](#contact-information)
- [FAQ](#faq)
- [Examples](#examples)

## Installation
You need to download all the project. Including the .bat file, which is used for deleting the temporal data. 

## Usage
### 1. Change the directories sections: 
- In the folder of *__SCRAPERS__* you are going to find 2 folders ("BUILDINGS" and "Lotes"). Just focus in BUILDINGS. Now there are another three folders (CC, FR, and ML) each of them correpond to a different page. According to this, if you just one ML page, just change this file.
- Now, the changes that you need to do is simple, you just need to change the directories paths in the .py file name directories. Don't you worry, you can find it in the followint path __(C:\ Users \ *{your_user}* \{*your_folder_to_save_the_project*} \ SCRAPERS \ BUILDINGS \ FR \ FR \ directories.py)__
- Taking this into account, you just gonna need change your user and the folder that you use. In this python file you are going to fins three important paths, the master directorie that is the directory you use to save the data, the driver directory you use to save the Selenium driver required in this program, and finally, the directory of the .bat file, that delete the temporal files in your machine.
- Now, you can use the jupyter notebooks that are really simple. For this step you need to understand that this program, at first catch the data of the front pages, where you just have the main information, but not the most relevant if you want to dive depper, such as the geograpich information inthis case. You need to use at first the notebooks that have the FRONT, for used and rent. When those scrapers ends, you can then run the INT notebooks for used and rent. If you want to run them simultanuously, go ahead, I recommend run Q1 and Q2 at first, then Q3 and Q4, for each operation. But If you have different machines, then, maybe you can run all of them simultanously. The time execution could vary, but normally it takes just one week or less for get all the information.
- Something that you may need is that the driver could change, in this case, the scraper is not going to work. Just look for the last version of drivers for testing. This program use Chrome driver. You can take a look of them here: https://chromedriver.chromium.org/downloads or https://googlechromelabs.github.io/chrome-for-testing/    

## Configuration
Details on any configuration settings and how to configure them.

## Contributing
Guidelines for contributing to the project.

## Credits
Give credit to external libraries, resources, or contributors.

## License
Specify the project's license.

## Contact Information
Provide a way for users to reach out for support or inquiries.

## FAQ
Anticipated frequently asked questions and their answers.

## Examples
Include examples of how the project can be used, along with sample outputs.
