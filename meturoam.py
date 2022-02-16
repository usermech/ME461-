greedyLength = 301
boxSize = 50
halfBox = 25
nCorr = 8
colorz = {
        'clr100':((225, 1, 1), 100, 1),
        'clr50':((1, 255, 1), 50, 2),
        'clr30':((1, 1, 255), 30, 2),
        'clr20':((200, 200, 1), 20, 2),
        'clr10':((255, 1, 255), 10, 2),
        'clr9':((1, 255, 255), 9, 3),
        'clr8':((1,1,150), 8, 3),
        'clr7':((120,120,40), 7, 3),
        'clr6':((150,1,150), 6, 3),
        'clr5':((1,150,150), 5, 3),
        'clr4':((222,55,222), 4, 3),
        'clr3':((1, 99, 55), 3, 3),
        'clr2':((200, 100, 10),2, 3),
        'clr1':((100, 10, 200),1, 3)
}
miniColorz = {'clr100':((225, 1, 1), 100, 1),
        'clr50':((1, 255, 1), 50, 2),
        'clr30':((1, 1, 255), 30, 2),           
}


class tulumba:

    def __init__(self, userName, clrDictionary, maxStepSize, maxTime):

        self.name = userName  # your object will be given a user name, i.e. your group name
        self.maxStep = maxStepSize  # maximum length of the returned path from run()
        self.maxTime = maxTime  # run() is supposed to return before maxTime
        self.colorz = clrDictionary
        self.grid = []
        self.counter = 0
        for i in range(1, nCorr):
            self.grid.append([])
            for j in range(1, nCorr):
                node = Node(i, j)
                self.grid[i - 1].append(node)
        self.miniGrid = [self.grid[0][0],self.grid[1][1],self.grid[0][2]]
        self.miniGrid2 = [self.grid[0][6],self.grid[1][5],self.grid[0][4]]
        
    def run(self, img, info):
        # get info
        self.info = info
        self.myX,self.myY = self.info[self.name][0]
        self.point = self.info[self.name][1]
        if self.point < 100:
            myQueue = [float("inf")]
            target = []
            array = []
            for row in self.grid:
                for node in row:
                    node.points = 0  
                    dX = node.x_dist(self.myX)
                    dY = node.y_dist(self.myY)
                    manDistance = dX + dY
                
                    
                    if manDistance < greedyLength:
                        flag = False
                        for dClr in colorz:
                            if tuple(img[node.x, node.y, :]) == colorz[dClr][0]:
                                node.update_points(colorz[dClr][1])
                                if node.points > self.point:
                                    node.points = float("inf")
                                elif node.points == self.point:
                                    target = [node.x,node.y]
                                    flag = True
                                    break
                        if flag:
                            break    
                        elif (self.point-node.points) < myQueue[0] and not node.points == 0:
                            myQueue[0] = (self.point-node.points)
                            target = [node.x,node.y]
            x,y = target
            #call create route here
            array = free_corridor(self.myX,self.myY,x,y)
            return array
        else:
            if (self.myX,self.myY) == (25,175):
                self.counter = 1
                miniQueue = [float("inf")]
                target = [75,275]
                array = []
                
                for node in self.miniGrid:
                    for clr in miniColorz:
                                if tuple(img[node.x, node.y, :]) == miniColorz[clr][0]:
                                    points = (miniColorz[clr][1])
                                    if 100 - points < miniQueue[0]:
                                        self.counter = 4
                                        miniQueue[0] = 100 - points
                                        target = [node.x,node.y]
                                        
                x,y = target
                #call create route here
                routeX,routeY = create_route(self.myX,x,self.myY,y)
                array.append(routeX)
                array.append(routeY)
                array = [ele for ele in array if ele != []]
                return array
            elif (self.myX,self.myY) == (25,575):
                self.counter = 7
                miniQueue = [float("inf")]
                target = [75,475]
                array = []
                
                for node in self.miniGrid2:
                    for clr in miniColorz:
                                if tuple(img[node.x, node.y, :]) == miniColorz[clr][0]:
                                    points = (miniColorz[clr][1])
                                    if 100 - points < miniQueue[0]:
                                        self.counter = 4
                                        miniQueue[0] = 100 - points
                                        target = [node.x,node.y]
                                        
                x,y = target
                #call create route here
                routeX,routeY = create_route(self.myX,x,self.myY,y)
                array.append(routeX)
                array.append(routeY)
                array = [ele for ele in array if ele != []]
                return array      


            elif self.counter > 4:
                if self.counter == 7:
                    self.counter -= 1
                    return [[52,498],[148,498]]
                elif self.counter == 6:
                    self.counter -=1
                    return [[248,498]]
                elif self.counter == 5:
                    self.counter -=1
                    return [[348,498]]
            
            elif self.counter < 4 and not self.counter == 0 :
                if self.counter == 1:
                    self.counter +=1
                    return [[52,252],[148,252]]
                elif self.counter == 2:
                    self.counter +=1
                    return [[248,252]]
                elif self.counter == 3:
                    self.counter +=1
                    return [[348,252]]
            

                                
            
            else:
                # get the nodes closer than 401 steps
                myQueue = [float("inf")]
                target = []
                array = []
                for row in self.grid:
                    for node in row:
                        node.points = 0  
                        dX = node.x_dist(self.myX)
                        dY = node.y_dist(self.myY)
                        manDistance = dX + dY
                    
                        
                        if manDistance < greedyLength:
                            for dClr in colorz:
                                if tuple(img[node.x, node.y, :]) == colorz[dClr][0]:
                                    node.update_points(colorz[dClr][1])
                                
                            if manDistance - (node.points*3) < myQueue[0] and not node.points == 0:
                                myQueue[0] = manDistance - (node.points*3)
                                target = [node.x,node.y]
                if target == []:
                    target = [450,300]
                
                x,y = target                
                #call create route here
                routeX,routeY = create_route(self.myX,x,self.myY,y)
                array.append(routeX)
                array.append(routeY)
                array = [ele for ele in array if ele != []]
                
                if get_distance(x,self.myX,y,self.myY) < 95:
                    ##make it a function after here and call it
                    try:
                        myX2,myY2 = array[-1]
                    except:
                        myX2,myY2 = self.myX,self.myY                        
                    myQueue = [float("inf")]
                    target = []
                    for row in self.grid:
                        for node in row:
                            if node.x == x and node.y == y:     
                                node.points = 0
                            else:  
                                pass  
                            
                            dX = node.x_dist(myX2)
                            dY = node.y_dist(myY2)
                            manDistance = dX + dY
                            
                            if manDistance < greedyLength:
                                
                                if manDistance -(node.points*3) < myQueue[0] and not node.points == 0:
                                        
                                    myQueue[0] = manDistance-(node.points*3)
                                    target = [node.x,node.y]
                    
                    if target == []:
                        target = [450,300]                    
                    x,y = target
                    routeX,routeY = create_route(myX2,x,myY2,y)
                    array.append(routeX)
                    array.append(routeY)
                    array = [ele for ele in array if ele != []]
                    
                    
                return array


