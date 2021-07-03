#!/usr/bin/env python
# coding: utf-8

# # Project:          Analytics for FAST Alumni Network

# In[ ]:


#!pip install selenium
#!pip install beautifulsoup4


# In[25]:


import requests, time, random
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

options = webdriver.ChromeOptions()
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])


driver_path = './driver/chromedriver'
driver = webdriver.Chrome(executable_path=driver_path,options=options)
driver.get("https://www.linkedin.com/login/")


# In[5]:


file = open("./config.txt")
line = file.readlines()
username = line[0]
password = line[1]


# In[6]:


elementID = driver.find_element_by_id('username')   
elementID.send_keys(username)
elementID = driver.find_element_by_id('password')
elementID.send_keys(password)
elementID.submit()


# In[190]:


driver.get('https://www.linkedin.com/school/fastnu/people/')


# In[191]:


rep = 100 #determine the rep enough to scroll all the page
last_height = driver.execute_script("return document.body.scrollHeight")

for i in range(rep):
  driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
  time.sleep(8)
  new_height = driver.execute_script("return document.body.scrollHeight")
  if new_height == last_height:
    break
  new_height = last_height


# In[192]:


src = driver.page_source
soup = BeautifulSoup(src, 'lxml')


# In[193]:


pav = soup.find('div', {'class' : 'artdeco-card pv5 pl5 pr1 mt4'})
all_links = pav.find_all('a', {'class' : 'ember-view link-without-visited-state'})


# In[194]:


profilesID = []
for link in all_links:
  profilesID.append(link.get('href'))


# In[195]:


profilesID


# In[196]:


len(profilesID)


# In[30]:


#!pip install simplelist
from simplelist import listfromtxt
from simplelist import txtfromlist


# In[197]:


txtfromlist('profilesID12.txt', profilesID)       # Read A Python List Into A TXT File


# In[198]:


Lists = listfromtxt('profilesID12.txt')           # Make A List From A TXT File


# In[199]:


Lists


# In[490]:


from parsel import Selector


names=[]
Current_Company =[]
Current_Job=[]
job_location=[]
Last_University=[]
Last_degree=[]
#skill_set=[]
ProfileIDS=[]
for profileID in Lists:                 #Here we use  For loop to iterate over each URL in the list
  fulllink = 'https://www.linkedin.com' + profileID
  driver.get(fulllink)
  time.sleep(5)                         #add a 5 second pause loading each URL

  src = driver.page_source              #Here, Beautiful Soup loads the page source. 
                                        #It extracts the required texts by iterating through all profiles.
  soup = BeautifulSoup(src, 'lxml')
 
  total_height = int(driver.execute_script("return document.body.scrollHeight"))

  for i in range(1, total_height, 5):
        driver.execute_script("window.scrollTo(0, {});".format(i))

    
  sel = Selector(text=driver.page_source)    # assigning the source code for the webpage to variable sel

  name = sel.xpath('//*[starts-with(@class, "text-heading-xlarge inline t-24 v-align-middle break-words")]/text()').extract_first()
  if name:
      name = name.strip()
  names.append(name)
      #print(name)
    
  #scraping companies
  company = sel.xpath('//*[starts-with(@class, "pv-entity__secondary-title t-14 t-black t-normal")]/text()').extract_first()
  if company:
    company = company.strip()
  Current_Company.append(company)
      #print(Current_Company)


  job_title = sel.xpath('//*[starts-with(@class, "t-16 t-black t-bold")]/text()').extract_first()
  if job_title:
      job_title = job_title.strip()
  Current_Job.append(job_title)
      #print(Current_Job)
    
  # job location
  job_locations = sel.xpath('//*[starts-with(@class, "pv-entity__location t-14 t-black--light t-normal block")]/span[2]/text()').extract_first()
  if job_locations:
      job_locations = job_locations.strip()
  job_location.append(job_locations)
     # print(Job location)
       
        
  University = sel.xpath('//*[starts-with(@class, "pv-entity__school-name t-16 t-black t-bold")]/text()').extract_first()
  if University:
      University = University.strip()
  Last_University.append(University)
      # print(Last_University)
    
    
          
  degree = sel.xpath('//*[starts-with(@class, "pv-entity__comma-item")]/text()').extract_first()
  
  if degree:
      degree = degree.strip()
  Last_degree.append(degree)
      # print(Last_degree)
    
    
  profileID = driver.current_url
  ProfileIDS.append(profileID)
    
  """
  locate link to expand skills
  show_more_skills_button = driver.find_element_by_class_name("pv-skills-section__chevron-icon")
  expand
  show_more_skills_button.click()

  skills = driver.find_elements_by_xpath("//*[starts-with(@class,'pv-skill-category-entity__name-text')]")

  create skills set
  skill_set = []
  for skill in skills:
      skill_set.append(skill.text)
      """
    




  df = pd.DataFrame(list(zip(names,Current_Company,Current_Job,job_location,Last_degree,Last_University,ProfileIDS)), 
               columns =['Name', 'Current_Company', 'Current_Job',      'job_location',  'Last_degree' ,   'Last_University', 'ProfileIDS'])
    
  df.to_csv('./Totalscrapedata.csv', index=False)


