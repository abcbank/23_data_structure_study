from enum import Enum

# 절대 방향을 의미하는 Enum
# 비교를 할 일 없으므로 람다식을 통해 바로바로 원하는 값을 도출
class AbsoluteDirection(Enum):
    East =  lambda x,y: [x, y + 1] #'→'
    West =  lambda x,y: [x, y - 1] #'←'
    South = lambda x,y: [x + 1, y] #'↓'
    North = lambda x,y: [x - 1, y] #'↑'

class NodeInfo(Enum):
    Wall =  'x'
    Node =  'o'


# 상대 방향를 의미하는 Enum
class RelativeDirection(Enum):
    # 현재 방향에서 왼쪽
    First   =  0# lambda x,y: [x - 1, y]
    # 현재 방향에서 직진
    Second  =  1# lambda x,y: [x + 1, y]
    # 현재 방향에서 오른쪽
    Third   =  2# lambda x,y: [x, y + 1]

# 현재 위치를 저장하기 위한 객체
class Explorer():
    def __init__(self, X = 0, Y = 0, Dir = AbsoluteDirection.East):
        self.Axis = [X,Y]
        self.Dir = Dir

def create_map(targetMap, startPoint, startDir):
    # 탐색할 간선을 리스트(스택) 형태로 저장
    stack = []
    # 탐색된 노드를 딕셔너리 형태로 저장
    nodeList = {}
    # 탐색된 간선을 그래프 형태로 저장
    # graph = []

    # 시작 지점 설정 / 시작 좌표 및 시작 좌표에서의 방향 설정
    exp = Explorer(startPoint[0], startPoint[1], startDir)
    # 시작 지점은 반드시 노드이므로 시작점을 노드 리스트에 추가
    nodeList[0] = startPoint

    # 시작 지점에서 갈 수 있는 간선 탐색
    for toCheck in RelativeDirection:
        # 상대 좌표에 따라 이동할 좌표를 확인
        # get_abs_dir(exp.Dir, toCheck): 현재 Explorer의 방향과 원하는 상대 방향을 사용해 절대 방향을 계산
        # get_abs_dir(exp.Dir, toCheck)(exp.Axis[0], exp.Axis[1]): 계산된 절대 방향에 현재 exp.Axis의 값을 대입해 이동 후 좌표 계산
        # ex) exp.Axis = [1,1], exp.Dir = AbsoluteDirection.South 일 경우
        #     1) toCheck == First일때
        #        get_abs_dir(exp.Dir, toCheck)(exp.Axis[0], exp.Axis[1]) = AbsoluteDirection.East(exp.Axis[0], exp.Axis[1])
        #                                                                = [exp.Axis[0], exp.Axis[1] + 1]
        #                                                                = [1,2]
        #     2) toCheck == Second일때
        #        get_abs_dir(exp.Dir, toCheck)(exp.Axis[0], exp.Axis[1]) = AbsoluteDirection.South(exp.Axis[0], exp.Axis[1])
        #                                                                = [exp.Axis[0] + 1, exp.Axis[1]]
        #                                                                = [2,1]
        #     3) toCheck == Third일때
        #        get_abs_dir(exp.Dir, toCheck)(exp.Axis[0], exp.Axis[1]) = AbsoluteDirection.West(exp.Axis[0], exp.Axis[1])
        #                                                                = [exp.Axis[0], exp.Axis[1] - 1]
        #                                                                = [1,0]
        toMove = get_abs_dir(exp.Dir, toCheck)(exp.Axis[0], exp.Axis[1])
        # 간선 추가 조건
        # 1. 이미 탐색된 위치가 아님. 즉, nodeList에 해당 값이 없음
        # 2. 맵의 바깥 좌표가 아님.
        # 3. toMove의 값이 Wall이 아님
        if(
            # 1번 조건
            not(toMove in nodeList.values()) and
            # 2번 조건 
            0 <= toMove[0] <= len(targetMap) and 0 <= toMove[1] <= len(targetMap) and 
            # 3번 조건
            targetMap[toMove[0]][toMove[1]] == NodeInfo.Node.value):
            # 모든 조건이 충족될 경우 해당 간선을 스택에 추가
            stack.append([exp.Axis, get_abs_dir(exp.Dir, toCheck)])

    # 스택과 노드 리스트를 통해 현재 탐색 진행 상황 출력
    displayMap(targetMap, stack, nodeList)

    while stack:
        # 이동할 간선 pop
        curMove = stack.pop(0)
        # 실제 오므로봇으로 이동할 경우, 이동의 시작점(curMove[0])으로 이동하는 함수 추가
        # 현재는 필요 없으므로 패스

        # 이동
        # 현재는 오므로봇이 이동하는 과정이 없으므로 좌표의 대입으로 대체
        # 이동 완료 후 exp의 좌표 및  방향을 이동한 간선의 것으로 변경
        exp.Axis = curMove[1](curMove[0][0], curMove[0][1])
        exp.Dir = curMove[1]
        
        # 이동 완료 후 현재 좌표가 이전에 탐색되지 않은 위치일 경우
        if not(exp.Axis in nodeList.values()):
            # 현재 위치를 노드 리스트에 추가
            nodeList[len(nodeList)] = exp.Axis
            # 해당 노드에서 이동할 수 있는 간선을 스택에 추가
            for toCheck in RelativeDirection:
                toMove = get_abs_dir(exp.Dir, toCheck)(exp.Axis[0], exp.Axis[1])
                if(not(toMove in nodeList.values()) and 
                    0 <= toMove[0] < len(targetMap) and 0 <= toMove[1] < len(targetMap) and 
                    targetMap[toMove[0]][toMove[1]] == NodeInfo.Node.value):
                    stack.append([exp.Axis, get_abs_dir(exp.Dir, toCheck)])
        
        # 진행 상황을 출력
        displayMap(targetMap, stack, nodeList)

    displayMap(targetMap, stack, nodeList)

