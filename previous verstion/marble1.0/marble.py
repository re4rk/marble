import sys, pygame, time, threading
from random import *

pygame.init()

def diceRandom(num, a = 1):
    i = randint(1,360)
    if     0        < i <= 10 - a*1 : return 2
    elif  10- a *  1< i <= 30 - a*3 : return 3
    elif  30- a *  3< i <= 60 - a*6 : return 4
    elif  60- a *  6< i <=100 - a*10: return 5
    elif 100- a * 10< i <=150 - a*15: return 6
    elif 150- a * 15< i <=210 - a*21: return 8
    elif 210- a * 21< i <=260 - a*26: return 8
    elif 260- a * 26< i <=300 - a*30: return 9
    elif 300- a * 30< i <=330 - a*33: return 10
    elif 330- a * 33< i <=350 - a*35: return 11
    elif 350- a * 35< i <=360 - a*36: return 12
    elif 360- a * 36< i <=360       : return num

def dice(num,user):
    while num != 0:
        num-=1  
        if user.h == 0:
            if user.w == 8 :
                user.h+=1
                user.Rect.move_ip(0,80)
            else :
                user.w+=1
                user.Rect.move_ip(142,0)
        elif user.h == 8:
            if user.w == 0 :
                user.h-=1
                user.Rect.move_ip(0,-80)
            else :
                user.w-=1
                user.Rect.move_ip(-142,0)            
        else :
            if user.w == 8:
                user.h+=1
                user.Rect.move_ip(0,80)
            elif user.w == 0 :
                user.h-=1
                user.Rect.move_ip(0,-80)
        user.index+=1
        time.sleep(0.15)
    zz= user.index//32
    user.index%=32
    return zz    

class Map():
    def __init__(self,location):
        self.map = pygame.image.load(location[0])
        self.screen = pygame.display.set_mode((1280,720))
    def blit(self,a,b):
        self.screen.blit(a,b)

class Object():
    def __init__(self,location,w = 0,h = 0):
        self.Surf = pygame.image.load(location)
        self.Rect = self.Surf.get_rect()
        self.Rect.move_ip(w,h)
        self.w = w
        self.h = h
    def move_ip(self,w,h):
        self.Rect.move_ip(w,h)

class Land(Object):
    def __init__(self,information):
        self.buyer = ""
        self.landName = information[0]
        self.w = int(information[1])
        self.h = int(information[2])
        self.ground = 0
        self.groundPrice = information[3]
        self.house = 0
        self.housePrice = information[4]
        self.building = 0
        self.buildingPrice = information[5]
        self.hotel = 0
        self.hotelPrice = information[6]
        self.landmark = 0        
        self.landmarkPrice = information[7]
        self.totalPrice = 0
        self.font = pygame.font.SysFont("comicsansms",15)
        self.a = self.landName +"   "+ str(self.totalPrice)+"won"
        self.Surf = self.font.render(self.a,True,(0,0,0))
        self.Rect = self.Surf.get_rect()
        self.Rect.move_ip(self.w*142+5,self.h*80+3)
    def buyLand(self,buyer,information):
        self.buyer = buyer
        self.ground = 0

    def getLandProfile(self,display):
        a = Object("./images/temp.png",500,300)
        ab = self.landName + self.groundPrice + self.housePrice + self.buildingPrice + self.hotelPrice + self.landmarkPrice
        a.Surf = self.font.render(ab,True,(0,0,0))
        a.Rect = self.Surf.get_rect()
        a.Rect.move_ip(500,300)
        return a


class Object():
    def __init__(self,location,w = 0,h = 0):
        self.Surf = pygame.image.load(location)
        self.Rect = self.Surf.get_rect()
        self.Rect.move_ip(w,h)
        self.w = w
        self.h = h
    def move_ip(self,w,h):
        self.Rect.move_ip(w,h)

def setLand(fileName,display):
    landList = []
    file = open(fileName,'r')
    dics = {}
    while True:
        line = file.readline()
        if not line: break
        line = line.replace('\n','').split('\t')
        print(line)
        landList.append(Land(line))

    return landList

class User(Object):
    population  = 0 
    Table   = 0
    def __init__(self,location,w = 0,h = 0):
        self.Surf = pygame.image.load(location)
        self.Rect = self.Surf.get_rect()
        self.Rect.move_ip(w,h)
        self.w = w
        self.h = h
        self.index = 0
        User.population  += 1
        self.lands = []

