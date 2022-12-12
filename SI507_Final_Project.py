#################################
##### Name: Ziwei Huang     #####
##### Uniqname: ziweih      #####
##### SI507 Final Project   #####
##### Fall 2022             #####
##### Umich Ann Arbor       #####
#################################

import requests
import secrets as secrets
import json
import webbrowser
import os
import re
import csv
from bs4 import BeautifulSoup
import plotly.graph_objects as go

api_key = secrets.API_KEY
base_url = "https://www.nps.gov"

def media_link():
    '''
    Collect data web from each state in USA

    Parameters
    ----------
        None

    Returns
    -------
        None
    '''
    media_link_list = []
    media_link_dict = {}
    link = BeautifulSoup(requests.get(base_url).text, 'html.parser').find(class_="GlobalFooter-socialLinks").find_all('a')

    for element in link:
        media_link_list.append(element.get('href'))

    media_link_dict['fackbook'] = media_link_list[0]
    media_link_dict['youtube'] = media_link_list[1]
    media_link_dict['twitter'] = media_link_list[2]
    media_link_dict['instagram'] = media_link_list[3]
    media_link_dict['flicker'] = media_link_list[4]

    return media_link_dict


def get_website_each_state():
    '''
    Collect the web url of all the states in USA

    Parameters
    ----------
        None

    Returns
    -------
        A dict which key is the name of state and the value is the list of web url of that state
    '''
    if os.path.exists("state_web.json"):
        with open("state_web.json", 'r') as f:
            state_web = json.load(f)
    else:
        state_web = {}
        web_list_each_state = BeautifulSoup(requests.get(base_url).text, 'html.parser').find(class_="dropdown-menu SearchBar-keywordSearch").find_all('a')

        for element in web_list_each_state:
            state_web[element.text.lower()] = base_url + element.get('href')


    if os.path.exists("state_web.json"):
        None
    else:
        with open("state_web.json", "w") as f:
            json.dump(state_web, f)

    return state_web


def each_park_url_in_one_state(state_web):
    '''
    Collect all the park url of one state

    Parameters
    ----------
        state_web: web url of the state(string)

    Returns
    -------
        A list of each park web url of one state
    '''
    site = BeautifulSoup(requests.get(state_web).text, 'html.parser').find('div',id="parkListResultsArea").find_all('h3')
    location = BeautifulSoup(requests.get(state_web).text, 'html.parser').find('div',id="parkListResultsArea").find_all('h4')
    location_list = []
    site_list = []
    park_web = []

    for element in location:
        location_list.append(element.text)
    for element in site:
        site_list.append(base_url + element.find('a').get('href') + "index.htm")

    park_web = site_list
    return park_web


def cache_park_url_of_each_state():
    '''
    Store all the park url of each state in a json file.

    Parameters
    ----------
        None

    Returns
    -------
        A dict whose key is the name of the state and the value is 
        all the park web url of that state
    '''
    if os.path.exists("park_web_state.json"):
        with open("park_web_state.json", 'r') as f:
            park_web_state = json.load(f)
    else:
        park_web_state = {}
        web_list_each_state = BeautifulSoup(requests.get(base_url).text, 'html.parser').find(class_="dropdown-menu SearchBar-keywordSearch").find_all('a')
        for element in web_list_each_state:
            state_web = get_website_each_state()[element.text.lower()]
            park_web_state[element.text.lower()] = each_park_url_in_one_state(state_web)

    if os.path.exists("park_web_state.json"):
        None
    else:
        with open("park_web_state.json", "w") as f:
            json.dump(park_web_state, f)
    return park_web_state


def park_info(park_web):
    '''
    collect other data web of one park including calender, map.etc

    Parameters
    ----------
        park_web: park wbe url(string)

    Returns
    -------
        A dict whose key is the name of the data like calender, alerts.ect.
        The value is all the web url of that data
    '''

    park_info = BeautifulSoup(requests.get(park_web).text, 'html.parser').find(class_="UtilityNav").find_all('a')
    info_list = {}

    for element in park_info:
        info_list[element.text.strip()] = base_url + element['href']

    return info_list


def park_data(park_web):
    '''
    collect data of one park

    Parameters
    ----------
        park_web: park wbe url(string)

    Returns
    -------
        A list contain all the data of that park
    '''
    params = {'api_key': secrets.API_KEY, 'parkCode': park_web.split('/')[3]}
    response = requests.get(f"https://developer.nps.gov/api/v1/parks", params).text
    data = json.loads(response)['data']
    return data


