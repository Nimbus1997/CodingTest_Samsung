# 싸움땅
import sys

sys.stdin = open("./input.txt")
input = sys.stdin.readline

# input ----------
def coverlist(x):
    x=int(x)
    if x!=0:
        return [x]
    else:
        return []


n, m, k= map(int, input().split())
gun_map = [list(map(coverlist, input().split())) for _ in range(n)]
player_list = [[] for _ in range(m)] # [[r,c, d,s,g], ...]
player_map =[[[] for _ in range(n)] for _ in range(n)]
for i in range(m):
    r,c,d,s = map(int,input().split())
    player_list[i] = [r-1,c-1,d,s,0]
    player_map[r-1][c-1].append(i)

# prepare ---------------------------
dr =[-1, 0, 1, 0] # 상 우 하 좌
dc = [0,1,0,-1]
rr, cc, dd, ss, gg = 0,1,2,3,4 # player 정보 바꾸기 편하게
point_list=[0]*m # 각자 point

# # def ----------------------------
def gun_choose(index):
    """
    바닥에 있는 총과 내가 (index)가 가진 총 비교해서 선택
    index: 사람 번호
    """
    global gun_map, player_list
    r,c,d,s,g = player_list[index]
    if len(gun_map[r][c]) ==0: # 칸에 총이 없다면, 그냥 return
        return
    if g==0: # 총을 안가지고 있으면,
        best_gun = max(gun_map[r][c])
        player_list[index][gg] = best_gun
        gun_map[r][c].remove(best_gun)
    else: #총을 가지고 있다면,
        best_gun = max(gun_map[r][c])
        if g>=best_gun: # 내 총이 더 좋음
            return
        else:
            gun_map[r][c].remove(best_gun)
            gun_map[r][c].append(g) # 총 내려 놓고
            player_list[index][gg] = best_gun # 총갖고
    return

def won(index, point):
    """"
    이긴것 처리 (1) 총 max, (2) point 업데이트
    """
    global gun_map, point_list
    # 총
    gun_choose(index)
    # point
    point_list[index] += point
    return
def loose(index):
    """
    진 것 처리 - (1) 총 내려 놓기, (2) 움직이기
    index:진 player index
    """
    global gun_map, player_list, player_map
    # (1) 총 내려놓기 (총을 가지고 있을 때만)
    r,c,d,s,g = player_list[index]
    if g!=0:
        player_list[index][gg] = 0
        gun_map[r][c].append(g)
    # (2) 이동
    for i in range(4):
        direction = (d+i)%4
        newr, newc = r+dr[direction], c+dc[direction]

        if not in_range(newr, newc) or len(player_map[newr][newc]) !=0:
            # 못가는 곳이면, 90도 회전
            continue
        else:
            # 갈 수 있으면, 이동
            player_list[index][dd] = direction # 방향 update
            player_list[index][rr], player_list[index][cc] = newr, newc
            player_map[r][c].remove(index)
            player_map[newr][newc].append(index)
            # 총 줍기
            if len(gun_map[newr][newc])!=0:
                best_gun = max(gun_map[newr][newc])
                player_list[index][gg] = best_gun
                gun_map[newr][newc].remove(best_gun)
            break
    return
def fight(r,c):
    """
    두사람 싸움
    r,c: 현재 위치
    """
    one, two = player_map[r][c]
    oner, onec, oned, ones, oneg = player_list[one]
    twor, twoc, twod, twos, twog = player_list[two]

    point = abs((ones + oneg) - (twos + twog))
    if ones+oneg >  twos+twog:
        # one이 이김
        loose(two)
        won(one,point)
    elif ones+oneg < twos+twog:
        # two가 이김
        loose(one)
        won(two, point)
    else:
        # 비김
        if ones>twos: # one이 이김
            loose(two)
            won(one, point)
        else:
            loose(one)
            won(two, point)

    return


def in_range(newr, newc):
    if 0<=newr<n and 0<=newc<n:
        return True
    else:
        return False

# main ----------------------------


for _ in range(k): # k round
    for i in range(m): # m 사람
        r,c,d,s,g = player_list[i] # 위치, direction, 스탯, 총
        newr, newc = r+dr[d], c + dc[d]
        if not in_range(newr, newc): # 범위 나가면 , 반대방향으로
            new_dir = (d+2)%4
            newr, newc = r+dr[new_dir], c+dc[new_dir]
            player_list[i][dd] = new_dir # 새로운 방향으로 update
        # 위치 업데이트 - map & list
        player_list[i][rr], player_list[i][cc] = newr, newc
        player_map[r][c].remove(i)
        player_map[newr][newc].append(i)

        # 이동한 곳에 뭐가 있는지.
        if len(player_map[newr][newc])!=1: # 사람이 있으면,
            fight(newr, newc)
        else: # 사람이 없으면 (len =1 이면 자기만 있는 것임)
            gun_choose(i)

# 정답 출력
for i, point in enumerate(point_list):
    if i<m-1:
        print(point, end=" ")
    else:
        print(point)