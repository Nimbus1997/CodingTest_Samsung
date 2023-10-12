# 정육면체 한번 더 굴리기
import sys
from collections import deque
# 기본 -------------------
sys.stdin = open("./input.txt")
input = sys.stdin.readline
# def -----------------
def in_range(r,c):
    if 0<=r<n and 0<=c<n:
        return True
    else:
        return False
def roll_dice(d, r,c):
    """
    주사위 굴리기 - 새 좌표, 주사위 전개도 수정
    :param d: 현재 주사위 굴리는 방향
    :param r, c: 원래 좌표
    :return: 새 좌표
    """
    global dice
    # [1] 새 좌표
    newr, newc = r+dr[d], c+dc[d]
    # [2] 주사위 전개도
    temp_dice = dice[:]
    if d==0:
        # 오른쪽
        dice=[temp_dice[left], temp_dice[right], temp_dice[top], temp_dice[bot], temp_dice[down], temp_dice[up]]
    elif d==1:
        # 아래
        dice = [temp_dice[up], temp_dice[down], temp_dice[right], temp_dice[left], temp_dice[top], temp_dice[bot]]

    elif d==2:
        # 왼쪽
        dice = [temp_dice[right], temp_dice[left], temp_dice[bot], temp_dice[top], temp_dice[down], temp_dice[up]]
    else:
        # 위
        dice=[temp_dice[down], temp_dice[up], temp_dice[right], temp_dice[left], temp_dice[bot], temp_dice[top]]

    return newr, newc

def point_cal(r,c):
    """
    점수 계산
    :param r: 좌표
    :param c: 좌표
    :return: 이번에 얻은 점수
    """
    pointnum = grid[r][c]
    point = grid[r][c]
    visited =[[False]*n for _ in range(n)]
    visited[r][c] =True
    q =deque()
    q.append((r,c))
    while q:
        r, c = q.popleft()
        for i in range(4):
            newr, newc = r+dr[i], c+dc[i]
            if in_range(newr,newc) and not visited[newr][newc] and grid[newr][newc] ==pointnum:
                visited[newr][newc] = True
                point +=pointnum
                q.append((newr, newc))

    return point

def change_direction(d,r,c):
    """
    주사위 굴러갈 방향 change
    :param d: 현재 방향
    :param r: 현재 좌표
    :param c: 
    :return: 새로운 방향 (가능한 곳으로) 0~3
    """
    # [1] 주사위와 grid 비교
    dice_bottom = dice[bot]
    grid_now = grid[r][c]
    if dice_bottom> grid_now:
        #시계방향
        newdir = (d+1)%4
        newr, newc = r+dr[newdir], c+dc[newdir]
    elif dice_bottom<grid_now:
        # 반시계
        newdir = (d+3)%4
        newr, newc = r+dr[newdir], c+dc[newdir]
    else:
        #같으면, 그대로
        newdir = d
        newr, newc = r+dr[newdir], c+dc[newdir]

    # [2] 만약 not in range()
    if not in_range(newr, newc):
        newdir = (newdir+2)%4
    return newdir
# prepare ----------------
# row, column 이동
dr = [0,1,0,-1] # 우 하 좌 상 순
dc = [1,0,-1,0]
# 주사위 위치 변경 편하게 (index) - top, bottom이 윗면 아랫면, 윗면기준으로 동서남북 순으로 오왼하상
top, bot, right, left, down, up= 0,1,2,3,4,5
# 초기 방향
direction =0 # 오른쪽
# 초기 주사위
dice = [1,6,3,4,2,5]
# 주사위 초기 위치
r, c = 0,0
# 총 점수
total_point =0
# input -----------------
n, m = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]

# main --------------------
for step in range(m):
    # [1] 주사위 굴리기
    r, c = roll_dice(direction,r,c) #주사위 위치 in grid
    # [2] 점수 계산
    total_point += point_cal(r, c)
    # [3] 방향 바꾸기 (새로운 위치)
    direction = change_direction(direction,r,c)

print(total_point)