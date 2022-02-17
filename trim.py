def TrimPath( path, L):
        '''
        path is the candidate path, i.e a list of points [[y1,x1], ... [yn,xn]]
        the function assumes that [y1,x1] is where the agent currently is, 
        and hence [y2,x2] is the first point to move
        L is the total distance that the agent can cover
        function returns the path trimmed so that it has a length of L
        '''
        # first veryfy path
        res = [path[0]] # initially coordinate is approved by default, others will be added if they are valid and within the span of L
        distRemaining = L # originially this is the distance to be covered by the send path
        for i in range(len(path)-1): # using pairs move on the path
            # move on only any distance to move is left
            
            if distRemaining <= 0:
                return res
            # get the points and their coordinates explicitly
            p1, p2 = path[i], path[i+1] # get two consequitive point coordinates
            try:
                y1, x1 = path[i][0], path[i][1]
                y2, x2 = path[i+1][0], path[i+1][1]
                dy = y2 - y1 #p2[0] - p1[0]
                dx = x2 - x1 #p2[1] - p1[1]
                # one of these has to be zero on a N4 path
                if abs(dx) >0 and abs(dy)>0: # we have a problem, one of them has to be zero on a N4 path
                    # just return the valid path found so far
                    return res
                # we also have a problem if consequtive points are the same, if so just ignore the latest one
                if not(dx == 0 and dy == 0): # 
                    pathL = max(abs(dy), abs(dx)) # length between p1-p2
                    if pathL <= distRemaining: # this part of the path (p1 to p2) completely belongs to the resulting path
                        res.append(p2)
                        distRemaining -= pathL
                        
                    else: # this is the tricky part, some part of the path will belong
                        # partial path should expand either in X or Y direction
                        # note that either dx or dy has to be zero at all times
                        if abs(dx) > 0: # going in X direction
                            res.append([y1, x1+np.sign(dx)*distRemaining])
                            
                        else: # going in Y direction
                            res.append([y1+np.sign(dy)*distRemaining, x1])
                            
                        return res
            except:
                pass
        return res

def nextStop(path):
    nextMove = TrimPath(path,100)
    for i in range(len(nextMove)-1):
        path.pop(0)
    path[0]=[nextMove[-1]]
    return path, nextMove
