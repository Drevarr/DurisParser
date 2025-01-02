from bs4 import BeautifulSoup
from pprint import pprint
import re
import csv
import requests
import sqlite3

apiStatus = True
listOfLogs = []

# REGEX for parsing elements
DmgLine = re.compile("\[Damage:\s+(\d+)\s+\]")
PromptLine = re.compile("< (?P<Cur_HP>\d+)h/(\d+)H (\d+)v/(\d+)V Pos: (.*) >")
RacesGood = re.compile("(?:A|a|An|an) (Human|Barbarian|Grey Elf|Mountain Dwarf|Halfling|Gnome|Centaur|Githzerai|Firbolg)")
RacesNeutral = re.compile("(?:A|a|An|an) (Thri-Kreen|Minotaur|Shade|ShadowBeast|Vampire)")
RacesEvil = re.compile("(?:A|a|An|an) (Orc|Troll|Drow Elf|Duergar|Goblin|Kobold|Ogre|Githyanki|Drider)")

# URL for fetching LogNumber
URL = 'https://www.durismud.com/pvp/logs/'


# Connect to the database
conn = sqlite3.connect('PVP_Logs_Dec_2024_Wipe.db')
cursor = conn.cursor()


# create sqlite table
conn.execute('''CREATE TABLE IF NOT EXISTS POV_Logs (
    Log_Number PRIMARY KEY,
    Total_Damage, 
    Max_Pulse_Damage, 
    Min_Pulse_Damage, 
    Average_Pulse_Damage, 
    Pulses
);''')

#Select all rows from table Logs where Log_Number is not in table POV_Logs stored in listOfLogs
query = "SELECT * FROM Logs WHERE Log_Number NOT IN (SELECT Log_Number FROM POV_Logs)"
cursor.execute(query)

# Fetch all the rows
rows = cursor.fetchall()

for item in rows:
    listOfLogs.append(item[0])

# open the file in the write mode
with open("PVP_Logs.csv", "w", newline='') as f:
    # create the csv writer
    writer = csv.writer(f)

    # write the header
    writer.writerow(["Log Number", "Total Damage", "Max Pulse Damage", "Min Pulse Damage", "Average Pulse Damage", "Pulses"])

    for log in listOfLogs:
        req = requests.get(URL + str(log))
        soup = BeautifulSoup(req.text, "html5lib")
        pvpLog = soup.find('pre', class_="ansi log")

        pulseDamageList = []
        pulseDamage = 0

        textLog = pvpLog.get_text()

        print(f"Processing PVP Log: {log}")

        for line in textLog.splitlines():
                
            foundDmg = DmgLine.findall(line)
            foundEnemy = RacesGood.findall(line) or RacesNeutral.findall(line) or RacesEvil.findall(line)  

            if foundEnemy:
                for item in foundDmg:
                    pulseDamage +=int(item)
                
            foundPrompt = PromptLine.match(line)
            if foundPrompt:
                if pulseDamage:
                    pulseDamageList.append(pulseDamage)
                    pulseDamage = 0
                    
        #Add final round damage when log ends without prompt
        if pulseDamage:
            pulseDamageList.append(pulseDamage)

        if pulseDamageList:
                
            totalDamage = sum(pulseDamageList) or 0
            maxPulse = max(pulseDamageList) or 0
            minPulse = min(pulseDamageList) or 0
            avgPulse = round(sum(pulseDamageList)/len(pulseDamageList),1) or 0
            pulses = len(pulseDamageList) or 0

            # write a row to the csv file
            writer.writerow([log, totalDamage, maxPulse, minPulse, avgPulse, pulses])

            # Insert the PVP data into the table
            cursor.execute('INSERT OR IGNORE INTO POV_Logs (Log_Number, Total_Damage, Max_Pulse_Damage, Min_Pulse_Damage, Average_Pulse_Damage, Pulses) VALUES (?, ?, ?, ?, ?, ?)',
                    (log, totalDamage, maxPulse, minPulse, avgPulse, pulses))

        else:
            writer.writerow([log, 0, 0, 0, 0, 0])

            # Insert the PVP data into the table
            cursor.execute('INSERT OR IGNORE INTO POV_Logs (Log_Number, Total_Damage, Max_Pulse_Damage, Min_Pulse_Damage, Average_Pulse_Damage, Pulses) VALUES (?, ?, ?, ?, ?, ?)',
                    (log, 0, 0, 0, 0, 0))


# Commit the changes and close the connection
conn.commit()
conn.close()
    
print("Complete")