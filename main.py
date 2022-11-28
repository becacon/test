import pygame , sys
import numpy as np
from pygame.locals import*
pygame.init()
WINDOW_SIZE = [600, 600]
displaysurf = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("CARO")
BG_COLOR= (28, 170, 156)
displaysurf.fill(BG_COLOR)
# cac bien trong tro choi
FPS = 120
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
# cai dat kich thuoc cua display
width = 600
heigh= 600
#cai dat so o trong tro coi
margin = 2
pygame.font.init()
game_font = pygame.font.SysFont('04B_19.ttf', 30)
circle_radius = 10
circle_wight=2
tmp = []
rownum = 15
colnum = 15
maxDepth = 6
maxMove = 4
node = []
Board = np.zeros((rownum , colnum)) # mang luu tru trang thai
Eboard = np.zeros((rownum,colnum)) # mang danh gia trang thai
Ascore = [0, 4, 27, 156, 1458] # mang tan cong
Dscore = [0, 2, 9, 99, 769]   # mang phong ngu
gopoint = []

def chu_choi_game():
    choi_game=game_font.render(f' Play Game ' , True , red , blue)
    displaysurf.blit(choi_game,(290,298))
    huong_dan=game_font.render(f'Huong Dan',True, red, blue)
    displaysurf.blit(huong_dan,(140 , 200))
def draw_line():
    #ve hang ngang
    for col in range (40,600,40):
        pygame.draw.line( displaysurf, black , (0 , col) , (600,col) , 1)
    # ve hang doc
    for row in range(40,600,40):
        pygame.draw.line(displaysurf,black,(row,0),(row,600),1)
def draw_fingure(row,col, player):
            if(player==2):
                pygame.draw.circle(displaysurf,red,(col*40+20,row*40+20),circle_radius,circle_wight )
            if(player==1):
                pygame.draw.line(displaysurf,red,(col*40,row*40),(col*40+40,row*40+40),circle_wight)
                pygame.draw.line(displaysurf, red, (col * 40, row * 40+40), (col * 40 + 40 , row * 40 ), circle_wight)
def maxpos(a):
    pos = []
    p0 =0
    p1 = 0
    max = 0
    for i in range (rownum):
        for j in  range (colnum):
            if a[i][j]> max:
                p0 = i
                p1 = j
                max = a[i][j]
    if max == 0:
        return None
    pos.append([p0, p1])
    return pos

def max_value(a):
    max = 0
    for i in range (rownum):
        for j in  range (colnum):
            if a[i][j]> max:
                max = a[i][j]
    if max == 0:
        return None
    else:
        return max
def setPositon(x,y,diem):
    Eboard[x][y]=diem
