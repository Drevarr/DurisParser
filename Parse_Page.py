#!/usr/bin/env python3

#    Parse_Page contains tools for retrieving PvP log data for DurisMUD.
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
                Good_Group_Count = 0
                Good_Frag = ""
                Good_Tds = col[2].findAll("td", class_="nowrap")
                for Good_Td in Good_Tds:
                    Good_Group_Count += 1
                    Good_Group.append(Good_Td.text.strip())
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
                        FragLink = Good_Td.find(href=True)
                        link = FragLink['href']
                        r = q.match(link)
                        Log_Number = r[1]
                        if int(Log_Number) <= Latest_Log:
                            return

                #Process the Evils Group subtable to capture each row Data
                Evil_Group = []
                Evil_Group_Count = 0
                Evil_Frag = ""
                Evil_Tds = col[3].findAll("td", class_="nowrap")
                for Evil_Td in Evil_Tds:
                    Evil_Group_Count += 1
                    Evil_Group.append(Evil_Td.text.strip())
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
                        FragLink = Good_Td.find(href=True)
                        link = FragLink['href']
                        r = q.match(link)
                        Log_Number = r[1]
                        if int(Log_Number) <= Latest_Log:
                            return

                # test print the info
                print_string = (Date+', '+Location+', '+str(Good_Group_Count)+', '+str(Evil_Group_Count)+', '+RaceWar_Side+', '+Frag_Level+', '+Frag_Class+', '+Frag_Name+', '+Frag_Guild+', '+Frag_Race+', '+Log_Number)
                print (print_string)
                
                # write a row to the csv file
                writer.writerow([Date, Location, Good_Group_Count, Evil_Group_Count, RaceWar_Side, Frag_Level, Frag_Class, Frag_Name, Frag_Guild, Frag_Race, Log_Number])
                
                # Set LogData for insertion into sqlite3 db
                LogData = (Log_Number, Date, Location, Good_Group_Count, Evil_Group_Count, RaceWar_Side, Frag_Level, Frag_Class, Frag_Name, Frag_Guild, Frag_Race, str(Good_Group), str(Evil_Group))
                print(LogData)
                #insert the new data if not already in table based on Log_Number
                #sql_insert(con, LogData)
                
                #commit new data
                #con.commit()
