#!/usr/bin/env python
# coding: utf-8


#!pip3 install selenium

import requests, time, random
from bs4 import BeautifulSoup
from selenium import webdriver

import pandas as pd
from typing import List
from parsel import Selector

#!pip3 install simplelist
#from simplelist import listfromtxt
#from simplelist import txtfromlist

def write(file,data):
    f = open(file, "a")
    for d in data:
        f.write(d+"\n")
    f.close()
def read(file):
    f = open(file, "r")
    data=f.read().split("\n")
    f.close()
    return data

def browser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches",["enable-automation"])
    
    driver_path = './chromedriver'
    driver = webdriver.Chrome(executable_path=driver_path,options=options)
    driver.get("https://www.linkedin.com/login/")
    return driver


def login():
    file = open("./config.txt")
    line = file.readlines()
    username = line[0]
    password = line[1]
    elementID = driver.find_element_by_id('username')
    elementID.send_keys(username)
    elementID = driver.find_element_by_id('password')
    elementID.send_keys(password)
    elementID.submit()
    return True

def profile_urls(ids_file="ids1.txt"):
    driver.get('https://www.linkedin.com/school/fastnu/people/?educationEndYear=2019&facetGeoRegion=au%3A0')
    rep = 2 #determine the rep enough to scroll all the page
    last_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(rep):
      driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
      time.sleep(5)
      new_height = driver.execute_script("return document.body.scrollHeight")
      if new_height == last_height:
        break
      new_height = last_height

    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    pav = soup.find('div', {'class' : 'artdeco-card pv5 pl5 pr1 mt4'})
    all_links = pav.find_all('a', {'class' : 'ember-view link-without-visited-state'})    
    profilesID = []
    for link in all_links:
      profilesID.append(link.get('href'))
    
    print(len(profilesID))
    write(ids_file,profilesID)
    
    return profilesID

