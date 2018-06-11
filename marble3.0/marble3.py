import sys, pygame, time, threading
from random import *

numtocolor = ["red","blue","green","yellow"]

whtoi ={"00":0,"10":1,"20":2,"30":3,"40":4,"50":5,"60":6,"70":7,"80":8,"01":31,"81": 9,"02":30,"82":10,"03":29,"83":11,"04":28,"84":12,"05":27,"85":13,"06":26,"86":14,"07":25,"87":15,"88":16,"78":17,"68":18,"58":19,"48":20,"38":21,"28":22,"18":23,"08":24}
            
itowh ={0:"00",1:"10",2:"20",3:"30",4:"40",5:"50",6:"60",7:"70",8:"80",31:"01",9:"81",30:"02",10:"82",29:"03",11:"83",28:"04",12:"84",27:"05",13:"85",26:"06",14:"86",25:"07",15:"87",16:"88",17:"78",18:"68",19:"58",20:"48",21:"38",22:"28",23:"18",24:"08"}

pygame.init()

class Dice():
    def __init__(self):
        self.gaugeNum = 0
        self.check = False
        self.w, self.h = (0,0)
        self.gaugebar = []
        self.threadd = True
        for i in range(2,13):
            self.gaugebar.append(Object("./images/gauge/gauge"+str(i)+".png",480,400))  #gauge bar loading
    def throw(self,world,pos): # dice throw
        (self.w,self.h) = pos
        button = world.obj

        if button[2].w <= self.w<=button[2].w +100:
            if button[2].h<self.h<=button[2].h+100:
                button[2] = button[1] # push dice button                
                self.check = False
                self.gauge(world)

    def gauge(self,world):
        i = 2
        j = True
        if not world.gaugebar:
            world.gaugebar.append(Object("./images/gauge/gauge"+'2'+".png",480,400)) # gauge bar picture
        while True: 
            self.threadd = True
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    self.up(world,event.pos)
                    t = threading.Thread(target=self.delay, args=())
                    t.daemon = True
                    t.start()
                    return 0

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:# ESC 키에 대한 처리
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.gaugeNum = i
            world.gaugebar[0] = self.gaugebar[i - 2]
            time.sleep(0.03)

            if j ==True : i += 1
            elif j == False : i -= 1

            if i == 2 : j = True
            elif i == 12 : j = False 

    def delay(self):
        self.threadd = True
        time.sleep(2)
        self.threadd = False

    def up(self,world,pos): 
        visitor = world.user[User.Table]
        lander = world.land[visitor.index]
        button = world.obj
        button[2] = button[0]

        dicenum = int(self.random(self.gaugeNum,3))

        (first, second) = self.boolDiceDouble(dicenum)
        self.displayDice(first, second)

        if self.move(dicenum ,world.user[User.Table]):        
            world.user[User.Table].addMoney(150000)
        self.check = True

        passGround(world)
        take_over(world)
        displayPriceList(world)
        tradebuild(world)  
        deleteWindow(world,pos)

        if (first != second):
            User.Table += 1
            User.Table %= User.population
            while world.user[User.Table].life == False:
                User.Table += 1
                User.Table %= User.population
        else:
            world.window.append(Object("./images/dice/double.png", 480, 100))

    def boolDiceDouble(self, dicenum):#Decide double
        if dicenum >= 7 : first = randint(dicenum-6, 6)            
        else: first = randint(1, dicenum-1)
        second = dicenum - first
        return (first, second)

    def displayDice(self, first,second):#Display dice on the screen
        world.window.append(Object("./images/dice/"+str(first)+".png", 480, 200))
        world.window.append(Object("./images/dice/"+str(second)+".png", 570, 200))

    def random(self,num, a = 1): #Probability of dice
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

    def move(self,num,user): # movement of players
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

        self.land = setLands(landName)
        self.user = []
        self.obj = []
        self.window = []
        self.text = []
        self.gaugebar =[]
        self.dice = Dice()

        for name in userName:
            self.user.append(User("./images/character/"+name+".png"))
        for name in objectName: 
            self.obj.append(Object("./images/button/"+name+".png",600,467))

        self.obj.append(Object("./images/button/"+objectName[0]+".png",600,467))

    def blit(self,a,b):
        self.screen.blit(a,b)

    def display(self):
        while True:
            self.blit(self.map, (0,0))

            self.blit(self.user[User.Table].Surf,(500,480))

            for i in range(32):
                if self.land[i].landhost !="":
                    wh = itowh[i]
                    displayBuilding(world,self.land[i],w = int(wh[0]),h = int(wh[1]))

            for i in self.land:
                self.blit(i.text,i.Rect)

            for i in self.obj:
                self.blit(i.Surf,i.Rect)

            for i in self.gaugebar:
                if self.dice.threadd == True:
                    self.blit(i.Surf,i.Rect)

            for i in self.user:
                self.blit(i.Surf,i.Rect)

            for i in self.window:
                self.blit(i.Surf,i.Rect)

            for i in self.text:
                self.blit(i.Surf,i.Rect)

            for i in range(User.population):
                self.user[i].profileInfo(180,100+110*i)

            pygame.display.update()
            time.sleep(0.02)

