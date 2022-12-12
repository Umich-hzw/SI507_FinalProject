# SI507 Final Project: National Park
This objective of this project is for people to get the main info of a national park in a convenient way(Fee, Description, etc.).
There is also a special function which can show the category of species in this park by a bar chart.

# Data Source:
1. National Park Website(https://www.nps.gov)
2. Detailed Info of a park(https://developer.nps.gov/api/v1/parks)
3. Spoces.csv file(https://www.kaggle.com/datasets/nationalparkservice/park-biodiversity)

# Data Structure:
I use a tree structure topology to store info of all the nationl parks in USA
The data structure show below structure 1

Structure 1:
{
    'alabama': {Structure 2}
    'alaska': {Structure 2}

            .
            .
            .

    'wisconsin': {Structure 2}
    'wyoming': {Structure 2}
}

Structure 2:
{
    'Park_1': {Structure 3}
    'Park_2': {Structure 3}

            .
            .
            .

    'Park_n-1': {Structure 3}
    'Park_n': {Structure 3}
}

Structure 3:
{
    'Park_1': {Info}
    'Park_2': {Info}

            .
            .
            .

    'Park_n-1': {Info}
    'Park_n': {Info}
}

Info:
{
    'id':{......}
    'url':{......}

            .
            .
            .

    'activities':{......}
    'designation':{......}

}

# How to use:
1.Dowoload the the code to your local computer
2.Ask for a api key from here(https://www.nps.gov/subjects/developer/get-started.htm)
3.Replace the key in the secrets.py
4.Click the run buttom

# Required Package:
1.requests: get data from api
2.BeautifulSoup: get data from web
3.plotly: plot bar chart
4.webbrowser: open web url

# Interaction:
1.The program will ask you whether to open the media link at in the termianl, you can choose yes or no. if yes, it will open. if no, program will ask you a next question.
2.The program will ask you to input a state name.
3.And then the program will show you the name of each park in the state you input above
4.The program will ask you to input a number to get more info about the park
5.The program will show the detail info of the park you choose above
5.And then the program will ask you if you want to look the bar chart about the category of the park you choose.
6.You can input 'exit' anytime to exit the program.


# Acknowledgments:
Many thanks to Prof.Madamanchi and the GSI team of SI 507 who offer such a high quality course and basic code examples.

# Author:
Name: Ziwei Huang
Unique name: ziweih
UMID: 12320144
Second year master in Electrical and Computer Engineering(Integrated Circuit Design)