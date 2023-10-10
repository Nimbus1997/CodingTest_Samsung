def inspect(film, k):
    # 열(w)마다 돌며, 각 행(d)의 끝까지 가야하므로, w가 밖, d가 안
    for i in range(w):
        # 한 막에 있는 셀 개수만큼
        stack =1 # 연속 셀 개수
        for j in range(d-1):
            # 막 개수 -1 만큼
            if film[j][i] == film[j+1][i]:
                #지금꺼랑 다음꺼랑 같으면,
                stack +=1
            else:
                # 다르면, 다시 세기 시작
                stack =1
            if stack ==k:
                # 기준 통과하면, 이 열은 더이상 안봐도 됨
                break
        # 한 열을 다 살펴봤는데, 개수가 k가 안되면, 불가능 한 것
        if stack !=k:
            return False
    # return False 안되었다는 것은, 다 True가 되었다는 것!
    return True

def dfs(l,s,film):
    """
    :param l: 약품 사용 횟수
    :param s: 약품 치는 곳 시작 위치 (0-1,2,3,4,5 / 1-2,3,4,5 / 2-3,4,5 / .. 이런식으로 combination
    :param film: 현재 film상태
    :return:
    """
    global answer
    if l>=answer:
        return
    if inspect(film, k): # 보호 필름 테스트 통과!
        if l<answer: # 현재 정답보다 투약횟수 적으면, 업데이트
            answer = l
        return
    # 테스트 통과 X
    if l==k: # 투약횟수가 최댓값이 되면,
        if l < answer: # 최댓값이 ans보다 작으면
            answer =l # 업데이트
        return
    else: # 투약횟수 아직 초과 X -> 투약 해줌
        # depth마다, 모든 열(w)을 바꿔줘야하니까, d가 밖 & w가 안
        for i in range(s,d):
            # (1) 1->0 0으로 다 바꿈
            switched = []
            for j in range(w):
                if film[i][j] == 1:
                    film[i][j] =0
                    switched.append(j) # 어디를 바꿨는지 기록
            # (2) 그 상태로 확인
            dfs(l+1,i+1, film)
            # (3) 다시 돌려놓음
            for j in switched:
                film[i][j] = 1
            switched=[]
            # (4) 1->0 . 1로 다 바꿈
            for j in range(w):
                if film[i][j] ==0:
                    film[i][j] =1
                    switched.append(j)
            # (5) 그 상태로 확인
            dfs(l+1, i+1, film)
            # (6) 다시 돌려 놓음
            for j in switched:
                film[i][j] =0



# main 문 ------
import sys
sys.stdin = open("./input.txt")
input = sys.stdin.readline
t = int(input())
for tt in  range(1, 1+t):
    d,w,k = map(int, input().split())
    films = [list(map(int, input().split())) for _ in range(d)] # d * w 배열
    answer = 1000000
    if k ==1:
        # 합격기준이 1이면 그냥 0임
        print(f'#{tt} {0}')
    else:
        dfs(0,0, films)
        print(f'#{tt} {answer}')