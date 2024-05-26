def shoot(self,mode=0,redundancy = 0.5):
        '''
        shooting
        Mode 0: Shoot from directly behind the football
        Mode 1: Rotate to face the ball and then shoot
        Mode 2: The ball is in the no-shooting zone on the left side of the field, move right to drag the ball to the shooting area and then shoot from directly behind
        Mode 3: The ball is in the no-shooting zone on the right side of the field, move left to drag the ball to the shooting area and then shoot from directly behind
        Mode 4: No shooting, do nothing

        go [redundancy] meters further
        '''
        if mode == 0:
            duration = (self.DIST + redundancy)/self.max_speed_x
            self.go_for(duration,[self.max_speed_x,.0,.0])
        elif mode == 1:
            ball_loc,me_loc = self.location.ball,self.location.red_dog
            if(me_loc[0] - ball_loc[0] < 0):
                left = -1
            else:
                left = 1
            rotation=self.rotate_aim_ball(0,left)*1.1 #请别吐槽。。
            duration = (self.DIST + redundancy)/self.max_speed_x
            self.go_for(duration,[self.max_speed_x,.0,.0])
            if rotation>0:
                self.go_for(rotation/0.5,[.0,.0,-0.5])
            else:
                rotation = abs(rotation)
                self.go_for(rotation/0.5,[.0,.0,0.5])
        elif mode == 2:
            pass