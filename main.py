from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import json

'''
used to traverse through the the courses and course description sent in through the parameter
courses -> holds the string representing the course numbers and course titles
descriptions -> holds the string representing the course descriptions
'''
def each_course(courses, descriptions, course_key):


    #loop through each course and course description saved
    for course, description in zip(courses,descriptions):
        #split the course, index 1 should be the course number, and every index after that holds the course title
        title = course.text.split(" ")
        num = title[1]
        title = title[3:]
        title = " ".join(title)
        #the key for the course is its number, and its values are the title and description
        course_key[num]={"title":title,"info":description.text}


#used to check whether the parameter is an int or not and return a boolean representing that result
def is_Integer(num):
    check = True
    try:
        num = int(num)
    except ValueError:
        check = False
    
    return check


def scrape_Start(driver, term_Options, f):
    #'where to write the course catalog info'
    dict_jason = {}
    f = open(f, 'w')

    #driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
    for term in term_Options:
        try:
            'Where to start the search'
            search = Select (WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "cat_term_in"))))
            #'the term to traverse into'
            search.select_by_visible_text(term)
            #'click on the submit button'
            submit = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='Submit']"))
            )
            submit.click()
            
            #'Access the menu for the courses and save the number of courses'
            course_search = Select (WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='sel_subj'"))))
            course_list_size = len(course_search.options)

            for x in range(course_list_size):

                #find the element representing the menu once again
                course_search = Select (WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='sel_subj'"))))
                
                #select the course under the menu through the index
                course_search.select_by_index(x)

                
                #the attribute "value" is associated with the nickname/short name for the course (Computer -> Comp)
                program_name = course_search.first_selected_option.get_attribute("value")

                #find and click on the submit button
                course_branches = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit'][value='Get Courses']")))
                course_branches.click()

                #find the elements representing the course title and course description
                courses = driver.find_elements_by_class_name("nttitle")

                courses_description = driver.find_elements_by_class_name("ntdefault")

                
                #print(program_name +"  "+ str(len(courses)) +"  "+ str(len(courses_description)))

                #call the each_course method to save the courses information under the correct key (short name for the courses (Computer -> Comp))
                #if the course number doesn't exist, add an empty dict to it
                if(dict_jason.get(program_name) is None):
                    dict_jason[program_name]={}
                

                each_course(courses, courses_description, dict_jason[program_name])
                
                #go back into the menu screen
                driver.back()

                #without driver.refresh() it takes the navigation longer to load into a course after each subsequent course
                #I assume the refresh method clears some of the cache, as using it seems to make the courses load faster, but I have yet to find an official answer as the documentation on selenium has no info written about it
                driver.refresh()

            #incase there is another term to traverse through

            driver.back()
            driver.refresh()
            
        except:
            print("Exception found")
            driver.quit()

    #after scraping the website into the dict format, save it as json format (json string)
    json_string = json.dumps(dict_jason, indent=4)
    #write into the file
    f.write(json_string)
    driver.quit()


#where all the process starts at
def main():

    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=PATH)

    #'where to save the course catalog'
    f = "attempt3.json"

    #'The course catalog location'
    driver.get("https://aurora.umanitoba.ca/banprod/bwckctlg.p_disp_cat_term_date")
    driver.implicitly_wait(15)
    #access the menu that holds the term selections
    search = Select (WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "cat_term_in"))))
    driver_Term_Options = []
    
    #save the options
    for option in search.options:
        driver_Term_Options.append(option.text)
    
    max_Options = len(driver_Term_Options)

    print(f"{max_Options} max term options\n")

    print("<>If more than one term has been picked<>\nCourse description of a specific course of the first term will be overriden by the course description of that same course in a different term throughout the traversal.")
    print("For example, if the first term is Fall 2021 and the next term is Winter 2022 and the course present in both terms is COMP 1012")
    print("The course description listed for COMP 1012 in Fall 2021 will be overriden by the one listed in Winter 2022\n")
    print("Therfore, when inserting the terms, insert oldest to latest.\n")

    #get user input for the number of terms to traverse through
    number = input("How many terms do you want to traverse through? ")
    while((not is_Integer(number)) or (is_Integer(number) and (int(number) <=0 or int(number) > max_Options))):
        print(f"\n{number} is an invalid input.\n")
        number = input("How many terms do you want to traverse through? ")
    
    print("Enter the terms you want to input, with case sensitivity in mind, after each request.")
    
    #get the name of the terms to traverse through
    term_Options= []
    for x in range(int(number)):
        term = input(f"Enter Term #{x+1}: ")
        while (term in driver_Term_Options and term in term_Options) or term not in driver_Term_Options:
            term = input(f"Invalid input: Enter Term #{x+1}: ")
        term_Options.append(term)
    
    
    scrape_Start(driver, term_Options, f)

    print("Program Finished.")

    

if __name__ == "__main__":
    main()