def displayMap(targetMap, stack, nodeList):
    # Target Map과 동일한 크기의 맵을 생성
    searchingMap = [['x' for ii in range(len(targetMap[0]))] for i in range(len(targetMap))]

    # 탐색된 위치(노드 리스트)를 각 위치가 탐색된 순서대로 표기
    for key, value in nodeList.items():
        searchingMap[value[0]][value[1]] = key
    
    # 탐색됐지만 아직 이동하지 않은 간선(stack) 'S'로 표기
    for val in stack:
        targetPosition = val[1](val[0][0], val[0][1])
        searchingMap[targetPosition[0]][targetPosition[1]] = 'S'
    
    # 스택이 비어있지 않다면, 스택의 마지막 값(다음 이동할 간선)은 N으로 표기
    if stack:
        popPosition = stack[0][1](stack[0][0][0], stack[0][0][1])
        searchingMap[popPosition[0]][popPosition[1]] = 'N'

    # 출력
    for i in range(len(searchingMap)):
        for ii in range(len(searchingMap[0])):
            print('%3s' % str(searchingMap[i][ii]) + " ", end="")
        print()
    print()



# 현재 방향과 현재 방향에 대한 상대 방향을 통해 절대 방향 계산
def get_abs_dir(cur_dir, rel_dir):
    # 두번째(직진)일 경우 현재 방향을 그대로 리턴
    if(rel_dir == RelativeDirection.Second):
        return cur_dir
    # 왼쪽 혹은 오른쪽 회전이 필요할 경우 그에 맞는 리턴 반환
    elif(rel_dir == RelativeDirection.First):
        if cur_dir == AbsoluteDirection.East:
            return AbsoluteDirection.North
        elif cur_dir == AbsoluteDirection.West:
            return AbsoluteDirection.South
        elif cur_dir == AbsoluteDirection.South:
            return AbsoluteDirection.East
        elif cur_dir == AbsoluteDirection.North:
            return AbsoluteDirection.West
    else:
        if cur_dir == AbsoluteDirection.East:
            return AbsoluteDirection.South
        elif cur_dir == AbsoluteDirection.West:
            return AbsoluteDirection.North
        elif cur_dir == AbsoluteDirection.South:
            return AbsoluteDirection.West
        elif cur_dir == AbsoluteDirection.North:
            return AbsoluteDirection.East

StartPoint = [0,3]
StartDir = AbsoluteDirection.South
Map = [
    ['x', 'x', 'x', 'o', 'x', 'x', 'x', 'x', 'x', 'x'], 
    ['x', 'o', 'o', 'o', 'x', 'o', 'x', 'x', 'x', 'o'], 
    ['x', 'o', 'o', 'o', 'x', 'o', 'o', 'o', 'o', 'o'], 
    ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'x', 'x', 'o'], 
    ['o', 'o', 'x', 'x', 'x', 'o', 'x', 'x', 'x', 'o'], 
    ['o', 'x', 'x', 'o', 'o', 'o', 'o', 'o', 'o', 'o'], 
    ['o', 'o', 'x', 'o', 'o', 'x', 'x', 'o', 'x', 'o'], 
    ['x', 'o', 'o', 'o', 'x', 'o', 'o', 'o', 'x', 'o'], 
    ['x', 'x', 'o', 'x', 'x', 'x', 'o', 'x', 'x', 'o'], 
    ['x', 'o', 'o', 'o', 'x', 'x', 'o', 'x', 'x', 'o']
]

create_map(Map, StartPoint, StartDir)