def get_profiles(Lists,driver):

    names=[]
    Current_Company =[]
    Current_Job=[]
    Total_year=[]
    Total_Experience=[]
    job_location=[]
    
    
    Last_University=[]
    Last_degree=[]
    Graduation_start_year=[]
    Graduation_end_year=[]
    
    
    
    skills_set=[]
    ProfileIDS=[]
    skl1=[]
    skl2=[]
    skl3=[]
    
    
    
    
    import random
      
    
    batch_size=10
    counter=0
    
    for profileID in Lists:
      counter+=1
      if(counter==batch_size):
          counter=0
          driver.quit()
          driver=browser()
          login()
      fulllink = 'https://www.linkedin.com' + profileID
      driver.get(fulllink)
      time.sleep(random.randint(5, 8))
      src = driver.page_source
      soup = BeautifulSoup(src, 'lxml')
      
      total_height = int(driver.execute_script("return document.body.scrollHeight"))
    
      for i in range(1, total_height, 5):
            driver.execute_script("window.scrollTo(0, {});".format(i))
    
        # assigning the source code for the webpage to variable sel
      sel = Selector(text=driver.page_source)
      
      #"""
      
      def get_education(sel,soup):
          print("Education")
          universities=[]
          degrees=[]
          st_years=[]
          end_years=[]
          educations=sel.xpath('//*[@id="education-section"]/ul/li/text()').extract()
          for education in educations:
              print(education)
              universities.append(education.xpath('//*[@class="pv-entity__degree-info"]/h3/text()').extract())
              print(education.xpath('//*[@class="pv-entity__degree-info"]/h3/text()').extract())
              degrees.append(education.xpath('//*[@class="pv-entity__degree-name"]/span[@class="pv-entity__comma-item"]/text()').extract())
              st_years.append(education.xpath('//*[@class="pv-entity__dates"]/span[2]/time[1]/text()').extract())
              end_years.append(education.xpath('//*[@class="pv-entity__dates"]/span[2]/time[2]/text()').extract())
          
          print(universities,degrees,st_years,end_years)
          return universities,degrees,st_years,end_years
      universities,degrees,st_years,end_years=get_education(sel,soup)
      #"""    
      
    
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
    
    
      job_title = sel.xpath('//*[starts-with(@class, "t-16 t-black t-bold")]/text()').extract_first()
      if job_title:
          job_title = job_title.strip()
      Current_Job.append(job_title)
          #print(jobtitle)
        
      # job location
      job_locations = sel.xpath('//*[starts-with(@class, "pv-entity__location t-14 t-black--light t-normal block")]/span[2]/text()').extract_first()
      #job_locations = job.find("span", class_="job-result-card__location").text
      if job_locations:
          job_locations = job_locations.strip()
      job_location.append(job_locations)
      # print(Job location)
      #else: 
         #job_locations = sel.xpath('//*[starts-with(@class, "text-body-small inline t-black--light break-words")]/text()').extract_first()
             #if job_locations:
                 #location = job_locations.strip()
             #job_location.append(job_locations)
          # print(location)
          
      #//*[@id="education-section"]/ul/li/div/div/a/div[2]/div/h3
      
      #education=sel.xpath('//*[@id="education-section"]')
      educations=sel.xpath('//*[@id="education-section"]/ul/li/div/div/a/div[2]/div/h3/text()')
      for u in educations:
        print(u.extract())
          
            
            
      University = sel.xpath('//*[starts-with(@class, "pv-entity__school-name t-16 t-black t-bold")]/text()').extract_first()
      if University:
          University = University.strip()
      Last_University.append(University)
          # print(location)
        
        
              
      degree = sel.xpath('//*[starts-with(@class, "pv-entity__comma-item")]/text()').extract_first()
      if degree:
          degree = degree.strip()
      Last_degree.append(degree)
          # print(last Degree)
        
      Grad_start_year = sel.xpath('//*[starts-with(@class, "pv-entity__dates t-14 t-black--light t-normal")]/span[2]/time[1]/text()').extract_first()
      if Grad_start_year:
         Grad_start_year = Grad_start_year.strip()
      Graduation_start_year.append(Grad_start_year)
          # print(Grad_end_year)
        
        
      Grad_end_year = sel.xpath('//*[starts-with(@class, "pv-entity__dates t-14 t-black--light t-normal")]/span[2]/time[2]/text()').extract_first()
      if Grad_end_year:
         Grad_end_year = Grad_end_year.strip()
      Graduation_end_year.append(Grad_end_year)
          # print(Grad_end_year)
        
      
    
      skill_ary=[]
       # skills = sel.xpath('//*[@id="ember534"]/span').extract_first();
      for skill in sel.xpath('//*[starts-with(@class, "pv-skill-category-entity__name-text t-16 t-black t-bold")]'):
            #print(li.xpath('.//@href').get())
            print(skill.xpath('.//text()').get());
            skill_ary.append(skill.xpath('.//text()').get())
      if len(skill_ary) > 0:
        skl1.append(skill_ary[0].strip())
      if len(skill_ary) > 1:
        skl2.append(skill_ary[1].strip())
      if len(skill_ary) > 2:
        skl3.append(skill_ary[2].strip())
      #skills = sel.xpath('//*[starts-with(@class, "pv-skill-category-entity__name-text t-16 t-black t-bold")]//text()').extract_first()
     
     ##Graduation_year = sel.xpath('//*[starts-with(@class, "pv-entity__secondary-title "pv-entity__degree-name t-14 t-black t-normal")]/span()/span()/text()').extract_first()
     
      time.sleep(random.randint(2, 8))
      #time.sleep(5)  
      #for skill in skills:
       #     skills = sel.xpath('//*[starts-with(@class,"pv-skill-category-entity__name-text t-16 t-black t-bold")]/text()').extract()
      #skills_set.append(skills)
         
    
      Dates_Employed = sel.xpath('//*[starts-with(@class, "pv-entity__date-range t-14 t-black--light t-normal")]/span[2]/text()').extract_first()
      if Dates_Employed:
         Dates_Employed = Dates_Employed.strip()
      Total_year.append(Dates_Employed)
          # print(Dates_Employed)
        
        
      Experience = sel.xpath('//*[starts-with(@class, "pv-entity__bullet-item-v2")]/text()').extract_first()
      if Experience:
            Experience = Experience.strip()
      Total_Experience.append(Experience)
          # print(Experience)
         
            
            
      profileID = driver.current_url
      ProfileIDS.append(profileID)
         
    
      #Print what information is being write to the CSV file
      rows = [name,company,job_title,Total_year,Total_Experience,job_location,degree,Graduation_start_year,Graduation_end_year,skl1,skl2,skl3,University,profileID]
      
      
      if(counter==batch_size):
          print('Writing to CSV:', rows)
          df = pd.DataFrame(list(zip(names,Current_Company,Current_Job,Total_year,Total_Experience,job_location,Last_degree,Graduation_start_year,Graduation_end_year,skl1,skl2,skl3,Last_University,ProfileIDS)), 
                   columns =['Name', 'Current_Company', 'Current_Job', 'Total_year',   'Total_Experience',  'job_location',  'Last_degree' ,  'Graduation_start_year', 'Graduation_end_year','skill_1','skill_2','skill_3',  'Last_University', 'ProfileIDS'])
        
          #print(df)
          df.to_csv('./Scrapdata1111.csv', index=False)

    df = pd.DataFrame(list(zip(names,Current_Company,Current_Job,Total_year,Total_Experience,job_location,Last_degree,Graduation_start_year,Graduation_end_year,skl1,skl2,skl3,Last_University,ProfileIDS)),
                  columns =['Name', 'Current_Company', 'Current_Job', 'Total_year',   'Total_Experience',  'job_location',  'Last_degree' ,  'Graduation_start_year', 'Graduation_end_year','skill_1','skill_2','skill_3',  'Last_University', 'ProfileIDS'])
    df.to_csv('./Scrapdata1111.csv', index=False)





