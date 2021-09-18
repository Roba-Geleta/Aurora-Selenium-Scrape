# Aurora-Selenium-Scrape

This program is used to Scrape the aurora course catalog website, for the terms specified by the user.

***

## How To

This program requires a Chrome browser and a Chrome driver to operate.

+ It is mainly written to run on the Chrome browser as running it on Firefox provided some errors.

+ The path where the driver is placed in must be specified before running the program.

```python
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(executable_path=PATH)
```

The program will need the number of terms to traverse through and the names of the terms.

At the end of the program, the scraped data (course name, course title and course description) is provided under a json file, the name of the file can be changed in the code.

If more than one terms are specified, the terms requested later on override the course description of the courses requested first.

+ Ex. if Fall 2021 was traversed through first, then Winter 2021 is being traversed through next, for the similar courses both terms share (example, COMP 1012), the course description for COMP 1012 that is stored is the one from Winter 2021.

+ There is a future plan to store the different course descrptions by terms if a difference exists. As of now, only ~3 courses have different course descriptions in both terms.

***

## Run

I wrote and ran this program on VSCode.

***

## Built Using

+ [Python 3.9.7](https://www.python.org/downloads/)
+ [selenium 3.141](https://www.selenium.dev/documentation/)
+ [Chrome  93.0.4577.82](https://www.google.com/intl/en_ca/chrome/)
+ [ChromeDriver 93.0.4577.63](https://chromedriver.chromium.org/downloads)
+ [VSCode 1.60.1](https://code.visualstudio.com/)
