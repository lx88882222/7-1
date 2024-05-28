'''
>   author: whf
>   date: 2024-05-23
>   all constants should be modified in this class and only called in other modules.
    usage:
        from .constants import C
        print(C.NAME)
'''
class C():
    GATE = [-0.2,8.8]               # (x,y)
    DIST = 1.0                      # get_goal_coords() distance to the ball (m)
    ERROR = 0.3                     # error for location.in_place (m)
    NAME = 'az1'                    # dog_name
    COLOR = 1                       # 0 FOR RED, 1 FOR BLACK, 2 FOR WHITE
    UPPER_IP = '10.0.0.144' 
    UPPER_PORT = 40000