class Profile(Object):
    def __init__(self,location,w = 0,h = 0):
        self.Surf = pygame.image.load(location)
        self.Rect = self.Surf.get_rect()
        self.Rect.move_ip(w,h)
        self.w = w
        self.h = h
        self.font = pygame.font.SysFont("comicsansms",30)
        self.money = 2000000
        self.text = self.font.render(str(self.money),True,(0,128,0))
        self.textRect = self.text.get_rect()
        self.textRect.move_ip(w+20,h)
    def info(self):
        display.blit(self.text,self.textRect)
    def addMoney(self,cost):
        self.money += cost
        self.text = self.font.render(str(self.money),True,(0,128,0))
    def subMoney(self,profit):
        self.money -= profit
        self.text = self.font.render(str(self.money),True,(0,128,0))
    def move_ip(self,w,h):
        self.Rect.move_ip(w,h)
        self.textRect = self.text.get_rect()
        self.textRect.move_ip(w+90,h+15)

class Objects():
    def __init__(self,a):
        self.info = a
    def build(self):return self.info[0]
    def obj(self):  return self.info[1]
    def user(self): return self.info[2]
    def profile(self):  return self.info[3]
    def window(self):  return self.info[4]

def displayPrint(objects,display):
    while True:
        display.blit(display.map, (0,0))

        display.blit(objects.user()[User.Table].Surf,(500,480))

        for i in objects.info:
            for j in i:
                display.blit(j.Surf,j.Rect)

        for i in objects.profile():
            i.info()


        pygame.display.update()
        time.sleep(0.05)

def diceMDown(button,pos,display):
    (w,h) = pos
    if button[2].w <= w<=button[2].w +100:
        if button[2].h<h<=button[2].h+100:
            button[2] = button [1]

def diceMUp(button,pos,display):
    (w,h) = pos
    if button[2].w <= w<=button[2].w +100:
        if button[2].h<h<=button[2].h+100:
            button[2] = button [0]
            if dice(diceRandom(2,1),objects.user()[User.Table]): 
                objects.profile()[User.Table].addMoney(150000)
            User.Table +=1
            User.Table %= User.population


whtoindex ={"00":0,"10":1,"20":2,"30":3,"40":4,"50":5,"60":6,"70":7,"80":8,
            "01":31,"81": 9,"02":30,"82":10,"03":29,"83":11,"04":28,"84":12,
            "05":27,"85":13,"06":26,"86":14,"07":25,"87":15,"88":16
            ,"78":17,"68":18,"58":19,"48":20,"38":21,"28":22,"18":23,"08":24
            }
            
def landClick(objects,pos,display):
    (w,h) = pos
    if len(objects.window()):
        return 0
    if 1<=(w//142)<8:
         if 1<=(h//80)<8:
            return 0
    objects.window().append(Object("./images/info/info.bmp",440,238))
    objects.window().append(objects.build()[whtoindex[str(w//142)+str(h//80)]].getLandProfile(display))

def landCheck(objects,pos,display):
    (w,h) = pos
    if 0 == len(objects.window()):
        return 0
    if 1<=(w//142)<8:
        if 1<=(h//80)<8:
            while 0 != len(objects.window()):
                objects.window().pop()

def handle(objects,display):
    while True:
####################
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                diceMDown(objects.obj(),event.pos,display)
                landClick(objects,event.pos,display)
            if event.type == pygame.MOUSEBUTTONUP:
                diceMUp(objects.obj(),event.pos,display)
            if event.type == pygame.MOUSEMOTION:
                landCheck(objects,event.pos,display)
                print('mouse move (%d,%d)'%event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:# ESC 키에 대한 처리
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def setup(mapName, userName,objectName,landName):
    display = Map(mapName)


    land = setLand(landName,display)

    user = []
    for name in userName:
        user.append(User("./images/character/"+name+".png"))

    profile = []
    for name in userName:
        profile.append(Profile("./images/character/"+name+".png"))

    for i in range(len(profile)):
        profile[i].move_ip(180,100+110*i)

    obj = []
    for name in objectName: 
        obj.append(Object("./images/button/"+name+".png",600,467))
    obj.append(Object("./images/button/"+objectName[0]+".png",600,467))

    window = []
    objects = Objects([land, obj, user, profile, window])

    display.blit(display.map, (0,0))
    for i in objects.info[1:]:
        for j in i:
            display.blit(j.Surf,j.Rect)

    pygame.display.flip()

    return objects,display

if __name__=="__main__":
    file = open("init.txt",'r')
    dics = {}
    while True:
        line = file.readline()
        if not line: break
        line = line.replace('\n','').split(' = ')
        dics[line[0]] = line[1].split(', ')

    mapName = dics["map"]
    userName = dics["user"]
    objectName = dics["button"]

    objects,display = setup(mapName,userName,objectName,"Building.txt")
    t = threading.Thread(target=displayPrint, args=(objects,display))
    t.daemon = True
    t.start()
    handle(objects,display)
