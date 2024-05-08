import math

def get_goal_coords(ball_coords,dog_coords,gate_coords,dist):
    right = 0
    
    # 计算球门和球之间的直线斜率
    slope = (gate_coords[1] - ball_coords[1]) / (gate_coords[0] - ball_coords[0])
    intercept = ((gate_coords[1] - slope * gate_coords[0])+ball_coords[1]-slope*ball_coords[0])/2
    # p是便于计算最终坐标的系数
    if slope>0:
        p=-1
    else:
        p=1
    dist_y=dist*(p*slope/math.sqrt(1+slope*slope))
    dist_x=dist*(p/math.sqrt(1+slope*slope))
    goal_coords=(ball_coords[0]+dist_x,ball_coords[1]+dist_y)
    intersection_x=(dog_coords[1]-intercept)/slope
    if intersection_x>ball_coords[0]:
        right = 1
    else:
        right = 0
    return goal_coords,right

def get_routine(ball_coords,dog_coords,goal_coords,right):
    #dis(dog,ball)^2
    b_d=(ball_coords[0]-dog_coords[0])**2+(ball_coords[1]-dog_coords[1])**2
    #dis(ball,goal)^2
    b_g=(ball_coords[0]-goal_coords[0])**2+(ball_coords[1]-goal_coords[1])**2
    #dis(dog,goal)^2
    d_g=(goal_coords[0]-dog_coords[0])**2+(goal_coords[1]-dog_coords[1])**2
    cos_theta=(b_d+d_g-b_g)/(2*math.sqrt(b_d)*math.sqrt(d_g))
    theta=math.acos(cos_theta)
    '''
    if dog_coords[0]>ball_coords[0]:
        theta=theta
    else:
        theta=-1*theta
    '''
    theta = theta*right
    goDist=math.sqrt(d_g)
    return theta,goDist

def main():
    ball_coords=[2,4]
    dog_coords=[1,3]
    gate_coords=[3,6]
    dist=1
    goal_coords,right=get_goal_coords(ball_coords,dog_coords,gate_coords,dist)
    print(goal_coords[0],goal_coords[1],right)
    theta,goDist=get_routine(ball_coords,dog_coords,goal_coords,right)
    print(theta,goDist)
    
if __name__ == '__main__':
    main()