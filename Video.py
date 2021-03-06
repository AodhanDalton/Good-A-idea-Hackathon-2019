import math
import scipy
from scipy import stats
import random

with open('data/names.txt') as n:
    names=n.read().split('\n')
    #shuffle the list
    random.shuffle(names)

class VectorPredictor:
    '''Object vector predictior
    Predictions are based on object classifier identifing bounding boxes
    and using these to build a predicted movement vector'''
    CHAIN_SIZE = 3
    LIST_MAX = CHAIN_SIZE #depth of frames to build chain
    LIFE_MAX = 1 # no. of dead frames before its dropped
    ITERATIONS = -1
    FRAMES =[] # stores most recent frames
    VECTORS = [] #stores active vectors
    DEAD_VECTORS = [] #stores vectors that did not get a frame refresh
    
    def build_chains(self):
        #get structure
        #TODO  FIx THiS SHit You LazY FUCkER
        for bbox in self.FRAMES[self.CHAIN_SIZE-3]:
            for bbox2 in self.FRAMES[self.CHAIN_SIZE-2]:
                if self.box_overlap(bbox,bbox2):
                    for bbox3 in self.FRAMES[self.CHAIN_SIZE-1]:
                        if self.box_overlap(bbox2, bbox3):
                            self.add_vector(bbox3,bbox2,bbox)
                            return 0



    def add_vector(self,*args):
        if len(args) != self.CHAIN_SIZE:
            raise NotImplementedError
        xlist = [x[0] for x, y in args]
        ylist = [x[1] for x, y in args]

        slope, intercept, r_value, p_value, std_err = stats.linregress(ylist, xlist)
        self.VECTORS.append(Vector(slope, intercept, *args))

    def add_frame(self, bboxs):
        #TODO IMPROVE HAVING TO REITERATE OVER THE VECTORS MULTIPLE TIMES
        #add it to structure
        self.FRAMES.append(bboxs)
        self.ITERATIONS += 1
        #check and remove vector bb0x
        #and strip out dead vectors

        if self.ITERATIONS < self.CHAIN_SIZE:
            return False
        self.FRAMES.pop(0)

        self.update_vectors()
        #form new chainz
        self.build_chains()
        #return vector lines
        
        return self.build_vector_lines()
    
    def update_vectors(self):
        '''Updates the vectors with the new bounding box and kills dead vectors'''
        #TODO could we get the lines here and add on the new chains???
        for v in self.VECTORS:
            #Check the newest set of frames
            for bbox in self.FRAMES[self.LIST_MAX-1]:
                #TODO DECIDE BETWEEN LINE OR BOX OVERLAP
                vbbox = v.bboxs[-1]

                if self.box_overlap(vbbox, bbox):
                    v.alive=0
                    v.add_bbox(bbox) 
                    #remove the item from the list
                    self.FRAMES[self.LIST_MAX-1].remove(bbox)
                else:
                    v.alive+=1
            #kill all expired vectors
            if(v.alive >= self.LIFE_MAX):
                self.DEAD_VECTORS.append(v)
                self.VECTORS.remove(v)


    def build_vector_lines(self):
        return [v.get_line() for v in self.VECTORS]
        
    def box_overlap(self, a, b):
        #a's
        amin_x = min(a[0][0],a[1][0])
        amax_x = max(a[0][0],a[1][0])
        amin_y = min(a[0][1], a[1][1])
        amax_y = max(a[0][1], a[1][1])
        #b's
        bmax_x = max(b[0][0], b[1][0])
        bmin_x = min(b[0][0], b[1][0])
        bmax_y = max(b[0][1], b[1][1])
        bmin_y = min(b[0][1], b[1][1])
        if amin_x > bmax_x or amax_x < bmin_x:
            return False
        if amin_y > bmax_y or amax_y < bmin_y:
            return False
        return True

class Vector:
    '''Calculates movement vector of an object based on a series of positions''' 
    LINE_LENGTH = 100
    MAX_BBOXS = 6

    def __init__(self,yinter,gradient,*bboxs):
        '''Initialises with a linear line and bounding boxes'''
        #random name 
        self.name = names.pop()
        self.alive = 0
        #plotting values
        self.yintercept= yinter
        self.gradient = gradient
        self.bboxs = [bboxs]

    def rebuild_from_bbox(self):
        xlist = [x[0] for x, y in self.bboxs]
        ylist = [x[1] for x, y in self.bboxs]
        slope, intercept, r_value, p_value, std_err = stats.linregress(ylist, xlist)
        self.yintercept = intercept
        self.gradient = abs(slope)

    def add_bbox(self, bbox):
        '''updates the prediction based on the bounding box added'''
        #TODO Implement this like wat even how?
        #Recalculate the bestfit
        #Adjust with new points
        self.bboxs.append(bbox)
        if(len(self.bboxs) > self.MAX_BBOXS):    
            self.bboxs.pop(0)
        self.rebuild_from_bbox()




    def get_line(self):
        '''Returns the coords to draw the line'''
        x1,y1 = self.bboxs[-1][0]
        
        #TODO IMPORVE THIS
        x2 = x1+self.LINE_LENGTH
        y2 = x2*self.gradient + self.yintercept

        
        return self.name, (x1,y1), (x2,int(abs(y2))), self.bboxs[-1][1]
