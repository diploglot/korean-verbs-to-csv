###
###
###     CODE BY MATT BOWLBY (MATT@BOWLBY.CO)
###     PYTHON SCRIPT
###     SCRAPE KOREAN VERB FORMS FROM KOREANVERBS.APP
###     SAVE DATA TO CSV FILE
###
###


# import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd


# python program to convert a list
# to string using join() function
def listToString(s): 
    
    # initialize an empty string
    str1 = ", " 
    
    # return string  
    return (str1.join(s))
        


# 1) READ LIST OF VERBS FROM TXT FILE

# initiate variables for verb list and urls
verb_file = "korean_verbs_input.txt"
verb_list = []    
urls = []

# open text file and read each line
with open(verb_file, "r") as f:
    lines = f.readlines()

# itierate over each line and generate list of verbs
for l in lines:
		 as_list = l.split(", ")
         # remove new lines
		 verb_list.append(as_list[0].replace("\n",""))

print('Scraping data for the following verbs/adjectives:')
print(listToString(verb_list))



# 2) GENERATE LIST OF URLS TO SCRAPE

# iterate over lines in text file and generate urls
urls = ['https://koreanverb.app/?search=' + format(i) for i in verb_list]
# print list of URLs 

print('Pinging the following URLs:')
print(listToString(urls))
 

###     3) SCRAPE VERB DATA FROM KOREANVERBS.APP USING LIST OF URLS

# function to parse the html data & get conjugations
def get_conjugations(url):
    #set return lists
    verb_title_text_kr = []
    verb_definition_text_en = []
    conjugation_names_en = []
    conjugation_names_kr = []
    
    #get html text
    html = requests.get(url).text
    #parse the html text
    soup = BeautifulSoup(html, 'html.parser')
    
    #get dictionary form and definition
    verb_definition = soup.find('dl', class_='dl-horizontal')
    
    #get dictionary form in Korean 
    verb_title_kr = verb_definition.find("dt",text="verb").findNext("dd")
    verb_title_text_kr = verb_title_kr.text

    #get definition in English
    verb_definition_en = verb_definition.find("dt",text="definition").findNext("dd")
    verb_definition_text_en = verb_definition_en.text
    
    #get table of verb conjugations
    table = soup.find("div", class_="table-responsive")
    table_rows = table.find_all("tr", class_="conjugation-row")
    
    #iterate through table rows and get verb form names in English and forms in Korean
    for row in table_rows:
        conjugation_name_en = row.find("td", class_="conjugation-name")
        conjugation_name_kr = conjugation_name_en.find_next_sibling("td")
        conjugation_names_en.append(conjugation_name_en.text)
        conjugation_names_kr.append(conjugation_name_kr.text)
    # add dictionary form and definition
    conjugation_names_en.insert(0, "dictionary form")
    conjugation_names_en.insert(1, "definition") 

    # return both lists
    return verb_title_text_kr, verb_definition_text_en, conjugation_names_en, conjugation_names_kr

###     4) OUTPUT SCRAPE DATA TO CSV FILE

# create csv file
outfile = open("korean_verbs_output.csv", "w", newline='')

# define dataframe columns
df = pd.DataFrame()

#construct first column for dictionary form, definition, and conjugation names
verb_title_text_kr, verb_definition_text_en, conjugation_names_en, conjugation_names_kr = get_conjugations(urls[0])

# define columns of DataFrame
df = pd.DataFrame(columns = conjugation_names_en)

# cycle through each individual verb webpage and assemble dataframe
for index, url in enumerate(urls[0:]):
     verb_title_text_kr, verb_definition_text_en, conjugation_names_en, conjugation_names_kr = get_conjugations(url)
     
     # set current verb
     current_verb = verb_title_text_kr

     df2 = current_verb
     
     conjugation_names_kr.insert(0, verb_title_text_kr)
     conjugation_names_kr.insert(1, verb_definition_text_en)
     to_append = conjugation_names_kr
     df_length = len(df)
     df.loc[df_length] = to_append

#save to csv
df.to_csv('korean_verbs_output.csv')
outfile.close()

# print done
print('Export to CSV completed successfully. Open file output.csv for a complete list of forms for the verbs in your list.')
