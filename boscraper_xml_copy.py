import requests
from bs4 import BeautifulSoup
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Initialize an XML root element
root = ET.Element('players')

i = 1

def get_data(url):
    r = requests.get(url)
    return r.text

print("Gathering Player Info....")
image_prefix = "https://lycomingathletics.com"
htmldata = get_data("https://lycomingathletics.com/sports/football/roster")
soup = BeautifulSoup(htmldata, 'html.parser')

for player in soup.find_all("li", class_="sidearm-roster-player"):
    player_id = str(i)
    player_position = player.find("span", class_="text-bold")
    player_pos = str(player_position.text).strip()
    player_pos = re.sub('[^A-Za-z0-9]+', '', str(player_pos))
    player_pos_len = len(player_pos)

    if player_pos_len == 7:
        player_pos_len = player_pos_len - 1
    else:
        player_pos_len = player_pos_len - 2
    player_pos = player_pos[:player_pos_len]

    player_height = player.find("span", class_="sidearm-roster-player-height")
    player_uni = player.find("span", class_="sidearm-roster-player-jersey-number")  # Change 'number' to 'uni'
    player_name = player.find("h3")
    player_grade = player.find("span", class_="sidearm-roster-player-academic-year")
    player_hometown = player.find("span", class_="sidearm-roster-player-hometown")
    player_high_school = player.find("span", class_="sidearm-roster-player-highschool")
    player_image = player.find("div", class_="sidearm-roster-player-image")

    try:
        str_item = str(player_image)
        begin_image_index = str_item.find('data-src') + 10
        end_image_index = str_item.find('?width')
        link_name = str_item[begin_image_index:end_image_index]

        player_element = ET.SubElement(root, 'player')
        ET.SubElement(player_element, 'id').text = player_id
        ET.SubElement(player_element, 'name').text = player_name.text.strip()
        ET.SubElement(player_element, 'class').text = player_grade.text.strip()
        ET.SubElement(player_element, 'position').text = player_pos
        ET.SubElement(player_element, 'height').text = player_height.text.strip()
        ET.SubElement(player_element, 'uni').text = player_uni.text.strip()  # Change 'number' to 'uni'
        ET.SubElement(player_element, 'hometown').text = player_hometown.text.strip()
        ET.SubElement(player_element, 'highschool').text = player_high_school.text.strip()
        ET.SubElement(player_element, 'image').text = image_prefix + link_name.strip()

        i += 1
    except AttributeError:
        pass

tree = ET.ElementTree(root)

# Pretty print the XML
xml_str = ET.tostring(root, encoding='utf-8').decode()
xml_str = minidom.parseString(xml_str).toprettyxml()

with open('players.xml', 'w') as xml_file:
    xml_file.write(xml_str)

print("Done! Data has been exported to players.xml")
