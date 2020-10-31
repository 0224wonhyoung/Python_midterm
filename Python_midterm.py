
from bangtal import *

scene1 = Scene("씬","Images/background.png")
setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)
setGameOption(GameOption.ROOM_TITLE, False)

STONE_BLANK = 0
STONE_BPOSSIBLE = 1
STONE_WPOSSIBLE = 2
STONE_BLACK = 3
STONE_WHITE = 4
stone_file = ["blank.png", "black possible.png", "white possible.png", "black.png", "white.png"]
turn = False     # 검은돌 차례?
both_nothing = False

dx = [0, -1, -1, -1, 0, 1, 1, 1]
dy = [1, 1, 0, -1, -1, -1, 0, 1]

class Stone(Object):
    def __init__(self, scene, file, bx, by):
        super().__init__(file)
        self.statement = STONE_BLANK
        self.locate(scene, 40+80*bx, 40+80*by)
        self.bx = bx
        self.by = by
        self.show()
        
    def change_statement(self, state):
        self.statement = state
        self.setImage("Images/"+stone_file[state])

    def onMouseAction(self, x, y, action):
        global turn
        if self.statement == STONE_WPOSSIBLE and turn:
            self.change_statement(STONE_WHITE)
            clean_possible()
            flip(self.bx, self.by)
            turn = not turn            
            check_possible()
            temp_statement()
        elif self.statement == STONE_BPOSSIBLE and (not turn):
            self.change_statement(STONE_BLACK)
            clean_possible()
            flip(self.bx, self.by)
            turn = not turn            
            check_possible()
            temp_statement()

class Number(Object):
    def __init__(self, file, x, y):
        super().__init__(file)
        self.locate(scene1, x, y)
        self.show()
    def change_num(self, num):   
        self.setImage("Images/L"+str(num)+".png")
        self.show()
        

def check_inboard(x, y):
    return 0 <= x <= 7 and 0 <= y <= 7
def check_possible():
    global turn, both_nothing
    nothing = True
    for i in range(0, 8):
        for j in range(0, 8):
            if stone[j][i].statement == (turn+3):
                for k in range(8):
                    tx = i + dx[k]
                    ty = j + dy[k]
                    exist = False                    
                    
                    while (check_inboard(tx, ty) and (stone[ty][tx].statement == ((not turn)+3))):                        
                        #print("LOOP")
                        #print("t : (%d, %d)"%(tx, ty))
                        #print( stone[ty][tx].statement )
                        #print((not turn)+3)
                        exist = True
                        tx = tx + dx[k]
                        ty = ty + dy[k]
                    if check_inboard(tx, ty) and exist == True and stone[ty][tx].statement == STONE_BLANK:
                        stone[ty][tx].change_statement(turn+1)
                        nothing = False
    """
    if nothing == True:
        print("NOTHING")
        if both_nothing == True:
            showMessage("게임종료")
        turn = not turn
        check_possible()
        both_nothing = True
    else :
        both_nothing = False
    """


def flip(x, y):
    global turn
    #print("=====")
    #print((not turn)+3)
    for i in range(8):
        tx = x + dx[i]
        ty = y + dy[i]
        msg = ""
        #print("t : (%d, %d), state : %d"%(tx, ty, stone[ty][tx].statement))
        
        while (check_inboard(tx, ty) and stone[ty][tx].statement == ((not turn)+3)):
            #print("change")
            #stone[ty][tx].change_statement(turn+3)
            tx = tx + dx[i]
            ty = ty + dy[i]        

        if check_inboard(tx, ty) and stone[ty][tx].statement == (turn+3):
            tx = x + dx[i]
            ty = y + dy[i]
            
            while (0 <= tx <= 8 and 0 <= ty <= 8 and stone[ty][tx].statement == ((not turn)+3)):
            
                stone[ty][tx].change_statement(turn+3)
                tx = tx + dx[i]
                ty = ty + dy[i]
            
            #print("t : (%d, %d), state : %d"%(tx, ty, stone[ty][tx].statement))

def clean_possible():
    for i in range(0, 8):
        for j in range(0, 8):
            if stone[i][j].statement == STONE_BPOSSIBLE or stone[i][j].statement == STONE_WPOSSIBLE:
                stone[i][j].change_statement(STONE_BLANK)

def temp_statement():
    black = 0
    white = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if stone[i][j].statement == STONE_BLACK :
                black +=1
            elif stone[i][j].statement == STONE_WHITE :
                white +=1
    if black == 0:
        number_b1.hide()
        number_b2.hide()
    elif black < 10:
        number_b1.hide()
        number_b2.change_num(black)
    else:
        number_b1.change_num(black//10)
        number_b2.change_num(black%10)

    if white == 0:
        number_w1.hide()
        number_w2.hide()
    elif white < 10:
        number_w2.hide()
        number_w1.change_num(white)
    else:
        number_w1.change_num(white//10)
        number_w2.change_num(white%10)

stone = []
stonerow = []
for i in range(0, 8):
    for j in range(0, 8):
        stonerow.append (Stone(scene1, "Images/blank.png", j, i))
    stone.append(stonerow)
    stonerow = []


stone[3][3].change_statement(STONE_BLACK)
stone[4][4].change_statement(STONE_BLACK)
stone[3][4].change_statement(STONE_WHITE)
stone[4][3].change_statement(STONE_WHITE)

number_b1 = Number("Images/L0.png", 750, 220)
number_b1.hide()
number_b2 = Number("Images/L1.png", 820, 220)
number_w1 = Number("Images/L1.png", 1080, 220)
number_w2 = Number("Images/L0.png", 1150, 220)
number_w2.hide()

print( stone[3][4].statement == ((not turn)+3) )
check_possible()

startGame(scene1)
