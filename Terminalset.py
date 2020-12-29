##########################################################################################################################################
## This file defines some terminal object to use for leaf node of GP processs.                          
## Terminal Objects included in this are:                                                               
##                  Lsub_tree() object includes 4 types leaf L and some subFunctions -- increase()      
##                                                                                   -- initchange() __ change all attributes of polygon
##                                                                                                      after init population.
##                                                                                   -- change() __ change one attribute of polygon after
##                                                                                                    applying GP operation.     
##                                                                                   -- decrease() 
##                                                                                   -- Rotate() ___ 0,90,180,270 
##                                                                                   -- changeMaxXY()       
##                                                                                                      
##                  Usub_tree() object includes 4 types leaf U and some subFunctions -- increase()      
##                                                                                   -- initchange()
##                                                                                   -- change()       
##                                                                                   -- decrease()      
##                                                                                   -- Rotate() 
##                                                                                   -- changeMaxXY()       
##########################################################################################################################################
# linh.homanh@hust.edu.vn - 2018
# bachthuan03111997@gmail.com - 2018
import numpy as np
import random
from shapely.geometry import Polygon
import geopandas as gpd
import initGlobal as initG

def compare2lists(list1,list2):
    if len(list1) != len(list2):
        raise ValueError('two lists are compared need have the same length')

    dif = []
    for i in range(len(list1)):
        if list1[i] != list2[i]:
            dif.append(i)
    return dif 

attrL = initG.L()
attrU = initG.U()
if initG.Re_trainning:
    import update_state as us 
    anten = initG.AnT()
    sub = initG.Sub()
    attrL   = initG.L()
    attrU   = initG.U()
    low = initG.lowlevel()
    inGP = initG.GP()
    #path = us.load_temporary_path()
    us.update_all_saved_parameters(anten, sub, attrL, attrU, inGP, low)
# Define some terminal node.
        ## Create the L terminal.
