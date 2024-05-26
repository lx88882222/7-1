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
    FREQUENCY = 0.3                 # frequency of updating status for move.goto()
    MARGIN = [[-2.0,8.8],[2.0,0.0]]
    SAFE_DIST = 0.5
    START_POINT = [-0.2,4.4-DIST]   # 每次射门成功后恢复到一个有利点位
    MOTION_ID = 305
    MAX_SPEED_X = 0.3
    MAX_SPEED_Y = 0.65
    MAX_SPEED_Z = 1.25
    GATE_RANGE = [-1.5,1.5]                 # 球门左右边界
    STEP_HEIGHT = [0.05,0.05]
    INFO_DELAY = 0.3                # threshold for determing a data is to dated to use.
    AVOID_DIST = 0.5
    BALL_SIZE_CLOSE = 100