ids_file="ProfilesID13.txt"
driver=browser()
login()
#profilesID=profile_urls(ids_file)

Lists=read(ids_file)
get_profiles(Lists,driver)


# # Data Visualizations 
# 

# In[ ]:


#!pip install matplotlib
# Load library
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# In[ ]:


Alumni_Data = pd.read_csv("./Scrapdata2.csv")


# In[ ]:


Alumni_Data 


# In[ ]:





# In[16]:


Alumni_Data.head()


# In[18]:


Alumni_Data.dtypes


# In[20]:


Alumni_Data.columns.values


# In[23]:


#Analytical Summary of the dataset
Alumni_Data.describe(include="all")


# In[ ]:





# In[ ]:





# In[32]:


#!pip install plotly
import pandas as pd
from os import getcwd, path
import plotly.express as px
import plotly.offline as pyo
pyo.init_notebook_mode()

path_to_data = path.join(getcwd(),"Scrapdata2.csv")
data = pd.read_csv(path_to_data)

data = data[["Last_degree"]]

data = data.dropna()
print(f"Rows left: {data.shape[0]:,}")

data.loc[:, "Last_degree"] = data.loc[:, "Last_degree"].map(
    lambda response: 
        "Master's degree" if (response == "Master’s degree (M.A., M.S., M.Eng., MBA, etc.)")
        else "Bachelor's degree" if (response == "Bachelor’s degree (B.A., B.S., B.Eng., etc.)")
        else "High School" if (response == "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)")
        else "Professional degree" if (response == "Professional degree (JD, MD, etc.)")
        else "Associate degree" if (response == "Associate degree (A.A., A.S., etc.)")
        else "Higher Ed. study w/o degree" if (response == "Some college/university study without earning a degree")
        else "Doctoral degree" if (response == "Other doctoral degree (Ph.D., Ed.D., etc.)")
        else "Elementary school" if (response == "Primary/elementary school")
        else "No formal education" if (response == "I never completed any formal education")
        else response
)

ed_level_counts = data["Last_degree"].value_counts(ascending=True)

fig = px.bar(
    ed_level_counts, 
    title="Education Level of Respondents",
    orientation="h"
)
fig.update_layout(
    xaxis_title = "Frequency",
    yaxis_title = "Education Level",
    title_x = 0.5,
    showlegend = False
)
fig.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[79]:


Education = pd.DataFrame(Alumni_Data)
Edu_data =Education[['Name','Last_degree','Last_University','ProfileIDS']]


# In[80]:


Edu_data


# In[ ]:





# In[86]:


#Creating column to identify degree earned

edu = Edu_data

# Function to identify degree
def degree(x):
    if x.find('Bachelor') != -1 or x.find("Bachelor's") != -1 or x.find('BS') != -1 or x.find('bs') != -1 or x.find('Bs') != -1 or x.find('Bachelors') != -1 or x.find('Undergraduate') != -1 or x.find('graduated')!= -1 or x.find('BSE')!= -1 or x.find('Enginee') != -1 or x.find('BCS') != -1:
        return(1)
    if x.find('Master') != -1 or x.find("Master's") != -1 or x.find('M.S') != -1 or x.find('MS') != -1 or x.find('MPhil') != -1 or x.find('MBA') != -1 or x.find('MicroMasters') != -1 or x.find('MSc') != -1 or x.find('MSCS') !=-1 or x.find('MSDS')!=-1:
        return(2)
    if x.find('PhD') != -1 or x.find('P.hd') != -1 or x.find('Ph.D') != -1 or x.find('ph.d') != -1:
        return(3)
    else:
        return(0)

    