class Lsub_tree:
    # the L tree has 4 types of tree.
    def __init__(self,maxX,maxY,type_of_tree = 1):
        self.type_of_tree = type_of_tree
        self._maxX = maxX
        self._maxY = maxY
        self._x1 = random.uniform(0,self._maxX/2) 
        self._x2 = random.uniform(0,(self._maxX - self._x1)/1)
        self._y1 = random.uniform(0,self._maxY/2)
        self._y2 = random.uniform(0,(self._maxY - self._y1)/1)
        self.originalPoint = self._createOriginalPoint()
        if self.type_of_tree == 1:
            self.polygon, self.X = self._createPolygon1()
        elif self.type_of_tree == 2:
            self.polygon, self.X = self._createPolygon2()
        elif self.type_of_tree == 3:
            self.polygon, self.X = self._createPolygon3()
        else:
            self.polygon, self.X = self._createPolygon4()
        self.edge = np.array([self._x1,self._x2,self._y1,self._y2]) # [x1,x2,y1,y2]

    def resestMaxXY(self,maxX,maxY):
        self._maxX = maxX
        self._maxY = maxY

    def initchange(self,x):
        # update the polygon after init.
        # input x: must be a list of 7 elements.
        self._oldx = x 
        rotate = x[0]
        rotate = round(((rotate+1)/2)*10)%4
        self._x1 = ((x[1]+1)/2)*(attrL.rangex1[1] - attrL.rangex1[0]) + attrL.rangex1[0]
        self._x2 = ((x[2]+1)/2)*(attrL.rangex2[1] - attrL.rangex2[0]) + attrL.rangex2[0]
        self._y1 = ((x[3]+1)/2)*(attrL.rangey1[1] - attrL.rangey1[0]) + attrL.rangey1[0]
        self._y2 = ((x[4]+1)/2)*(attrL.rangey2[1] - attrL.rangey2[0]) + attrL.rangey2[0]
        self.edge = np.array([self._x1,self._x2,self._y1,self._y2]) # [x1,x2,y1,y2]
        temp1 = self._maxX - self._x1 - self._x2
        temp2 = self._maxY - self._y1 - self._y2
        self.rangeOriPointx = [0,temp1]
        self.rangeOriPointy = [0,temp2]
        self.originalPoint[0] = ((x[5]+1)/2)*temp1
        self.originalPoint[1] = ((x[6]+1)/2)*temp2
        if rotate == 1:
            self.polygon, self.X = self._createPolygon1()
        elif rotate == 2:
            self.polygon, self.X = self._createPolygon2()
        elif rotate == 3:
            self.polygon, self.X = self._createPolygon3()
        else:
            temp2 = self._maxY - self._y1
            temp4 = self._y2
            self.rangeOriPointy = [temp4,temp2]
            self.originalPoint[1] = ((x[6]+1)/2)*(self.rangeOriPointy[1] - self.rangeOriPointy[0]) + self.rangeOriPointy[0]
            self.polygon, self.X = self._createPolygon4()

    def change(self,x):
        # This function only use for changing of red terminal.
        # update the polygon after apply gp operation.
        # input x: must be a list of 7 elements.
        dif = compare2lists(self._oldx,x)
        if len(dif) == 0:
            return 
        elif len(dif) == 1:
            self._oldx = x 
            dif = dif[0]
            if dif == 0: # need rotate current polygon.
                rotate = x[0]
                rotate = round(((rotate+1)/2)*10)%4
                self.initchange(x)
            elif (dif == 1) or (dif == 2) or (dif == 3) or (dif == 4): # changing the coordinate.
                self._x1 = ((x[1]+1)/2)*(attrL.rangex1[1] - attrL.rangex1[0]) + attrL.rangex1[0]
                self._x2 = ((x[2]+1)/2)*(attrL.rangex2[1] - attrL.rangex2[0]) + attrL.rangex2[0]
                self._y1 = ((x[3]+1)/2)*(attrL.rangey1[1] - attrL.rangey1[0]) + attrL.rangey1[0]
                self._y2 = ((x[4]+1)/2)*(attrL.rangey2[1] - attrL.rangey2[0]) + attrL.rangey2[0]
                self.edge = np.array([self._x1,self._x2,self._y1,self._y2]) # [x1,x2,y1,y2]
                temp1 = self._maxX - self._x1 - self._x2
                temp2 = self._maxY - self._y1 - self._y2
                self.rangeOriPointx = [0,temp1]
                self.rangeOriPointy = [0,temp2]
                if (self.strname == 'L1') or (self.strname == 'L2') or (self.strname == 'L3'):
                    if (self.originalPoint[0] < (self._maxX - self._x1 - self._x2)) and (self.originalPoint[1] < (self._maxY - self._y1 - self._y2)):
                        if self.strname == 'L1':
                            self.polygon, self.X = self._createPolygon1()
                        elif self.strname == 'L2':
                            self.polygon, self.X = self._createPolygon2()
                        else: # self.strname == 'L3'
                            self.polygon, self.X = self._createPolygon3()
                    else:
                        self.originalPoint[0] = ((x[5]+1)/2)*self.rangeOriPointx[1]
                        self.originalPoint[1] = ((x[6]+1)/2)*self.rangeOriPointy[1]
                        if self.strname == 'L1':
                            self.polygon, self.X = self._createPolygon1()
                        elif self.strname == 'L2':
                            self.polygon, self.X = self._createPolygon2()
                        else:
                            self.polygon, self.X = self._createPolygon3()
                else: # self.strname == 'L4'
                    if (self.originalPoint[0] < (self._maxX - self._x1 - self._x2)) and (self.originalPoint[1] < (self._maxY - self._y1)) and (self.originalPoint[1] > self._y2):
                        self.polygon, self.X = self._createPolygon4()
                    else: 
                        temp2 = self._maxY - self._y1
                        self.rangeOriPointy = [self._y2,temp2]
                        self.originalPoint[1] = ((x[6]+1)/2)*(self.rangeOriPointy[1] - self.rangeOriPointy[0]) + self.rangeOriPointy[0]
                        self.polygon, self.X = self._createPolygon4()
            else: # adjust the coordinate.
                self.originalPoint[0] = ((x[5]+1)/2)*(self.rangeOriPointx[1]- self.rangeOriPointx[0]) + self.rangeOriPointx[0]
                self.originalPoint[1] = ((x[6]+1)/2)*(self.rangeOriPointy[1] - self.rangeOriPointy[0]) + self.rangeOriPointy[0]
                if self.strname == 'L1':
                    self.polygon, self.X = self._createPolygon1()
                elif self.strname == 'L2':
                    self.polygon, self.X = self._createPolygon2()
                elif self.strname == 'L3':
                    self.polygon, self.X = self._createPolygon3()
                else:
                    self.polygon, self.X = self._createPolygon4()
        else:
            raise ValueError('can not vary more than one element in red set node when appling operators.')
    def change_all(self,MaxXY,x):
        # change all attrubites of current class.
        self._oldx = x 
        self._maxX = MaxXY[0]
        self._maxY = MaxXY[1]
        self._x1 = ((x[1]+1)/2)*(attrL.rangex1[1] - attrL.rangex1[0]) + attrL.rangex1[0]
        self._x2 = ((x[2]+1)/2)*(attrL.rangex2[1] - attrL.rangex2[0]) + attrL.rangex2[0]
        self._y1 = ((x[3]+1)/2)*(attrL.rangey1[1] - attrL.rangey1[0]) + attrL.rangey1[0]
        self._y2 = ((x[4]+1)/2)*(attrL.rangey2[1] - attrL.rangey2[0]) + attrL.rangey2[0]
        self.edge = np.array([self._x1,self._x2,self._y1,self._y2]) # [x1,x2,y1,y2]
        temp1 = self._maxX - self._x1 - self._x2
        temp2 = self._maxY - self._y1 - self._y2
        self.rangeOriPointx = [0,temp1]
        self.rangeOriPointy = [0,temp2]
        self.originalPoint[0] = ((x[5]+1)/2)*temp1
        self.originalPoint[1] = ((x[6]+1)/2)*temp2
        if self.strname == 'L1':
            self.polygon, self.X = self._createPolygon1()
        elif self.strname == 'L2':
            self.polygon, self.X = self._createPolygon2()
        elif self.strname == 'L3':
            self.polygon, self.X = self._createPolygon3()
        else:
            temp2 = self._maxY - self._y1
            temp4 = self._y2
            self.originalPoint[1] = ((x[6]+1)/2)*(temp2-temp4) + temp4
            self.polygon, self.X = self._createPolygon4()
        


    def changeMaxXY(self,MaxXY):
        # This function change all of attributes of current class.
        temp = [self._maxX,self._maxY]
        if not temp == MaxXY:
            self._maxX = MaxXY[0]
            self._maxY = MaxXY[1]
            temp1 = self._maxX - self._x1 - self._x2
            temp2 = self._maxY - self._y1 - self._y2
            self.rangeOriPointx = [0,temp1]
            self.rangeOriPointy = [0,temp2]
            self.originalPoint[0] = ((self._oldx[5]+1)/2)*self.rangeOriPointx[1]
            self.originalPoint[1] = ((self._oldx[6]+1)/2)*self.rangeOriPointy[1]
            if self.strname == 'L1':
                self.polygon, self.X = self._createPolygon1()
            elif self.strname == 'L2':
                self.polygon, self.X = self._createPolygon2()
            elif self.strname == 'L3':
                self.polygon, self.X = self._createPolygon3()
            else:
                temp2 = self._maxY - self._y1
                self.rangeOriPointy = [self._y2,temp2]
                self.originalPoint[1] = ((self._oldx[6]+1)/2)*(self.rangeOriPointy[1] - self.rangeOriPointy[0]) + self.rangeOriPointy[0]
                self.polygon, self.X = self._createPolygon4()


    def Rotate(self,degree):
        # This function rotates a polygon.
        # Degree: 1 --- 90 degree.
        #         2 --- 180 degree.
        #         3 --- 270 degree.
        #         4 --- 0 degree.
        if not ((degree == 1) or (degree == 2) or (degree == 3) or (degree == 0)):
            raise ValueError('degree need be 1 or 2 or 3 or 0')
        x1 = self._x1
        x2 = self._x2
        y1 = self._y1
        y2 = self._y2
        if self.strname == 'L1':
            if ((self._x1 + self._x2) < self._maxY) and ((self._y1 + self._y2) < self._maxX): # check whether the polygon can be rotated.
                if degree == 1: # 90 degree.
                    self._y2 = x1
                    self._x2 = y1
                    self._y1 = x2
                    self._x1 = y2
                    self.edge = np.array([self._x1,self._x2,self._y1,self._y2]) # [x1,x2,y1,y2]
                    if ((self.originalPoint[0] + self._x1 + self._x2) <= self._maxX) and ((self.originalPoint[1] + self._y1 + self._y2) <= self._maxY):
                        # If originalPoint is not suitable. It need be recreated.
                        # In this case, it is not need be recreated.
                        self.polygon, self.X = self._createPolygon3()
                        self.type_of_tree = 3
                    else:
                        self.originalPoint = self._createOriginalPoint()
                        self.polygon, self.X = self._createPolygon3()
                        self.type_of_tree = 3
                elif degree == 2: # 180 degree.
                    self._y1 = y2
                    self._x1 = x2
                    self._y2 = y1
                    self._x2 = x1
                    self.edge = np.array([self._x1,self._x2,self._y1,self._y2]) # [x1,x2,y1,y2]
                    if ((self.originalPoint[0] + self._x1 + self._x2) <= self._maxX) and (self.originalPoint[1] >= self._y2) and (self.originalPoint[1]<=(self._maxY-self._y1)):
                        self.polygon, self.X = self._createPolygon4()
                        self.type_of_tree = 4
                    else:
                        #print('fsadfsafasf')
                        self.originalPoint = self._createOriginalPoint()
                        self.polygon, self.X = self._createPolygon4()
                        self.type_of_tree = 4
                elif degree == 3: # 270 degree.
                    self._y2 = x1
                    self._x2 = y1
                    self._y1 = x2
                    self._x1 = y2
                    self.edge = np.array([self._x1,self._x2,self._y1,self._y2]) # [x1,x2,y1,y2]
                    if ((self.originalPoint[0] + self._x1 + self._x2) <= self._maxX) and ((self.originalPoint[1] + self._y1 + self._y2) <= self._maxY):
                        self.polygon, self.X = self._createPolygon2()
                        self.type_of_tree = 2
                    else:
                        self.originalPoint = self._createOriginalPoint()
                        self.polygon, self.X = self._createPolygon2()
                        self.type_of_tree = 2
                else:
                    pass
        elif self.strname == 'L2':
            if ((self._x1 + self._x2) < self._maxY) and ((self._y1 + self._y2) < self._maxX): # check whether the polygon can be rotated.
                if degree == 1: # 90 degree.
                    self._x1 = y2
                    self._y1 = x2
                    self._x2 = y1
                    self._y2 = x1
                    self.edge = np.array([self._x1,self._x2,self._y1,self._y2]) # [x1,x2,y1,y2]
                    if ((self.originalPoint[0] + self._x1 + self._x2) <= self._maxX) and ((self.originalPoint[1] + self._y1 + self._y2) <= self._maxY):
                        self.polygon, self.X = self._createPolygon1()
                        self.type_of_tree = 1
                    else:
                        self.originalPoint = self._createOriginalPoint()
                        self.polygon, self.X = self._createPolygon1()
                        self.type_of_tree = 1
                elif degree == 2: # 180 degree.
                    if ((self.originalPoint[0] + self._x1 + self._x2) <= self._maxX) and ((self.originalPoint[1] + self._y1 + self._y2) <= self._maxY):
                        self.polygon, self.X = self._createPolygon3()
                        self.type_of_tree = 3
                    else:
                        self.originalPoint = self._createOriginalPoint()
                        self.polygon, self.X = self._createPolygon3()
                        self.type_of_tree = 3
                elif degree == 3:
                    self._y1 = x1
                    self._x1 = y1
                    self._y2 = x2
                    self._x2 = y2
                    self.edge = np.array([self._x1,self._x2,self._y1,self._y2]) # [x1,x2,y1,y2]
                    if ((self.originalPoint[0] + self._x1 + self._x2) <= self._maxX):
                        self.polygon, self.X = self._createPolygon4()
                        self.type_of_tree = 4
                    else:
                        self.originalPoint = self._createOriginalPoint()
                        self.polygon, self.X = self._createPolygon4()
                        self.type_of_tree = 4
                else:
                    pass 
        elif self.strname == 'L3':
            if ((self._x1 + self._x2) < self._maxY) and ((self._y1 + self._y2) < self._maxX): # check whether the polygon can be rotated.
                if degree == 1: # 90 degree.
                    self._y1 = x1
                    self._x1 = y1
                    self._y2 = x2
                    self._x2 = y2
                    self.edge = np.array([self._x1,self._x2,self._y1,self._y2]) # [x1,x2,y1,y2]
                    if ((self.originalPoint[0] + self._x1 + self._x2) <= self._maxX):
                        # If originalPoint is not suitable. It need be recreated.
                        # In this case, it is not need be recreated.
                        self.polygon, self.X = self._createPolygon4()
                        self.type_of_tree = 4
                    else:
                        self.originalPoint = self._createOriginalPoint()
                        self.polygon, self.X = self._createPolygon4()
                        self.type_of_tree = 4
                elif degree == 2: # 180 degree.
                    self._y2 = y2
                    self._x2 = x2
                    self._y1 = y1
                    self._x1 = x1
                    self.edge = np.array([self._x1,self._x2,self._y1,self._y2]) # [x1,x2,y1,y2]
                    if ((self.originalPoint[0] + self._x1 + self._x2) <= self._maxX) and ((self.originalPoint[1] + self._y1 + self._y2) <= self._maxY):
                        self.polygon, self.X = self._createPolygon2()
                        self.type_of_tree = 2
                    else:
                        #print('fsadfsafasf')
                        self.originalPoint = self._createOriginalPoint()
                        self.polygon, self.X = self._createPolygon2()
                        self.type_of_tree = 2
                elif degree  == 3: # 270 degree.
                    self._x1 = y2
                    self._y1 = x2
                    self._x2 = y1
                    self._y2 = x1
                    self.edge = np.array([self._x1,self._x2,self._y1,self._y2]) # [x1,x2,y1,y2]
                    if ((self.originalPoint[0] + self._x1 + self._x2) <= self._maxX) and ((self.originalPoint[1] + self._y1 + self._y2) <= self._maxY):
                        self.polygon, self.X = self._createPolygon1()
                        self.type_of_tree = 1
                    else:
                        self.originalPoint = self._createOriginalPoint()
                        self.polygon, self.X = self._createPolygon1()
                        self.type_of_tree = 1
                else: 
                    pass

        else: # L4 type.
            if ((self._x1 + self._x2) < self._maxY) and ((self._y1 + self._y2) < self._maxX): # check whether the polygon can be rotated.
                if degree == 1: # 90 degree.
                    self._x1 = y1
                    self._x2 = y2
                    self._y1 = x1
                    self._y2 = x2
                    self.edge = np.array([self._x1,self._x2,self._y1,self._y2]) # [x1,x2,y1,y2]
                    if ((self.originalPoint[0] + self._x1 + self._x2) <= self._maxX) and ((self.originalPoint[1] + self._y1 + self._y2) <= self._maxY):
                        self.polygon, self.X = self._createPolygon2()
                        self.type_of_tree = 2
                    else:
                        self.originalPoint = self._createOriginalPoint()
                        self.polygon, self.X = self._createPolygon2()
                        self.type_of_tree = 2
                elif degree == 2: # 180 degree.
                    self._x1 = x2
                    self._y1 = y2
                    self._x2 = x1
                    self._y2 = y1
                    self.edge = np.array([self._x1,self._x2,self._y1,self._y2]) # [x1,x2,y1,y2]
                    if ((self.originalPoint[0] + self._x1 + self._x2) <= self._maxX) and ((self.originalPoint[1] + self._y1 + self._y2) <= self._maxY):
                        self.polygon, self.X = self._createPolygon1()
                        self.type_of_tree = 1
                    else:
                        self.originalPoint = self._createOriginalPoint()
                        self.polygon, self.X = self._createPolygon1()
                        self.type_of_tree = 1
                elif degree == 3: # 270 degree
                    self._x1 = y1
                    self._y1 = x1
                    self._x2 = y2
                    self._y2 = x2
                    self.edge = np.array([self._x1,self._x2,self._y1,self._y2]) # [x1,x2,y1,y2]
                    if ((self.originalPoint[0] + self._x1 + self._x2) <= self._maxX) and ((self.originalPoint[1] + self._y1 + self._y2) <= self._maxY):
                        self.polygon, self.X = self._createPolygon3()
                        self.type_of_tree = 3
                    else:
                        self.originalPoint = self._createOriginalPoint()
                        self.polygon, self.X = self._createPolygon3()
                        self.type_of_tree = 3
                else: 
                    pass

    def increase(self):  
        # This function to increase randomly the size of current polygon.
        self._x1 = random.uniform(self._x1,self._maxX/2) 
        self._x2 = random.uniform(self._x2,self._maxX - self._x1)
        self._y1 = random.uniform(self._y1,self._maxY/2)
        self._y2 = random.uniform(self._y2,self._maxY - self._y1)
        self.originalPoint = self._createOriginalPoint()
        if self.strname == 'L1':
            self.polygon, self.X = self._createPolygon1()
        elif self.strname == 'L2':
            self.polygon, self.X = self._createPolygon2()
        elif self.strname == 'L3':
            self.polygon, self.X = self._createPolygon3()
        else:
            self.polygon, self.X = self._createPolygon4()

        self.edge = np.array([self._x1,self._x2,self._y1,self._y2]) # [x1,x2,y1,y2]
    def decrease(self):
        # This function to decrease randomly the size of current polygon.
        self._x1 = random.uniform(0,self._x1) 
        self._x2 = random.uniform(0,self._x2)
        self._y1 = random.uniform(0,self._y1)
        self._y2 = random.uniform(0,self._y2)
        #self.originalPoint = self._createOriginalPoint()
        if self.strname == 'L1':
            self.polygon, self.X = self._createPolygon1()
        elif self.strname == 'L2':
            self.polygon, self.X = self._createPolygon2()
        elif self.strname == 'L3':
            self.polygon, self.X = self._createPolygon3()
        else:
            self.polygon, self.X = self._createPolygon4()

        self.edge = np.array([self._x1,self._x2,self._y1,self._y2]) # [x1,x2,y1,y2]

    
    def _createOriginalPoint(self):
        if self.type_of_tree == 4:
            x = random.uniform(0,self._maxX - self._x1 - self._x2)
            y = random.uniform(self._y2,self._maxY - self._y1)
            originalPoint = np.array([x,y])
        else:
            x = random.uniform(0,self._maxX - self._x1 - self._x2)
            y = random.uniform(0,self._maxY - self._y1 - self._y2)
            originalPoint = [x,y]
        return originalPoint
    
    def _createPolygon1(self):
        self.strname = 'L1'
        x1 = self.originalPoint
        X = np.zeros((6,2)) # all coordinate of L polygon.
        X[0] = x1
        X[1][0] = X[0][0] + self._x1 + self._x2
        X[1][1] = X[0][1]
        X[2][0] = X[1][0]
        X[2][1] = X[1][1] + self._y2
        X[3][0] = X[2][0] - self._x2
        X[3][1] = X[2][1]
        X[4][0] = X[3][0]
        X[4][1] = X[3][1] + self._y1
        X[5][0] = X[4][0] - self._x1
        X[5][1] = X[4][1]
        polys = gpd.GeoSeries(Polygon(X))
        df = gpd.GeoDataFrame({'geometry': polys})
        return df,X
    def _createPolygon2(self):
        self.strname = 'L2'
        x1 = self.originalPoint
        X = np.zeros((6,2)) # all coordinate of L polygon.
        X[0] = x1
        X[1][0] = X[0][0] + self._x1 + self._x2
        X[1][1] = X[0][1]
        X[2][0] = X[1][0]
        X[2][1] = X[1][1] + self._y2 + self._y1
        X[3][0] = X[2][0] - self._x1
        X[3][1] = X[2][1]
        X[4][0] = X[3][0]
        X[4][1] = X[3][1] - self._y1
        X[5][0] = X[4][0] - self._x2
        X[5][1] = X[4][1]
        polys = gpd.GeoSeries(Polygon(X))
        df = gpd.GeoDataFrame({'geometry': polys})
        return df,X
    def _createPolygon3(self):
        x1 = self.originalPoint
        self.strname = 'L3'
        X = np.zeros((6,2)) # all coordinate of L polygon.
        X[0] = x1
        X[1][0] = X[0][0] + self._x1
        X[1][1] = X[0][1]
        X[2][0] = X[1][0]
        X[2][1] = X[1][1] + self._y1
        X[3][0] = X[2][0] + self._x2
        X[3][1] = X[2][1]
        X[4][0] = X[3][0]
        X[4][1] = X[3][1] + self._y2
        X[5][0] = X[4][0] - self._x2 - self._x1
        X[5][1] = X[4][1]
        polys = gpd.GeoSeries(Polygon(X))
        df = gpd.GeoDataFrame({'geometry': polys})
        return df,X
    def _createPolygon4(self):
        x1 = self.originalPoint
        self.strname = 'L4'
        X = np.zeros((6,2)) # all coordinate of L polygon.
        X[0] = x1
        X[1][0] = X[0][0] + self._x1
        X[1][1] = X[0][1]
        X[2][0] = X[1][0]
        X[2][1] = X[1][1] - self._y2
        X[3][0] = X[2][0] + self._x2
        X[3][1] = X[2][1]
        X[4][0] = X[3][0]
        X[4][1] = X[3][1] + self._y2 + self._y1
        X[5][0] = X[4][0] - self._x2 - self._x1
        X[5][1] = X[4][1]
        polys = gpd.GeoSeries(Polygon(X))
        df = gpd.GeoDataFrame({'geometry': polys})
        return df,X