def evalChessBoard(player, Eboard ):
    for i in range(rownum):
        for j in range(colnum):
            Eboard[i][j] = 0
    # Duyet theo hang
    for row in range (rownum):
        for col in range (colnum-4):
            ePC = 0
            eHuman = 0
            for i in range(5):
                if (Board[row][col+i]==1): # neu quan co do la Human
                    eHuman += 1
                if (Board[row][col+i]==2):  # quan co la PC
                    ePC += 1
            if (eHuman * ePC == 0 and  eHuman != ePC):
                for i in range(5):
                    if(Board[row][col +i ] == 0):
                        if (eHuman == 0): # ePC khac 0
                            if player ==1:
                                Eboard[row][col+i]+=Dscore[ePC] # cho diem phong ngu
                            else:
                                Eboard[row][col+i]+=Ascore[ePC] # cho diem tan cong
                        if (ePC == 0):
                            if player == 2:
                                Eboard[row][col + i] += Dscore[eHuman] # cho diem phong ngu
                            else:
                                Eboard[row][col + i] += Ascore[eHuman] # cho diem tan cong
                        if (eHuman ==4 or ePC ==4):
                            Eboard[row][col + i] *= 2

    # Duyet theo cot
    for row in range (rownum - 4):
        for col in range (colnum):
            ePC = 0
            eHuman = 0
            for i in range (5):
                if (Board[ row + i][col] == 1):
                    eHuman +=1
                if (Board [row + i][col] == 2):
                    ePC += 1
            if (eHuman * ePC == 0 and eHuman != ePC):
                for i in range (5):
                    if(Board[row + i][col] == 0):
                        if eHuman == 0:
                            if player == 1:
                                Eboard[row + i][col] += Dscore[ePC]
                            else:
                                Eboard[row + i][col] += Ascore[ePC]
                        if ePC == 0:
                            if player == 2:
                                Eboard[row + i][col] += Dscore[eHuman]
                            else:
                                Eboard[row + i][col] += Ascore[eHuman]
                        if (eHuman ==4 or ePC ==4):
                            Eboard[row][col+1] *=2

    # duyet duong cheo xuong
    for row in range (rownum-4):
        for col in range (colnum-4):
            ePC = 0
            eHuman = 0
            for i in range (5):
                if (Board[row +i ][col + i] == 1):
                    eHuman +=1
                if (Board[row + i][col + i] == 2):
                    ePC += 1
            if (eHuman * ePC == 0 and eHuman != ePC):
                for i in range (5):
                    if (Board[row + i][col + i] == 0):
                        if eHuman == 0:
                            if player == 1:
                                Eboard[row + i][col + i] += Dscore[ePC]
                            else:
                                Eboard[row + i][col + i] += Ascore[ePC]
                        if ePC == 0:
                            if player == 2:
                                Eboard[row + i][col + i] += Dscore[eHuman]
                            else:
                                Eboard[row + i][col + i] += Ascore[eHuman]
                        if (eHuman ==4 or ePC ==4):
                            Eboard[row][col+1] *= 2

    # Duyet duong cheo len
    for row in range (4,rownum,1):
        for col in range(colnum - 4):
            ePC = 0
            eHuman = 0
            for i in range(5):
                if (Board[row - i][col + i] == 1):
                    eHuman += 1
                if (Board[row - i][col + i] == 2):
                    ePC += 1
            if (eHuman * ePC == 0 and eHuman != ePC):
                for i in range(5):
                    if (Board[row - i][col + i] == 0):
                        if eHuman == 0:
                            if player == 1:
                                Eboard[row - i][col + i] += Dscore[ePC]
                            else:
                                Eboard[row - i][col + i] += Ascore[ePC]
                        if ePC == 0:
                            if player == 2:
                                Eboard[row - i][col + i] += Dscore[eHuman]
                            else:
                                Eboard[row - i][col + i] += Ascore[eHuman]
                        if (eHuman == 4 or ePC == 4):
                            Eboard[row][col + 1] *= 2
    print("eBOARD ne", Eboard)
def check_end(state, row, col):
    c = 0
    r = 0
    #check hang ngang
    while c < colnum - 4:
        human = True
        PC = True
        for i in range (5):
            if (state[row][c+i] != 1):
                human = False
            if (state[row][c + i] != 2):
                PC = False
        if (human):
            return 1
        if (PC):
            return 2
        c += 1


    # check hang doc
    while r < rownum - 4:
        human = True
        PC = True
        for i in range(5):
            if (state[r+i][col] != 1):
                human = False
            if (state[r + i][col] != 2):
                PC = False
        if (human):
            return 1
        if (PC):
            return 2
        r += 1

    #check duong cheo xuong
    r =row
    c = col
    while (r>0 and c>0):
        r -= 1
        c -= 1
    while ( r < rownum - 4 and c < colnum - 4 ):
        human = True
        PC = True
        for i in range (5):
            if (state[r + i][c + i] != 1):
                human = False
            if (state[r + i][c + i] != 1):
                PC = False
        if (human):
            return 1
        if (PC):
            return 2
        r += 1
        c += 1

    #check duong cheo len
    r = row
    c = col
    while ( r < rownum - 1 and c > 0):
        r += 1
        c -= 1
    while (r >= 4 and c < rownum - 4):
        human = True
        PC = True
        for i in range (5):
            if ( state[r - i][c + i] !=1):
                human = False
            if (state[r - i][c -+ i] != 2):
                PC = False
        if (human):
            return 1
        if (PC):
            return 2
        r -= 1
        c += 1
    return 0
