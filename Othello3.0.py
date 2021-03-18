import numpy as np
import time


def inBoard(pos):
    if 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7:
        return 1
    return 0


def findRoad(pos, moveDir, nowChessBoard, nowColor, enemyColor):
    nextPos = pos + moveDir
    canPut = 0
    while 1:
        if inBoard(nextPos):
            meet = nowChessBoard[nextPos[0]][nextPos[1]]
            if meet == enemyColor:
                nextPos = nextPos + moveDir
                canPut = 1
            elif meet == nowColor:
                if canPut == 1:
                    canPut = 2
                break
            else:
                break
        else:
            break
    canPut = canPut >> 1
    return canPut


def stable(nowChessBoard, pos, moveDir, nowColor, recordChessBoard):
    corPos = pos
    maxPos = np.array([7, 7, 7])
    cntTotal = 0
    while 1:
        # corMeet = nowChessBoard[corPos[0]][corPos[1]]
        minPos = np.min(maxPos)
        # print(minPos,maxPos)
        if nowChessBoard[corPos[0]][corPos[1]] == nowColor and minPos >= 0:
            recordChessBoard[corPos[0]][corPos[1]] = nowColor
            if cntTotal >= 7:
                break
        else:
            break
        for i in range(1, 3):
            nextPos = corPos
            cnt = 0
            while 1:
                nextPos = nextPos + moveDir[i]
                # meet = nowChessBoard[nextPos[0]][nextPos[1]]
                # print(nextPos, cnt, maxPos[i])
                if cnt < maxPos[i] and nowChessBoard[nextPos[0]][nextPos[1]] == nowColor:
                    recordChessBoard[nextPos[0]][nextPos[1]] = nowColor
                else:
                    # print(nextPos, cnt, maxPos[i])
                    maxPos[i] = min(cnt, maxPos[i]) - 1
                    break
                cnt += 1
        tmp = max(maxPos[1], maxPos[2])
        if maxPos[1] == tmp:
            maxPos[1] -= 1
        if maxPos[2] == tmp:
            maxPos[2] -= 1
        corPos = corPos + moveDir[0]
        cntTotal += 1


