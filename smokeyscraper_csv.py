import requests 
from bs4 import BeautifulSoup 
import re

i = 1
file_name = input("Enter the name for your file:")
file_name_with_extension = file_name + ".txt"
outfile = open(file_name_with_extension, "w")
outfile.write("id | name | class | position | height | uni | hometown | highschool | Image \n")
	
def getdata(url): 
	r = requests.get(url) 
	return r.text 
print("Gathering Player Info....")
imagePrefix = "https://ursinusathletics.com/"
htmldata = getdata("https://ursinusathletics.com/sports/football/roster") 
soup = BeautifulSoup(htmldata, 'html.parser') 
for players in soup("li", class_="sidearm-roster-player"):
    #print(players)
    
    player_id = str(i) 
    player_position = players.find("span", class_="text-bold")
    player_pos = str(player_position.text).strip()
    player_pos = re.sub('[^A-Za-z0-9]+', '',str(player_pos))
    player_pos_len = len(player_pos)
    
    if player_pos_len == 7:
        player_pos_len = player_pos_len - 1
    else:
        player_pos_len = player_pos_len - 2
    player_pos = player_pos[:player_pos_len]
    
        
    player_height = players.find("span", class_="sidearm-roster-player-height")
    player_number = players.find("span", class_="sidearm-roster-player-jersey-number")
    player_name = players.find("h3")
    player_grade = players.find("span", class_="sidearm-roster-player-academic-year")
    player_hometown = players.find("span", class_="sidearm-roster-player-hometown")
    player_high_school = players.find("span", class_="sidearm-roster-player-highschool")
    player_image = players.find("div", class_="sidearm-roster-player-image")
    try:
        player_url = player_image("href")
    except TypeError:
        pass   
    beginImageIndex = (str(player_image).find('data-src') + 10)
    endImageIndex = str(player_image).find('?width')
    strItem = str(player_image)
    linkName = strItem[beginImageIndex:endImageIndex]
   
    try:
        # print(f'{str(player_id)} | {str(player_name.text).strip()} | {str(player_grade.text).strip()} |\
        #     {str(player_pos).strip()} | {str(player_height.text).strip()} |\
        #     {str(player_number.text).strip()} | {str(player_hometown.text).strip()} |\
        #     {str(player_high_school.text).strip()} |') 
        outputImage = f'{str(player_id)} | {str(player_name.text).strip()} | {str(player_grade.text).strip()} |\
 {str(player_pos).strip()} | {str(player_height.text).strip()} |\
 {str(player_number.text).strip()} | {str(player_hometown.text).strip()} |\
 {str(player_high_school.text).strip()} | {imagePrefix + str(linkName).strip()} \n'
        outfile.write(outputImage) 
        i = i + 1 
    except AttributeError:
        pass      
outfile.close()
print("Done!")