def cache_each_park_data():
    '''
    Store data of all the parks in USA in a json file
    Data include name, web url, description.etc

    Parameters
    ----------
        None

    Returns
    -------
        A dict whose key is the name of state and the value is a list.
        The list contain a dict whose value is the name of park and the
        value is all the data info of that park
    '''

    if os.path.exists("park_info.json"):
        with open("park_info.json", 'r') as f:
            park_info = json.load(f)
    else:
        park_info = {}
        name_list = list(cache_park_url_of_each_state().keys())# name of each state
        for x in name_list:
            park_url_list = cache_park_url_of_each_state()[x]
            park_data_dict = {}
            for y in park_url_list:
                a = park_data(y)
                if a == []:
                    None
                else:
                    park_name = a[0]['fullName']
                    park_data_dict[park_name] = a
            park_info[x] = park_data_dict

    if os.path.exists("park_info.json"):
        None
    else:
        with open("park_info.json", "w") as f:
            json.dump(park_info, f)
    return park_info


def read_csv_to_dicts(filepath, encoding='utf-8', newline='', delimiter=','):
    """
    Accepts a file path for a .csv file to be read, creates a file object,
    and uses csv.DictReader() to return a list of dictionaries
    that represent the row values from the file.

    Parameters
    ----------
        filepath (str): path to csv file
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values

    Returns
    ----------
        list: nested dictionaries representing the file contents
    """

    with open(filepath, 'r', newline=newline, encoding=encoding) as file_obj:
        data = []
        reader = csv.DictReader(file_obj, delimiter=delimiter)
        for line in reader:
            data.append(line)

    return data


def get_species_data(park_name):
    '''
    collect species data of one park

    Parameters
    ----------
        park_name: the name of a park(string)

    Returns
    -------
        A list cotain several tuples. A tuple has two element, the first one is the name
        of category and second one is the number of that category.
    '''
    species = read_csv_to_dicts('species.csv')
    species_name = ['Mammal', 'Bird', 'Reptile', 'Amphibian', 'Fish', 'Vascular_Plant', 'Spider_or_Scorpion', 'Insect', 'Invertebrate','Fungi','Nonvascular_Plant', 'Crab_or_Lobster_or_Shrimp', 'Slug_or_Snail','Algae']
    Mammal = 0
    Bird = 0
    Reptile = 0
    Amphibian = 0
    Fish = 0
    Vascular_Plant = 0
    Spider_or_Scorpion = 0
    Insect = 0
    Invertebrate = 0
    Fungi = 0
    Nonvascular_Plant = 0
    Crab_or_Lobster_or_Shrimp = 0
    Slug_or_Snail = 0
    Algae = 0
    result = []
    for x in species:
        if(x['Park Name'] == park_name):
            if (x['Category'] == "Mammal"):
                Mammal = Mammal + 1
            if (x['Category'] == "Bird"):
                Bird = Bird + 1
            if (x['Category'] == "Reptile"):
                Reptile = Reptile + 1
            if (x['Category'] == "Amphibian"):
                Amphibian = Amphibian + 1
            if (x['Category'] == "Fish"):
                Fish = Fish + 1
            if (x['Category'] == "Vascular Plant"):
                Vascular_Plant = Vascular_Plant + 1
            if (x['Category'] == "Spider/Scorpion"):
                Spider_or_Scorpion = Spider_or_Scorpion + 1
            if (x['Category'] == "Insect"):
                Insect = Insect + 1
            if (x['Category'] == "Invertebrate"):
                Invertebrate = Invertebrate + 1
            if (x['Category'] == "Fungi"):
                Fungi = Fungi + 1
            if (x['Category'] == "Nonvascular Plant"):
                Nonvascular_Plant = Nonvascular_Plant + 1
            if (x['Category'] == "Crab/Lobster/Shrimp"):
                Crab_or_Lobster_or_Shrimp = Crab_or_Lobster_or_Shrimp + 1
            if (x['Category'] == "Slug/Snail"):
                Slug_or_Snail = Slug_or_Snail + 1
            if (x['Category'] == "Algae"):
                Algae = Algae + 1
    num=[Mammal, Bird, Reptile, Amphibian, Fish, Vascular_Plant, Spider_or_Scorpion, Insect, Invertebrate, Fungi, Nonvascular_Plant, Crab_or_Lobster_or_Shrimp, Slug_or_Snail, Algae]

    for i in range(len(species_name)):
        if num[i] == 0:
            None
        else:
            a = species_name[i]
            b = num[i]
            c = (a, b)
            result.append(c)

    return result


def category_bar_chart(result, park_name):
    '''
    Plot bar chart showing the number of species

    Parameters
    ----------
    result: list
        A list of tuples with the information for plot
    park_name: string
        a string of park name

    Returns
    -------
        A bar plot made with plotly
    '''
    x_axis = []
    y_axis = []

    for x in result:
        x_axis.append(x[0])
        y_axis.append(x[1])

    data = go.Bar(x = x_axis, y = y_axis)
    Title = go.Layout(title = f"Category at {park_name}")
    fig = go.Figure(data = data, layout = Title)

    return fig.show()


