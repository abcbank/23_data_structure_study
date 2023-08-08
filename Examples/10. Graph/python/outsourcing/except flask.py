from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from enum import Enum
import pandas as pd
import numpy as np
import folium
from folium.plugins import MiniMap
from collections import Counter
import itertools
import math
from haversine import haversine
import ctypes as c
import os
from array import array
import json
from datetime import datetime, timedelta

# 연결되지 않은 간선 - 대충 높은 숫자로 대입
INF = 1000000	
# 최대 노드의 개수 - 적당히 조절할 것.
MAX_VERTICES = 120
# 최대 노드의 개수 * 2 => ctypes에서 사용됨.
# 왠진 모르겠으나 곱셈을 거쳐 대입하면 이상한 값이 도출됨. 따라서 새로 값을 정의해 사용
DOUBLE_MAX_VERTICES = 240


# 위키에서 데이터를 크롤링한 결과
class WikiColumn(Enum):
    Name = 0
    Location = 1
    Highway1 = 2
    Highway2 = 3
    Highway3 = 4

app = Flask(__name__)

# 이름을 통해 노드 번호를 참조하도록 딕셔너리 생성
NodeIndex = {}
# JC 리스트
JCList = []
# 고속도로 리스트
HighwayList = []
# 그래프
Graph = []

# 고속도로 크롤링 관련
# JC 데이터 저장 클래스
class JunctionChangeData:
    def __init__(self, Name:str, Location, HighWay1:str, Highway2:str, Highway3:str):
        self.Name = Name
        self.HighwayList = [HighWay1, Highway2, Highway3]
        self.Location = Location

    def toArray(self):
        return [str(self.Name) , str(self.HighwayList[0]), str(self.HighwayList[1]), str(self.HighwayList[2]), self.Location[0], self.Location[1]]

# 고속도로 데이터 저장 클래스
class HighwayData:
    def __init__(self, Name:str, JCList):
        self.Name = Name
        self.JCList = JCList
    def toArray(self):
        return [str(self.Name) , str(list(map(lambda x: x.Name, self.JCList)))]

# api - 파라미터로 받아온 이름을 카카오 맵에 검색하고, 위치 정보를 가져옴. 
def getLocation(Name:str):
    # 카카오를 통해 검색한 값의 json(데이터) 파일을 가져옴
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    # query: 검색할 검색어, page: 검색 결과 창 인덱스 
    params = {'query': Name,'page': 1} 
    # 카카오 인증 키 필요
    headers = {"Authorization": "KakaoAK 1bda4eb2f5999e2a836ab330dda7209a"}
    # 장소에 대한 데이터 요청
    places = requests.get(url, params=params, headers=headers).json()['documents']
    # 첫번째 검색어의 이름이 일치하는 경우에만 좌표 반환. 이름이 일치하지 않는 경우, 신설 JC로 판단.
    if(places[0]['place_name'] == Name):
        return (float(places[0]['y']), float(places[0]['x']))
    else:
        return (-1,-1)

# 웹크롤링 - 지정된 링크에서 웹페이지를 읽고, 이를 분석해 JC 목록을 생성
def getJuncionChangeNames():
    global Graph
    try:
        # 페이지 요청
        html = requests.get("https://ko.wikipedia.org/wiki/%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EA%B3%A0%EC%86%8D%EB%8F%84%EB%A1%9C_%EB%B6%84%EA%B8%B0%EC%A0%90_%EB%AA%A9%EB%A1%9D")
        # html 해석
        bsObj = BeautifulSoup(html.text, "html.parser")
        
        # html 페이지 분석
        jcList = bsObj.find_all("table","wikitable")
        for jcs in jcList:
            trs = jcs.find_all("tr")
            for tr in trs:
                a = tr.select("a")
                length = len(a)
                if not (length == 0):
                    Name = a[WikiColumn.Name.value].text.replace(" ", "")
                    # 위치는 모호하게 나와있으므로 kakao api를 통해 이름 검색 후 위도와 경도로 설정.
                    Location = getLocation(Name)
                    # 일부 데이터엔 이상한 값이 들어있는 것 확인. '고속'이라는 단어가 포함된 것만 고속도로 정보로 인식. 데이터가 없을 경우 none 추가
                    Highway1 = a[WikiColumn.Highway1.value].text if ((length > WikiColumn.Highway1.value) and ("고속" in a[WikiColumn.Highway1.value].text)) else None
                    Highway2 = a[WikiColumn.Highway2.value].text if ((length > WikiColumn.Highway2.value) and ("고속" in a[WikiColumn.Highway2.value].text)) else None
                    Highway3 = a[WikiColumn.Highway3.value].text if ((length > WikiColumn.Highway3.value) and ("고속" in a[WikiColumn.Highway3.value].text)) else None
                    # 신설 JC의 경우 카카오 맵에서 위치 정보를 제대로 가져올 수 없으므로 제외. 위치가 확실한 경우에만 유효한 데이터로 인식 및 추가
                    if(Location != (-1,-1)):
                        # 유효한 데이터라 판단될 경우 JCList에 해당 JC 관련 데이터 추가
                        JCList.append(JunctionChangeData(Name, Location, Highway1, Highway2, Highway3))
                        # 이름을 통해 JCList의 인덱스를 알 수 있도록 NodeIndex에 값 추가
                        NodeIndex[Name] = len(NodeIndex)
                        # 필요할 경우 각주 해제할 것. JC 목록에 추가한 것 확인용 print 구문
                        # print("Name: " + JCList[-1].Name)
                        # print("HighwayList: " + str(JCList[-1].HighwayList))
                        # print("Location: " + str(JCList[-1].Location))
        # 위키 데이터를 취합한 후 그래프 생성
        # 그래프의 노드의 개수는 위키 데이터를 통해 얻어온 JC의 개수와 동일함
        Graph = [[float(INF)]*len(JCList) for i in range(len(JCList))]
        # 그래프 상에서 목적지와 출발지가 같은 경우는 0으로 통일
        for g in range(len(Graph)):
            Graph[g][g] = 0
    except Exception as e:
        print("웹 크롤링에 실패했습니다.")
        print(e)
    

