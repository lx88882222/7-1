'''
>   geometry.py
>   author: whf wmy
>   date: 2024-5-11
>   define a class Line
    - three ways to initialize a line:
        1. point_slope: given a point and a slope
        2. point_point: given two points
        3. slope_interception: given a slope and an interception
    - function:
        1. get_x(y) and get_y(x): given x or y return intersection
        2. get_target(self,dist,mode=-1,point=None) ->[x,y]
            mode=-1: get the target with smaller y; mode=1, get the target with larger y
            find a point on the line that have certain diatance (dist) to the given point (point,if not given, then use piont2 of Line)

    define a function get_routine(aim_i,aim_f,center): ->theta(float), goDist(float)
        routine from aiming at aim_i to aiming at aim_f
'''
import math
class Line:
    
    def __init__(self,slope,interception):
        self.slope = slope
        self.interception = interception
        self.point1 = [.0,.0] 
        self.point2 = [.0,.0] # always save ball's loc as point2
    @classmethod
    def point_slope(cls,point,slope):
        interception = point[1]-slope*point[0]
        s=cls(slope,interception)
        s.point1=point
        return s
    @classmethod
    def point_point(cls,point1,point2):
        if (point2[0]-point1[0]) < 0.05:
            slope = None
            interception =point2[0]
        else:
            slope = (point2[1]-point1[1])/(point2[0]-point1[0])
            interception = point1[1]-slope*point1[0]
        s=cls(slope,interception)
        s.point1 = point1
        s.point2 = point2
        return s
    
    #   given x or y return intersection
    def get_y(self,x):
        if self.slope == None:
            return None
        else:
            return self.slope*x+self.interception
    def get_x(self,y):
        if self.slope < 0.05:
            return None
        elif self.slope == None:
            return self.interception
        else:
            return (self.y-self.interception)/self.slope
    
    #   find a point on the line that have certain diatance (dist) to the given point (point,if not given, then use piont2 of Line)
    def get_target(self,dist,mode=-1,point=None): #   mode=-1: get the target with smaller y; mode=1, get the target with larger y
        # p是便于计算最终坐标的系数
        if self.slope>0:
            p=1*mode
        else:
            p=-1*mode
        if point == None and self.point2 == [.0,.0]:
            return None
        elif point == None:
            center = point
        else:
            center = self.point2
        dist_y=dist*(p*self.slope/math.sqrt(1+self.slope*self.slope))
        dist_x=dist*(p/math.sqrt(1+self.slope*self.slope))
        target_loc=(center[0]+dist_x,center[1]+dist_y)
        return target_loc
    
    def get_routine(aim_i,aim_f,center):
        vector1 = [aim_i[0]-center[0],aim_i[1]-center[1]]
        vector2 = [aim_f[0]-center[0],aim_f[1]-center[1]]
        v1=math.sqrt(vector1[0]**2+vector1[1]**2)
        v2=math.sqrt(vector2[0]**2+vector2[1]**2)
        cross_product = vector1[0]*vector2[1]-vector1[1]*vector2[0]
        theta = math.asin(cross_product/(v1*v2))
        return theta,v2