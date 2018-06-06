import sys, pygame, time, threading
from random import *

pygame.init()


class Dice():
    def __init__(self):
        self.gaugeNum = 0
        self.check = False
        self.w, self.h = (0,0)
        self.gaugebar = []
        self.threadd = True
        for i in range(2,13):
            self.gaugebar.append(Object("./images/gauge/gauge"+str(i)+".png",480,400))

    def throw(self,world,pos):
        (self.w,self.h) = pos
        button = world.obj()
        if button[2].w <= self.w<=button[2].w +100:
            if button[2].h<self.h<=button[2].h+100:
                button[2] = button[1]
                self.check = False
                self.gauge()
    def gauge(self):
        i = 2
        j = True
        if not world.gaugebar():
            world.gaugebar().append(Object("./images/gauge/gauge"+'2'+".png",480,400))
        self.threadd = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    self.up(world,event.pos)
                    t = threading.Thread(target=self.delay, args=())
                    t.daemon = True
                    t.start()
                    self.threadd = True
                    return 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:# ESC 키에 대한 처리
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.gaugeNum = i
            world.gaugebar()[0] = Object("./images/gauge/gauge"+str(i)+".png",480,400)
            time.sleep(0.03)

            if j ==True : i += 1
            elif j == False : i -= 1

            if i == 2 : j = True
            elif i == 12 : j = False 

    def delay(self):
        time.sleep(2)
        if self.threadd ==True:
            world.gaugebar().pop()

    def up(self,world,pos):
        button = world.obj()
        button[2] = button[0]
        print(self.gaugeNum)
        if self.move(self.random(self.gaugeNum,10),world.user()[User.Table]):
            world.user()[User.Table].addMoney(150000)    
        displayPriceList(world)
        passGround(world)     
        User.Table +=1
        User.Table %= User.population
        self.check = True

    def random(self,num, a = 1):
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

    def move(self,num,user):
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
            time.sleep(0.10)
        index= user.index//32
        user.index%=32
        return index    

class World():
    def __init__(self,mapName, userName,objectName,landName):
        self.map = pygame.image.load(mapName[0])
        self.screen = pygame.display.set_mode((1278,720))
        land = setLands(landName)
        user = []
        for name in userName:
            user.append(User("./images/character/"+name+".png"))
        obj = []
        for name in objectName: 
            obj.append(Object("./images/button/"+name+".png",600,467))
        obj.append(Object("./images/button/"+objectName[0]+".png",600,467))
        window = []

        self.dice = Dice()


        self.objects=[land, obj, [], user, window, [],[]]
    def blit(self,a,b):
        self.screen.blit(a,b)
    def land(self):return self.objects[0]
    def obj(self):return self.objects[1]
    def building(self):return self.objects[2]
    def user(self):return self.objects[3]
    def window(self):return self.objects[4]
    def text(self):return self.objects[5]
    def gaugebar(self):return self.objects[6]
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
            time.sleep(0.02)

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
        self.village = False
        self.villagePrice = information[4]
        self.building = False
        self.buildingPrice = information[5]
        self.hotel = False
        self.hotelPrice = information[6]
        self.landmark = False        
        self.landmarkPrice = information[7]
        self.totalPrice = 0
        self.font = pygame.font.SysFont("comicsansms",15)
        self.a = self.landName
        self.Surf = self.font.render(self.a,True,(0,0,0))
        self.Rect = self.Surf.get_rect()
        self.Rect.move_ip(self.w*142+5,self.h*80+3)

    def getTotalPrice(self):
        self.totalPrice = 0
        if self.ground == True:
            self.totalPrice += int(self.groundPrice)
        if(self.village == True):
            self.totalPrice += int(self.villagePrice)
        if(self.building == True ):
            self.totalPrice += int(self.buildingPrice)
        if(self.hotel == True ):
            self.totalPrice += int(self.hotelPrice)
        if(self.landmark == True):
            self.totalPrice += int(self.landmarkPrice)
        self.totalPrice *= 1.5

    def getInfo(self,world):
        world.window().append(Object("./images/info/info.bmp",480,263))

        a = Object("./images/temp.png",500,300)
        hostName = ["Red","Blue","Green","Yellow"]


        self.getTotalPrice()

        content = self.landName + ", toll : "+ str(int(self.totalPrice)) +"won"
        self.info(content,500,280)

        if self.landhost =="":
            content = "There is no owner of the island."
        else:
            content = "land's owner is "+ hostName[int(self.landhost)]
        self.info(content,500,300)


        content = "Ground : " + self.groundPrice+"won"
        self.info(content,500,330)

        content = "village : " + self.villagePrice+"won"
        self.info(content,500,350)

        content = "building : " + self.buildingPrice+"won"
        self.info(content,500,370)

        content = "hotel : " + self.hotelPrice+"won"
        self.info(content,500,390)

        content = "landmark : " + self.landmarkPrice+"won"
        self.info(content,500,410)


        return a

    def info(self,info,w,h):
        temp = Object("./images/temp.png",500,300)
        temp.Surf = self.font.render(info,True,(0,0,0))
        temp.Rect = self.Surf.get_rect()
        temp.Rect.move_ip(w,h)
        world.window().append(temp)