class AI(object):
    # init
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.candidate_list = []
        self.enemyColor = 0 - self.color
        self.selectPos = ()
        self.win = ()
        self.seedList = []
        # global
        self.move = np.array([[-1, -1], [-1, 0], [-1, 1], [0, -1],
                              [0, 1], [1, -1], [1, 0], [1, 1]])
        self.rightDown = np.array([[1, 1], [0, 1], [1, 0]])
        self.leftDown = np.array([[1, -1], [1, 0], [0, -1]])
        self.rightUp = np.array([[-1, 1], [-1, 0], [0, 1]])
        self.leftUp = np.array([[-1, -1], [0, -1], [-1, 0]])
        self.moveTo = np.array([[[1, 1], [0, 1], [1, 0]],
                                [[1, -1], [1, 0], [0, -1]],
                                [[-1, 1], [-1, 0], [0, 1]],
                                [[-1, -1], [0, -1], [-1, 0]]])
        self.corner = np.array([[0, 0], [0, 7], [7, 0], [7, 7]])
        self.nextCorner = np.array([[[1, 1], [0, 1], [1, 0]],
                                    [[1, 6], [1, 7], [0, 6]],
                                    [[6, 1], [6, 0], [7, 1]],
                                    [[6, 6], [6, 7], [7, 6]]])
        self.corner2 = [[0, 0], [0, 7], [7, 0], [7, 7]]
        self.nextCorner2 = [(1, 1), (0, 1), (1, 0),
                            (1, 6), (1, 7), (0, 6),
                            (6, 1), (6, 0), (7, 1),
                            (6, 6), (6, 7), (7, 6)]
        self.board = np.array([[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7],
                               [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7],
                               [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7],
                               [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7],
                               [4, 0], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6], [4, 7],
                               [5, 0], [5, 1], [5, 2], [5, 3], [5, 4], [5, 5], [5, 6], [5, 7],
                               [6, 0], [6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [6, 6], [6, 7],
                               [7, 0], [7, 1], [7, 2], [7, 3], [7, 4], [7, 5], [7, 6], [7, 7]])
        self.time = 0.035
        # num
        self.preNextSide = -1500
        self.nextSide = -3000
        self.cor = -10000
        self.nextCor = 400
        self.spCor = 0

    def canDown(self, pos, nowColor, enemyColor, nowChessBoard):
        canPut = 0
        for i in range(0, 8):
            moveDir = self.move[i]
            canPut = findRoad(pos, moveDir, nowChessBoard, nowColor, enemyColor)
            if canPut:
                break
        return canPut

    def change(self, pos, nowColor, enemyColor, nowChessBoard):
        newChessBoard = nowChessBoard * 1
        for moveDir in self.move:
            if findRoad(pos, moveDir, nowChessBoard, nowColor, enemyColor):
                newChessBoard[pos[0]][pos[1]] = nowColor
                nextPos = pos + moveDir
                while 1:
                    meet = newChessBoard[nextPos[0]][nextPos[1]]
                    if meet == enemyColor:
                        newChessBoard[nextPos[0]][nextPos[1]] = nowColor
                        nextPos = nextPos + moveDir
                    else:
                        break
        return newChessBoard

    def getCandidate(self, nowChessBoard, nowColor, enemyColor):
        candidate = []
        leftSeats = np.where(nowChessBoard == 0)
        lenSeats = len(leftSeats[0])
        for i in range(0, lenSeats):
            x = leftSeats[0][i]
            y = leftSeats[1][i]
            pos = np.array([x, y])
            if self.canDown(pos, nowColor, enemyColor, nowChessBoard):
                candidate.append((x, y))
        return candidate

    def calNumber(self, nowChessBoard):
        myCount = np.sum(nowChessBoard == self.color)
        enemyCount = np.sum(nowChessBoard == self.enemyColor)
        return [myCount, enemyCount]

    def stableTotal(self, nowChessBoard, myColor, enemyColor, haveSeatsCount):
        recordChessBoard = np.zeros((8, 8), dtype=int)
        corCount = 0
        for i in range(0, 4):
            meet = nowChessBoard[self.corner[i][0]][self.corner[i][1]]
            if meet == myColor:
                corCount += 1
            elif meet == enemyColor:
                corCount -= 1
            stable(nowChessBoard, self.corner[i], self.moveTo[i], myColor, recordChessBoard)
            stable(nowChessBoard, self.corner[i], self.moveTo[i], enemyColor, recordChessBoard)
        count = self.calNumber(recordChessBoard)
        ans = count[0] - count[1] + corCount
        #
        # a = board[0:8, 0:1]
        # a = board[0:1, 0:8]
        # a = board[0:8, 7:8]
        # a = board[7:8, 0:8]
        one = [0, 0, 0, 7]
        two = [8, 1, 8, 8]
        three = [0, 0, 7, 0]
        four = [1, 8, 8, 8]
        for k in range(0, 4):
            tmpBoard = nowChessBoard[one[k]:two[k], three[k]:four[k]]
            zeroCount = np.sum(tmpBoard == 0)
            if zeroCount == 0:
                tmpRecordBoard = recordChessBoard[one[k]:two[k], three[k]:four[k]]
                if len(tmpBoard) == 1:
                    tmpBoard = tmpBoard[0]
                    tmpRecordBoard = tmpRecordBoard[0]
                for i in range(0, 8):
                    meet = tmpBoard[i]
                    reMeet = tmpRecordBoard[i]
                    if reMeet == 0:
                        if meet == self.color:
                            ans += 1
                        else:
                            ans -= 1
        # print('-----------------------------------')
        # print(count[0], count[1], myColor)
        # print(nowChessBoard)
        # print(recordChessBoard)
        return ans

    def chessBoard(self, nowChessBoard, nowColor, enemyColor, haveSeatsCount, check=0):
        ans = 0
        for i in range(0, 4):
            meet = nowChessBoard[self.corner[i][0]][self.corner[i][1]]
            if meet == 0:
                pos = self.corner[i] + self.moveTo[i][0]
                meet = nowChessBoard[pos[0]][pos[1]]
                if meet == nowColor:
                    ans += self.cor
                elif meet == 0:
                    for dir in range(0, 3):
                        tmpPos = pos + self.moveTo[i][dir]
                        if haveSeatsCount >= 40 and nowChessBoard[tmpPos[0]][tmpPos[1]] == nowColor:
                            ans += self.nextCor
                for dir in range(1, 3):
                    pos = self.corner[i] + self.moveTo[i][dir]
                    count = 1
                    if nowChessBoard[pos[0]][pos[1]] == nowColor:
                        ans += self.preNextSide
                        k = 2
                        while 1:
                            pos = self.corner[i] + self.moveTo[i][dir] * k
                            k += 1
                            meet = nowChessBoard[pos[0]][pos[1]]

                            if meet == enemyColor:
                                count = 0
                            elif meet == 0:
                                tmpPos = pos + self.moveTo[i][3 - dir]
                                if k == 7 and nowChessBoard[tmpPos[0]][tmpPos[1]] != nowColor and count == 1:
                                    count = -2
                                    break
                                count = 0
                            elif meet == nowColor and count == 0:
                                count = -1
                                break

                            if k >= 8:
                                break
                        if count == -1:
                            ans += self.nextSide
                        elif count == -2:
                            ans += self.spCor
            for j in range(1, 7):
                pos = self.corner[i] + self.moveTo[i][1] * j
                meet = nowChessBoard[pos[0]][pos[1]]
                if meet == nowColor:
                    ans += 80
                    # if haveSeatsCount > 30:
                    #     ans += 300
        return ans

    def sideCount(self, nowChessBoard):
        mySideCount = 0
        enemySideCount = 0
        for pos in self.board:
            nowMeet = nowChessBoard[pos[0]][pos[1]]
            if nowMeet == 0:
                continue
            for dir in self.move:
                tmpPos = pos + dir
                if inBoard(tmpPos) and nowChessBoard[tmpPos[0]][tmpPos[1]] == 0:
                    if nowMeet == self.color:
                        mySideCount += 1
                    else:
                        enemySideCount += 1
                    break
        return [mySideCount, enemySideCount]

    # 确定子，动态权重，行动力
    #  eva
    def evaluate(self, nowChessBoard, nowColor, myColor, enemyColor, haveSeatsCount):
        stableScore = self.stableTotal(nowChessBoard, myColor, enemyColor, haveSeatsCount)
        chessBoardScore = self.chessBoard(nowChessBoard, myColor, enemyColor, haveSeatsCount) - self.chessBoard(
            nowChessBoard, enemyColor, myColor, haveSeatsCount)
        movePowerScore = 100 * (len(self.getCandidate(nowChessBoard, myColor, enemyColor)) - len(
            self.getCandidate(nowChessBoard, enemyColor, myColor)))
        # countScore = 100 * (self.totalOriCount[0] - self.calNumber(nowChessBoard)[0]) if self.calNumber(nowChessBoard)[
        #                                                                                      0] != 0 else -33333333
        count = self.calNumber(nowChessBoard)
        countScore = 100 * (count[1] - count[0]) if count[0] != 0 else -33333333
        side = self.sideCount(nowChessBoard)
        sideScore = 100 * (side[1] - side[0])
        # 1 4 4 1
        # 1 7 2 1
        # 1 7 1 1
        # 1 2 0 2
        if haveSeatsCount <= 22:
            ans = 10000 * stableScore + 1 * chessBoardScore + 4 * movePowerScore + 4 * countScore + 1 * sideScore
        elif haveSeatsCount <= 32:
            ans = 10000 * stableScore + 1 * chessBoardScore + 4 * movePowerScore + 2 * countScore + 1 * sideScore
            if chessBoardScore > 0 and movePowerScore > 0 and countScore > 0 and sideScore > 0:
                ans += 500
        elif haveSeatsCount <= 38:
            ans = 10000 * stableScore + 1 * chessBoardScore + 4 * movePowerScore + 1 * countScore + 1 * sideScore
            if chessBoardScore > 0 and movePowerScore > 0 and sideScore > 0:
                ans += 500
        elif haveSeatsCount <= 43:
            ans = 10000 * stableScore + 1 * chessBoardScore + 4 * movePowerScore + 0 * countScore + 2 * sideScore
        elif haveSeatsCount <= 50:
            ans = 10000 * stableScore + 1 * chessBoardScore + 4 * movePowerScore + 0 * countScore + 1 * sideScore
        else:
            ans = 10000 * stableScore + 1 * chessBoardScore + 4 * movePowerScore
        # if ans == 3980:
        #     # print(nowChessBoard,self.color)
        #     print(30000 * stableScore, 1 * chessBoardScore, movePowerScore, countScore, sideScore)
        #     print(self.chessBoard(nowChessBoard, myColor, enemyColor, haveSeatsCount), self.chessBoard(nowChessBoard,
        #                                                                                                enemyColor,
        #                                                                                                myColor,
        #                                                                                                haveSeatsCount))
        return ans

    def go(self, chessboard):
        self.start = time.time()
        self.selectPos = ()
        self.win = ()
        self.seedList = []
        self.candidate_list.clear()
        self.candidate_list = self.getCandidate(chessboard, self.color, self.enemyColor)
        self.totalOriCount = self.calNumber(chessboard)
        # print(len(self.candidate_list), len(self.getCandidate(chessboard, self.enemyColor, self.color)))
        if len(self.candidate_list) == 0:
            return
        # sort
        count = self.calNumber(chessboard)
        haveCount = count[0] + count[1] - 4
        oriDepth = 1
        if 48 <= haveCount <= 50:
            oriDepth = 6
        elif haveCount > 50:
            oriDepth = 60 - haveCount + 1
        cnt = 0
        while time.time() - self.start < self.time_out - self.time:
            cnt += 1
            print(oriDepth, self.candidate_list)
            if cnt > 60:
                break
            self.alphaBeta(oriDepth, -99999999, 99999999, chessboard, 0, oriDepth, haveCount)
            if self.win != ():
                self.candidate_list.append(self.win)
                print("win win win win win")
                print("time: ", time.time() - self.start)
                return
            if self.selectPos != ():
                self.candidate_list.append(self.selectPos)
            oriDepth += 1
            if oriDepth > 6:
                oriDepth += 1
            if haveCount >= 48:
                oriDepth = 60 - haveCount + 1
            print("time: ", time.time() - self.start)

    def alphaBeta(self, depth, alpha, beta, nowChessBoard, who, oriDepth, haveSeatsCount):
        if time.time() - self.start > self.time_out - self.time or self.win != ():
            self.selectPos = ()
            return -99999999
        if depth == 0:
            if haveSeatsCount >= 60:
                count = self.calNumber(nowChessBoard)
                return (count[0] - count[1]) * 1000000
            ans = self.evaluate(nowChessBoard, self.color if who == 0 else self.enemyColor, self.color,
                                self.enemyColor,
                                haveSeatsCount)
            # if ans == -534158:
            #     print(nowChessBoard)
            return ans
        if who == 0:
            myMove = self.getCandidate(nowChessBoard, self.color, self.enemyColor)
            # oneadd
            # if oriDepth == depth:
            #     myMove = [(1,1)]
            if oriDepth == depth and self.seedList != []:
                for seed in self.seedList:
                    myMove.remove(seed)
                    myMove.insert(0, seed)
                self.seedList = []
            myMoveNp = np.array(myMove)
            myMovePower = len(myMove)
            if myMovePower == 0:
                enemyMove = self.getCandidate(nowChessBoard, self.enemyColor, self.color)
                enemyMovePower = len(enemyMove)
                if enemyMovePower == 0:
                    count = self.calNumber(nowChessBoard)
                    if count[1] == 0:
                        return 88888888
                    elif count[0] == 0:
                        return -88888888
                    return (count[0] - count[1]) * 1000000
                else:
                    alpha = max(alpha, self.alphaBeta(depth, alpha, beta, nowChessBoard, 1 - who,
                                                      oriDepth, haveSeatsCount))
                    return min(alpha, beta)
            else:
                for i in range(0, myMovePower):
                    newChessBoard = self.change(myMoveNp[i], self.color, self.enemyColor, nowChessBoard)
                    tmp = self.alphaBeta(depth - 1, alpha, beta, newChessBoard, 1 - who,
                                         oriDepth, haveSeatsCount + 1)
                    if depth == oriDepth:
                        if alpha < tmp:
                            if tmp % 1000000 == 0 and tmp > 0:
                                self.win = myMove[i]
                                return
                            alpha = tmp
                            self.selectPos = myMove[i]
                            self.seedList.append(self.selectPos)
                            print(alpha, self.selectPos)
                    else:
                        alpha = max(alpha, tmp)
                    if alpha >= beta:
                        return beta
                return alpha
        else:
            enemyMove = self.getCandidate(nowChessBoard, self.enemyColor, self.color)
            enemyMove = np.array(enemyMove)
            enemyMovePower = len(enemyMove)
            if enemyMovePower == 0:
                myMove = self.getCandidate(nowChessBoard, self.color, self.enemyColor)
                myMovePower = len(myMove)
                if myMovePower == 0:
                    count = self.calNumber(nowChessBoard)
                    if count[1] == 0:
                        return 88888888
                    elif count[0] == 0:
                        return -88888888
                    return (count[0] - count[1]) * 1000000
                else:
                    beta = min(beta, self.alphaBeta(depth, alpha, beta, nowChessBoard, 1 - who,
                                                    oriDepth, haveSeatsCount))
                    return max(beta, alpha)
            else:
                for pos in enemyMove:
                    newChessBoard = self.change(pos, self.enemyColor, self.color, nowChessBoard)
                    beta = min(beta, self.alphaBeta(depth - 1, alpha, beta, newChessBoard, 1 - who,
                                                    oriDepth, haveSeatsCount + 1))
                    if alpha >= beta:
                        return alpha
                return beta