# Create degree column
edu['deg'] = list(map(degree, edu['Last_degree']))

edu


# In[87]:


#Gathering only the employee's last completed education before employment 

eduF = Edu_data.groupby('ProfileIDS').first()
eduF


# In[88]:


#Looking into the percentages of each last degree earned 

eduF['deg'].value_counts(normalize=True) * 100


# In[89]:


pie = eduF['deg'].value_counts().plot(kind="pie", autopct='%1.1f%%', labels=None)

pie.set_title("Last Degree Received", fontsize=18)
Bachelor = mpatches.Patch(color='blue', label='Bachelor')
Master = mpatches.Patch(color='orange', label='Master')
Other = mpatches.Patch(color='green', label='Others')
PhD = mpatches.Patch(color='red', label='Ph.D')
plt.legend(handles=[Bachelor,Master,PhD,Other], loc='center left', bbox_to_anchor=(1, 0.5))


# In[195]:


eduF['deg'].value_counts(normalize=True)


# In[200]:


edu_counts= eduF['deg'].value_counts()
edu_counts


# In[207]:


edu_counts= eduF['deg'].value_counts()
fig = px.bar(
    edu_counts, 
    title="Education Level of Respondents",
    orientation="v"
    #rotation=90
)
fig.update_layout(
    xaxis_title = "Frequency",
    yaxis_title = "Education Level",
    title_x = 0.5,
    showlegend = False
)
fig.show()


# In[202]:


ploting = sns.countplot(x='parental level of education',edu_counts = edu_counts,hue = "Above_85", palette="Blues_d")
plt.setp(ploting.get_xticklabels(), rotation=45) 
plt.xlabel("Parental Level of\nEducation")
plt.ylabel("Count")
plt.show()


# In[ ]:





# In[ ]:





# In[369]:


len(Lists1)


# In[ ]:





# In[368]:


Lists2 = listfromtxt('ProfilesID13.txt') # Make A List From A TXT File
Lists1 = listfromtxt('totalprofileIDs.txt') # Make A List From A TXT File
NewList = list(set(Lists2)-set(Lists1))
len(NewList)


# In[ ]:





# In[ ]:





# In[223]:


txtfromlist('newProfileID11.txt', NewList) # Read A Python List Into A TXT File


# In[ ]:





# In[ ]:





# In[ ]:





# In[414]:


Lists = listfromtxt('ProfilesID1.txt') # Make A List From A TXT File


# In[415]:


len(Lists)


# In[416]:


from typing import List


# In[419]:


# For loop to iterate over each URL in the list
from parsel import Selector


names=[]
Current_Company =[]
Current_Job=[]
Total_year=[]
Total_Experience=[]
job_location=[]
Last_University=[]
Last_degree=[]
Graduation_start_year=[]
Graduation_end_year=[]
skills_set=[]
ProfileIDS=[]
skl1=[]
skl2=[]
skl3=[]