def deleteWindow(world,pos):
    (w,h) = pos

    if 480 <= w < 780:
        if 263 <= h < 443:
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
                if world.dice.check == True:
                    buttonRange(event, world)   
                deleteWindow(world,event.pos)
                world.dice.throw(world,event.pos)  

                (w,h) = event.pos
                w //= 142; h //= 80
                if (0 == w or w ==8)|(0 == h or h == 8) :
                    landIndex = whtoi[str(w)+str(h)]
                    world.land()[landIndex].getInfo(world)

            if event.type == pygame.MOUSEBUTTONUP:
                pass
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

def passGround(world):
    player = world.user()[User.Table]
    lander = world.land()[player.index]

    if(lander.landhost != str(User.Table)):
        if lander.landhost != "":
            host = world.user()[int(lander.landhost)]
        if(str(User.Table) != lander.landhost):
            if(lander.ground == True):
                player.subMoney(float(lander.groundPrice)*1.5)
                host.addMoney(float(lander.groundPrice)*1.5)
            if(lander.village == True):
                player.subMoney(float(lander.villagePrice)*1.5)
                host.addMoney(float(lander.villagePrice)*1.5)
            if(lander.building == True ):
                player.subMoney(float(lander.buildingPrice)*1.5)
                host.addMoney(float(lander.buildingPrice)*1.5)
            if(lander.hotel == True ):
                player.subMoney(float(lander.hotelPrice)*1.5)
                host.addMoney(float(lander.hotelPrice)*1.5)
            if(lander.landmark == True):
                player.subMoney(float(lander.landmarkPrice)*1.5)
                host.addMoney(float(lander.landmarkPrice)*1.5)



def buttonRange(event, world):
    player = world.user()[(User.Table+3)%4]
    lander = world.land()[player.index]
    if player.index%8 == 0:
        return 0
    if str((User.Table+3)%4) == lander.landhost or lander.landhost == "":
        ground = village = building = hotel = False

        while world.dice.check:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    (w, h) = event.pos
                    if 190 <= h <= 260:
                        if 650 <= w <=744 :
                            world.window().append(Object("./images/button/dbuy.png", 650, 190))
                            ground = True
                            break
                        elif 744 <= w <=838 :
                            world.window().append(Object("./images/button/dvillage.png", 744, 190))
                            village = True
                        elif 838 <= w <=932 :
                            world.window().append(Object("./images/button/dbuilding.png", 838, 190))
                            building = True
                        elif 932 <= w <=1026 :
                            world.window().append(Object("./images/button/dhotel.png", 932, 190))
                            hotel = True
                        elif 1026 <= w <=1120 :
                            world.dice.check = False
                            return 0
                        elif 600<= w <= 700 and 467<= h <=567:
                            world.dice.check = False
                            return 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:# ESC 키에 대한 처리
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if ground == True:
                break
        world.dice.check = False
        if (ground == True and lander.ground == False):
            lander.ground = True
            makeBuilding( "Ground.png",player.w, player.h)
            player.subMoney( lander.groundPrice)       
        if (village == True and lander.village == False):
            lander.village = True
            makeBuilding( "Village.bmp",player.w, player.h)
            player.subMoney( lander.villagePrice)
        if (building == True and lander.building == False):
            lander.building = True
            makeBuilding( "Building.bmp",player.w, player.h)
            player.subMoney( lander.buildingPrice)
        if (hotel == True and lander.hotel == False):
            lander.hotel = True
            makeBuilding( "Hotel.bmp",player.w, player.h)
            player.subMoney( lander.hotelPrice)
        lander.landhost = str((User.Table+3)%4)
        return 0

numtocolor = ["red","blue","green","yellow"]
def makeBuilding(name,w, h):
    w *= 142 ; h *= 80

    color = numtocolor[(User.Table+3)%4]

    if (name=="Village.bmp"): w += 65+48; h += 49
    elif(name=="Building.bmp"): w += 65+24; h += 19
    elif(name=="Hotel.bmp"): h +=5; w += 65
    elif(name=="Ground.png"): pass

    world.building().append(Object("./images/building/"+color+name, w, h))

def displayPriceList(world):
    visitorIndex = world.user()[User.Table].index
    land = world.land()[visitorIndex]

    if str(User.Table) == land.landhost or land.landhost == "":
        if(visitorIndex%8 != 0):
            if land.ground == False:
                world.window().append(Object("./images/button/buy.png", 650, 190))
            else :
                world.window().append(Object("./images/button/dbuy.png", 650, 190))
            if land.village == False:    
                world.window().append(Object("./images/button/village.png", 744, 190))
            else :
                world.window().append(Object("./images/button/dvillage.png", 744, 190))
            if land.building == False: 
                world.window().append(Object("./images/button/building.png", 838, 190))
            else :
                world.window().append(Object("./images/button/dbuilding.png", 838, 190))
            if land.hotel == False: 
                world.window().append(Object("./images/button/hotel.png", 932, 190))
            else :
                world.window().append(Object("./images/button/dhotel.png", 932, 190))

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