def setLands(fileName): #loading information about the land
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
        self.groundObject = True
        self.groundPrice = information[3]
        self.village = False
        self.villageObject = True
        self.villagePrice = information[4]
        self.building = False
        self.buildingObject = True
        self.buildingPrice = information[5]
        self.hotel = False
        self.hotelObject = True
        self.hotelPrice = information[6]
        self.landmark = False        
        self.landmarkObject = True
        self.landmarkPrice = information[7]
        self.take_over =False        

        self.totalPrice = 0
        self.font = pygame.font.SysFont("comicsansms",15)
        #self.a = self.landName
        self.text = self.font.render(self.landName,True,(0,0,0))
        self.Rect = (self.w*142+5,self.h*80+3)

    def getTotalPrice(self): #total price of building and ground.
        self.totalPrice = 0
        if self.ground == True:
            self.totalPrice += int(self.groundPrice)
        if self.village == True:
            self.totalPrice += int(self.villagePrice)
        if self.building == True :
            self.totalPrice += int(self.buildingPrice)
        if self.hotel == True :
            self.totalPrice += int(self.hotelPrice)
        if self.landmark == True:
            self.totalPrice += int(self.landmarkPrice)
        return self.totalPrice

    def buildLandmark(self):
        if False not in [self.ground,self.village,self.building,self.hotel]:
            self.ground = self.village = self.building = self.hotel = False
            self.landmark = True
            self.getTotalPrice()

    def getInfo(self,world):
        world.window.append(Object("./images/info/info.bmp",w = 480,h = 263))

        hostName = ["Red","Blue","Green","Yellow"]

        displayinfo(self.landName + ", toll : "+ str(self.getTotalPrice()* 1.5) +"won",size = 20,w = 500,h = 280,RGB = (0,128,0))

        if self.landhost =="":
            displayinfo("There is no owner of the island.",size = 15,w = 500,h = 310,RGB = (0,128,0))
        else:
            displayinfo("land's owner is "+ hostName[int(self.landhost)],size = 15,w = 500,h = 310,RGB = (0,128,0))

        displayinfo("Ground : " + self.groundPrice+"won",size = 15,w = 500,h = 330,RGB = (0,128,0))
        displayinfo("village : " + self.villagePrice+"won",size = 15,w = 500,h = 350,RGB = (0,128,0))
        displayinfo("building : " + self.buildingPrice+"won",size = 15,w = 500,h = 370,RGB = (0,128,0))
        displayinfo("hotel : " + self.hotelPrice+"won",w = 500,size = 15,h = 390,RGB = (0,128,0))
        displayinfo("landmark : " + self.landmarkPrice+"won",size = 15,w = 500,h = 410,RGB = (0,128,0))