def create_route(x1,x2,y1,y2):
    rx = [x1,y1]
    
    if x1 >=  x2 + 24:
        rx = [x2+23,y1]
        ry = [x2+23,y1]
    elif x1 <= x2 -24:
        rx = [x2-23,y1]
        ry = [x2-23,y1]
    else:
        rx =[]
        ry = [x1,y1]
           
    if y1 >=  y2 + 24:
        ry[1] = y2 + 23
    elif y1 <= y2 -24:
        ry[1] = y2 - 23
    else:
        ry = []
    

    return rx,ry

def free_corridor(myX,myY,targetX,targetY):
    

    quotX,remX = divmod(myX,50)
    quotY,remY = divmod(myY,50)
    quotTX = targetX // 50
    quotTY = targetY // 50
    array = []
    if (abs(quotTX-quotX) + abs(quotTY-quotY))<3:
        routeX,routeY = create_route(myX,targetX,myY,targetY)
        array.append(routeX)
        array.append(routeY)
        array = [ele for ele in array if ele != []]
         
    else:
        if (quotX % 2) == 0:
            if myY > targetY:
                array.append([myX,targetY+28])
                if myX >=  targetX + 24:
                    array.append([targetX+23 ,targetY+28])
                    array.append([targetX+23 ,targetY+23])
                elif myX <= targetX - 24:
                    array.append([targetX-23,targetY+28])
                    array.append([targetX-23,targetY+23])
            else:
                array.append([myX,targetY-28])
                if myX >=  targetX + 24:
                    array.append([targetX+23 ,targetY-28])
                    array.append([targetX+23 ,targetY-23])
                elif myX <= targetX - 24:
                    array.append([targetX-23,targetY-28])
                    array.append([targetX-23,targetY-23])
                    
        elif (quotY % 2) == 0:
                if myX > targetX:
                    array.append([targetX+28,myY])
                    if myY >=  targetY + 24:
                        array.append([targetX+28 ,targetY+23])
                        array.append([targetX+23 ,targetY+23])
                    elif myY <= targetY - 24:
                        array.append([targetX+28,targetY-23])
                        array.append([targetX+23,targetY-23])
                else:
                    array.append([targetX-28,myY])
                    if myY >=  targetY + 24:
                        array.append([targetX-28 ,targetY+23])
                        array.append([targetX-23 ,targetY+23])
                    elif myY <= targetY - 24:
                        array.append([targetX-28,targetY-23])
                        array.append([targetX-23,targetY-23])
        else:
            if myX >=  targetX:
                array.append([myX-(remX+2),myY])
                newX = myX-(remX+2)
                if myY > targetY:
                    array.append([newX,targetY+28])
                    if newX >=  targetX + 24:
                        array.append([targetX+23 ,targetY+28])
                        array.append([targetX+23 ,targetY+23])
                    elif newX <= targetX - 24:
                        array.append([targetX-23,targetY+28])
                        array.append([targetX-23,targetY+23])
                    else:
                        array.append([myX,targetY-28])
                        if newX >=  targetX + 24:
                            array.append([targetX+23 ,targetY-28])
                            array.append([targetX+23 ,targetY-23])
                        elif newX <= targetX - 24:
                            array.append([targetX-23,targetY-28])
                            array.append([targetX-23,targetY-23])
                
            else:
                array.append([myX+(52-remX),myY])
                newX = myX+(52-remX)
                if myY > targetY:
                    array.append([newX,targetY+28])
                    if newX >=  targetX + 24:
                        array.append([targetX+23 ,targetY+28])
                        array.append([targetX+23 ,targetY+23])
                    elif newX <= targetX - 24:
                        array.append([targetX-23,targetY+28])
                        array.append([targetX-23,targetY+23])
                    else:
                        array.append([myX,targetY-28])
                        if newX >=  targetX + 24:
                            array.append([targetX+23 ,targetY-28])
                            array.append([targetX+23 ,targetY-23])
                        elif newX <= targetX - 24:
                            array.append([targetX-23,targetY-28])
                            array.append([targetX-23,targetY-23])
    return array

def get_distance(x1,x2,y1,y2):
    return abs(x1-x2)+abs(y1-y2)

class Node:
    def __init__(self,row,column):
        self.row = row
        self.col = column
        self.x = self.row * 2 * boxSize - halfBox
        self.y = self.col * 2 * boxSize - halfBox
        self.points = 0
        
    def update_points(self,points):
        self.points = points

    def x_dist(self,myX):
        dX = abs(myX - self.x)
        return dX
        

    def y_dist(self,myY):
       dY = abs(myY - self.y)
       return dY
        