def maxValue(Board, alpha, beta, depth):
    evalChessBoard(2, Eboard)
    value = max_value(Eboard)
    print("max ne", value)# gia tri max hien tai
    print("depth max", depth)
    if ( depth >= maxDepth):
        return value

    for i in range (maxMove):
        max_pos = maxpos(Eboard) # toa do co diem cao nhat
        print("maxpos",max_pos)
        if (max_pos == None):
            break
        node.append(max_pos) # list cac nut con
        Eboard[max_pos[0]]=0
    v = -10000000000
    for i in range (len(node)):
        print("node", node[i])
        com = node[i]
        Board[com[0][0]][com[0][1]]=2
        v = max( v, miniValue(Board, alpha, beta, depth+1))
        Board[com[0][0]][com[0][1]] = 0
        if (v >=beta or check_end(Board,com[0][0],com[0][1]) == 2 ):
            global gopoint
            gopoint = com
            print("ne", gopoint)
            break
        alpha = max(alpha, v)
        print("alpha max", alpha)
    return v
def miniValue(Board, alpha, beta, depth):
    evalChessBoard(1,Eboard)
    value = max_value(Eboard)
    print("board ne", Board)
    print("min ne",value)
    print("depth min", depth)
    if (depth >= maxDepth):
        return value
    for i in range (maxMove):
        maxposs = maxpos(Eboard)
        if maxposs == None:
            break
        node.append(maxposs)
        print("minpos ne",maxposs)

    v = 1000000000
    for i in range (len(node)):
        com = node[i]
        Board[com[0][0]][com[0][1]] = 1
        v = min(v , maxValue(Board, alpha, beta, depth+1))
        Board[com[0][0]][com[0][1]] = 0
        print("alpha min", alpha)
        if(v <= alpha or check_end(Board, com[0][0], com[0][1])==1):
            break
        beta = min(beta,v)
    return v
def minimax():
    maxValue(Board, 0 , 1, 2)
    global tmp
    tmp = gopoint

    print("temp", tmp)
    if (tmp != []):
        x = tmp[0][0]
        y = tmp[0][1]
        print("xy ne", x,y)
        Board[x][y] = 2
        draw_fingure(x,y,2)
    else:
        tmp = maxpos(Eboard)
        x = tmp[0][0]
        y = tmp[0][1]
        print("xy ne", x,y)
        Board[x][y] = 2
        draw_fingure(x,y,2)


player =1 # nguoi
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            mouse_X = event.pos[1]
            mouse_Y = event.pos[0]
            click_mouse_X = int(mouse_X // 40)
            click_mouse_Y = int(mouse_Y // 40)
            print(click_mouse_X, click_mouse_Y)
            # print(Board[click_mouse_X][click_mouse_Y])
            if Board[click_mouse_X][click_mouse_Y] == 0:
                if(player==1):
                    Board[click_mouse_X][click_mouse_Y]=1
                    draw_fingure(click_mouse_X,click_mouse_Y,player)
                    # print(check_end())
                    if(check_end(Board , click_mouse_X , click_mouse_Y) == 1):
                        print("human win")
                    if(check_end(Board , click_mouse_X , click_mouse_Y) == 2):
                        print("game win")
                    if(check_end(Board , click_mouse_X ,  click_mouse_Y) == 0):
                        print("hoa")
                player=2
            if(player==2):
                minimax()
                player=1
        draw_line()
        # chu_choi_game()
        pygame.display.update()
        # status= check_win(a)
        # in_ket_qua(status)
        pygame.display.update()




