class Object():
    def __init__(self,location,w = 0,h = 0):
        self.Surf = pygame.image.load(location)
        self.Rect = self.Surf.get_rect()
        self.Rect.move_ip(w,h)
        self.w, self.h = w, h

    def move_ip(self,w,h):
        self.Rect.move_ip(w,h)



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

        self.life = True

        self.money = 4000000
        self.font = pygame.font.SysFont("comicsansms",30)
        self.text = self.font.render(str(self.money),True,(0,128,0))

        self.totalmoney = 4000000
        self.totalfont = pygame.font.SysFont("Consolas",20)
        self.totaltext = self.totalfont.render(str(self.totalmoney),True,(128,0,0))

    def addtMoney(self,cost): #addition of total money
        self.totalmoney += int(cost)
        self.totaltext = self.totalfont.render(str(self.totalmoney),True,(128,0,0))

    def subtMoney(self,profit): #subtraction of total money
        self.totalmoney -= int(profit)
        self.totaltext = self.totalfont.render(str(self.totalmoney),True,(128,0,0))

    def addMoney(self,cost): #addtion of current money
        self.money += int(cost)
        self.text = self.font.render(str(self.money),True,(0,128,0))

    def subMoney(self,profit): #subtraction of current money
        self.money -= int(profit)
        self.text = self.font.render(str(self.money),True,(0,128,0))

    def profileInfo(self,w,h): #About profile
        world.blit(self.Surf,(w,h))
        world.blit(self.text,(w+90,h+15))
        world.blit(self.totaltext,(w+90,h+55))

class Object():
    def __init__(self,location,w = 0,h = 0):
        self.Surf = pygame.image.load(location)
        self.Rect = self.Surf.get_rect()
        self.Rect.move_ip(w,h)
        self.w, self.h = w, h

    def move_ip(self,w,h):
        self.Rect.move_ip(w,h)
        
class TextObject():
    def __init__(self,content,font = "comicsansms",size = 0,w = 0,h = 0,RGB = (0,128,0)):
        self.font = pygame.font.SysFont(font, size)
        self.Surf = self.font.render(str(content),True,(0,128,0))
        self.Rect = (w,h)

def passGround(world): # A toll payment
    visitor = world.user[User.Table]
    visitorName = str(User.Table)
    owner = world.land[visitor.index]

    if owner.landhost == "":
        return 0

    host = world.user[int(owner.landhost)]
    if visitorName != owner.landhost:
        owner.getTotalPrice()

        visitor.subMoney(float(owner.totalPrice)*1.5)
        host.addMoney(float(owner.totalPrice)*1.5)
        visitor.subtMoney(float(owner.totalPrice)*1.5)
        host.addtMoney(float(owner.totalPrice)*1.5)

        boolBankruptcy(visitor,0)

def boolBankruptcy(user,Price):
    if user.money <= Price:
        user.life = False
        displayinfoEternal("I'm dead..", w=200, h=100 + 120 * User.Table, size=35, RGB=(128, 0, 0))
        for i in range(32):
            land = world.land[i]
            if land.landhost == str(User.Table):
                land.landhost=""
                land.ground = False
                land.groundObject = True
                land.village = False
                land.villageObject = True
                land.building = False
                land.buildingObject = True
                land.hotel = False
                land.hotelObject = True
                land.landmark = False
                land.landmarkObject = True
                land.totalPrice = 0

def chooselandmark(world): #build landmark
    color = numtocolor[int(User.Table)]
    visitor = world.user[User.Table]
    lander = world.land[visitor.index]
    landmark = ground = village = building = hotel = False

    while world.dice.check:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                (w, h) = event.pos
                if 300+200 <= h <= 300+250:
                    if 450+20 <= w <=450+350 :
                        lander.village = lander.building = lander.hotel = False
                        world.window.append(Object("./images/button/afterlandmark.png", 470, 509))
                        landmark = True
                        world.dice.check = False
                        break
                elif 305 <= h <=345 :
                    if 835<= w <= 875:
                        world.dice.check = False
                        return 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:# ESC 키에 대한 처리
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    #while end
    world.dice.check = False
    w = lander.w *142 ; h = 80 * lander.h
    if (landmark == True and lander.landmark == False):
        lander.landmarkObject = Object("./images/building/"+color+"landmark.png",w + 40, h - 20)
        lander.landmark = True
        visitor.subMoney( lander.landmarkPrice)

