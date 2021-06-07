import requests
import warnings
import pandas as pd
from bs4 import BeautifulSoup

#storing URL in a variable and filters the warnings from entering the website
baruchMenSwimURL = 'https://athletics.baruch.cuny.edu/sports/mens-swimming-and-diving/roster'
bauchMenVolleyballURL = 'https://athletics.baruch.cuny.edu/sports/mens-volleyball/roster'
baruchWomenSwimURL = 'https://athletics.baruch.cuny.edu/sports/womens-swimming-and-diving/roster'
baruchWomenVolleyballURL = 'https://athletics.baruch.cuny.edu/sports/womens-volleyball/roster'
brooklynMenSwimURL = 'https://www.brooklyncollegeathletics.com/sports/mens-swimming-and-diving/roster'
brooklynMenVolleyballURL = 'https://www.brooklyncollegeathletics.com/sports/mens-volleyball/roster/2019'
brooklynWomenSwimURL = 'https://www.brooklyncollegeathletics.com/sports/womens-swimming-and-diving/roster'
brooklynWomenVolleyballURL = 'https://www.brooklyncollegeathletics.com/sports/womens-volleyball/roster/2019'
yorkMenVolleyballURL = 'https://yorkathletics.com/sports/mens-volleyball/roster'
yorkMenSwimURL = 'https://yorkathletics.com/sports/mens-swimming-and-diving/roster'
johnJayWomenVolleyballURL = 'https://johnjayathletics.com/sports/womens-volleyball/roster'
queensWomenSwimURL = 'https://queensknights.com/sports/womens-swimming-and-diving/roster'
warnings.filterwarnings('ignore')

#connects to URL, scrapes heights and names using parameters
def getDataFromURL(URL, tagType, className, isHeight):
    page = requests.get(URL, verify = False)
    soup = BeautifulSoup(page.content, 'html.parser')
    if isHeight:
        dataList = [float(tag['data-sort']) for tag in soup.find_all(tagType, class_ = className)]
        return dataList
    else:
        dataList = [tag['data-sort'] for tag in soup.find_all(tagType, class_ = className)]
        cleanedNames = []
        for name in dataList:
            if len(name.split(', ')) > 2:
                cleanedNames.append(name.split(', ')[2]+ " " + name.split(', ')[0] + " " + name.split(', ')[1])
            else:
                cleanedNames.append(name.split(', ')[1] + " " + name.split(', ')[0])
        return cleanedNames

#function that creates a dataframe from the lists of heights and names
def getDataframesFromLists(URLList):
    formattedData = pd.DataFrame()
    for URL in URLList:
        heightList = getDataFromURL(URL, 'td', 'height', True)
        nameList = getDataFromURL(URL, 'td', 'sidearm-table-player-name', False)
        nameToHeightMapping = pd.DataFrame({"Name": nameList,"Height (inches)": heightList})
        formattedData = formattedData.append(nameToHeightMapping, ignore_index=True)
    return formattedData

menSwimURLs = list([baruchMenSwimURL, brooklynMenSwimURL, yorkMenSwimURL])
womenSwimURLs = list([baruchWomenSwimURL, brooklynWomenSwimURL, queensWomenSwimURL])
menVolleyballURLs = list([bauchMenVolleyballURL, brooklynMenVolleyballURL, yorkMenVolleyballURL])
womenVolleyballURLs = list([baruchWomenVolleyballURL, brooklynWomenVolleyballURL, johnJayWomenVolleyballURL])

#groups dataframes separated by mens' and womens' and sports type
mensSwimDataFrame = getDataframesFromLists(menSwimURLs)
womensSwimDataFrame = getDataframesFromLists(womenSwimURLs)
mensVolleyballDataFrame = getDataframesFromLists(menVolleyballURLs)
womensVolleyballDataFrame = getDataframesFromLists(womenVolleyballURLs)

#prints results for average heights separated by mens' and womens' and sports type
print("Mens' swim average height: ", round(mensSwimDataFrame["Height (inches)"].mean(axis=0), 2), "inches")
print("Womens' swim average height: ", round(womensSwimDataFrame["Height (inches)"].mean(axis=0),2), "inches")
print("Mens' volleyball average height: ", round(mensVolleyballDataFrame["Height (inches)"].mean(axis=0), 2), "inches")
print("Womens' Volleyball average height: ", round(womensVolleyballDataFrame["Height (inches)"].mean(axis=0), 2), "inches")
print('\n')

#sorts dataframes by height column
mensSwimDataFrame = mensSwimDataFrame.sort_values(by=["Height (inches)"], ascending = False) 
womensSwimDataFrame = womensSwimDataFrame.sort_values(by=["Height (inches)"], ascending = False)
mensVolleyballDataFrame = mensVolleyballDataFrame.sort_values(by=["Height (inches)"], ascending = False)
womensVolleyballDataFrame = womensVolleyballDataFrame.sort_values(by=["Height (inches)"], ascending = False)

#prints results for top 5 and bottom 5 tallest/shortest sports players separated by mens' and womens' and sports type
print("These are the 5 tallest men swimmers from the data:", '\n', mensSwimDataFrame.head().to_string(index=False),'\n', '\n')
print("These are the 5 shortest men swimmers from the data:", '\n', mensSwimDataFrame.tail().to_string(index=False),'\n', '\n')
print("These are the 5 tallest women swimmers from the data:", '\n', womensSwimDataFrame.head().to_string(index=False), '\n', '\n')
print("These are the 5 shortest women swimmers from the data:", '\n', womensSwimDataFrame.tail().to_string(index=False), '\n', '\n')
print("These are the 5 tallest men volleyball players from the data:", '\n', mensVolleyballDataFrame.head().to_string(index=False), '\n', '\n')
print("These are the 5 shortest men volleyball players from the data:", '\n', mensVolleyballDataFrame.tail().to_string(index=False), '\n', '\n')
print("These are the 5 tallest women volleyball players from the data:", '\n', womensVolleyballDataFrame.head().to_string(index=False), '\n', '\n')
print("These are the 5 shortest women volleyball players from the data:", '\n', womensVolleyballDataFrame.tail().to_string(index=False), '\n', '\n')
