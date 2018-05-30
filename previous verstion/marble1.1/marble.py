import sys, pygame, time, threading
from random import *

pygame.init()

class Dice():
    w,h = (0,0)
    def down(world,pos):
        (Dice.w,Dice.h) = pos
        button = world.obj()
        if button[2].w <= Dice.w<=button[2].w +100:
            if button[2].h<Dice.h<=button[2].h+100:
                button[2] = button[1]
    def up(world,pos):
        button = world.obj()
        if button[2].w <= Dice.w<=button[2].w +100:
            if button[2].h<Dice.h<=button[2].h+100:
                button[2] = button[0]
                if Dice.move(Dice.random(2,1),world.user()[User.Table]):
                    world.profile()[User.Table].addMoney(150000)
                Event_Arr(world)            
                User.Table +=1
                User.Table %= User.population
    def random(num, a = 1):
        i = randint(1,360)
        if     0         < i <= 10 - a* 1 : return 2
        elif  10 - a *  1< i <= 30 - a* 3 : return 3
        elif  30 - a *  3< i <= 60 - a* 6 : return 4
        elif  60 - a *  6< i <=100 - a*10 : return 5
        elif 100 - a * 10< i <=150 - a*15 : return 6
        elif 150 - a * 15< i <=210 - a*21 : return 8
        elif 210 - a * 21< i <=260 - a*26 : return 8
        elif 260 - a * 26< i <=300 - a*30 : return 9
        elif 300 - a * 30< i <=330 - a*33 : return 10
        elif 330 - a * 33< i <=350 - a*35 : return 11
        elif 350 - a * 35< i <=360 - a*36 : return 12
        elif 360 - a * 36< i <=360        : return num
    def move(num,user):
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
        index= user.index//32
        user.index%=32
        return index    

class World():
    def __init__(self,mapName, userName,objectName,landName):
        self.map = pygame.image.load(mapName[0])
        self.screen = pygame.display.set_mode((1280,720))
        land = setLands(landName)
        user = []
        for name in userName:
            user.append(User("./images/character/"+name+".png"))
        obj = []
        for name in objectName: 
            obj.append(Object("./images/button/"+name+".png",600,467))
        obj.append(Object("./images/button/"+objectName[0]+".png",600,467))
        window = []
        self.objects=[land, obj, [], user, window, []]
    def blit(self,a,b):
        self.screen.blit(a,b)

    def land(self):return self.objects[0]
    def obj(self):return self.objects[1]
    def building(self):return self.objects[2]
    def user(self):return self.objects[3]
    def window(self):return self.objects[4]
    def text(self):return self.objects[5]
    def display(self):
        while True:
            self.blit(self.map, (0,0))
            self.blit(self.user()[User.Table].Surf,(500,480))
            for i in self.objects:
                for j in i:
                    self.blit(j.Surf,j.Rect)
            for i in range(User.population):
                self.user()[i].profileInfo(180,100+110*i)

            pygame.display.update()
            time.sleep(0.05)

def setLands(fileName):
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


class Land():
    def __init__(self,information):
        self.landhost = ""
        self.landName = information[0]
        self.w = int(information[1])
        self.h = int(information[2])
        self.ground = False
        self.groundPrice = information[3]
        self.house = False
        self.housePrice = information[4]
        self.building = False
        self.buildingPrice = information[5]
        self.hotel = False
        self.hotelPrice = information[6]
        self.landmark = False        
        self.landmarkPrice = information[7]
        self.totalPrice = 0
        self.font = pygame.font.SysFont("comicsansms",15)
        self.a = self.landName +"   "+ str(self.totalPrice)+"won"
        self.Surf = self.font.render(self.a,True,(0,0,0))
        self.Rect = self.Surf.get_rect()
        self.Rect.move_ip(self.w*142+5,self.h*80+3)

    def moneyLand(self,landhost,information):
        self.landhost = landhost
        self.ground = 0

    def getProfile(self):
        a = Object("./images/temp.png",500,300)
        ab = self.landName +" land's owner is "+ self.landhost
        a.Surf = self.font.render(ab,True,(0,0,0))
        a.Rect = self.Surf.get_rect()
        return a
    def mouseClick(world,pos):
        (w,h) = pos
        if len(world.window()):
            return 0
        w //= 142; h //= 80
        if 1 <= w < 8:
             if 1 <= h < 8:
                return 0
        world.window().append(Object("./images/info/info.bmp",440,238))
        world.window().append(world.land()[whtoi[str(w)+str(h)]].getProfile())

    def mouseCheck(world,pos):
        (w,h) = pos
        if 0 == len(world.window()):
            return 0
        w //= 142; h //= 80
        if 3 <= w < 6:
            if 3 <= h < 6:
                return 0
        while 0 != len(world.window()):
            world.window().pop()

whtoi ={"00":0,"10":1,"20":2,"30":3,"40":4,"50":5,"60":6,"70":7,"80":8,
            "01":31,"81": 9,"02":30,"82":10,"03":29,"83":11,"04":28,"84":12,
            "05":27,"85":13,"06":26,"86":14,"07":25,"87":15,"88":16
            ,"78":17,"68":18,"58":19,"48":20,"38":21,"28":22,"18":23,"08":24
            }
            

itowh ={0:"00",1:"10",2:"20",3:"30",4:"40",5:"50",6:"60",7:"70",8:"80",
            31:"01",9:"81",30:"02",10:"82",29:"03",11:"83",28:"04",12:"84",
            27:"05",13:"85",26:"06",14:"86",25:"07",15:"87",16:"88"
            ,17:"78",18:"68",19:"58",20:"48",21:"38",22:"28",23:"18",24:"08"
            }


class User():
    population  = 0 
    Table   = 0
    def __init__(self,location,w = 0,h = 0):
        User.population  += 1
        self.Surf = pygame.image.load(location)
        self.Rect = self.Surf.get_rect()
        self.Rect.move_ip(w,h)
        self.w, self.h = w , h
        self.index = 0

        self.font = pygame.font.SysFont("comicsansms",30)
        self.money = 2000000
        self.text = self.font.render(str(self.money),True,(0,128,0))

    def profileInfo(self,w,h):
        world.blit(self.Surf,(w,h))
        self.textRect = self.text.get_rect()
        world.blit(self.text,self.textRect.move(w+90,h+15))

    def addMoney(self,cost):
        self.money += int(cost)
        self.text = self.font.render(str(self.money),True,(0,128,0))

    def subMoney(self,profit):
        self.money -= int(profit)
        self.text = self.font.render(str(self.money),True,(0,128,0))

    def profileMove(self,w,h):
        self.Rect.move_ip(w,h)
        self.textRect = self.text.get_rect()
        self.textRect.move_ip(w+90,h+15)

class Object():
    def __init__(self,location,w = 0,h = 0):
        self.Surf = pygame.image.load(location)
        self.Rect = self.Surf.get_rect()
        self.Rect.move_ip(w,h)
        self.w = w
        self.h = h
    def move_ip(self,w,h):
        self.Rect.move_ip(w,h)
        
def handle(world):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                (w, h) = event.pos
                if(650 <= w <=1120 and 190 <= h <= 260):
                    buttonRange(event.pos, world)                    
                Land.mouseCheck(world,event.pos)
                Dice.down(world,event.pos)                
                Land.mouseClick(world,event.pos)

            if event.type == pygame.MOUSEBUTTONUP:
                Dice.up(world,event.pos)
                
            if event.type == pygame.MOUSEMOTION:
                #Land.landCheck(world,event.pos)
                #print('mouse move (%d,%d)'%event.pos)
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:# ESC 키에 대한 처리
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
#########################################
def buttonRange(pos, world):
    (w, h) = pos
    player = world.user()[(User.Table+3)%4]
    bbb = world.land()[player.index]

    if (650 <= w <=744 and 190 <= h <= 260):
        lander.ground = True
        landRange(player.w, player.h, "Ground")
        player.subMoney( bbb.groundPrice)       
    elif (744 <= w <=838 and 190 <= h <= 260):
        lander.landmark = True
        landRange(player.w, player.h, "Landmark.bmp")
        player.subMoney( bbb.housePrice)
    elif (838 <= w <=932 and 190 <= h <= 260):
        lander.hotel = True
        landRange(player.w, player.h, "Hotel.bmp")
        player.subMoney( bbb.buildingPrice)
    elif (932 <= w <=1026 and 190 <= h <= 260):
        lander.building = True
        landRange(player.w, player.h, "Building.bmp")
        player.subMoney( bbb.hotel)
    elif (1026 <= w <=1120 and 190 <= h <= 260):
        lander.house = True
        landRange(player.w, player.h, "Village.bmp")
        player.subMoney( bbb.landmarkPrice)


def landRange(w, h, name):        
    if(1 <= w <= 7 and  0 == h):
        for i in range(1, 7):
            if(w == i):
                checkBuilding(name, i*144, 0)
                print(name)        
    elif( 8 == w and 1 <= h <= 7):
        for i in range(1, 8):
            if(h == i):
                print("I : %d", i)
                checkBuilding(name, 1280-144, i*80)      
    elif(1 <= w <= 7 and h == 8):
        for i in range(1, 7):
            if(w == i):
                checkBuilding(name, i*144, 645)
    elif( 0 == w and 1 <= h <= 7):
        for i in range(1, 8):
            if(h == i):
                checkBuilding(name, 0, i*80)

def checkBuilding(name, w, h):
    if(name=="Village.bmp"):
        world.building().append(Object("./images/building/blue"+name, w+48, h+80-31))
        print("USER: %d %d", w, h)
    elif(name=="Building.bmp"):
        world.building().append(Object("./images/building/blue"+name, w+24, h+20))
    elif(name=="Hotel.bmp"):
        world.building().append(Object("./images/building/blue"+name, w, h+5))
    elif(name=="Landmark.bmp"):
        print("Landmark")
    elif(name=="Ground"):
        world.building().append(Object("./images/building/redHotel.bmp", w+48, h+31))

def Event_Arr(world):
    #if True:
    visitor = world.user()[User.Table]
    visitorLocation = visitor.index
    host = world.land()[visitorLocation].landhost

    i=0
    if host=="":
        world.window().append(Object("./images/button/buy.png", 650, 190))
    else:
        if checkNum(user.index, host):        
            if(Land.village+Land.building+Land.hotel == 3):
                objects.window().append(Object("./images/text/landmark.png", 744, 190))
            else:
                while(1):
                    if(i==3):
                        break
                    else:
                        if(Land.village == 0):                        
                            objects.window().append(Object("./images/text/village.png", 838, 190))
                            i+=1
                        elif(Land.building == 0):
                            objects.window().append(Object("./images/text/building.png", 932, 190))
                            i+=1
                        elif(Land.hotel == 0):
                            objects.window().append(Object("./images/text/hotel.png", 1026, 190))
                            i+=1



#########################################

def openInitFile(fileName):
    file = open(fileName,'r')
    dics = {}
    while True:
        line = file.readline()
        if not line: break
        line = line.replace('\n','').split(' = ')
        dics[line[0]] = line[1].split(', ')

    return dics["map"], dics["user"],  dics["button"]

if __name__=="__main__":
    mapName, userName, objectName = openInitFile("init.txt")

    world = World(mapName,userName,objectName,"Building.txt")

    t = threading.Thread(target=world.display, args=())
    t.daemon = True
    t.start()

    handle(world)