# JC 정보를 기반으로 고속도로 정보 생성 -> JC 연결 상태 등을 대략적으로 확인.
def createHighwayData():
    # JC 정보 중 고속도로의 이름을 종류별로 취합
    NameList = Counter(itertools.chain(*list(map(lambda x: x.HighwayList, JCList))))
    
    # 이름을 통해 고속도로에 관련 데이터 취합
    for HighwayName in NameList:
        # 고속도로 이름이 None 값이 아닌 경우 -> 유효한 고속도로 이름이므로 고속도로 데이터 리스트에 추가
        if HighwayName != None:
            # 이름과 해당 이름이 포함된 HighwayList를 가지고 있는 JC를 변수로 던져줌
            HighwayList.append(HighwayData(HighwayName, list(filter(lambda x: HighwayName in x.HighwayList, JCList))))
            # 확인용 print 구문. 필요할 경우 각주 해제할 것
            # print("Highway Name: " + HighwayName)
            # for jc in HighwayList[-1].JCList:
            #     print("JC Name: " + jc.Name)
            #     print("JC HighwayList: " + str(jc.HighwayList))
            #     print("JC Location: " + str(jc.Location))
        else:
            continue

    # 고속도로 데이터에 있는 JC 리스트를 JC간 거리에 따라 재배열
    # 순환 고속도로를 제외한 모든 고속도로는 직선형이라 가정
    for Highway in HighwayList:
        # 직선형이라 가정했을 경우, 양 끝 노드는 시작과 끝 노드가 됨.
        # 이를 활용해 시작과 끝 중 하나의 노드를 특정할 수 있음.
        if not ('순환' in Highway.Name):
            StartPoint = -1
            MaxDistance = -1

            for jcA in Highway.JCList:
                for jcB in Highway.JCList:
                    # 위도 경도의 차이를 이용해 두 지점 사이의 거리를 계산
                    Distance = haversine(jcA.Location, jcB.Location, unit='km')
                    if Distance > MaxDistance:
                        MaxDistance = Distance
                        StartPoint = Highway.JCList.index(jcA)

        #순환 고속도로들의 경우, 특정하기 힘드므로 하드코딩을 통해 지정
        elif Highway.Name == '수도권제1순환고속도로':
            StartPoint = Highway.JCList.index(list(filter(lambda x: x.Name == '고양JC', Highway.JCList))[0])

        elif Highway.Name == '수도권제2순환고속도로':
            StartPoint = Highway.JCList.index(list(filter(lambda x: x.Name == '마도JC', Highway.JCList))[0])

        elif Highway.Name == '대전남부순환고속도로':
            StartPoint = Highway.JCList.index(list(filter(lambda x: x.Name == '서대전JC', Highway.JCList))[0])
        
        # 고속도로의 JC 순서 재배열

        # 소팅 여부 확인
        isSorted = [False for i in range(len(Highway.JCList))]
        # 시작점은 가장 처음에 추가
        isSorted[StartPoint] = True
        sortedJC = []
        sortedJC.append(Highway.JCList[StartPoint])

        while True:
            # 모두 소팅됐다면 종료
            if len(list(filter(lambda x: not x, isSorted))) == 0:
                break
            # 소팅이 안된 것이 하나라면 추가 후 종료
            elif len(list(filter(lambda x: not x, isSorted))) == 1:
                sortedJC.append(Highway.JCList[isSorted.index(False)])
                break
            # 그 외의 경우, 거리 비교 후 마지막으로 sort한 JC와 가장 가까운 JC를 추가
            else:
                NextPoint = -1
                MinDistance = 150000
                for nextJC in Highway.JCList:
                    if not isSorted[Highway.JCList.index(nextJC)]:
                        Distance = haversine(nextJC.Location, Highway.JCList[StartPoint].Location, unit='km')
                        if Distance < MinDistance:
                            MinDistance = Distance
                            NextPoint = Highway.JCList.index(nextJC)
                isSorted[NextPoint] = True
                sortedJC.append(Highway.JCList[NextPoint])
                # 마지막으로 추가한 JC에 대해 재연산
                StartPoint = NextPoint

        # 고속도로의 리스트를 소팅된 리스트로 변경
        Highway.JCList = sortedJC
        # 확인용 print() 구문. 필요하다면 각주 해제할 것.
        # print()
        # print()
        # print("Highway Name: " + Highway.Name)
        # for jc in Highway.JCList:
        #     print("JC Name: " + jc.Name)
        #     print("JC HighwayList: " + str(jc.HighwayList))
        #     print("JC Location: " + str(jc.Location))

    # 계산된 노드(JC)와 간선(고속도로의 연결 상황)에 대하여 그래프 생성
    for Highway in HighwayList:
        for i in range(len(Highway.JCList) - 1):
            Graph[NodeIndex[Highway.JCList[i].Name]][NodeIndex[Highway.JCList[i + 1].Name]] = Graph[NodeIndex[Highway.JCList[i + 1].Name]][NodeIndex[Highway.JCList[i].Name]] = haversine(Highway.JCList[i].Location, Highway.JCList[i + 1].Location, unit='km')