for profileID in Lists:
  fulllink = 'https://www.linkedin.com' + profileID
  driver.get(fulllink)
  time.sleep(5)
  src = driver.page_source
  soup = BeautifulSoup(src, 'lxml')
    # open profile URL
    #driver.get(profileID)

    # add a 3 second pause loading each URL
    #time.sleep(8)
    
  total_height = int(driver.execute_script("return document.body.scrollHeight"))

  for i in range(1, total_height, 5):
        driver.execute_script("window.scrollTo(0, {});".format(i))

    # assigning the source code for the webpage to variable sel
  sel = Selector(text=driver.page_source)

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


  job_title = sel.xpath('//*[starts-with(@class, "t-16 t-black t-bold")]/text()').extract_first()
  if job_title:
      job_title = job_title.strip()
  Current_Job.append(job_title)
      #print(jobtitle)
    
  # job location
  job_locations = sel.xpath('//*[starts-with(@class, "pv-entity__location t-14 t-black--light t-normal block")]/span[2]/text()').extract_first()
  #job_locations = job.find("span", class_="job-result-card__location").text
  if job_locations:
      job_locations = job_locations.strip()
  job_location.append(job_locations)
  # print(Job location)
  #else: 
     #job_locations = sel.xpath('//*[starts-with(@class, "text-body-small inline t-black--light break-words")]/text()').extract_first()
         #if job_locations:
             #location = job_locations.strip()
         #job_location.append(job_locations)
      # print(location)
        
        
  University = sel.xpath('//*[starts-with(@class, "pv-entity__school-name t-16 t-black t-bold")]/text()').extract_first()
  if University:
      University = University.strip()
  Last_University.append(University)
      # print(location)
    
    
          
  degree = sel.xpath('//*[starts-with(@class, "pv-entity__comma-item")]/text()').extract_first()
  if degree:
      degree = degree.strip()
  Last_degree.append(degree)
      # print(last Degree)
    
  Grad_start_year = sel.xpath('//*[starts-with(@class, "pv-entity__dates t-14 t-black--light t-normal")]/span[2]/time[1]/text()').extract_first()
  if Grad_start_year:
     Grad_start_year = Grad_start_year.strip()
  Graduation_start_year.append(Grad_start_year)
      # print(Grad_end_year)
    
    
  Grad_end_year = sel.xpath('//*[starts-with(@class, "pv-entity__dates t-14 t-black--light t-normal")]/span[2]/time[2]/text()').extract_first()
  if Grad_end_year:
     Grad_end_year = Grad_end_year.strip()
  Graduation_end_year.append(Grad_end_year)
      # print(Grad_end_year)
    
  
  
  skill_ary=[]
   # skills = sel.xpath('//*[@id="ember534"]/span').extract_first();
  for skill in sel.xpath('//*[starts-with(@class, "pv-skill-category-entity__name-text t-16 t-black t-bold")]'):
        #print(li.xpath('.//@href').get())
        print(skill.xpath('.//text()').get());
        skill_ary.append(skill.xpath('.//text()').get())
  if len(skill_ary) > 0:
    skl1.append(skill_ary[0].strip())
  if len(skill_ary) > 1:
    skl2.append(skill_ary[1].strip())
  if len(skill_ary) > 2:
    skl3.append(skill_ary[2].strip())
  #skills = sel.xpath('//*[starts-with(@class, "pv-skill-category-entity__name-text t-16 t-black t-bold")]//text()').extract_first()
 
 ##Graduation_year = sel.xpath('//*[starts-with(@class, "pv-entity__secondary-title "pv-entity__degree-name t-14 t-black t-normal")]/span()/span()/text()').extract_first()
  if skills:
     skills = skills.strip()
  skills_set.append(skills)
      # print(skills)
    


    

  Dates_Employed = sel.xpath('//*[starts-with(@class, "pv-entity__date-range t-14 t-black--light t-normal")]/span[2]/text()').extract_first()
  if Dates_Employed:
     Dates_Employed = Dates_Employed.strip()
  Total_year.append(Dates_Employed)
      # print(Dates_Employed)
    
    
  Experience = sel.xpath('//*[starts-with(@class, "pv-entity__bullet-item-v2")]/text()').extract_first()
  if Experience:
        Experience = Experience.strip()
  Total_Experience.append(Experience)
      # print(Experience)
     
        
        
  profileID = driver.current_url
  ProfileIDS.append(profileID)
  time.sleep(5)  

  #Print what information is being write to the CSV file
  rows = [name,company,job_title,Total_year,Total_Experience,job_location,degree,Graduation_start_year,Graduation_end_year,skl1,skl2,skl3,University,profileID]
  print('Writing to CSV:', rows)
  df = pd.DataFrame(list(zip(names,Current_Company,Current_Job,Total_year,Total_Experience,job_location,Last_degree,Graduation_start_year,Graduation_end_year,skl1,skl2,skl3,Last_University,ProfileIDS)), 
               columns =['Name', 'Current_Company', 'Current_Job', 'Total_year',   'Total_Experience',  'job_location',  'Last_degree' ,  'Graduation_start_year', 'Graduation_end_year','skill_1','skill_2','skill_3',  'Last_University', 'ProfileIDS'])
    
  #print(df)
  df.to_csv('./dataset1.csv', index=False)



# plot confirmed cases world map 
merge.plot(column='job_location', scheme="quantiles",
           figsize=(25, 20),
           legend=True,cmap='coolwarm')
plt.title('2020 Jan-May Confirmed Case Amount in Different Countries',fontsize=25)
# add countries names and numbers 
for i in range(0,10):
    plt.text(float(merge.longitude[i]),float(merge.latitude[i]),"{}\n{}".format(merge.name[i],merge.Confirmed_Cases[i]),size=10)


plt.show()


# In[ ]:




