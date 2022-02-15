def create_route(x1,x2,y1,y2):
    array =[[],[]]
    
    
    if x1 >=  x2 + 24:
        array[0] = [x2+23,y1]
        array[1] = [x2+23,y1]
    elif x1 <= x2 -24:
        array[0] = [x2-23,y1]
        array[1] = [x2-23,y1]
    else:
        array[0] =[]
        array[1] = [x1,y1]
           
    if y1 >=  y2 + 24:
        array[1][1] = y2 + 23
    elif y1 <= y2 -24:
        array[1][1] = y2 - 23
    else:
        array[1] = []
    
    array = [ele for ele in array if ele != []]

    return array