def normalbuilding(world): #build building except landmark
    visitor = world.user[User.Table]
    lander = world.land[visitor.index]
    landmark = ground = village = building = hotel = False
    totalPrice = 0
    while world.dice.check:

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                (w, h) = event.pos
                if 509 <= h <= 579:
                    # click ground village
                    if 470 <= w <=550 :
                        print(totalPrice)
                        if visitor.money >= totalPrice:
                            world.window.append(Object("./images/button/afterbuy.png", 470, 509))
                            ground = True
                            world.dice.check = False
                            break
                        elif totalPrice != 0:
                            world.window.append(Object("./images/info/cant buy.png", 450, 250))
                            time.sleep(1.5)
                            continue
                    # click building village
                    elif 570 <= w <=650 :
                        if village == False and lander.village == False:
                            world.window.append(Object("./images/button/aftervillage.png", 570, 509))
                            village = True
                            totalPrice+= int(lander.villagePrice)
                        elif village == True and lander.village == False:
                            world.window.append(Object("./images/button/beforevillage.png", 570, 509))
                            village = False
                            totalPrice-= int(lander.villagePrice)
                    # click building button
                    elif 670 <= w <=750 :
                        if building == False and lander.building == False:
                            world.window.append(Object("./images/button/afterbuilding.png", 670, 509))
                            building = True
                            totalPrice+= int(lander.buildingPrice)
                        elif building == True and lander.building == False:
                            world.window.append(Object("./images/button/beforebuilding.png", 670, 509))
                            building = False
                            totalPrice-= int(lander.buildingPrice)
                    # click Hotel button
                    elif 770 <= w <=850 :
                        if hotel == False and lander.hotel == False:
                            world.window.append(Object("./images/button/afterhotel.png", 770, 509))
                            hotel = True
                            totalPrice+= int(lander.hotelPrice)
                        elif hotel == True and lander.hotel == False:
                            world.window.append(Object("./images/button/beforehotel.png", 770, 509))
                            hotel = False
                            totalPrice-= int(lander.hotelPrice)
                elif 305 <= h <=345 :
                    if 835<= w <= 875:
                        world.dice.check = False
                        return 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:# ESC 키에 대한 처리
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    # while end

    color = numtocolor[int(User.Table)]
    w = lander.w *142 ; h = 80 * lander.h
    if visitor.money >= totalPrice:
        #build a building according to a player
        if (ground == True and lander.ground == False): 
            lander.groundObject = Object("./images/building/"+color+"Ground.png",w, h)
            lander.ground = True
            visitor.subMoney(lander.groundPrice)        

        if (village == True and lander.village == False):
            lander.villageObject = Object("./images/building/"+color+"Village.bmp", w + 113, h + 49)
            lander.village = True
            visitor.subMoney( lander.villagePrice)

        if (building == True and lander.building == False):
            lander.buildingObject = Object("./images/building/"+color+"Building.bmp",w + 89, h + 19)
            lander.building = True
            visitor.subMoney( lander.buildingPrice)

        if (hotel == True and lander.hotel == False):
            lander.hotelObject = Object("./images/building/"+color+"Hotel.bmp",w + 65, h + 5)
            lander.hotel = True
            visitor.subMoney( lander.hotelPrice)
        lander.landhost = str(User.Table)
    ######normalbuilding end

def tradebuild(world): #Buy and sell a building
    visitor = world.user[User.Table]
    visitorName = str(User.Table)
    lander = world.land[visitor.index]
    hostName = lander.landhost

    if (visitor.money >0 and visitor.money > lander.getTotalPrice() and visitor.totalmoney > 0):
        if visitor.index%8 == 0:
            return 0


        if visitorName == hostName or hostName == "":
            if False not in [lander.ground,lander.village,lander.building,lander.hotel]:
                chooselandmark(world)
            elif lander.landmark== False:
                normalbuilding(world)

