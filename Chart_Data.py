# fetch rows from PVP_logs table Fight_Logs and logs in good and evil groups that are in pov logs table
import sqlite3
import ast
import re
from datetime import datetime

#LogNames dictionary of log Numbers as key and POV Name as value
LogNames={}

#NameCounts dictionary of POV Names as key and total number of fights
NameCounts = {}

# Connect to the database
conn = sqlite3.connect('PVP_Logs_Dec_2024_Wipe.db')
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

playerNameRegex = re.compile(r'\] (\w+) ')
#Gather Logs with POV Name
for row in DurisData:
    goodKeys = ast.literal_eval(row[13])
    goodValues = ast.literal_eval(row[12])
    evilKeys = ast.literal_eval(row[15])
    evilValues = ast.literal_eval(row[14])
    for i, key in enumerate(goodKeys):
        LogNames[key] = goodValues[i]
        pn = playerNameRegex.search(goodValues[i]) 
        playerName = pn.group(1)
        if playerName not in NameCounts:
            NameCounts[playerName] = 1
        else:
            NameCounts[playerName] += 1

    for i, key in enumerate(evilKeys):
        LogNames[key] = evilValues[i]
        pn = playerNameRegex.search(evilValues[i]) 
        playerName = pn.group(1)
        if playerName not in NameCounts:
            NameCounts[playerName] = 1
        else:
            NameCounts[playerName] += 1

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

#Collect Class Damage per fight
PlayerClassDamage = {}

for row in PovTotalDamageData:
    longName = LogNames[row[0]]
    playerClassRegex = re.compile(r'\[\s*\d+ (.*)]') 
    pc = playerClassRegex.search(longName) 
    playerClass = pc.group(1)
    maxDamage = row[2]
    #print(playerClass, maxDamage)
    if playerClass not in PlayerClassDamage:
        PlayerClassDamage[playerClass]=[]
    PlayerClassDamage[playerClass].append(maxDamage)

PlayerClassMaxDamage={}
for spec in PlayerClassDamage:
    MaxSpecDmg = round(sum(PlayerClassDamage[spec])/len(PlayerClassDamage[spec]),2)
    PlayerClassMaxDamage[spec] = MaxSpecDmg

sorted_PlayerClassMaxDamage = sorted(PlayerClassMaxDamage.items(), key=lambda x: x[1], reverse = True)

#Collect Death Level Data for BoxPlot chart
AvgDeathLevel = {}
for row in DurisData:
    DeathDate = row[1]
    DeathSide = row[6]
    DeathLevel = int(row[7])
    if DeathDate not in AvgDeathLevel:
        AvgDeathLevel[DeathDate] = []
    AvgDeathLevel[DeathDate].append(DeathLevel)

print("Avg Death Level Data")
for item in DeathDates:
    print(item, AvgDeathLevel[item])

