from bs4 import BeautifulSoup
from pprint import pprint
import re
import csv
import requests
import sqlite3

apiStatus = True
listOfLogs = ["295710","295709","295708","295707","295706","295705","295704","295703","295702","295701"]

# REGEX for parsing elements
DmgLine = re.compile("\[Damage: (\d+) \]")
PromptLine = re.compile("< (?P<Cur_HP>\d+)h/(\d+)H (\d+)v/(\d+)V Pos: (.*) >")

# URL for fetching LogNumber
URL = 'https://www.durismud.com/pvp/logs/'


# Connect to the database
conn = sqlite3.connect('PVP_Logs.db')
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

        for line in textLog.splitlines():
                
            foundDmg = DmgLine.findall(line)
            for item in foundDmg:
                pulseDamage +=int(item)
            
            foundPrompt = PromptLine.match(line)
            if foundPrompt:
                if pulseDamage:
                    pulseDamageList.append(pulseDamage)
                    pulseDamage = 0
                    
        #Add final round damage when log endds without prompt
        if pulseDamage:
            pulseDamageList.append(pulseDamage)

        if pulseDamageList:
                
            totalDamage = sum(pulseDamageList) or 0
            maxPulse = max(pulseDamageList) or 0
            minPulse = min(pulseDamageList) or 0
            avgPulse = sum(pulseDamageList)/len(pulseDamageList) or 0
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