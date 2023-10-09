# 코드트리 빵
import sys
from collections import deque
import copy

sys.stdin = open("./input.txt")
input = sys.stdin.readline
def int_minus(x):
    return int(x)-1
# input [0] --------------------------------------
n, m = map(int, input().split())
basecamp_map=[list(map(int, input().split())) for _ in range(n)] # 1: basecamp 0: blank
store_index  =[tuple(map(int_minus,input().split())) for _ in range(m)] # [(r,c), (r,c)]

# def --------------------------------------
def grid_move(i):
    """[1] grid에 있는 사람 움직임"""
    global semi, grid_people_list
    nowr, nowc = grid_people_list[i]
    if nowr ==-1: # 이미 도착하거나, 출발 안했으면, 움직이지 않음
        return 
        
    # 1) 가장 가까운 path 찾기 (path는 처음 움직이는 방향만 check하면 됨)
    # bfs
    visited = [[False] * n for _ in range(n)]
    q = deque()
    visited[nowr][nowc] = True
    q.append((nowr, nowc, []))
    first_dir=5
    while q:
        r, c, path = q.popleft()
        for direction in range(4):
            newr, newc = r+dr[direction], c+dc[direction]
            # 못가는 곳이면 넘어가기
            if not(0<=newr<n) or not(0<=newc<n) or cannot_go_map[newr][newc] or visited[newr][newc]:
                continue
            # 도착 하면, 해당 path가 가장 짧은 것! -> 끝!!! 길찾기 끝내고(for break, while q =[]), 해당 path로 한칸 움직이기
            if (newr, newc) == store_index[i]:
                if len(path)>0:
                    first_dir = path[0]#무조건 도착
                else:
                    first_dir= direction
                q =[]
                break
            temppath=path[:]
            temppath.append(direction)
            visited[newr][newc] = True
            q.append((newr,newc,temppath))

    # 2) 한칸 옮기기 - 편의점 도착했는지 check
    oner, onec = nowr+dr[first_dir], nowc+dc[first_dir]

    if (oner, onec) ==store_index[i]:  # 도착하면, 1) grid_people_list에서 없애기 2) semi에 표시
        grid_people_list[i] =(-1,-1)
        semi.append((oner, onec))
    else: # 도착안하면 위치만 업데이트
        grid_people_list[i] = (oner, onec)
    return



def basecamp_move(number):
    """[3] 시간되면, basecamp로 나오기"""
    # semi update  & 만약 그 위치에 사람 없으면, 바로 못가게 하는 것 까지
    global semi, grid_people_list
    # 1) basecamp찾기
    br, bc = n, n #갈 basecamp위치 (초기화- 안되는 값으로. 큰값 중 최솟값)
    arrived = False
    q=deque()
    q.append(store_index[number]) #편의점에서 부터 출발
    visited =[[False]*n for _ in range(n)]
    visited[store_index[number][0]][store_index[number][1]]=True

    while q:
        qlen = len(q)
        for _ in range(qlen):
            r, c = q.popleft()
            for direction in range(4):
                newr,newc = r+dr[direction], c +dc[direction]
                if not(0<=newr<n) or not(0<=newc<n) or cannot_go_map[newr][newc] or visited[newr][newc]:
                    continue
                visited[newr][newc] = True
                if basecamp_map[newr][newc]==1: # basecamp에 도착하면
                    arrived=True
                    if newr<br:
                        br, bc = newr, newc
                    elif newr == br:
                        if newc<bc:
                            br, bc = newr, newc
                elif not arrived: # 도착안했고, 도착한 적 없으면, 한단계 깊게 가봄 아니면 끝
                    q.append((newr, newc))
        if arrived:
            break

    # 2) base camp deactivate 결정
    if (br, bc) in grid_people_list:  #거기에 사람 있으면, 다음에 다시 검사
        semi.append((br,bc))
    else: # 사람 없으면 바로 deactivate
        cannot_go_map[br][bc] = True
    grid_people_list[number] = (br,bc) # 해당 사람 위치 시키기
    return


def cannot_go_check():
    """[2] 도착했고, 거기에 사람 없으면 deactivate"""
    global semi, cannot_go_map
    tempsemi = semi[:]
    semi =[]
    for location in tempsemi:
        if location in grid_people_list: #거기에 사람이 있으면 다음에 다시 check
            semi.append(location)
            continue
        else:
            cannot_go_map[location[0]][location[1]] = True
    return
def end():
    total = len(grid_people_list)
    cnt=0
    for i in range(total):
        if (-1,-1) == grid_people_list[i]:
            cnt+=1
    return True if cnt==m else False
#
# main --------------------------------------
grid_people_list = [(-1,-1) for _ in range(m)] # (r, c) 만약 출발전이나 도착후면, (-1,-1)
semi = []  # (r,c) 해당위치에 사람이 다 나가면, cannot_go[r][c] True로 바꾸고, 여기선 없앰
cannot_go_map = [[False]*n for _ in range(n)] # 못움직이는 위치
dr = [-1, 0,0,1] #상좌우하
dc = [0,-1,1,0]
minute =1
while True:
    # 1) 격자내 움직임 ------------------
    for i in range(m):
        # 비어있으면, 통과됨
        grid_move(i)
    # 1-1) 움직임 이후, 못가는 곳 표시 ------------------
    if len(semi)!=0:
        cannot_go_check()

    # 2) basecame로 이동 (m분이 지나면, 이 과정 필요 없음) ------------------
    if minute<=m:
        basecamp_move(minute-1) # 현재 시간과 같은 번호인 사람이 basecamp로 움직임

    # 3) End check ------------------
    if end():
        # 다 도착하면, while 문 break
        break

    minute  +=1 # 시간 흐름

print(minute) # 도착 시간