# In[3]:


import pandas as pd
Data = pd.read_csv("./Totalscrapedata.csv")


# In[4]:


len(Data)


# # Preprocessing

# In[5]:


#Analytical Summary of the dataset
Data.describe(include="all")


# In[6]:


Data.shape


# In[7]:


Data.count()


# In[8]:


#Rows containing duplicate data
duplicate_rows= Data[Data.duplicated()]
print ("Number of duplicate rows: ",duplicate_rows.shape)


# In[9]:


#Drop the duplicates
new_data = Data.drop_duplicates()
new_data.count()


# In[10]:


#fill the null values with space(“ “)
modifiedDataset=new_data.fillna(" ")
modifiedDataset.count()


# # Analytical Summary of the Final dataset 

# In[11]:


#Analytical Summary of the dataset
modifiedDataset.describe(include="all")


# In[12]:


#Find the null values
null_values= modifiedDataset.isnull().sum()
null_values


# In[13]:


#fill the null values with space(" ") 
modifiedDataset=new_data.fillna(" ")
modifiedDataset


# In[ ]:





# # Data Visualizations 

# In[14]:


#!pip install matplotlib
# Load library
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# In[ ]:





#  # Educational Analytics
# 

# In[15]:


Education = pd.DataFrame(modifiedDataset)
Edu_data =Education[['Name','Last_degree','Last_University','ProfileIDS']]
Edu_data


# In[16]:


#Find the null values
null_values= Edu_data.isnull().sum()
null_values


# In[17]:


df = pd.DataFrame(Edu_data)
df.to_csv('./Educational_Analysis.csv', index=False)


# In[ ]:





# In[18]:


#Here is we are creating a column in our dataset to identify degree recived by our Alumni 

edu = Edu_data

#Here we are creating a Function named as degree  to identify which last degree recived by our Alumni 
def degree(x):
    if x.find('Bachelor') != -1 or x.find("Bachelor's") != -1 or x.find('BS') != -1 or x.find('bs') != -1 or x.find('Bs') != -1 or x.find('Bachelors') != -1 or x.find('Undergraduate') != -1 or x.find('graduated')!= -1 or x.find('BSE')!= -1 or x.find('Enginee') != -1 or x.find('BCS') != -1:
        return(1)
    if x.find('Master') != -1 or x.find("Master's") != -1 or x.find('M.S') != -1 or x.find('MS') != -1 or x.find('MPhil') != -1 or x.find('MBA') != -1 or x.find('MicroMasters') != -1 or x.find('MSc') != -1 or x.find('MSCS') !=-1 or x.find('MSDS')!=-1:
        return(2)
    if x.find('PhD') != -1 or x.find('P.hd') != -1 or x.find('Ph.D') != -1 or x.find('ph.d') != -1:
        return(3)
    if x.find(" ")!= -1:
        return(4)
    else:
        return(0)

    
#Here we are Creating degree column named as deg
edu['deg'] = list(map(degree, edu['Last_degree']))

edu


# In[ ]:





# In[19]:


#Here we are Looking into the percentages of each last degree earned by our Alumni 
edu['deg'].value_counts(normalize=True) * 100