# C dll 사용 관련
# c dll 로드
mydll = c.windll.LoadLibrary(os.path.join(os.getcwd(), "dijkstra.dll")) 

# 사용할 함수의 매개변수 형태 지정
def initDll():
    mydll.dijkstra.argtypes = (c.POINTER(c.c_float), c.c_int, c.c_int, c.c_int)

def list2dToList(toChange):
    return [item for sublist in toChange for item in sublist]

# 다익스트라 알고리즘 수행
# 리턴 - distance([0:Max_Vertex]): StartPoint로부터 최소 이동거리
#        path([Max_Vertex:]): StartPoint로부터 DestPoint까지 이동 경로
def runDijkstra(graph:list[list], startIdx, destIndex):
    # 매개변수로 전달할 그래프 길이
    listLength = len(graph)
    totalLength = len(graph) * len(graph[0])
    # mydll.dijkstra.restype = c.POINTER(c.c_float * listLength)
    # 사용할 함수의 출력 형태 지정
    mydll.dijkstra.restype = c.POINTER(c.c_float * DOUBLE_MAX_VERTICES)
    # 2차원 그래프를 1차원 그래프 형태로 변환
    flatlist = list2dToList(graph)
    # 각 항에 대해 flaot으로 확실하게 변환
    flatlist = [float(i) for i in flatlist]
    # 1차원 그래프의 내부 데이터를 기반으로 매개변수로 건내줄 데이터 생성
    cArray = c.cast((c.c_float * totalLength)(*flatlist), c.POINTER(c.c_float))
    # 실행 후 데이터 가져옴
    result = mydll.dijkstra(cArray, c.c_int(listLength), c.c_int(startIdx), c.c_int(destIndex))
    # python에 적합한 형식으로 데이터 변환
    result = [x for x in result.contents]
    # 거리 관련 데이터 추출
    distance = result[0:listLength]
    # 경로 관련 데이터 추출
    path =  list(map(lambda x: JCList[x].Name, reversed([value for value in [int(i) for i in result[MAX_VERTICES:MAX_VERTICES + listLength]] if value != -1])))
    return (distance, path)

# 플라스크 관련 함수

@app.route('/')
def home():
    # 홈일 경우, 현재 보유한 JC 목록과 Highway 목록을 html에 전송.
    JCArray = list(map(lambda x: x.toArray(), JCList))
    HighwayArray = list(map(lambda x: x.toArray(), HighwayList))
    return render_template("index.html",
        JCList = JCArray,
        HighwayList = HighwayArray,
        PathList = [])

@app.route('/navigate', methods=['GET'])
def navigate():
    # navigate일 경우, 파라미터를 확인
    source = request.args.get('validationDefaultSource')
    dest = request.args.get('validationDefaultDestination')
    # 적합하지 않은 파라미터일 경우 home 출력
    if ((len(list(filter(lambda x: x.Name == source, JCList))) == 0) or (len(list(filter(lambda x: x.Name == dest, JCList))) == 0)):
        return home()
    # 필요한 데이터 연산
    middlePointA = (JCList[NodeIndex[source]].Location[0] + JCList[NodeIndex[dest]].Location[0])/2
    middlePointB = (JCList[NodeIndex[source]].Location[1] + JCList[NodeIndex[dest]].Location[1])/2
    distance,path = runDijkstra(Graph, NodeIndex[source], NodeIndex[dest])
    distanceToDest = distance[NodeIndex[dest]]
    delta = timedelta(hours=(distanceToDest / 80))
    if(delta.seconds >= 3600):
        deltaString = str(delta.seconds//3600) + "시간 " + str((delta.seconds//60)%60) + "분"
    else:
        deltaString = str((delta.seconds//60)%60) + "분"
    JCArray = list(map(lambda x: x.toArray(), JCList))
    HighwayArray = list(map(lambda x: x.toArray(), HighwayList))
    PathArray = [source, dest, format(distanceToDest, ".2f") , deltaString, (datetime.now() + delta).strftime("%H시 %M분"), middlePointA, middlePointB, str(path)]

    return render_template("index.html",
        JCList = JCArray,
        HighwayList = HighwayArray,
        PathList = PathArray)

if __name__ == '__main__':
    initDll()
    getJuncionChangeNames()
    createHighwayData()    
    
    while True:
        print("-------------------")
        print("1. Show Nodes")
        print("2. Show Graph")
        print("3. Show Highways")
        print("4. Dijkstra")
        print("5. Exit")
        print("-------------------")
        print("Select Menu: ", end="")
        menu = -1
        try:
            menu = int(input())
        except:
            menu = -1
        if(menu == 1):
            for i in range(len(JCList)):
                print("Index: " + str(i))
                print("Name: " + JCList[i].Name)
                print("Connected Highways: " + str(JCList[i].HighwayList))
                print("Latitude: " + str(JCList[i].Location[0]))
                print("Longtitude: " + str(JCList[i].Location[1]))
                print()
                
            print("Total " + str(len(JCList)) + " Nodes")
        elif(menu == 2):
            for i in range(len(Graph)):
                for j in range(len(Graph[i])):
                    if(Graph[j][i] == INF):
                        print("INF".rjust(5) + " ", end="")
                    else:
                        print(format(Graph[j][i], ".2f").rjust(5) + " ", end="")
                print()
        elif(menu == 3):
            for i in range(len(HighwayList)):
                print("Index: " + str(i))
                print("Name: " + HighwayList[i].Name)
                print("Connected JCs: " + str(list(map(lambda x: x.Name, HighwayList[i].JCList))))
                print()
                
            print("Total " + str(len(HighwayList)) + " Highways")
        elif(menu == 4):
            stx = -1
            edx = -1
            while stx < 0 or stx > len(Graph):
                try:
                    print("Start Node(Index): ", end="")
                    stx = int(input())
                except:
                    stx = -1
            while edx < 0 or edx > len(Graph):
                try:
                    print("End Node(Index): ", end="")
                    edx = int(input())
                except:
                    edx = -1
            distance,path = runDijkstra(Graph, stx, edx)
            distanceToDest = distance[edx]
            delta = timedelta(hours=(distanceToDest / 80))
            if(delta.seconds >= 3600):
                deltaString = str(delta.seconds//3600) + "시간 " + str((delta.seconds//60)%60) + "분"
            else:
                deltaString = str((delta.seconds//60)%60) + "분"
            JCArray = list(map(lambda x: x.toArray(), JCList))
            HighwayArray = list(map(lambda x: x.toArray(), HighwayList))
            print("Require Time: " + deltaString)
            print("Dest Time: " +  (datetime.now() + delta).strftime("%H시 %M분"))
            print("Distance: " + format(distanceToDest, ".2f"))
            print("Path: ", end="")
            for i in range(len(path) -1):
                print(str(NodeIndex[path[i]]).rjust(4) + " -> ", end="")
            print(str(NodeIndex[path[-1]]).rjust(4))
        elif(menu == 5):
            break
    
    # listA = [[ 0,  7,  INF, INF,   3,  10, INF ],
    #         [ 7,  0,    4,  10,   2,   6, INF ],
    #         [ INF,  4,    0,   2, INF, INF, INF ],
    #         [ INF, 10,    2,   0,  11,   9,   4 ],
    #         [ 3,  2,  INF,  11,   0, INF,   5 ],
    #         [ 10,  6,  INF,   9, INF,   0, INF ],
    #         [ INF, INF, INF,   4,   5, INF,   0 ]]
    # distance,path = runDijkstra(listA, 0)
    # print("거리: " + str(distance))
    # print("경로: " + str(path))
    # for i in range(len(path)):
    #     print("Location " + str(i) + " 가중치: " + str(distance[i]) + "\t/ 이동 경로: " + str(getPath(path, 0, i)))