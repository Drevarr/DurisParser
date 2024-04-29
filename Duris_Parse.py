#!/usr/bin/env python3

#    Duris_Parse.py contains tools for retrieving PvP log data for DurisMUD.
#    Copyright (C) 2021 John Long
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from bs4 import BeautifulSoup
from pprint import pprint
import re
import csv
import requests
import sqlite3

#TO DO
#refactor for functions
#develop config file
#develop beak out based on last previous log recorded
#write append logic
#clean up
# 
# https://www.durismud.com/pvp/logs/295681

Num_Pages = 1
Latest_Log = 295681

def Parse_Page(number, pages):

    Latest_Log = number
    Num_Pages = pages

    for page in range(1,Num_Pages+1):
        req = requests.get(URL + str(page))
        soup = BeautifulSoup(req.text, "html5lib")
        table = soup.find('table')
        tbody = table.find('tbody')
        rows = tbody.findAll("tr", recursive=False)
        for row in rows:
            if len(row)==9:
                col = row.findAll ("td", recursive=False)
                Date = col[0].text
                Location = col[1].text.strip()
                #Process the Good Group subtable to capture each row Data
                Good_Group = []
                Good_Group_Logs = []
                Good_Group_Count = 0
                Good_Frag = ""
                Good_Tds = col[2].findAll("td", class_="nowrap")
                for Good_Td in Good_Tds:
                    Good_Group_Count += 1
                    Good_Group.append(Good_Td.text.strip())
                    FightLink = Good_Td.find(href=True)
                    link = FightLink['href']
                    r = q.match(link)
                    POV_Log_Number = r[1]
                    Good_Group_Logs.append(POV_Log_Number)
                    if Good_Td.find("span", class_="blood"):
                        RaceWar_Side = "Goodies"
                        Good_Frag = Good_Td.text.strip()
                        m = p.match(Good_Frag)
                        FragDict = m.groupdict()
                        Frag_Level = FragDict['PC_LEVEL']
                        Frag_Class = FragDict['PC_CLASS']
                        Frag_Name = FragDict['PC_NAME']
                        Frag_Guild = FragDict['PC_GUILD']
                        Frag_Race = FragDict['PC_RACE']
                        #q = re.compile(r'\/pvp\/logs\/(?P<Log_Number>\d*)')
                        #FragLink = Good_Td.find(href=True)
                        #link = FragLink['href']
                        #r = q.match(link)
                        Log_Number = POV_Log_Number
                        if int(Log_Number) <= Latest_Log:
                            return

                #Process the Evils Group subtable to capture each row Data
                Evil_Group = []
                Evil_Group_Logs = []
                Evil_Group_Count = 0
                Evil_Frag = ""
                Evil_Tds = col[3].findAll("td", class_="nowrap")
                for Evil_Td in Evil_Tds:
                    Evil_Group_Count += 1
                    Evil_Group.append(Evil_Td.text.strip())
                    FightLink = Evil_Td.find(href=True)
                    link = FightLink['href']
                    r = q.match(link)
                    POV_Log_Number = r[1]
                    Evil_Group_Logs.append(POV_Log_Number)
                    if Evil_Td.find("span", class_="blood"):
                        RaceWar_Side = "Evils"
                        Evil_Frag = Evil_Td.text.strip()
                        m = p.match(Evil_Frag)
                        FragDict = m.groupdict()
                        Frag_Level = FragDict['PC_LEVEL']
                        Frag_Class = FragDict['PC_CLASS']
                        Frag_Name = FragDict['PC_NAME']
                        Frag_Guild = FragDict['PC_GUILD']
                        Frag_Race = FragDict['PC_RACE']
                        #q = re.compile(r'\/pvp\/logs\/(?P<Log_Number>\d*)')
                        #FragLink = Good_Td.find(href=True)
                        #link = FragLink['href']
                        #r = q.match(link)
                        Log_Number = POV_Log_Number
                        if int(Log_Number) <= Latest_Log:
                            return

                # test print the info
                #print_string = (Date+', '+Location+', '+str(Good_Group_Count)+', '+str(Evil_Group_Count)+', '+RaceWar_Side+', '+Frag_Level+', '+Frag_Class+', '+Frag_Name+', '+Frag_Guild+', '+Frag_Race+', '+Log_Number)
                #print (print_string)
                
                # write a row to the csv file
                writer.writerow([Date, Location, Good_Group_Count, Evil_Group_Count, RaceWar_Side, Frag_Level, Frag_Class, Frag_Name, Frag_Guild, Frag_Race, Log_Number, str(Good_Group), str(Good_Group_Logs), str(Evil_Group), str(Evil_Group_Logs)])
                
                # Set LogData for insertion into sqlite3 db
                LogData = (Log_Number, Date, Location, Good_Group_Count, Evil_Group_Count, RaceWar_Side, Frag_Level, Frag_Class, Frag_Name, Frag_Guild, Frag_Race, str(Good_Group), str(Good_Group_Logs), str(Evil_Group), str(Evil_Group_Logs))
                print("(Log_Number, Date, Location, Good_Group_Count, Evil_Group_Count, RaceWar_Side, Frag_Level, Frag_Class, Frag_Name, Frag_Guild, Frag_Race, str(Good_Group), str(Evil_Group))")
                print(LogData)
                #insert the new data if not already in table based on Log_Number
                #sql_insert(con, LogData)
                print(str(Good_Group_Logs))
                print(str(Evil_Group_Logs))

                #for log in Good_Group_Logs:
                    #cursor.execute('INSERT OR IGNORE INTO Logs (Log_Number) VALUES (?)', log)
                #for log in Evil_Group_Logs:
                    #cursor.execute('INSERT OR IGNORE INTO Logs (Log_Number) VALUES (?)', log)
                    
                # Insert the PVP data into the table
                cursor.execute('INSERT OR IGNORE INTO Fight_Logs (Log_Number, Date, Location, Good_Group_Count, Evil_Group_Count, RaceWar_Side, Frag_Level, Frag_Class, Frag_Name, Frag_Guild, Frag_Race, Good_Group, Good_Group_Logs, Evil_Group, Evil_Group_Logs) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        LogData)
                 
                #commit new data
                #con.commit()

# Connect to the database
conn = sqlite3.connect('PVP_Logs.db')
cursor = conn.cursor()


# create sqlite table
conn.execute('''CREATE TABLE IF NOT EXISTS Fight_Logs (
    Log_Number PRIMARY KEY,
    Date,
    Location,
    Good_Group_Count,
    Evil_Group_Count,
    RaceWar_Side,
    Frag_Level,
    Frag_Class,
    Frag_Name,
    Frag_Guild,
    Frag_Race,
    Good_Group,
    Good_Group_Logs,
    Evil_Group,
    Evil_Group_Logs
);''')

conn.execute('''CREATE TABLE IF NOT EXISTS Logs (Log_Number PRIMARY KEY);''')

# open the file in the write mode
with open("PVP_Data.csv", "w", newline='') as f:
    # create the csv writer
    writer = csv.writer(f)

    # write the header
    writer.writerow(["Date", "Location", "Good_Group_Count", "Evil_Group_Count", "RaceWar_Side", "Frag_Level", "Frag_Class", "Frag_Name", "Frag_Guild", "Frag_Race", "Log_Number", "Good Group", "Good Group Logs", "Evil Group", "Evil Group Logs"])

    # REGEX for parsing elements
    p = re.compile(r'\[\s*(?P<PC_LEVEL>\d*)\s(?P<PC_CLASS>.*)]\s(?P<PC_NAME>\w*)\s(?P<PC_GUILD>.*)\((?P<PC_RACE>.*)\)\s*')
    q = re.compile(r'\/pvp\/logs\/(?P<Log_Number>\d*)')
    URL = 'https://www.durismud.com/pvp/events?page='
  
    Parse_Page(Latest_Log, Num_Pages)

# Commit the changes and close the connection
conn.commit()
conn.close()

print ("Processing Complete. See file: PVP_Data.csv or PVP_Logs.db")