####
        ## Create the I terminal.
#class Isub_tree:
#    def __init__(self,maxX,maxY,type_of_tree):

####
        ## Create the U terminal. 
class Usub_tree:
    # the U tree has 4 types of tree.
    def __init__(self,maxX,maxY,type_of_tree=1):
        self._maxX = maxX
        self._maxY = maxY
        self.type_of_tree = type_of_tree
        if self.type_of_tree == 1 or self.type_of_tree == 2:
            
            self._x1 = random.uniform(0,(self._maxX)/3)
            self._x2 = random.uniform(0,(self._maxX)/3)
            self._x3 = random.uniform(0,(self._maxX)/3)
            self._y2 = random.uniform(0,(self._maxY)/2)
            self._y1 = random.uniform(self._y2,self._maxY)
            self._y3 = random.uniform(self._y2,self._maxY)
            self.originalPoint = self._createOriginalPoint()
            if self.type_of_tree == 1:
                self.polygon, self.X = self._createPolygon1()
            else:
                self.polygon, self.X = self._createPolygon2()
        else:
            
            self._y1 = random.uniform(0,(self._maxY)/3)
            self._y2 = random.uniform(0,(self._maxY)/3)
            self._y3 = random.uniform(0,(self._maxY)/3)
            self._x2 = random.uniform(0,(self._maxX)/2)
            self._x1 = random.uniform(self._x2,self._maxX)
            self._x3 = random.uniform(self._x2,self._maxX)
            self.originalPoint = self._createOriginalPoint()
            if self.type_of_tree == 3:
                self.polygon, self.X = self._createPolygon3()
            else:
                self.polygon, self.X = self._createPolygon4()
        self.edge = np.array([self._x1,self._x2,self._x3,self._y1,self._y2,self._y3]) # [x1,x2,x3,y1,y2,y3]

    def resestMaxXY(self,maxX,maxY):
        self._maxX = maxX
        self._maxY = maxY

    def initchange(self,x):
        # updatte the polygon after init.
        # input x: must be a list of 9 elements.
        self._oldx = x 
        rotate = x[0]
        rotate = round(((rotate+1)/2)*10)%4
        self._x1 = ((x[1]+1)/2)*(attrU.rangex1[1] - attrU.rangex1[0]) + attrU.rangex1[0]
        self._x2 = ((x[2]+1)/2)*(attrU.rangex2[1] - attrU.rangex2[0]) + attrU.rangex2[0]
        self._x3 = ((x[3]+1)/2)*(attrU.rangex3[1] - attrU.rangex3[0]) + attrU.rangex3[0]
        self._y2 = ((x[5]+1)/2)*(attrU.rangey2[1] - attrU.rangey2[0]) + attrU.rangey2[0]
        self._y1 = ((x[4]+1)/2)*(attrU.rangey1[1] - self._y2) + self._y2
        self._y3 = ((x[6]+1)/2)*(attrU.rangey3[1] - self._y2) + self._y2
        self.edge = np.array([self._x1,self._x2,self._x3,self._y1,self._y2,self._y3]) # [x1,x2,x3,y1,y2,y3]
        if (rotate == 0) or (rotate == 1):
            temp1 = self._maxX - self._x1 - self._x2 - self._x3
            temp2 = self._maxY - max(self._y1,self._y3)
            self.rangeOriPointx = [0,temp1]
            self.originalPoint[0] = ((x[7]+1)/2)*(self.rangeOriPointx[1] - self.rangeOriPointx[0]) + self.rangeOriPointx[0]
            if rotate == 0:
                self.rangeOriPointy = [0,temp2]
                self.originalPoint[1] = ((x[8]+1)/2)*(self.rangeOriPointy[1]- self.rangeOriPointy[0]) + self.rangeOriPointy[0]
                self.polygon, self.X = self._createPolygon1()
            else:
                temp3 = abs(self._y1 - self._y3)
                self.rangeOriPointy = [temp3,temp2]
                self.originalPoint[1] = ((x[8]+1)/2)*(self.rangeOriPointy[1]- self.rangeOriPointy[0]) + self.rangeOriPointy[0]
                self.polygon, self.X = self._createPolygon2()
        else: # rotate == 2 or == 3.
            x1 = self._x1
            x2 = self._x2
            x3 = self._x3
            self._x1 = self._y1
            self._x2 = self._y2 
            self._x3 = self._y3
            self._y1 = x1
            self._y2 = x2 
            self._y3 = x3
            self.edge = np.array([self._x1,self._x2,self._x3,self._y1,self._y2,self._y3])
            temp2 = self._maxY - self._y1 - self._y2 - self._y3
            temp1 = self._maxX - max(self._x3,self._x1)
            self.rangeOriPointy = [0,temp2]
            self.originalPoint[1] = ((x[8]+1)/2)*(self.rangeOriPointy[1]- self.rangeOriPointy[0]) + self.rangeOriPointy[0]
            if rotate == 3:
                self.rangeOriPointx = [0,temp1]
                self.originalPoint[0] = ((x[7]+1)/2)*(self.rangeOriPointx[1] - self.rangeOriPointx[0]) + self.rangeOriPointx[0]
                self.polygon, self.X = self._createPolygon4()
            else:
                temp3 = abs(self._x1 - self._x3)
                self.rangeOriPointx = [temp3,temp1]
                self.originalPoint[0] = ((x[7]+1)/2)*(self.rangeOriPointx[1] - self.rangeOriPointx[0]) + self.rangeOriPointx[0]
                self.polygon, self.X = self._createPolygon3()
    def change(self,x):
        # This function only use for changing of red terminal.
        # update the polygon after apply gp operation.
        # input x: must be a list of 9 elements.
        dif = compare2lists(self._oldx,x)
        if len(dif) == 0:
            return 
        elif len(dif) == 1:
            self._oldx = x 
            dif = dif[0]
            if dif == 0: # need rotate current polygon.
                rotate = x[0]
                rotate = round(((rotate+1)/2)*10)%4
                self.initchange(x)
            elif (dif == 1) or (dif == 2) or (dif == 3) or (dif == 4) or (dif == 5) or (dif == 6):
                if (self.strname == 'U1') or (self.strname == 'U2'):
                    self._x1 = ((x[1]+1)/2)*(attrU.rangex1[1] - attrU.rangex1[0]) + attrU.rangex1[0]
                    self._x2 = ((x[2]+1)/2)*(attrU.rangex2[1] - attrU.rangex2[0]) + attrU.rangex2[0]
                    self._x3 = ((x[3]+1)/2)*(attrU.rangex3[1] - attrU.rangex3[0]) + attrU.rangex3[0]
                    self._y2 = ((x[5]+1)/2)*(attrU.rangey2[1] - attrU.rangey2[0]) + attrU.rangey2[0]
                    self._y1 = ((x[4]+1)/2)*(attrU.rangey1[1] - self._y2) + self._y2
                    self._y3 = ((x[6]+1)/2)*(attrU.rangey3[1] - self._y2) + self._y2
                    self.edge = np.array([self._x1,self._x2,self._x3,self._y1,self._y2,self._y3]) # [x1,x2,x3,y1,y2,y3]
                    temp1 = self._maxX - self._x1 - self._x2 - self._x3
                    temp2 = self._maxY - max(self._y1,self._y3)
                    self.rangeOriPointx = [0,temp1]
                    if self.strname == 'U1':
                        self.rangeOriPointy = [0,temp2]
                        if (self.originalPoint[0] < self.rangeOriPointx[1]) and (self.originalPoint[1] < self.rangeOriPointy[1]) and (self.originalPoint[1] > self.rangeOriPointy[0]):
                            self.polygon, self.X = self._createPolygon1()
                        else: # need reset up the original points.
                            self.originalPoint[0] = ((x[7]+1)/2)*(self.rangeOriPointx[1] - self.rangeOriPointx[0]) + self.rangeOriPointx[0]
                            self.originalPoint[1] = ((x[8]+1)/2)*(self.rangeOriPointy[1] - self.rangeOriPointy[0]) + self.rangeOriPointy[0]
                            self.polygon, self.X = self._createPolygon1()
                    else: # self.strname == 'U2'
                        temp3 = abs(self._y1 - self._y3)
                        self.rangeOriPointy = [temp3,temp2]
                        if ((self.originalPoint[0] < self.rangeOriPointx[1]) and (self.originalPoint[1] < self.rangeOriPointy[1]) and (self.originalPoint[0] > self.rangeOriPointy[0])):
                            self.polygon, self.X = self._createPolygon2()
                        else:
                            self.originalPoint[0] = ((x[7]+1)/2)*(self.rangeOriPointx[1] - self.rangeOriPointx[0]) + self.rangeOriPointx[0]
                            self.originalPoint[1] = ((x[8]+1)/2)*(self.rangeOriPointy[1] - self.rangeOriPointy[0]) + self.rangeOriPointy[0]
                            self.polygon, self.X = self._createPolygon2()
                else: # U3 or U4 type.
                    self._y1 = ((x[1]+1)/2)*(attrU.rangex1[1] - attrU.rangex1[0]) + attrU.rangex1[0]
                    self._y2 = ((x[2]+1)/2)*(attrU.rangex2[1] - attrU.rangex2[0]) + attrU.rangex2[0]
                    self._y3 = ((x[3]+1)/2)*(attrU.rangex3[1] - attrU.rangex3[0]) + attrU.rangex3[0]
                    self._x2 = ((x[5]+1)/2)*(attrU.rangey2[1] - attrU.rangey2[0]) + attrU.rangey2[0]
                    self._x1 = ((x[4]+1)/2)*(attrU.rangey1[1] - self._x2) + self._x2
                    self._x3 = ((x[6]+1)/2)*(attrU.rangey3[1] - self._x2) + self._x2
                    self.edge = np.array([self._x1,self._x2,self._x3,self._y1,self._y2,self._y3]) # [x1,x2,x3,y1,y2,y3]
                    temp2 = self._maxY - self._y1 - self._y2 - self._y3
                    temp1 = self._maxX - max(self._x3,self._x1)
                    self.rangeOriPointy = [0,temp2]
                    self.originalPoint[1] = ((x[8]+1)/2)*(self.rangeOriPointy[1]- self.rangeOriPointy[0]) + self.rangeOriPointy[0]
                    if self.strname == 'U4':
                        self.rangeOriPointx = [0,temp1]
                        if (self.originalPoint[0] < self.rangeOriPointx[1]) and (self.originalPoint[1] < self.rangeOriPointy[1]) and (self.originalPoint[0] > self.rangeOriPointx[0]):
                            self.polygon, self.X = self._createPolygon4()
                        else: # need reset up the original point of the polygon.
                            self.originalPoint[0] = ((x[7]+1)/2)*(self.rangeOriPointx[1] - self.rangeOriPointx[0]) + self.rangeOriPointx[0]
                            self.originalPoint[1] = ((x[8]+1)/2)*(self.rangeOriPointy[1] - self.rangeOriPointy[0]) + self.rangeOriPointy[0]
                            self.polygon, self.X = self._createPolygon4()
                    else:# 'U3' type
                        temp3 = abs(self._x1 - self._x3)
                        self.rangeOriPointx = [temp3,temp1]
                        if (self.originalPoint[0] < self.rangeOriPointx[1]) and (self.originalPoint[1] < self.rangeOriPointy[1]) and (self.originalPoint[0] > self.rangeOriPointx[0]):
                            self.polygon, self.X = self._createPolygon3()
                        else:
                            self.originalPoint[0] = ((x[7]+1)/2)*(self.rangeOriPointx[1] - self.rangeOriPointx[0]) + self.rangeOriPointx[0]
                            self.originalPoint[1] = ((x[8]+1)/2)*(self.rangeOriPointy[1] - self.rangeOriPointy[0]) + self.rangeOriPointy[0]
                            self.polygon, self.X = self._createPolygon3()
            else:
                self.originalPoint[0] = ((x[7]+1)/2)*(self.rangeOriPointx[1] - self.rangeOriPointx[0]) + self.rangeOriPointx[0]
                self.originalPoint[1] = ((x[8]+1)/2)*(self.rangeOriPointy[1] - self.rangeOriPointy[0]) + self.rangeOriPointy[0]
                if self.strname == 'U1':
                    self.polygon, self.X = self._createPolygon1()
                elif self.strname == 'U2':
                    self.polygon, self.X = self._createPolygon2()
                elif self.strname == 'U3':
                    self.polygon, self.X = self._createPolygon3()
                else:
                    self.polygon, self.X = self._createPolygon4()
        else:
            raise ValueError('can not vary more than one element in red set node when appling operators.')

    def changeMaxXY(self,MaxXY):
        # change the maxX, maxY.
        temp = [self._maxX,self._maxY]
        if not temp == MaxXY:
            self._maxX = MaxXY[0]
            self._maxY = MaxXY[1]
            if self.strname == 'U1' or self.strname == 'U2':
                temp1 = self._maxX - self._x1 - self._x2 - self._x3
                temp2 = self._maxY - max(self._y1,self._y3)
                self.rangeOriPointx = [0,temp1]
                self.rangeOriPointy = [0,temp2]
                if self.strname == 'U1':
                    self.originalPoint[0] = ((self._oldx[7]+1)/2)*(self.rangeOriPointx[1] - self.rangeOriPointx[0]) + self.rangeOriPointx[0]
                    self.originalPoint[1] = ((self._oldx[8]+1)/2)*(self.rangeOriPointy[1] - self.rangeOriPointy[0]) + self.rangeOriPointy[0]
                    self.polygon, self.X = self._createPolygon1()
                else: # self.strname == 'U2'
                    self.rangeOriPointy = [abs(self._y1 - self._y3),temp2]
                    self.originalPoint[0] = ((self._oldx[7]+1)/2)*(self.rangeOriPointx[1] - self.rangeOriPointx[0]) + self.rangeOriPointx[0]
                    self.originalPoint[1] = ((self._oldx[8]+1)/2)*(self.rangeOriPointy[1] - self.rangeOriPointy[0]) + self.rangeOriPointy[0]
                    self.polygon, self.X = self._createPolygon2()
            else: # strname == 'U3' or 'U4'
                temp1 = self._maxY - self._y1 - self._y2 - self._y3
                temp2 = self._maxX - max(self._x1,self._x3)
                self.rangeOriPointx = [0,temp2]
                self.rangeOriPointy = [0,temp1]
                if self.strname == 'U4':
                    self.originalPoint[0] = ((self._oldx[7]+1)/2)*(self.rangeOriPointx[1] - self.rangeOriPointx[0]) + self.rangeOriPointx[0]
                    self.originalPoint[1] = ((self._oldx[8]+1)/2)*(self.rangeOriPointy[1] - self.rangeOriPointy[0]) + self.rangeOriPointy[0]
                    self.polygon, self.X = self._createPolygon4()
                else:
                    self.rangeOriPointx = [abs(self._x1 - self._x3),temp2]
                    self.originalPoint[0] = ((self._oldx[7]+1)/2)*(self.rangeOriPointx[1] - self.rangeOriPointx[0]) + self.rangeOriPointx[0]
                    self.originalPoint[1] = ((self._oldx[8]+1)/2)*(self.rangeOriPointy[1] - self.rangeOriPointy[0]) + self.rangeOriPointy[0]
                    self.polygon, self.X = self._createPolygon3()
    def change_all(self,MaxXY,x):
        # change all atributes of current class. (some other attributes are not changed)
        self._maxX = MaxXY[0]
        self._maxY = MaxXY[1]
        self._oldx = x 
        # rotate = x[0]
        # rotate = round(((rotate+1)/2)*10)%4
        self._x1 = ((x[1]+1)/2)*(attrU.rangex1[1] - attrU.rangex1[0]) + attrU.rangex1[0]
        self._x2 = ((x[2]+1)/2)*(attrU.rangex2[1] - attrU.rangex2[0]) + attrU.rangex2[0]
        self._x3 = ((x[3]+1)/2)*(attrU.rangex3[1] - attrU.rangex3[0]) + attrU.rangex3[0]
        self._y2 = ((x[5]+1)/2)*(attrU.rangey2[1] - attrU.rangey2[0]) + attrU.rangey2[0]
        self._y1 = ((x[4]+1)/2)*(attrU.rangey1[1] - self._y2) + self._y2
        self._y3 = ((x[6]+1)/2)*(attrU.rangey3[1] - self._y2) + self._y2
        self.edge = np.array([self._x1,self._x2,self._x3,self._y1,self._y2,self._y3]) # [x1,x2,x3,y1,y2,y3]

        if self.strname == 'U1':
            self.rangeOriPointx = [0,self._maxX - self._x1 - self._x2 - self._x3]
            self.rangeOriPointy = [0,self._maxY - max(self._y1,self._y3)]
            self.originalPoint[0] = ((x[7]+1)/2)*self.rangeOriPointx[1]
            self.originalPoint[1] = ((x[8]+1)/2)*self.rangeOriPointy[1]
            self.polygon, self.X = self._createPolygon1()
        elif self.strname == 'U2':
            self.rangeOriPointx = [0,self._maxX - self._x1 - self._x2 - self._x3]
            self.rangeOriPointy = [abs(self._y1 - self._y3), self._maxY - max(self._y1,self._y3)]
            self.originalPoint[0] = ((x[7]+1)/2)*self.rangeOriPointx[1] + self.rangeOriPointx[0]
            self.originalPoint[1] = ((x[8]+1)/2)*self.rangeOriPointy[1] + self.rangeOriPointy[0]
            self.polygon, self.X = self._createPolygon2()
        elif self.strname == 'U3':
            self.rangeOriPointx = [abs(self._x1-self._x3),self._maxX - max(self._x3,self._x1)]
            self.rangeOriPointy = [0,self._maxY - self._y1 - self._y2 - self._y3]
            self.originalPoint[0] = ((x[7]+1)/2)*self.rangeOriPointx[1] + self.rangeOriPointx[0]
            self.originalPoint[1] = ((x[8]+1)/2)*self.rangeOriPointy[1] + self.rangeOriPointy[0]
            self.polygon, self.X = self._createPolygon3()
        else:
            self.rangeOriPointx = [0,self._maxX - max(self._x1,self._x3)]
            self.rangeOriPointy = [0,self._maxY - self._y1 - self._y2 - self._y3]
            self.originalPoint[0] = ((x[7]+1)/2)*self.rangeOriPointx[1] + self.rangeOriPointx[0]
            self.originalPoint[1] = ((x[8]+1)/2)*self.rangeOriPointy[1] + self.rangeOriPointy[0]
            self.polygon, self.X = self._createPolygon4()


    def Rotate(self,degree):
        # This function rotates a polygon.
        # Degree: 1 --- 90 degree.
        #         2 --- 180 degree.
        #         3 --- 270 degree.
        #         4 --- 0 degree.
        if not ((degree == 1) or (degree == 2) or (degree == 3) or (degree == 0)):
            raise ValueError('degree need be 1 or 2 or 3 or 0')
        x1 = self._x1
        x2 = self._x2
        x3 = self._x3
        y1 = self._y1
        y2 = self._y2
        y3 = self._y3
        if self.strname == 'U1':
            if degree == 1 or degree == 3:
                if ((self._x1 + self._x2 + self._x3) < self._maxY) and (max(self._y1,self._y2,self._y3) < self._maxX): # check whether polygon can be rotated.
                    if degree == 1:  # 90 degree.
                        self._y1 = x1
                        self._y2 = x2
                        self._y3 = x3
                        self._x1 = y1
                        self._x2 = y2
                        self._x3 = y3
                        self.edge = np.array([self._x1,self._x2,self._x3,self._y1,self._y2,self._y3]) # [x1,x2,x3,y1,y2,y3]
                        if ((self.originalPoint[0] + max(self._x1, self._x2,self._x3)) <= self._maxX) and ((self.originalPoint[1] + self._y1 + self._y2 + self._y3) <= self._maxY):
                            # check whether OrinalPoint is valid after rotated.
                            self.polygon, self.X = self._createPolygon4()
                            self.type_of_tree = 4
                        else:
                            self.type_of_tree = 4
                            self.originalPoint = self._createOriginalPoint()
                            self.polygon, self.X = self._createPolygon4()
                    else: # degree == 3, 270 degree.
                        self._x1 = y3
                        self._x2 = y2
                        self._x3 = y1
                        self._y1 = x3
                        self._y2 = x2
                        self._y3 = x1
                        self.edge = np.array([self._x1,self._x2,self._x3,self._y1,self._y2,self._y3]) # [x1,x2,x3,y1,y2,y3]
                        if ((self.originalPoint[1] + self._y1+ self._y2 + self._y3) <= self._maxY):
                            if ((self._x3 >= self._x1) and ((self.originalPoint[0] + self._x3) <= self._maxX)) or ((self.originalPoint[0]>=(self._x1 - self._x3)) and ((self.originalPoint[0] + self._x1)<=self._maxX)):
                                # check whether OrinalPoint is valid after rotated.
                                self.polygon, self.X = self._createPolygon3()
                                self.type_of_tree = 3
                            else:
                                self.type_of_tree = 3
                                self.originalPoint = self._createOriginalPoint()
                                self.polygon, self.X = self._createPolygon3()
            elif degree == 2:
                # degree = 2, 180 degree.
                self._x1 = x3
                self._x2 = x2
                self._x3 = x1
                self._y1 = y3
                self._y2 = y2
                self._y3 = y1
                self.edge = np.array([self._x1,self._x2,self._x3,self._y1,self._y2,self._y3]) # [x1,x2,x3,y1,y2,y3]
                if ((self.originalPoint[0] + self._x1 + self._x2 + self._x3) <= self._maxX):
                    if ((self._y1 >= self._y3) and ((self.originalPoint[1] + self._y1) <= self._maxY)) or ((self.originalPoint[1]>=(self._y3 - self._y1)) and ((self.originalPoint[0] + self._y3)<=self._maxY)):
                        self.polygon, self.X = self._createPolygon2()
                        self.type_of_tree = 2
                    else:
                        self.type_of_tree = 2
                        self.originalPoint = self._createOriginalPoint()
                        self.polygon, self.X = self._createPolygon2()
            else:
                pass
        elif self.strname == 'U2':
            if degree == 1 or degree == 3:
                if ((self._x1 + self._x2 + self._x3) < self._maxY) and (max(self._y1,self._y2,self._y3) < self._maxX): # check whether polygon can be rotated.
                    if degree == 1:  # 90 degree.
                        self._y1 = x1
                        self._y2 = x2
                        self._y3 = x3
                        self._x1 = y1
                        self._x2 = y2
                        self._x3 = y3
                        self.edge = np.array([self._x1,self._x2,self._x3,self._y1,self._y2,self._y3]) # [x1,x2,x3,y1,y2,y3]
                        if ((self.originalPoint[1] + self._y1+ self._y2 + self._y3) <= self._maxY):
                            if ((self._x3 >= self._x1) and ((self.originalPoint[0] + self._x3) <= self._maxX)) or ((self.originalPoint[0]>=(self._x1 - self._x3)) and ((self.originalPoint[0] + self._x1)<=self._maxX)):
                                # check whether OrinalPoint is valid after rotated.
                                self.polygon, self.X = self._createPolygon3()
                                self.type_of_tree = 3
                            else:
                                self.type_of_tree = 3
                                self.originalPoint = self._createOriginalPoint()
                                self.polygon, self.X = self._createPolygon3()
                    else: # degree == 3, 270 degree.
                        self._x1 = y3
                        self._x2 = y2
                        self._x3 = y1
                        self._y1 = x3
                        self._y2 = x2
                        self._y3 = x1
                        self.edge = np.array([self._x1,self._x2,self._x3,self._y1,self._y2,self._y3]) # [x1,x2,x3,y1,y2,y3]
                        if ((self.originalPoint[0] + max(self._x1, self._x2,self._x3)) <= self._maxX) and ((self.originalPoint[1] + self._y1 + self._y2 + self._y3) <= self._maxY):
                            # check whether OrinalPoint is valid after rotated.
                            self.polygon, self.X = self._createPolygon4()
                            self.type_of_tree = 4
                        else:
                            self.type_of_tree = 4
                            self.originalPoint = self._createOriginalPoint()
                            self.polygon, self.X = self._createPolygon4()
            elif degree == 2:
                # degree = 2, 180 degree.
                self._x1 = x3
                self._x2 = x2
                self._x3 = x1
                self._y1 = y3
                self._y2 = y2
                self._y3 = y1
                self.edge = np.array([self._x1,self._x2,self._x3,self._y1,self._y2,self._y3]) # [x1,x2,x3,y1,y2,y3]
                if ((self.originalPoint[0] + self._x1 + self._x2 + self._x3) <= self._maxX) and ((self.originalPoint[1] + max(self._y1,self._y3)) <= self._maxY):
                    self.polygon, self.X = self._createPolygon1()
                    self.type_of_tree = 1
                else:
                    self.type_of_tree = 1
                    self.originalPoint = self._createOriginalPoint()
                    self.polygon, self.X = self._createPolygon1()
            else: 
                pass
        elif self.strname == 'U3':
            if degree == 1 or degree == 3:
                if ((self._y1 + self._y2 + self._y3) < self._maxX) and (max(self._x1,self._x3) < self._maxY): # check whether polygon can be rotated.
                    if degree == 1:  # 90 degree.
                        self._y1 = x3
                        self._y2 = x2
                        self._y3 = x1
                        self._x1 = y3
                        self._x2 = y2
                        self._x3 = y1
                        self.edge = np.array([self._x1,self._x2,self._x3,self._y1,self._y2,self._y3]) # [x1,x2,x3,y1,y2,y3]
                        if ((self.originalPoint[0] + self._x1 + self._x2 + self._x3) <= self._maxX) and ((self.originalPoint[1] + max(self._y1,self._y3)) <= self._maxY):
                            self.polygon, self.X = self._createPolygon1()
                            self.type_of_tree = 1
                        else:
                            self.type_of_tree = 1
                            self.originalPoint = self._createOriginalPoint()
                            self.polygon, self.X = self._createPolygon1()
                    else: # degree == 3, 270 degree.
                        self._x1 = y1
                        self._x2 = y2
                        self._x3 = y3
                        self._y1 = x1
                        self._y2 = x2
                        self._y3 = x3
                        self.edge = np.array([self._x1,self._x2,self._x3,self._y1,self._y2,self._y3]) # [x1,x2,x3,y1,y2,y3]
                        if ((self.originalPoint[0] + self._x1 + self._x2 + self._x3) <= self._maxX):
                            if ((self._y1 >= self._y3) and ((self.originalPoint[1] + self._y1) <= self._maxY)) or ((self.originalPoint[1]>=(self._y3 - self._y1)) and ((self.originalPoint[0] + self._y3)<=self._maxY)):
                                self.polygon, self.X = self._createPolygon2()
                                self.type_of_tree = 2
                            else:
                                self.type_of_tree = 2
                                self.originalPoint = self._createOriginalPoint()
                                self.polygon, self.X = self._createPolygon2()
            elif degree ==2:
                # degree = 2, 180 degree.
                self._x1 = x3
                self._x2 = x2
                self._x3 = x1
                self._y1 = y3
                self._y2 = y2
                self._y3 = y1
                self.edge = np.array([self._x1,self._x2,self._x3,self._y1,self._y2,self._y3]) # [x1,x2,x3,y1,y2,y3]
                if ((self.originalPoint[0] + max(self._x1, self._x2,self._x3)) <= self._maxX) and ((self.originalPoint[1] + self._y1 + self._y2 + self._y3) <= self._maxY):
                    # check whether OrinalPoint is valid after rotated.
                    self.polygon, self.X = self._createPolygon4()
                    self.type_of_tree = 4
                else:
                    self.type_of_tree = 4
                    self.originalPoint = self._createOriginalPoint()
                    self.polygon, self.X = self._createPolygon4()
            else:
                pass
        else: # strname == 'U4'
            if degree == 1 or degree == 3:
                if ((self._y1 + self._y2 + self._y3) < self._maxX) and (max(self._x1,self._x3) < self._maxY): # check whether polygon can be rotated.
                    if degree == 1:  # 90 degree.
                        self._y1 = x3
                        self._y2 = x2
                        self._y3 = x1
                        self._x1 = y3
                        self._x2 = y2
                        self._x3 = y1
                        self.edge = np.array([self._x1,self._x2,self._x3,self._y1,self._y2,self._y3]) # [x1,x2,x3,y1,y2,y3]
                        if ((self.originalPoint[0] + self._x1 + self._x2 + self._x3) <= self._maxX):
                            if ((self._y1 >= self._y3) and ((self.originalPoint[1] + self._y1) <= self._maxY)) or ((self.originalPoint[1]>=(self._y3 - self._y1)) and ((self.originalPoint[0] + self._y3)<=self._maxY)):
                                self.polygon, self.X = self._createPolygon2()
                                self.type_of_tree = 2
                            else:
                                self.type_of_tree = 2
                                self.originalPoint = self._createOriginalPoint()
                                self.polygon, self.X = self._createPolygon2()
                    else: # degree == 3, 270 degree.
                        self._x1 = y1
                        self._x2 = y2
                        self._x3 = y3
                        self._y1 = x1
                        self._y2 = x2
                        self._y3 = x3
                        self.edge = np.array([self._x1,self._x2,self._x3,self._y1,self._y2,self._y3]) # [x1,x2,x3,y1,y2,y3]
                        if ((self.originalPoint[0] + self._x1 + self._x2 + self._x3) <= self._maxX) and ((self.originalPoint[1] + max(self._y1,self._y3)) <= self._maxY):
                            self.polygon, self.X = self._createPolygon1()
                            self.type_of_tree = 1
                        else:
                            self.type_of_tree = 1
                            self.originalPoint = self._createOriginalPoint()
                            self.polygon, self.X = self._createPolygon1()
            elif degree == 2:
                # degree = 2, 180 degree.
                self._x1 = x3
                self._x2 = x2
                self._x3 = x1
                self._y1 = y3
                self._y2 = y2
                self._y3 = y1
                self.edge = np.array([self._x1,self._x2,self._x3,self._y1,self._y2,self._y3]) # [x1,x2,x3,y1,y2,y3]
                if ((self.originalPoint[1] + self._y1+ self._y2 + self._y3) <= self._maxY):
                    if ((self._x3 >= self._x1) and ((self.originalPoint[0] + self._x3) <= self._maxX)) or ((self.originalPoint[0]>=(self._x1 - self._x3)) and ((self.originalPoint[0] + self._x1)<=self._maxX)):
                        # check whether OrinalPoint is valid after rotated.
                        self.polygon, self.X = self._createPolygon3()
                        self.type_of_tree = 3
                    else:
                        self.type_of_tree = 3
                        self.originalPoint = self._createOriginalPoint()
                        self.polygon, self.X = self._createPolygon3()
            else:
                pass

    def increase(self):
        if self.strname == 'U1' or self.strname == 'U2':
            self._x1 = random.uniform(self._x1,(self._maxX)/3)
            #print(self._x1,'  ',(self._maxX)/3)
            self._x2 = random.uniform(self._x2,(self._maxX)/3)
            self._x3 = random.uniform(self._x3,(self._maxX)/3)
            #print(self._x1 + self._x2 + self._x3)
            self._y2 = random.uniform(self._y2,(self._maxY)/2)
            if self._y1 > self._y2:
                self._y1 = random.uniform(self._y1,self._maxY)
            else:
                self._y1 = random.uniform(self._y2,self._maxY)
            if self._y3 > self._y2:
                self._y3 = random.uniform(self._y3,self._maxY)
            else:
                self._y3 = random.uniform(self._y2,self._maxY)
            if self.strname == 'U1':
                self.originalPoint = self._createOriginalPoint()
                self.polygon, self.X = self._createPolygon1()
            else:
                self.originalPoint = self._createOriginalPoint()
                self.polygon, self.X = self._createPolygon2()
        else:
            self._y1 = random.uniform(self._y1,(self._maxY)/3)
            self._y2 = random.uniform(self._y2,(self._maxY)/3)
            self._y3 = random.uniform(self._y3,(self._maxY)/3)
            self._x2 = random.uniform(self._x2,(self._maxX)/2)
            if self._x1 > self._x2:
                self._x1 = random.uniform(self._x1,self._maxX)
            else:
                self._x1 = random.uniform(self._x2,self._maxX)
            if self._x3 > self._x3:
                self._x3 = random.uniform(self._x3,self._maxX)
            else:
                self._x3 = random.uniform(self._x2,self._maxX)
            if self.strname == 'U3':
                self.originalPoint = self._createOriginalPoint()
                self.polygon, self.X = self._createPolygon3()
            else:
                self.originalPoint = self._createOriginalPoint()
                self.polygon, self.X = self._createPolygon4()
        self.edge = np.array([self._x1,self._x2,self._x3,self._y1,self._y2,self._y3]) # [x1,x2,x3,y1,y2,y3]

    def decrease(self):
        if self.strname == 'U1' or self.strname == 'U2':
            self._x1 = random.uniform(0,self._x1)
            #print(self._x1,'  ',(self._maxX)/3)
            self._x2 = random.uniform(0,self._x2)
            self._x3 = random.uniform(0,self._x3)
            #print(self._x1 + self._x2 + self._x3)
            self._y2 = random.uniform(0,self._y2)
            self._y1 = random.uniform(self._y2,self._y1)
            self._y3 = random.uniform(self._y2,self._y3)
            if self.strname == 'U1':
                #self.originalPoint = self._createOriginalPoint()
                self.polygon, self.X = self._createPolygon1()
            else:
                #self.originalPoint = self._createOriginalPoint()
                self.polygon, self.X = self._createPolygon2()
        else:
            self._y1 = random.uniform(0,self._y1)
            self._y2 = random.uniform(0,self._y2)
            self._y3 = random.uniform(0,self._y3)
            self._x2 = random.uniform(0,self._x2)
            self._x1 = random.uniform(self._x2,self._x1)
            self._x3 = random.uniform(self._x2,self._x3)
            if self.strname == 'U3':
                #self.originalPoint = self._createOriginalPoint()
                self.polygon, self.X = self._createPolygon3()
            else:
                #self.originalPoint = self._createOriginalPoint()
                self.polygon, self.X = self._createPolygon4()
        self.edge = np.array([self._x1,self._x2,self._x3,self._y1,self._y2,self._y3]) # [x1,x2,x3,y1,y2,y3]



    def _createOriginalPoint(self):
        if self.type_of_tree == 2:
            x = random.uniform(0,self._maxX - self._x1 - self._x2 - self._x3)
            if self._y3 - self._y1 > 0:
                y = random.uniform(self._y3 - self._y1 ,self._maxY - max(self._y1, self._y3))
            else:
                y = random.uniform(0,self._maxY - max(self._y1, self._y3))
        elif self.type_of_tree == 1:
            x = random.uniform(0,self._maxX - self._x1 - self._x2 - self._x3)
            y = random.uniform(0,self._maxY - max(self._y1, self._y3))
        elif (self.type_of_tree == 3):
            y = random.uniform(0,self._maxY - self._y1 - self._y3 - self._y2)
            if self._x1 > self._x3:
                x = random.uniform(self._x1 - self._x3,self._maxX - max(self._x1,self._x3))
            else:
                x = random.uniform(0,self._maxX - max(self._x1,self._x2,self._x3))
        else:
            y = random.uniform(0,self._maxY - self._y1 - self._y3 - self._y2)
            x = random.uniform(0,self._maxX - max(self._x1,self._x3))

        originalPoint = [x,y]
        return originalPoint
    def _createPolygon1(self):
        self.strname = 'U1'
        x1 = self.originalPoint
        X = np.zeros((8,2))
        X[0] = x1
        X[1][0] = X[0][0] + self._x1 + self._x2 + self._x3
        X[1][1] = X[0][1]
        X[2][0] = X[1][0]
        X[2][1] = X[1][1] + self._y3
        X[3][0] = X[2][0] - self._x3
        X[3][1] = X[2][1]
        X[4][0] = X[3][0]
        X[4][1] = X[3][1] - (self._y3 - self._y2)
        X[5][0] = X[4][0] - self._x2
        X[5][1] = X[4][1]
        X[6][0] = X[5][0] 
        X[6][1] = X[5][1] + (self._y1 - self._y2)
        X[7][0] = X[6][0] - self._x1
        X[7][1] = X[6][1]
        polys = gpd.GeoSeries(Polygon(X))
        df = gpd.GeoDataFrame({'geometry': polys})
        return df,X

    def _createPolygon2(self):
        self.strname = 'U2'
        x1 = self.originalPoint
        X = np.zeros((8,2))
        X[0] = x1
        X[1][0] = X[0][0] + self._x1
        X[1][1] = X[0][1]
        X[2][0] = X[1][0]
        X[2][1] = X[1][1] + self._y1 - self._y2
        X[3][0] = X[2][0] + self._x2
        X[3][1] = X[2][1]
        X[4][0] = X[3][0]
        X[4][1] = X[3][1] - (self._y3 - self._y2)
        X[5][0] = X[4][0] + self._x3
        X[5][1] = X[4][1]
        X[6][0] = X[5][0] 
        X[6][1] = X[5][1] + self._y3
        X[7][0] = X[6][0] - self._x1 - self._x2 - self._x3
        X[7][1] = X[6][1]
        polys = gpd.GeoSeries(Polygon(X))
        df = gpd.GeoDataFrame({'geometry': polys})
        return df,X

    def _createPolygon3(self):
        self.strname = 'U3'
        x1 = self.originalPoint
        X = np.zeros((8,2))
        X[0] = x1
        X[1][0] = X[0][0] + self._x3
        X[1][1] = X[0][1]
        X[2][0] = X[1][0] 
        X[2][1] = X[1][1] + self._y1 + self._y2 + self._y3
        X[3][0] = X[2][0] - self._x1
        X[3][1] = X[2][1]
        X[4][0] = X[3][0]
        X[4][1] = X[3][1] - self._y1
        X[5][0] = X[4][0] + (self._x1 - self._x2)
        X[5][1] = X[4][1]
        X[6][0] = X[5][0] 
        X[6][1] = X[5][1] - self._y2
        X[7][0] = X[6][0] - (self._x3 - self._x2)
        X[7][1] = X[6][1]
        polys = gpd.GeoSeries(Polygon(X))
        df = gpd.GeoDataFrame({'geometry': polys})
        return df,X

    def _createPolygon4(self):
        self.strname = 'U4'
        x1 = self.originalPoint
        X = np.zeros((8,2))
        X[0] = x1
        X[1][0] = X[0][0] + self._x3
        X[1][1] = X[0][1]
        X[2][0] = X[1][0]
        X[2][1] = X[1][1] + self._y3
        X[3][0] = X[2][0] - (self._x3  - self._x2)
        X[3][1] = X[2][1]
        X[4][0] = X[3][0]
        X[4][1] = X[3][1] + self._y2
        X[5][0] = X[4][0] + (self._x1 - self._x2)
        X[5][1] = X[4][1]
        X[6][0] = X[5][0]
        X[6][1] = X[5][1] + self._y1
        X[7][0] = X[6][0] - self._x1
        X[7][1] = X[6][1]
        polys = gpd.GeoSeries(Polygon(X))
        df = gpd.GeoDataFrame({'geometry': polys})
        return df,X