#write echarts .tid file with chart data
ChartList =[
    '2024DecWipe_GroupSize_Data',
    '2024DecWipe_TopDamageLogs',
    '2024DecWipe_DeathByRaceGood_Data',
    '2024DecWipe_DeathByRaceEvil_Data',
    '2024DecWipe_DeathByDay_Data',
    '2024DecWipe_DeathTotals',
    '2024DecWipe_TotalDamage_Data',
    '2024DecWipe_EvilDeathsByName_Data',
    '2024DecWipe_GoodDeathsByName_Data',
    '2024DecWipe_PlayerClassMaxDamage_Data',
    '2024DecWipe_DeathLevels_Data',
    '2024DecWipe_FightsVersusDeaths_Data'
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

        if item == '2024DecWipe_GroupSize_Data':
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

        if item == '2024DecWipe_TopDamageLogs':
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

        if item == '2024DecWipe_DeathByRaceGood_Data':
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
                axisTick: {{
                  alignWithLabel: true
                }},
                axisLabel: {{
                  rotate: 30
                }},
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

        if item == '2024DecWipe_DeathByRaceEvil_Data':
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
                axisTick: {{
                  alignWithLabel: true
                }},
                axisLabel: {{
                  rotate: 30
                }},                
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

        if item == '2024DecWipe_DeathByDay_Data':
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

        if item == '2024DecWipe_DeathTotals':
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

        if item == '2024DecWipe_TotalDamage_Data':
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

            total_range=len(LogNames)-1
            if total_range > 100:
                total_range = 100

            for i in range(total_range, -1, -1):  #change from 100 ot len(PovTotalDamageData)
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
			min: 0, // lower bound
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

        if item == '2024DecWipe_EvilDeathsByName_Data':
            sorted_dict = sorted(NamedDeaths['Evils'].items(), key=lambda x: x[1], reverse = True)
            print_String = f"""
option = {{
    dataset: {{
    source: [
    ['Name', 'Deaths', 'No Deaths'],
"""
            f.write(print_String)
            top_range=len(sorted_dict)
            if top_range > 25:
                top_range = 25

            for i in range(top_range):
                player_name = list(sorted_dict[i])[0]
                death_count = list(sorted_dict[i])[1]
                no_death_count = NameCounts[player_name] - death_count
                output_string = f"    ['{player_name}', {death_count}, {no_death_count}],\n"
                f.write(output_string)
                pName=list(sorted_dict[i])[0]
                numDeaths = list(sorted_dict[i])[1]
                nonDeaths = NameCounts[pName] - numDeaths
                print_String = f"    ['{pName}', {numDeaths}, {nonDeaths}],\n"
                f.write(print_String)
            print_String = f"""
    ]
  }},
  grid: {{ containLabel: true }},
  title: {{
    text: 'Player Deaths - Evils',
    subtext: '          Top 25 Player Deaths - Evils'
  }},
  legend: {{}},
  tooltip: {{
      trigger: 'axis',
      showContent: true
    }},
  xAxis: {{}},
  yAxis: {{
    type: 'category',
    inverse: true
    }},
  dataZoom: [{{id: 'dataZoomY', type: 'slider', yAxisIndex: [0], filterMode: 'filter', start: 0, end: 75}},{{id: 'dataZoomY2', type: 'inside', yAxisIndex: [0], filterMode: 'filter', start: 0, end: 75}}],    
  series: [{{ type: 'bar', stack: 'Logs'}}, {{ type: 'bar', stack: 'Logs' }}]
}};"""
            f.write(print_String)
            f.close()

        if item == '2024DecWipe_GoodDeathsByName_Data':
            sorted_dict = sorted(NamedDeaths['Goods'].items(), key=lambda x: x[1], reverse = True)
            print_String = f"""
option = {{
    dataset: {{
    source: [
    ['Name', 'Deaths', 'No Deaths'],
"""
            f.write(print_String)
            top_range=len(sorted_dict)
            if top_range > 25:
                top_range = 25

            for i in range(top_range):
                pName=list(sorted_dict[i])[0]
                numDeaths = list(sorted_dict[i])[1]
                nonDeaths = NameCounts[pName] - numDeaths
                print_String = f"    ['{pName}', {numDeaths}, {nonDeaths}],\n"
                f.write(print_String)
            print_String = f"""
    ]
  }},
  grid: {{ containLabel: true }},
  title: {{
    text: 'Player Deaths - Goods',
    subtext: '          Top 25 Player Deaths - Goods'
  }},
  legend: {{}},
  tooltip: {{
      trigger: 'axis',
      showContent: true
    }},
  xAxis: {{ name: 'Deaths' }},
  yAxis: {{
    type: 'category',
    inverse: true
    }},
  dataZoom: [{{id: 'dataZoomY', type: 'slider', yAxisIndex: [0], filterMode: 'filter', start: 0, end: 75}},{{id: 'dataZoomY2', type: 'inside', yAxisIndex: [0], filterMode: 'filter', start: 0, end: 75}}],
  series: [{{ type: 'bar', stack: 'Logs'}}, {{ type: 'bar', stack: 'Logs' }}]
}};"""
            f.write(print_String)
            f.close()
        
        if item == '2024DecWipe_PlayerClassMaxDamage_Data':
            SpecList=[]
            for spec in sorted_PlayerClassMaxDamage:
                SpecList.append(spec[0])
            #sorted_PlayerClassMaxDamage
            print_String = f"\nconst professions = {SpecList}"

            f.write(print_String)

            print_String = f"""

option = {{
  title: [
    {{text: 'Max Pulse Damage by Class across all fights', left: 'center'}},
    {{text: 'upper: Q3 + 1.5 * IQR \\nlower: Q1 - 1.5 * IQR', borderColor: '#999', borderWidth: 1, textStyle: {{fontSize: 12}}, left: '10%', top: '88%'}}
  ],
dataset: [
    {{
      // prettier-ignore
      source: ["""

            f.write(print_String)

            for spec in sorted_PlayerClassMaxDamage:
                print_String = f"{PlayerClassDamage[spec[0]]},\n"
                f.write(print_String)

            print_String = f"""]
    }},
    {{
      transform: {{
        type: 'boxplot',
        config: {{
          itemNameFormatter: function (params) {{
            return professions[params.value];
          }}
        }}
      }},
    }},
    {{
      fromDatasetIndex: 1,
      fromTransformResult: 1
    }}
  ],
  dataZoom: [{{id: 'dataZoomY', type: 'slider', yAxisIndex: [0], filterMode: 'filter', start: 0, end: 25}},{{id: 'dataZoomY2', type: 'inside', yAxisIndex: [0], filterMode: 'filter', start: 0, end: 25}}],
  tooltip: {{trigger: 'item', axisPointer: {{type: 'shadow'}}}},
  grid: {{left: '10%', right: '10%', bottom: '15%'}},
  yAxis: {{type: 'category', boundaryGap: true, nameGap: 30, splitArea: {{show: true}}, splitLine: {{show: true}},inverse: true}},
  xAxis: {{type: 'value', name: 'Max Pulse Damage', splitArea: {{show: true}}}},
  series: [
    {{
      name: 'boxplot',
      type: 'boxplot',
      datasetIndex: 1,
      itemStyle: {{
        color: function(seriesIndex) {{
        	console.log(datasetIndex);
          return colors[seriesIndex];
        }}
      }},
      encode:{{tooltip: [ 1, 2, 3, 4, 5]}},
      }},
    {{
      name: 'outlier',
      type: 'scatter',
      encode: {{ x: 1, y: 0 }},
      datasetIndex: 2
    }}
  ]
}};
"""

            f.write(print_String)
            f.close()

        if item == '2024DecWipe_DeathLevels_Data':
            print_String = f"\nconst deathDates = {DeathDates}"

            f.write(print_String)
            print_String = f"""
option = {{
  title: [
    {{
      text: 'Death Level by Day',
      left: 'center'
    }},
    {{
      text: 'upper: Q3 + 1.5 * IQR \\nlower: Q1 - 1.5 * IQR',
      borderColor: '#999',
      borderWidth: 1,
      textStyle: {{
        fontWeight: 'normal',
        fontSize: 9,
        lineHeight: 10
      }},
      left: '10%',
      top: '89%'
    }}
  ],
  dataset: [
    {{
      // prettier-ignore
      source: ["""
            
            f.write(print_String)

            for item in DeathDates:
                f.write(f"{AvgDeathLevel[item]},\n")
                        
            print_String = f"""
            ]
    }},
    {{
      transform: {{
        type: 'boxplot',
        config: {{
          itemNameFormatter: function (params) {{
            return deathDates[params.value];
          }}
        }}
      }}
    }},
    {{
      fromDatasetIndex: 1,
      fromTransformResult: 1
    }}
  ],
  tooltip: {{
    trigger: 'item',
    axisPointer: {{
      type: 'shadow'
    }}
  }},
  grid: {{
    left: '10%',
    right: '10%',
    bottom: '15%'
  }},
  xAxis: {{
    type: 'category',
    boundaryGap: true,
    nameGap: 30,
    splitArea: {{
      show: false
    }},
    splitLine: {{
      show: false
    }}
  }},
  yAxis: {{
    type: 'value',
    name: 'Level',
    splitArea: {{
      show: true
    }}
  }},
  dataZoom: [
  {{
    type: 'inside'
  }},
  {{
    type: 'slider',
    height: 20
  }}
],
  series: [
    {{
      name: 'Death Level',
      type: 'boxplot',
      datasetIndex: 1,
      encode:{{tooltip: [ 1, 2, 3, 4, 5]}},
    }},
    {{
      name: 'outlier',
      type: 'scatter',
      datasetIndex: 2
    }}
  ]
}};
"""

            f.write(print_String)

            f.close()

        if item == '2024DecWipe_FightsVersusDeaths_Data':
            sorted_Goods_dict = sorted(NamedDeaths['Goods'].items(), key=lambda x: x[1], reverse = True)
            sorted_Evils_dict = sorted(NamedDeaths['Evils'].items(), key=lambda x: x[1], reverse = True)
            print_String = f"""
SideColor = {{'Goods':'ForestGreen', 'Evils':'DodgerBlue'}};

option = {{
    dataset: {{
    source: [
    ['Name', 'Fights', 'Deaths', 'Side'],
"""
            f.write(print_String)

            for pName in NameCounts:
                Fight_Count = NameCounts[pName]
                if pName in NamedDeaths['Goods']:
                    Death_Count = NamedDeaths['Goods'][pName]
                    raceWareSide = 'Goods'
                elif pName in NamedDeaths['Evils']:
                    Death_Count = NamedDeaths['Evils'][pName]
                    raceWareSide = 'Evils'
                else:
                    Death_Count = 0
                print_String = f"    ['{pName}', {Fight_Count}, {Death_Count}, '{raceWareSide}'],\n"
                f.write(print_String)

            print_String = f"""
    ]
  }},
  grid: {{ 
    containLabel: true,
    grid: '5px' 
    }},
  title: {{
    text: 'Fights verus Deaths - Bubble Chart',
    subtext: '          Bubble size based on fight/death ratio'
  }},
  legend: {{}},
  tooltip: {{
      trigger: 'axis',
    axisPointer: {{
      type: 'cross'
    }}
  }},
  xAxis: {{ name: 'Fights', nameLocation: 'center', nameGap: 45 }},
  yAxis: {{
    type: 'value',
    name: 'Deaths',
    minInterval: 1,
    inverse: true,
    nameLocation: 'center',
	  nameGap: 45,
    }},
  series: [
    {{
      type: 'scatter',
      symbolSize: function (data) {{
          if (data[1] / (data[2] +1)< 5) {{
            return 10;
          }} else {{
            return (data[1] / (data[2] +1)+25);
          }}
      }},
      itemStyle: {{
        color: function(seriesIndex) {{
        	if (seriesIndex.data[3]){{
        	  return SideColor[seriesIndex.data[3]];
        	}}
        }}
      }},
      encode: {{
        // Map the "amount" column to X axis.
        x: 'Fights',
        // Map the "product" column to Y axis
        y: 'Deaths',
        tooltip: [0, 1, 2, 3]
      }}
    }}
  ]
}};"""
            f.write(print_String)
            f.close()