def take_over(world): #take over the ground and building
    visitor = world.user[User.Table]
    visitorName = str(User.Table)
    lander = world.land[visitor.index]
    if lander.landmark == False and lander.landhost != "" and visitor.money > lander.getTotalPrice() and visitor.totalmoney >0:
        hostName = lander.landhost  
        host = world.user[int(lander.landhost)]
        if visitorName != hostName:       
            world.window.append(Button.window)
            world.window.append(Button.exitbutton)
            displayinfo( lander.landName ,w = 490,h = 325,size = 30, RGB = (0,128,0))
            displayinfo("Totalprice : " + str(lander.getTotalPrice()) +"won",w = 472,h = 370,size = 20, RGB = (0,128,0))                       
            world.window.append(Object("./images/button/beforebuy.png", 20+450, 109+300))

            while world.dice.check:                
                for event in pygame.event.get():                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        (w, h) = event.pos
                        if 109+300 <= h <= 109+300+50:
                            if 450+20 <= w <= 450+20+80 and lander.take_over == False:       
                                world.window.append(Object("./images/button/afterbuy.png", 20+450, 109+300))            
                                lander.take_over=True            
                                lander.getTotalPrice()

                                boolBankruptcy(visitor,lander.getTotalPrice())  

                                lander.take_over =False 
                                visitor.subMoney(float(lander.totalPrice))
                                host.addMoney(float(lander.totalPrice))
                                visitor.subtMoney(float(lander.totalPrice))
                                host.addtMoney(float(lander.totalPrice))
                                lander.landhost = visitorName                                  
                                color = numtocolor[int(User.Table)]
                                w = lander.w *142 ; h = 80 * lander.h
                                #change the color according to player
                                if (lander.ground == True):
                                    lander.groundObject = Object("./images/building/"+color+"Ground.png",w, h)
                                    lander.ground = True            

                                if (lander.village == True):
                                    lander.villageObject = Object("./images/building/"+color+"Village.bmp", w + 113, h + 49)
                                    lander.village = True            

                                if (lander.building == True):
                                    lander.buildingObject = Object("./images/building/"+color+"Building.bmp",w + 89, h + 19)
                                    lander.building = True            

                                if (lander.hotel == True):
                                    lander.hotelObject = Object("./images/building/"+color+"Hotel.bmp",w + 65, h + 5)
                                    lander.hotel = True

                                return 0                             

                        elif 305 <= h <=345 :
                            if 835<= w <= 875:
                                world.dice.check = False
                                lander.take_over =False                                
                                return 0

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:# ESC 키에 대한 처리
                            pygame.quit()
                            sys.exit()

                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

def displayPriceList(world): #Displat prices and buttons on the screen
    visitorIndex = world.user[User.Table].index
    visitorName = str(User.Table)

    land = world.land[visitorIndex]
    hostName = land.landhost

    if visitorName == hostName or hostName == "":
        if(visitorIndex%8 != 0):
            # when build lanmark
            if False not in [land.ground,land.village,land.building,land.hotel]:
                world.window.append(Button.landmarkwindow)
                world.window.append(Button.exitbutton)
                world.window.append(Button.beforelandmark)
                displayinfo( land.landName ,w = 490,h = 325,size = 30, RGB = (0,128,0))
                displayinfo("landmark : " + land.landmarkPrice+"won",w = 472,h = 400,size = 20, RGB = (0,128,0))
            elif land.landmark== False:
                world.window.append(Button.window)
                world.window.append(Button.exitbutton)
                displayinfo( land.landName ,w = 490,h = 325,size = 30, RGB = (0,128,0))
                displayinfo("Ground : " + land.groundPrice+"won",w = 472,h = 370,size = 20, RGB = (0,128,0))
                displayinfo("Village : " + land.villagePrice+"won",w = 472,h = 392,size = 20, RGB = (0,128,0))
                displayinfo("Building : " + land.buildingPrice+"won",w = 472,h = 414,size = 20, RGB = (0,128,0))
                displayinfo("Hotel : " + land.hotelPrice+"won",w = 472,h = 436,size = 20, RGB = (0,128,0))
                world.window.append(Button.beforebuy)
                if land.village == False:    
                    world.window.append(Button.beforevillage)
                else :
                    world.window.append(Button.aftervillage)
                if land.building == False: 
                    world.window.append(Button.beforebuilding)
                else :
                    world.window.append(Button.afterbuilding)
                if land.hotel == False: 
                    world.window.append(Button.beforehotel)
                else :
                    world.window.append(Button.afterhotel)


