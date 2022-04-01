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
import Parse_Page

#TO DO
#refactor for functions
#develop config file
#develop beak out based on last previous log recorded
#write append logic
#clean up
# 
# 

Num_Pages = 1
Latest_Log = 275010

# open the file in the write mode
with open("PVP_Data.csv", "w", newline='') as f:
    # create the csv writer
    writer = csv.writer(f)

    # write the header
    writer.writerow(["Date", "Location", "Good_Group_Count", "Evil_Group_Count", "RaceWar_Side", "Frag_Level", "Frag_Class", "Frag_Name", "Frag_Guild", "Frag_Race", "Log_Number"])

    # REGEX for parsing elements
    p = re.compile(r'\[\s*(?P<PC_LEVEL>\d*)\s(?P<PC_CLASS>.*)]\s(?P<PC_NAME>\w*)\s(?P<PC_GUILD>.*)\((?P<PC_RACE>.*)\)\s*')
    q = re.compile(r'\/pvp\/logs\/(?P<Log_Number>\d*)')
    URL = 'https://www.durismud.com/pvp/events?page='
  
    Parse_Page(Latest_Log, Num_Pages)


print ("Processing Complete. See file: PVP_Data.csv")