# In[20]:


#Here we create pie chart to represent the persentage of each last degree earned by our Alumni. 
pie = edu['deg'].value_counts().plot(kind="pie", autopct='%1.1f%%', labels=None)

pie.set_title("Last Degree Received", fontsize=18)
Bachelor = mpatches.Patch(color='blue', label='Bachelor')
Master = mpatches.Patch(color='orange', label='Master')
Other = mpatches.Patch(color='green', label='Others')
PhD = mpatches.Patch(color='red', label='Ph.D')
NA = mpatches.Patch(color='brown', label='NA')
plt.legend(handles=[Bachelor,Master,PhD,Other,NA], loc='center left', bbox_to_anchor=(1, 0.5))


# In[21]:


#Creating column to identify degree earned

edu = Edu_data

# Function to identify degree
def degree_Name(x):
    if x.find('Bachelor') != -1 or x.find("Bachelor's") != -1 or x.find('BS') != -1 or x.find('bs') != -1 or x.find('Bs') != -1 or x.find('Bachelors') != -1 or x.find('Undergraduate') != -1 or x.find('graduated')!= -1 or x.find('BSE')!= -1 or x.find('Enginee') != -1 or x.find('BCS') != -1:
        return("Bachelor")
    if x.find('Master') != -1 or x.find("Master's") != -1 or x.find('M.S') != -1 or x.find('MS') != -1 or x.find('MPhil') != -1 or x.find('MBA') != -1 or x.find('MicroMasters') != -1 or x.find('MSc') != -1 or x.find('MSCS') !=-1 or x.find('MSDS')!=-1:
        return("Master")
    if x.find('PhD') != -1 or x.find('P.hd') != -1 or x.find('Ph.D') != -1 or x.find('ph.d') != -1:
        return('PhD')
    if x.find(" ")!= -1:
        return("NA")
    else:
        return("other")

    
# Create degree column
edu['degree'] = list(map(degree_Name, edu['Last_degree']))

edu


# In[26]:


#Here we are count each degree holders
edu_counts= edu['degree'].value_counts()

#Here we represent aur analysis in bar chart
fig = px.bar(
    edu_counts, 
    title="Education Level of Alumni",      #Title name of our bar chart
    orientation="v"                         #v means vertical orientation
)
fig.update_layout(
    xaxis_title = "Degree",
    yaxis_title = "Number of Students",
    title_x = 0.5,
    showlegend = False
)
fig.show()


# In[ ]:





# In[60]:


#!pip install plotly
import pandas as pd
from os import getcwd, path
import plotly.express as px
import plotly.offline as pyo
pyo.init_notebook_mode()

path_to_data = path.join(getcwd(),"Educational_Analysis.csv")
data = pd.read_csv(path_to_data)

data = data[["Last_degree"]]

data = data.dropna()
print(f"Rows left: {data.shape[0]:,}")

data.loc[:, "Last_degree"] = data.loc[:, "Last_degree"].map(
    lambda response: 
        "Master's degree" if (response == "Master’s degree (M.A., M.S., M.Eng., MBA,Master of Business Administration, etc.)")
        else "Bachelor's degree" if (response == "Bachelor’s degree (BBA,Bachelor,Bachelor's Degree (BSCS),B.A., B.S., B.Eng.,BCS,bscs, etc.)")
        else "High School" if (response == "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)")
        else "Professional degree" if (response == "Professional degree (JD, MD, etc.)")
        else "Associate degree" if (response == "Associate degree (A.A., A.S., etc.)")
        else "Higher Ed. study w/o degree" if (response == "Some college/university study without earning a degree")
        else "Doctoral degree" if (response == "Other doctoral degree (Ph.D., Ed.D., etc.)")
        else response
)

ed_level_counts = data["Last_degree"].value_counts(ascending=True)

fig = px.bar(
    ed_level_counts, 
    title="Education Level of Alumni",
    orientation="h"
)
fig.update_layout(
    xaxis_title = "Number of Students",
    yaxis_title = "Education Level",
    title_x = 0.5,
    showlegend = False
)
fig.show()


# In[ ]:




