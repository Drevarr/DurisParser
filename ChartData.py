# fetch rows from PVP_logs table Fight_Logs and logs in good and evil groups that are in pov logs table
import sqlite3


# Connect to the database
conn = sqlite3.connect('PVP_Logs.db')
cursor = conn.cursor()

#RaceWar_Side, Frag_Level, Frag_Class, Frag_Name, Frag_Guild, Frag_Race, Good_Group, Good_Group_Logs, Evil_Group, Evil_Group_Logs

# summarize FightLogs table by counting number of rows in each group for each Date and RaceWar_Side

# Group deaths bu side and date
cursor.execute('''SELECT Date, RaceWar_Side, COUNT(*) AS Deaths, COUNT(*) OVER(PARTITION BY Date ORDER BY Date) AS Total_Deaths
FROM Fight_Logs
GROUP BY Date, RaceWar_Side, Date;''')

# store all the fetched data in the ans variable
DailyDeathByRacewarSides = cursor.fetchall()

# Group deaths by side and race
cursor.execute('''
    SELECT RaceWar_Side, Frag_Race, COUNT(*) AS Count
    FROM Fight_Logs
    GROUP BY RaceWar_Side, Frag_Race;
''')
RaceDeathsbySide = cursor.fetchall()

print(DailyDeathByRacewarSides)
print("\n")
print(RaceDeathsbySide)

conn.close()