class Park_detail_info:
    """
    A class to represent park info.

    Attributes
    ----------
    Name (str): The name of the park
    Url (str): The web url of the park
    Description (str): The short escription of the park
    Category (str): The category of the park
    Contact (str): The phone numeber of the park
    Email (str): The eamil address of the park
    Entrance_fee (str): The fee of the park
    Address (str): The address of the park
    Activities (list): The activities of the park

    Methods
    -------
    print_info(): print all the attributes info

    """

    def __init__(self, park_name, state_info):
        if state_info == None:
            self.Name = None
            self.Url = None
            self.Description = None
            self.Category = None
            self.Contact = None
            self.Email = None
            self.Entrance_fee = None
            self.Address = None
            self.Activities = None
        else:
            activities = []
            self.Name = state_info[park_name][0]['fullName']
            self.Url = state_info[park_name][0]['url']
            self.Description = state_info[park_name][0]['description']
            self.Category = state_info[park_name][0]['designation']
            self.Contact = state_info[park_name][0]['contacts']['phoneNumbers'][0]['phoneNumber']
            self.Email = state_info[park_name][0]['contacts']['emailAddresses'][0]["emailAddress"]
            self.Entrance_fee = state_info[park_name][0]['entranceFees'][0]['cost']
            self.Address = state_info[park_name][0]["addresses"][0]["line1"] + ', ' + state_info[park_name][0]["addresses"][0]["city"]+ ', ' + state_info[park_name][0]["addresses"][0]["stateCode"]+ ', ' + state_info[park_name][0]["addresses"][0]["postalCode"]
            for activity in state_info[park_name][0]["activities"]:
                activities.append(activity["name"]+',')
            self.Activities = activities

    def print_info(self):
        '''
        Print detalied info
        '''
        print(
                "Name: ", self.Name, '\n'
                "Url: ", self.Url, '\n'
                "Description: ", self.Description, '\n'
                "Category: ", self.Category, '\n'
                "Contact: ", self.Contact, '\n'
                "Email: ", self.Email, '\n'
                "Entrance_fee: ", self.Entrance_fee, '\n'
                "Address: ", self.Address, '\n'
                "Activities: ", self.Activities, '\n'
        )

    def open_url(self):
        '''
        open website
        '''
        webbrowser.open(self.Url)

if __name__ == "__main__":


    '''
    Initial necessary data
    '''
    Media_name = list(media_link().keys())
    Media_url = list(media_link().values())
    State_name = list(cache_each_park_data().keys())
    Park_data = cache_each_park_data()
    print('Welcome to access national parks!\n\n')


    '''
    Access media of national park
    '''
    while True:
        command_1 = input("Do you want to access below media of national park website? Please input 'yes' or 'no' or 'exit': ")
        if command_1 == 'exit':
            print("Bye!")
            exit()
        else:
            if command_1 == 'yes' or command_1 =='no':
                if command_1 == 'yes':
                    for i in range(len(Media_name)):
                        print(f"{i+1}: {Media_name[i]}")
                    command_2 = input("Which one do you want to access? Please input a number: ")
                    if command_2 =='1' or command_2 =='2' or command_2 =='3' or command_2 =='4' or command_2 =='5':
                        webbrowser.open(Media_url[int(command_2)-1])
                        break
                    else:
                        print("Please input a number between 1 and 5! try again!")
                else:
                    break
            else:
                print("Please input 'yes' or 'no', try again! ")


    '''
    Access data of park
    '''
    while True:
        command_3 = input("\nPlease input a state name(e.g. alabama) or 'exit': ")
        if command_3 == 'exit':
            print("Bye!")
            exit()
        else:
            if command_3.lower() in State_name:
                list_1 = list(Park_data[command_3.lower()].keys())
                #print(Park_detail_info(list_1[0],Park_data).print_info())
                for i in range(len(list_1)):
                    print(f"{i+1}:{list_1[i]}")

                while True:
                    command_4 = input("\nWhich one do you want to know more? please input a valid number in the range or input 'exit': ")
                    if command_4 == 'exit':
                        print("Bye!")
                        exit()
                    else:
                        if command_4.isdigit():
                            if int(command_4) >=1 and int(command_4)<=len(list_1):
                                print("\n")
                                Park_detail_info(list_1[int(command_4)-1],Park_data[command_3.lower()]).print_info()
                                Park_detail_info(list_1[int(command_4)-1],Park_data[command_3.lower()]).open_url()
                                while True:
                                    command_5 = input("\nDo you want to check the species diversity of this park? Please input 'yes' or 'no': ")
                                    if command_5=='yes' or command_5=='no':
                                        if command_5 =='yes':
                                            print("If nothing show in the bar chart means the lack of related data")
                                            data = get_species_data(list_1[int(command_4)-1])
                                            category_bar_chart(data,list_1[int(command_4)-1])
                                            break
                                        else:
                                            break
                                    else:
                                        print("Please input 'yes' or 'no'! try again!")
                                break
                            else:
                                print("Please input a number in the range! try again!")
                        else:
                            print("Please input a number!")

            else:
                print("Please input a valid state name! try again!")