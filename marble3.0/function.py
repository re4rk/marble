import sys, pygame, time, threading
from random import *

pygame.init()
numtocolor = ["red","blue","green","yellow"]
# define : 37 개, class : 7개 Dice, World, Land, User, Object, Button

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

class Dice():
    def __init__(self):
    def throw(self,world,pos): # dice throw
    def gauge(self,world): # set gauge number and display gaugebar
    def delay(self): # Slow down on removing the gauge bar.
    def up(self,world,pos): # if mouse click up
    def doublebool(self, dicenum):#Decide double
    def displayDice(self, num):#Display dice on the screen
    def random(self,num, a = 1): #Probability of dice
    def move(self,num,user): # movement of players
class World():
    def __init__(self,mapName, userName,objectName,landName):
    def blit(self,a,b):
    def display(self):
class Land():
    def __init__(self,information):
    def getTotalPrice(self): #total price of building and ground.
    def buildLandmark(self):
    def getInfo(self,world):
    def displayinfo(self,info,w,h):

class User():
    population  = 0 
    Table   = 0
    def __init__(self,location,w = 0,h = 0):
    def addtMoney(self,cost): #addition of total money
    def subtMoney(self,profit): #subtraction of total money
    def profileInfo(self,w,h): #About profile
    def addMoney(self,cost): #addtion of current money
    def subMoney(self,profit): #subtraction of current money
    def profileMove(self,w,h): # just move profile
class Object():
    def __init__(self,location,w = 0,h = 0):
    def move_ip(self,w,h):

class Button(): # list of button path
    def __init__(self,Ww,Wh):

def setLands(fileName): #loading information about the land
def passGround(world): # A toll payment
def tradebuild(world): #Buy and sell a building
def chooselandmark(world): #build landmark
def normalbuilding(world): #build building except landmark
def take_over(world): #take over the ground and building
def buildLandmark(self): #build a landmark
def displayPriceList(world): #Displat prices and buttons on the screen
def displayBuilding(world,land,w, h): #Display building on the screen
def displayinfo(info,w,h,size,RGB): #Display text information on the screen
def displayinfointernal(info, w, h, size, RGB): #Display dead information on the screen
def handle(world): #Dice throw motion
def openInitFile(fileName):

if __name__=="__main__":
    mapName, userName, objectName = openInitFile("init.txt")
    Button(450,300)
    world = World(mapName,userName,objectName,"Building.txt")

    t = threading.Thread(target=world.display, args=())
    t.daemon = True
    t.start()

    handle(world)