def buildLandmark(self): #build a landmark
    if False not in [self.ground,self.village,self.building,self.hotel]:
        self.ground = self.village = self.building = self.hotel = False
        self.landmark = True
        self.getTotalPrice()
    lander.landhost = str((User.Table+3)%4)
    return 0

def handle(world): #Dice throw motion
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                deleteWindow(world,event.pos)
                (w, h) = event.pos
                world.dice.throw(world,event.pos)  

                (w,h) = event.pos
                w //= 142; h //= 80
                if (0 == w or w ==8)|(0 == h or h == 8) :
                    landIndex = whtoi[str(w)+str(h)]
                    world.land[landIndex].getInfo(world)

            if event.type == pygame.MOUSEBUTTONUP:
                pass
            if event.type == pygame.MOUSEMOTION:
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:# ESC 키에 대한 처리
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
def displayBuilding(world,land,w, h): #Display building on the screen
    w *= 142 ; h *= 80
    if land.ground == True:
        world.blit(land.groundObject.Surf, land.groundObject.Rect)
    if land.village == True:
        world.blit(land.villageObject.Surf, land.villageObject.Rect)
    if land.building == True:
        world.blit(land.buildingObject.Surf, land.buildingObject.Rect)
    if land.hotel == True:
        world.blit(land.hotelObject.Surf, land.hotelObject.Rect)
    if land.landmark == True:
        world.blit(land.landmarkObject.Surf, land.landmarkObject.Rect)

def displayinfo(content,w,h,size,RGB):
    world.window.append(TextObject(content,"comicsansms",size,w,h,RGB))

def displayinfoEternal(content, w, h, size, RGB): #Display dead information on the screen
    world.text.append(TextObject(content,"comicsansms",size,w,h,RGB))

class Button(): # list of button path
    def __init__(self,Ww,Wh):
        Button.window = Object("./images/button/aaa.png", Ww, Wh)
        Button.landmarkwindow = Object("./images/button/bbb.png", Ww, Wh)

        Button.exitbutton = Object("./images/button/exitbutton.png", Ww+385, Wh+5)

        Button.beforebuy = Object("./images/button/beforebuy.png", 20+Ww, 209+Wh)
        Button.afterbuy= Object("./images/button/afterbuy.png", 20+Ww, 209+Wh)

        Button.beforevillage= Object("./images/button/beforevillage.png", 120+Ww, 209+Wh)
        Button.aftervillage= Object("./images/button/aftervillage.png", 120+Ww, 209+Wh)

        Button.beforebuilding= Object("./images/button/beforebuilding.png", 220+Ww, 209+Wh)
        Button.afterbuilding= Object("./images/button/afterbuilding.png", 220+Ww, 209+Wh)

        Button.beforehotel= Object("./images/button/beforehotel.png", 320+Ww, 209+Wh)
        Button.afterhotel= Object("./images/button/afterhotel.png", 320+Ww, 209+Wh)

        Button.beforelandmark = Object("./images/button/beforelandmark.png",20 +Ww,200+Wh)
        Button.afterlandmark = Object("./images/button/afterlandmark.png",20 +Ww,200+Wh)

def deleteWindow(world,pos):
    (w,h) = pos

    if 480 <= w < 780:
        if 263 <= h < 443:
            return 0
    while 0 != len(world.window):
        world.window.pop()

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
    Button(450,300)
    world = World(mapName,userName,objectName,"Building.txt")

    t = threading.Thread(target=world.display, args=())
    t.daemon = True
    t.start()

    handle(world)