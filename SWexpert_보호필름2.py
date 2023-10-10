def passtest():
    """
    test 통과 여부
    :return: True / False
    """
    for j in range(w):
        cnt = 1
        for i in range(d-1):
            if film[i][j] == film[i+1][j]: # 지금과 다음이 같으면 cnt +=1
                cnt+=1
            else: # 아니면 초기화
                cnt=1
            if cnt==k: # 현재 k개 되면, 다음 열 확인
                break
        if cnt<k:
            return False # break 안되었으면, 통과 못했다이야기 - 한 열이라도 통과못하면 아웃
    return True # 다 break되었으면, 통과
        
def dfs(pillcnt, start):
    """
    :param pillcnt: 투약 횟수
    :param start: 약 어디서 부터 넣으면 되는지
    :return:
    """
    global answer, film
    # 이미 필요 없는 과정은 자르기
    if pillcnt >= answer: # 1) 현재 최솟값보다 작지 않은 경우
        return
    if pillcnt ==k: # 2) 최솟값의 최댓값보다 커지는 순간 - 무조건 통과함
        if answer>pillcnt:
            answer= pillcnt
        return
    # 다 검증을 할 필요도 없는 케이스를 다 했으니, 검증하기
    if passtest(): # test통과시
        if pillcnt<answer:
            answer=pillcnt
            return
    else: # 테스트 통과 못했으면, 더 투약하기 (더 깊게 들어가기)
        for i in range(start,d): # 앞에서 해본 경우는 안해봄
            # 깊게 들어갈 때, 투약을 먼저함 - film 변화 - 어떻게 변화하는지 저장 (메모리 효율)
            # [1] 약 ver1. 0->1
            #  1-1. 0->1 로 다 바꿈
            switched  =[] # 바뀐 부분 체크
            for j in range(w):
                if film[i][j] ==0:
                    switched .append(j)
                    film[i][j] =1
            # 1-2. 그 상태 check
            dfs(pillcnt+1, i+1)
            # 1-3. 다시 상태 돌려놓기
            for j in switched :
                film[i][j] =0

            # [2] 약 ver2. 1->0
            # 2-1. 1->0 로 다 바꿈
            switched =[]
            for j in range(w):
                if film[i][j] ==1:
                    switched.append(j)
                    film[i][j] =0
            # 2-2. 그 상태 check
            dfs(pillcnt+1, i+1)
            # 2-3. 다시 상태 돌려놓기
            for j in switched:
                film[i][j] =1
    return


import sys
sys.stdin = open("./input.txt")
input = sys.stdin.readline
# main & input
t= int(input())
for tt in range(t):
    answer = int(1e9) # 큰 값 넣어둠 (최솟값 찾는 것이므로)
    d,w,k = map(int, input().split())
    film = [list(map(int, input().split())) for _ in range(d)]
    if k ==1:
        print(f'#{tt+1} {0}')
    else:
        dfs(0,0)
        print(f'#{tt+1} {answer}')


