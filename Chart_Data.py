# fetch rows from PVP_logs table Fight_Logs and logs in good and evil groups that are in pov logs table
import sqlite3
import ast
from datetime import datetime

#LogNames dictionary of log Numbers as key and POV Name as value
LogNames={}

# Connect to the database
conn = sqlite3.connect('PVP_Logs_May_2024_Wipe.db')
cursor = conn.cursor()

#RaceWar_Side, Frag_Level, Frag_Class, Frag_Name, Frag_Guild, Frag_Race, Good_Group, Good_Group_Logs, Evil_Group, Evil_Group_Logs

# summarize FightLogs table by counting number of rows in each group for each Date and RaceWar_Side

# Group deaths bu side and date
cursor.execute('''SELECT Date, RaceWar_Side, COUNT(*) AS Deaths
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

# POV Log Data
cursor.execute('''
    SELECT *
    FROM POV_Logs
    ORDER BY Max_Pulse_Damage DESC;
''')

PovData = cursor.fetchall()

cursor.execute('''
    SELECT *
    FROM POV_Logs
    ORDER BY Total_Damage DESC;
''')

PovTotalDamageData = cursor.fetchall()

# Duris PvP Data
cursor.execute('''
    SELECT *
    FROM Fight_Logs;
''')

DurisData = cursor.fetchall()


#Gather Logs with POV Name
for row in DurisData:
    goodKeys = ast.literal_eval(row[13])
    goodValues = ast.literal_eval(row[12])
    evilKeys = ast.literal_eval(row[15])
    evilValues = ast.literal_eval(row[14])
    for i, key in enumerate(goodKeys):
        LogNames[key] = goodValues[i]
    for i, key in enumerate(evilKeys):
        LogNames[key] = evilValues[i]
        
print(DailyDeathByRacewarSides)
print("\n")
print(RaceDeathsbySide)

conn.close()

#Collect Evil and Good deaths by date
EvilDeaths={}
GoodDeaths={}
for item in DailyDeathByRacewarSides:
    date, side, deaths = item
    if side == 'Evils':
        EvilDeaths[date] = deaths
    else:
        GoodDeaths[date] = deaths

#Convert EvilDeaths and GoodDeaths into lists for chart data
DeathDates=[]
EvilCount=[]
GoodCount=[]
EvilTotalCount=[]
GoodTotalCount=[]
EvilRaceDeaths = {}
GoodRaceDeaths = {}

#Collect DeathDates
for date in EvilDeaths:
    DeathDates.append(date)
for date in GoodDeaths:
    if date not in DeathDates:
        DeathDates.append(date)


#Sort DeathDates
DeathDates.sort(key = lambda date: datetime.strptime(date, '%m/%d/%y'))

print(DeathDates)

#Fill EvilCount and GoodCount by sorted DeathDates
for date in DeathDates:
    if date in EvilDeaths:
        EvilCount.append(EvilDeaths[date])
    else:
        EvilCount.append(0)

    if date in GoodDeaths:
        GoodCount.append(GoodDeaths[date])
    else:
        GoodCount.append(0)

print('Evils:', EvilCount)
print('Goods:', GoodCount)

#Fill EvilTotalCount for cumulative by day chart
sumTotal = 0
for i in EvilCount:
    sumTotal += i
    EvilTotalCount.append(sumTotal)
print('Evils', EvilTotalCount)

#Fill GoodTotalCount for cumulative by day chart
sumTotal = 0
for i in GoodCount:
    sumTotal += i
    GoodTotalCount.append(sumTotal)
print('Goods', GoodTotalCount)

#Collect deaths by race
for item in RaceDeathsbySide:
    side, race, count = item
    if side == "Evils":
        EvilRaceDeaths[race] = count
    else:
        GoodRaceDeaths[race] = count

#Convert EvilRaceDeaths and GoodRaceDeaths into lists for chart data
EvilRaces = EvilRaceDeaths.keys()
EvilRaceCount = EvilRaceDeaths.values()
print(list(EvilRaces))
print(list(EvilRaceCount))

GoodRaces = GoodRaceDeaths.keys()
GoodRaceCount = GoodRaceDeaths.values()
print(list(GoodRaces))
print(list(GoodRaceCount))

#print top 20 pulse damage table
POV_Keys = ['Log', 'Total', 'Max', 'Min', 'Avg', 'Pulses']
url="https://www.durismud.com/pvp/logs/"
print("|Rank |Log | Total Dmg| Max Dmg| Min Dmg| Avg Dmg| Pulses|h")

for i in range(20):
    print(f"|{i+1} |[[{LogNames[PovData[i][0]]}|{url+PovData[i][0]}]] | {PovData[i][1]}| {PovData[i][2]}| {PovData[i][3]}| {PovData[i][4]}| {PovData[i][5]}|")
 

#LogNames dictionary of log Numbers as key and POV Name as value
LogNames={}
#Gather Logs with POV Name
for row in DurisData:
    goodKeys = ast.literal_eval(row[13])
    goodValues = ast.literal_eval(row[12])
    evilKeys = ast.literal_eval(row[15])
    evilValues = ast.literal_eval(row[14])
    for i, key in enumerate(goodKeys):
        LogNames[key] = goodValues[i]
    for i, key in enumerate(evilKeys):
        LogNames[key] = evilValues[i]

#Collect Group Sizes by Date
GroupSizeData = {}

for row in DurisData:
    if row[1] not in GroupSizeData:
        GroupSizeData[row[1]] ={}
        GroupSizeData[row[1]]['Goods'] = []
        GroupSizeData[row[1]]['Evils'] = []
    GroupSizeData[row[1]]['Goods'].append(row[4])
    GroupSizeData[row[1]]['Evils'].append(row[5])

#Print Group Sizes by Date for chart data
print("['Date', 'Fights', 'Avg Goods', 'Avg Evils'],")
for date in DeathDates:
    cntFights = len(GroupSizeData[date]['Goods'])
    avgGoods = sum(GroupSizeData[date]['Goods'])/len(GroupSizeData[date]['Goods'])
    avgEvils = sum(GroupSizeData[date]['Evils'])/len(GroupSizeData[date]['Evils'])
    print (f"      ['{str(date)}', {cntFights}, {round(avgGoods,2)}, {round(avgEvils,2)}],")

#Collect Deaths by RaceWar_Side and name for chart data
NamedDeaths={}
NamedDeaths['Evils']={}
NamedDeaths['Goods']={}

for row in DurisData:
    Name=row[9]
    Side=row[6]
    if Side == 'Evils':
        if Name not in NamedDeaths['Evils']:
            NamedDeaths['Evils'][Name] = 1
        else:
            NamedDeaths['Evils'][Name] += 1
    else:
        if Name not in NamedDeaths['Goods']:
            NamedDeaths['Goods'][Name] = 1
        else:
            NamedDeaths['Goods'][Name] += 1


#write echarts .tid file with chart data
ChartList =[
    '2024MayWipe_GroupSize_Data',
    '2024MayWipe_TopDamageLogs',
    '2024MayWipe_DeathByRaceGood_Data',
    '2024MayWipe_DeathByRaceEvil_Data',
    '2024MayWipe_DeathByDay_Data',
    '2024MayWipe_DeathTotals',
    '2024MayWipe_TotalDamage_Data',
    '2024MayWipe_EvilDeathsByName_Data',
    '2024MayWipe_GoodDeathsByName_Data',
    ]

for item in ChartList:
    with open(f'{item}.tid', 'w', encoding='utf8') as f:
        print_String = f"""created: {datetime.now().strftime("%Y%m%d%H%M%S")}
creator: Drevarr
tags: ChartData
title: {item}
type: text/vnd.tiddlywiki
"""
        f.write(print_String)

        if item == '2024MayWipe_GroupSize_Data':
            print_String = f"""
            option = {{
            title: {{
                text: 'Average Group Size for Fights'
                }},
            legend: {{}},
            tooltip: {{
                trigger: 'axis',
                confine: true
                }},
            dataZoom: [
                {{
                type: 'inside',
                xAxisIndex: [0, 1],
                start: 0,
                end: 100
                }},
                {{
                show: true,
                xAxisIndex: [0, 1],
                type: 'slider',
                bottom: 10,
                start: 0,
                end: 100
                }}
            ],
            dataset: {{
                source: [
                ['Date', 'Fights', 'Avg Goods', 'Avg Evils'],
            """
            f.write(print_String)

            for date in DeathDates:
                cntFights = len(GroupSizeData[date]['Goods'])
                avgGoods = sum(GroupSizeData[date]['Goods'])/len(GroupSizeData[date]['Goods'])
                avgEvils = sum(GroupSizeData[date]['Evils'])/len(GroupSizeData[date]['Evils'])
                print_String = f"""
                ['{str(date)}', {cntFights}, {round(avgGoods,2):.2f}, {round(avgEvils,2):.2f}],
                """
                f.write(print_String)

            print_String = f"""
            ]
            }},
            xAxis: [{{type: 'category', gridIndex: 0,}},{{type: 'category', gridIndex: 1,}}],
            xAxis: {{ type: 'category' }},
            yAxis: {{}},
            // Declare several bar series, each will be mapped
            // to a column of dataset.source by default.
            series: [{{ type: 'line' }}, {{ type: 'bar' }}, {{ type: 'bar' }}]
            }};
        """
            f.write(print_String)
            f.close()

        if item == '2024MayWipe_TopDamageLogs':
            #print top 20 pulse damage table
            POV_Keys = ['Log', 'Total', 'Max', 'Min', 'Avg', 'Pulses']
            url="https://www.durismud.com/pvp/logs/"
            print_String ="\n|thead-dark table-hover sortable w-75|k\n"
            f.write(print_String)
            print_String ="|Rank |Log | Total Dmg| Max Dmg| Min Dmg| Avg Dmg| Pulses|h\n"
            f.write(print_String)

            for i in range(20):
                print_String = f"|{i+1} |[[{LogNames[PovData[i][0]]}|{url+PovData[i][0]}]] | {PovData[i][1]}| {PovData[i][2]}| {PovData[i][3]}| {PovData[i][4]}| {PovData[i][5]}|\n"
                f.write(print_String)
            f.close()

        if item == '2024MayWipe_DeathByRaceGood_Data':
            print_String = f"""
            option = {{
            title: {{
                text: 'Good Race Deaths'
            }},
            tooltip: {{
                trigger: 'axis'
            }},
            xAxis: {{
                type: 'category',
                data: {list(GoodRaces)}
            }},
            yAxis: {{
                type: 'value'
            }},
            series: [
                {{
                data: {list(GoodRaceCount)},
                type: 'bar'
                }}
            ]
            }};"""
            f.write(print_String)
            f.close()

        if item == '2024MayWipe_DeathByRaceEvil_Data':
            print_String = f"""
            option = {{
            title: {{
                text: 'Evil Race Deaths'
            }},
            tooltip: {{
                trigger: 'axis'
            }},
            xAxis: {{
                type: 'category',
                data: {list(EvilRaces)}
            }},
            yAxis: {{
                type: 'value'
            }},
            series: [
                {{
                data: {list(EvilRaceCount)},
                type: 'bar'
                }}
            ]
            }};"""
            f.write(print_String)
            f.close()

        if item == '2024MayWipe_DeathByDay_Data':
            print_String = f"""
            option = {{
            title: {{
                text: 'Deaths by Day'
            }},
            tooltip: {{
                trigger: 'axis'
            }},
            legend: {{
                data: ['Evils', 'Goods']
            }},
            dataZoom: [
                {{
                type: 'inside',
                xAxisIndex: [0, 1],
                start: 0,
                end: 100
                }},
                {{
                show: true,
                xAxisIndex: [0, 1],
                type: 'slider',
                bottom: 10,
                start: 0,
                end: 100
                }}
            ],
            xAxis: {{
                type: 'category',
                data: {DeathDates}
            }},
            yAxis: {{
                type: 'value'
            }},
            series: [
                {{
                data: {EvilCount},
                name: 'Evils',
                type: 'line',
                smooth: true
                }},
                {{
                data: {GoodCount},
                name: 'Goods',
                type: 'line',
                smooth: true
                }}
            ]
            }};"""
            f.write(print_String)
            f.close()

        if item == '2024MayWipe_DeathTotals':
            print_String = f"""
            option = {{
            title: {{
                text: 'Death Totals for Wipe'
            }},
            tooltip: {{
                trigger: 'axis'
            }},
            legend: {{
                data: ['Evils', 'Goods']
            }},
            dataZoom: [
                {{
                type: 'inside',
                xAxisIndex: [0, 1],
                start: 0,
                end: 100
                }},
                {{
                show: true,
                xAxisIndex: [0, 1],
                type: 'slider',
                bottom: 10,
                start: 0,
                end: 100
                }}
            ],
            xAxis: {{
                type: 'category',
                data: {DeathDates}
            }},
            yAxis: {{
                type: 'value'
            }},
            series: [
                {{
                data: {EvilTotalCount},
                name: 'Evils',
                type: 'line',
                smooth: true
                }},
                {{
                data: {GoodTotalCount},
                name: 'Goods',
                type: 'line',
                smooth: true
                }}
            ]
            }};"""
            f.write(print_String)
            f.close()

        if item == '2024MayWipe_TotalDamage_Data':
            print_String = f"""
    var option = {{
        dataset: [{{
            source: [\n"""
            f.write(print_String)
            header = ["Name+Log", "Total Damage", "Max Damage", "Avg Damage", "Total Pulses"]
            print_String = str(header)
            print_String+=",\n"
            f.write(print_String)
            UpperBoundDamage=0
            for i in range(100, -1, -1):
                DataList = []
                NameAndLog = LogNames[PovTotalDamageData[i][0]]+"-Log:"+str(PovTotalDamageData[i][0])
                DataList.append(NameAndLog)
                LogTotalDamage = PovTotalDamageData[i][1]
                LogMaxDamage = PovTotalDamageData[i][2]
                LogAvgDamage = PovTotalDamageData[i][4]
                LogTotalPulses = PovTotalDamageData[i][5]
                if PovTotalDamageData[i][2] > UpperBoundDamage:
                    UpperBoundDamage = PovTotalDamageData[i][2]
                print_String = f"['{NameAndLog}',{LogTotalDamage},{LogMaxDamage},{LogAvgDamage},{LogTotalPulses}],\n"
                f.write(print_String)

            print_String = f"""
		    ]
		    }}],
		    visualMap: {{
			show: true,
			dimension: 2, // means the 2nd column		
			orient: 'horizontal',
			left: 'center',
			min: 100, // lower bound
			max: {UpperBoundDamage}, // upper bound
			text: ['High Max Damage', 'Low Max Damage'],
			inRange: {{
			// Size of the bubble.
			symbolSize: [5, 50],
			color: ['#65B581', '#FFCE34', '#FD665F']
			}}
		    }},			
		    xAxis: {{
			type: 'value',
			name: "Average Damage",
			nameLocation: 'end',
			nameGap: 15
		    }},
		    yAxis: {{
			type: 'value',
			name: "Total Damage",
			nameLocation: 'center',
			nameGap: 45,
			min: 90
		    }},
		    title: {{
			text:"Total Damage / Average Damage",
			subtext: "Bubble Size based on Max Pulse Damage\\nTop 100 based on Total Damage",
			textAlign: "left",
			padding: [0, 0, 15, 10],
			top: 5
			
		    }},
		    grid: {{ 
			top: '15%'
		    }},
		    tooltip: {{trigger: 'item',
			    axisPointer: {{
			    type: 'shadow'
			    }},    
		    }},
		    series: [
			{{
			type: 'scatter',
			encode: {{
			    // Map "amount" column to x-axis.
			    x: 'Avg Damage',
			    // Map "product" row to y-axis.
			    y: 'Total Damage',
			    // format tooltip
			    tooltip: [0, 1, 2, 3, 4],
			}},	
			}}
		    ]
		    }};"""
            f.write(print_String)
            f.close()

        if item == '2024MayWipe_EvilDeathsByName_Data':
            sorted_dict = sorted(NamedDeaths['Evils'].items(), key=lambda x: x[1], reverse = True)
            VisualMapMax = 0
            print_String = f"""
option = {{
    dataset: {{
    source: [
    ['Name', 'Deaths'],
"""
            f.write(print_String)

            for i in range(25):
                print_String = f"    ['{list(sorted_dict[i])[0]}', {list(sorted_dict[i])[1]}],\n"
                f.write(print_String)
                if sorted_dict[i][1] > VisualMapMax:
                    VisualMapMax = sorted_dict[i][1]

            print_String = f"""
    ]
  }},
  grid: {{ containLabel: true }},
  title: {{
    text: 'Player Deaths - Evils',
    subtext: '          Top 25 Player Deaths - Evils'
  }},
  xAxis: {{ name: 'Deaths' }},
  yAxis: {{
    type: 'category',
    inverse: true
    }},
  visualMap: {{
    orient: 'horizontal',
    left: 'center',
    min: 1,
    max: {VisualMapMax},
    //inverse: true,
    text: ['High Score', 'Low Score'],
    // Map the score column to color
    dimension: 1,
    inRange: {{
      color: ['#65B581', '#FFCE34', '#FD665F']
    }}
  }},
  series: [
    {{
      type: 'bar',
      encode: {{
        // Map the "amount" column to X axis.
        x: 'Deaths',
        // Map the "product" column to Y axis
        y: 'Name'
      }}
    }}
  ]
}};"""
            f.write(print_String)
            f.close()

        if item == '2024MayWipe_GoodDeathsByName_Data':
            sorted_dict = sorted(NamedDeaths['Goods'].items(), key=lambda x: x[1], reverse = True)
            VisualMapMax = 0
            print_String = f"""
option = {{
    dataset: {{
    source: [
    ['Name', 'Deaths'],
"""
            f.write(print_String)

            for i in range(25):
                print_String = f"    ['{list(sorted_dict[i])[0]}', {list(sorted_dict[i])[1]}],\n"
                f.write(print_String)
                if sorted_dict[i][1] > VisualMapMax:
                    VisualMapMax = sorted_dict[i][1]

            print_String = f"""
    ]
  }},
  grid: {{ containLabel: true }},
  title: {{
    text: 'Player Deaths - Goods',
    subtext: '          Top 25 Player Deaths - Goods'
  }},
  xAxis: {{ name: 'Deaths' }},
  yAxis: {{
    type: 'category',
    inverse: true
    }},
  visualMap: {{
    orient: 'horizontal',
    left: 'center',
    min: 1,
    max: {VisualMapMax},
    //inverse: true,
    text: ['High Score', 'Low Score'],
    // Map the score column to color
    dimension: 1,
    inRange: {{
      color: ['#65B581', '#FFCE34', '#FD665F']
    }}
  }},
  series: [
    {{
      type: 'bar',
      encode: {{
        // Map the "amount" column to X axis.
        x: 'Deaths',
        // Map the "product" column to Y axis
        y: 'Name'
      }}
    }}
  ]
}};"""
            f.write(print_String)
            f.close()