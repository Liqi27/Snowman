
## 苏莉琦-8年纪12班-AIsnowman程序作品
## python3

import pygame, random, time

# open config file
with open('config.txt','r') as config_file:
    config = config_file.readlines()

# select and pick up the value from str in config
def value_number(value):
    number = value[value.find("{") + 1 : value.find("}")]
    return number

# put the value into the variable
for value in config:
    if value.find("GRID") != -1:
        GRID = int(value_number(value))
    elif value.find("FRAME_IMG") != -1:
        FRAME_IMG = value_number(value)
    elif value.find("PIXEL_IMG") != -1:
        PIXEL_IMG = value_number(value)
    elif value.find("FLAG_IMG") != -1:
        FLAG_IMG = value_number(value)
    elif value.find("TREE_IMG") != -1:
        TREE_IMG = value_number(value)
    elif value.find("SNOWMAN0_IMG") != -1:
        SNOWMAN0_IMG = value_number(value)
    elif value.find("SNOWMAN0_CRASH") != -1:
        SNOWMAN0_CRASH = value_number(value)
    elif value.find("SNOWMAN0_SCORE") != -1:
        SNOWMAN0_SCORE = value_number(value)
    elif value.find("SNOWMAN1_IMG") != -1:
        SNOWMAN1_IMG = value_number(value)
    elif value.find("SNOWMAN1_CRASH") != -1:
        SNOWMAN1_CRASH = value_number(value)
    elif value.find("SNOWMAN1_SCORE") != -1:
        SNOWMAN1_SCORE = value_number(value)
    elif value.find("SNOWMAN2_IMG") != -1:
        SNOWMAN2_IMG = value_number(value)
    elif value.find("SNOWMAN2_CRASH") != -1:
        SNOWMAN2_CRASH = value_number(value)
    elif value.find("SNOWMAN2_SCORE") != -1:
        SNOWMAN2_SCORE = value_number(value)
    elif value.find("SNOWMAN3_IMG") != -1:
        SNOWMAN3_IMG = value_number(value)
    elif value.find("SNOWMAN3_CRASH") != -1:
        SNOWMAN3_CRASH = value_number(value)
    elif value.find("SNOWMAN3_SCORE") != -1:
        SNOWMAN3_SCORE = value_number(value)

# initial variables
background_move = 6
obstacles = pygame.sprite.Group()   # create the group of obstacles
map_position = 0
points_before = 0
base_speed = 6
speed_old = 0
more_trees = 0
ice_angle = 0
update_times = False
who_list = []
count = 0

# load images
frame = pygame.image.load(FRAME_IMG)
pixel_100 = pygame.image.load(PIXEL_IMG)

class SkierClass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite. __init__(self)
        self.images_list = ["skier_down.png", "skier_right1.png", "skier_right2.png", "skier_left2.png", "skier_left1.png"]
        self.image = pygame.image.load("skier_down.png")   # current image
        self.rect = self.image.get_rect()
        self.rect.center = [320, 300]
        
        self.angle = 0
        self.speed = [0, 6]
        self.stop_frame = 7
        self.if_hit = False
        self.if_flag = False
        self.temp_frame = self.stop_frame
        self.continue_image = "skier_down.png"

    def turn(self, direction):        
        self.angle = self.angle + direction
        if self.angle < -2: self.angle = -2
        if self.angle > 2: self.angle = 2
        center = self.rect.center
        self.image = pygame.image.load(self.images_list[self.angle])
        self.rect = self.image.get_rect() 
        self.rect.center = center
        self.speed = [self.angle, base_speed - abs(self.angle) * 2]

    def left_right(self):   # control self move to left or right
        self.rect.centerx = self.rect.centerx + self.speed[0]   # regulate self's centerx
        if self.rect.centerx < 20: self.rect.centerx = 20   # don't let self get out of the left side of the screen
        if self.rect.centerx > SCREEN_WIDTH - 20: self.rect.centerx = SCREEN_WIDTH - 20   # don't left self get out of right side of screen

class SnowmanClass(SkierClass):  # inherit SkierClass
    def __init__(self, position, image, crash_image, score_str):
        pygame.sprite.Sprite.__init__(self)  # initial pygame.sprite.Sprite
        # initial attributes
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.angle = 0
        self.stop_frame = 12
        self.if_hit = False
        self.if_flag = False
        self.temp_frame = self.stop_frame
        self.continue_image = image
        self.speed = [0, 6]
        self.front_location = []
        self.CW = []
        self.left_distance = {}
        self.right_distance = {}
        self.before_change = 0
        self.close_right_side = {}
        self.close_left_side = {}
        self.keep_turn_right = False
        self.keep_turn_left = False
        self.right_tree = None
        self.left_tree = None
        self.gap_right = 0
        self.gap_left = 0
        self.if_left_front = False
        self.if_right_front = False
        self.if_close_left = False
        self.if_close_right = False
        self.frame_position = []
        self.passed = None
        self.points = 0
        self.crash_image = crash_image
        self.score_text = None
        self.score_str = score_str

    def turn(self, direction):   # turn the direction
        self.angle = self.angle + direction # calculate the angle of snowman(current angle + direction that the snowman going to turn)
        if self.angle < -2: self.angle = -2  # set the smallest value of the angle(set the range of turning)
        if self.angle > 2: self.angle = 2  # set the biggest value of angle (set the range of turning)
        self.speed = [self.angle, base_speed - abs(self.angle) * 2]  # put the angle into self.speed[0], put the speed into self.speed[1]

    def smallest(self, distance_list):  # get the distance between the snowman and the tree that closest to the snowman
        smallest = SCREEN_WIDTH   # initial smallest
        for i in distance_list: 
            if i < smallest:  # let the i compare with the smallest
                smallest = i   # replace the smallest with the smaller value
                
        return smallest   # get a smallest distance
        
    # after check_tree, get the distances list(snowman.left/right_distance, snowman.if_close_left/right_distance)
    # switch the True/False of variable(if_left/right_front, if_close_left/right)
    def calculate(self): 
        smallest_left = SCREEN_WIDTH  # minimum value in left_distance(the tree closest to snowman in the lower left)
        smallest_right = SCREEN_WIDTH  # minimum value in right_distance(the tree closest to snowman in the lower right)
        smallest_close_left = SCREEN_WIDTH  # minimum value in close_left_side(the tree closest to snowman in left side)
        smallest_close_right = SCREEN_WIDTH  # minimum value in close_right_side(the tree closest to snowman in right side)
        pre = [self.if_left_front,self.if_right_front,self.if_close_left,self.if_close_right]

        # draw the frame or the red line
        for j in self.close_left_side:    # check the value in the close_left_side dictionary
            if self.close_left_side[j] == "left_wall":  # check if the snowman close to the left_wall
                self.frame_position.append([(0 - frame.get_width() + 2), self.rect.topleft[1]])   # draw a red line on the wall
        for a in self.left_distance:      # check the value in the left_distance dictionary
            if a <= 0 and self.left_distance[a] != "right_wall":  # check if the tree block the snowman
                self.frame_position.append(self.left_distance[a].rect.topleft)   # draw a frame around the tree
                
        for k in self.close_right_side:   # check the value in the close_right_side dictionary
            if self.close_right_side[k] == "right_wall":   # check if the snowman close to the right_wall
                self.frame_position.append([SCREEN_WIDTH - 2, self.rect.topleft[1]])   # draw a red line on the wall
        for b in self.right_distance:     # check the value in the right_distance dictionary
            if b <= 0 and self.right_distance[b] != "left_wall":   # check if the tree block the snowman
                self.frame_position.append(self.right_distance[b].rect.topleft)   # draw a frame around the tree

                
        # get smallest_left
        if self.left_distance: # if there is a tree in left front of snowman
            smallest_left = self.smallest(self.left_distance)  # get the smallest distance between the snowman and the tree that closest to the snowman
            # print("smallest left:", smallest_left)
                        
        # get smallest_right
        if self.right_distance: # if there is a tree in the right front of snowman
            smallest_right = self.smallest(self.right_distance)  # get the smallest distance between the snowman and the tree that closest to the snowman
            # print("smallest right:", smallest_right)

        # switch if_left_front(to tell if there is a obstacle in snowman's way)
        if smallest_left:  # if there is a tree closest to the snowman in left front
            if smallest_left <= 0 and smallest_right > 0:  # if the tree block the left way of snowman and there is no tree in the right front of snowman
                self.if_left_front = True  # make a flag that a tree block the left way of snowman
                    
            if smallest_left > 0:  # if no tree block the left way of snowman
                self.if_left_front = False  # make a flag that no tree block the left way of snowman
                self.if_close_right = False  # make a flag that no tree close to the snowman in the right side
  
        if smallest_right: # if there is a tree closest to the snowman in right front
            if smallest_right <= 0 and smallest_left > 0:  # if the tree block the right way of snowman and there is no tree in the left front of snowman
                self.if_right_front = True  # make a flag that a tree block the right way of snowman
                    
            if smallest_right > 0:  # if no tree block the right way of snowman
                self.if_right_front = False  # make a flag that no tree block the right way of snowman
                self.if_close_left = False   # make a flag that no tree close to snowman in the left side

        if smallest_right and smallest_left:  # if there is tree in the left side of snowman and there is also a tree in the right side of snowman
            if smallest_left <= 0 and smallest_right <= 0:  # if the tree block the way of snowman
                if smallest_left < smallest_right:  # if the left tree is closer to the snowman than right tree
                    self.if_left_front = True  # make a flag that a tree block the left way of snowman
                    self.if_right_front = False  # make a flag that no tree block the right way of snowman
                if smallest_right < smallest_left: # if the right tree is closer to the snowman than left tree
                    self.if_right_front = True  # make a flag that a tree block the right way of snowman
                    self.if_left_front = False  # make a flag that no tree block the left way of snowman
                if smallest_right == smallest_left: # if the distance between the right tree and snowman is equal to the distance between the left tree and snowman
                    self.if_right_front = True  # make a flag that a tree block the right way of snowman
                    self.if_left_front = False # make a flag that no tree block the left way of snowman

        # get if_close_left(if snowman can't go through the gap between the two tree)
        if self.close_left_side and self.if_right_front:  # if there is a tree in the left side of snowman and there is a tree in the right front of snowman
            smallest_close_left = self.smallest(self.close_left_side)  # get the distance between the snowman and the tree that closest to the snowman in the left side
            self.gap_left = self.rect.width - abs(smallest_right) + smallest_close_left  # see OneNote - Think with pencil - snowman - variable - gap_left
            # print("gap_left", self.gap_left)
            if self.gap_left <= self.rect.width:  # snowman may collide the tree in the left side(if gap_left smaller than the width of snowman)
                self.if_close_left = True  # make a flag that snowman may collide the tree in the leftside
                if self.close_left_side[smallest_close_left] != "left_wall" and self.close_left_side[smallest_close_left] != "right_wall":  # if this is a tree not a wall
                    self.frame_position.append(self.close_left_side[smallest_close_left].rect.topleft)  # frame this tree
                
            else:  # snowman will not collide the tree in the left side(if gap_left bigger than the width of snowman)
                self.if_close_left = False # make a flag that snowman will not collide the tree in the left side

        # get if_close_right(if snowman can't go through the gap between the two tree)
        if self.close_right_side and self.if_left_front: # if there is a tree in the right side of snowman and there is a tree in the left front of snowman
            smallest_close_right = self.smallest(self.close_right_side)  # get the distance between the snowman and the tree that closest to snowman in the right side
            self.gap_right = self.rect.width - abs(smallest_left) + smallest_close_right # see OneNote - Think with pencil - snowman - variable - gap_right
            # print("gap_right", self.gap_right)
            if self.gap_right <= self.rect.width:  # snowman may collide the tree in the right side(if gap_right smaller than the width of snowman)
                self.if_close_right = True  # make a flag that snowman my collide the tree in the right side
                if self.close_right_side[smallest_close_right] != "left_wall" and self.close_right_side[smallest_close_right] != "right_wall":  # if this is a tree not a wall
                    self.frame_position.append(self.close_right_side[smallest_close_right].rect.topleft) # frame this tree
                 
            else: # snowman will not collide the tree in the right side(if gap_right bigger than the width of snowman)
                self.if_close_right = False # make a flag that snowman will not collide the tree in the right side

        if [self.if_left_front,self.if_right_front,self.if_close_left,self.if_close_right] == [False,False,False,False]:
            pre = [False,False,False,False]
        if pre != [False,False,False,False] and pre != [self.if_left_front,self.if_right_front,self.if_close_left,self.if_close_right]:
            self.if_left_front = pre[0]
            self.if_right_front = pre[1]
            self.if_close_left = pre[2]
            self.if_close_right = pre[3]
      
    # after calculate
    # turn left or right depend on the value of variables(if_left/right_front, if_close_left/right)
    def action(self):
        # print(self.if_left_front, self.if_right_front, self.if_close_left, self.if_close_right)
        if self.if_close_right and self.if_left_front: # see OneNote - snowman - action
            self.turn(-1) # turn left
            # time.sleep(1)
        elif self.if_close_left and self.if_right_front: # see OneNote - snowman - action
            self.turn(1) # turn right
            # time.sleep(1)
        elif self.if_left_front and not self.if_close_right: # see OneNote - snowman - action
            self.turn(1) # turn right
            # time.sleep(1)
        elif self.if_right_front and not self.if_close_left: # see OneNote - in - action
            self.turn(-1) # turn left
            # time.sleep(1)
        elif not self.if_right_front and not self.if_left_front:  # if no tree block the way of snowman
            self.turn(-self.angle) # reset the angle of snowman

    def collide(self): # do some action after collide a tree or a flag
        global background_move
        # check the collide between obstacle in the group and the snowman
        snowman_hit = pygame.sprite.spritecollide(self, obstacles, False)  # put the result of checking into the snowman_hit
        if snowman_hit: # if obstacle collide with snowman
            if snowman_hit[0].type == "tree" and self.passed != snowman_hit[0]:  # if snowman collide the tree for the first time
                self.image = pygame.image.load(self.crash_image)  # change the image to the crash_image
                animate()  # display the new image
                # skier.stop_frame = 1 
                self.speed[1] = 0  # let the snowman stop
                self.if_hit = True  # make a flag that snowman collide the tree
                self.points -= 20   # minus the score of snowman
                self.passed = snowman_hit[0]  # make a flag that snowman collided this tree
            elif snowman_hit[0].type == "flag":  # if snowman collide the flag
                # print ("\nhit----points: ", points)
                snowman_hit[0].kill()  # remove the flag from the screen
                self.if_flag = True  # make a flag that snowman collide the flag
                self.points += 10  # plus the score of snowman

        if self.if_flag == True:    # if snowman collide the flag     
            hit_move_stop(self, background_move-3, "flag")
        if self.if_hit == True:    # if snowman collide the tree
            hit_move_stop(self, -background_move, "tree")

##        if smallest_left <= 0 and smallest_right > 0:
##            # print ("here", smallest_left, smallest_right)
##            if_wider = self.rect.width - abs(smallest_left) + smallest_right
##            
##            
##            if self.gap_left < self.rect.width:
##                self.keep_turn_left = True
##                print ("right_side tree:", self.close_right_side)
##                print("snowman: ", snowman.rect.top, snowman.rect.bottom)
##                time.sleep(2)
##            if self.keep_turn_left == True:
##                print ("keep_turn_left: ", self.keep_turn_left,"\n")
##                self.turn(-1)
##            elif if_wider >= snowman.rect.width:
##                self.turn(1)
##                print("---------------------")
##            elif if_wider < snowman.rect.width:
##                self.turn(-1)
##                print("---------------------")
##                
##        if smallest_right <= 0 and smallest_left > 0:
##            if_wider = self.rect.width - abs(smallest_right) + smallest_left
##            
##            
##            if self.gap_right < self.rect.width:
##                self.keep_turn_right = True
##                print ("left_side tree:", self.close_left_side)
##                print("snowman: ", snowman.rect.top, snowman.rect.bottom)
##                time.sleep(2)
##            if self.keep_turn_right == True:
##                print ("keep_turn_right: ", self.keep_turn_right, "\n")
##                self.turn(1)
##            elif if_wider >= snowman.rect.width:
##                self.turn(-1)
##                print("---------------------")
##            elif if_wider < snowman.rect.width:
##                self.turn(1)
##                print("---------------------")
##
##        if smallest_right > 0 and smallest_left > 0:
##            self.turn(-self.angle)
##        if self.right_tree:
##            if smallest_right > 0 and smallest_left > 0 or self.rect.top > self.right_tree.rect.bottom:
##                self.keep_turn_left = False
##        if self.left_tree:
##            if smallest_right > 0 and smallest_left > 0 or self.rect.top > self.left_tree.rect.bottom:
##                self.keep_turn_right = False
          
##class InvisibleSnowman(SnowmanClass):
##    def __init__(self):
##        pygame.sprite.Sprite.__init__(self)
##        SnowmanClass.__init__(self)
##        self.image = pygame.image.load("invisible_snowman.png")
##        self.rect = self.image.get_rect()
        
class ObstacleClass(pygame.sprite.Sprite):  # create the obstacle
    def __init__(self, image_file, location, type): 
        pygame.sprite.Sprite.__init__(self)  # initial pygame.sprite.Sprite
        # initial attributes
        self.image_file = image_file
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = type
        self.skier_passed = False
        self.distance = SCREEN_WIDTH

    def check_tree(self, who):   # put the tree that block the snowman into the dictionary
        close_distance = who.rect.left - 0    # change the close_distance to a "key"
        who.close_left_side[close_distance] = self   # initial\reset the who.close_left_side[close_distance]
        close_distance = SCREEN_WIDTH - who.rect.right   # change the close_distance into another "key"
        who.close_right_side[close_distance] = self   # initial\reset the who.close_right_side[close_distance]

        # get the distance between who side and tree side, then put it in dictionary - right/left_distance
        if self.rect.top - 100 <= who.rect.bottom and self.rect.top > who.rect.bottom and self.type == "tree":  # set the range of the tree that get into the dictionary
            if self.rect.centerx <= who.rect.centerx:   # check the centerx to see if the tree is on the left side of snowman
                distance = who.rect.left - self.rect.right   # calculate the distance between the left side of the snowman and the right side of the tree
                who.left_distance[distance] = self    # put the distance into the left_distance dictionary as a key and put the tree into dictionary as a value
            if self.rect.centerx > who.rect.centerx:    # check the centerx to see if the tree is on the right side of snowman
                distance = self.rect.left - who.rect.right   # calculate the distance between the right side of the snowman and the left side of the tree
                who.right_distance[distance] = self   # put the distance into the right_distance dictionary as a key and put the tree into dictionary as a value

        # close_distence is the distance from who-side to tree-side that is in range of who's top and bottom
        # put close_distance in dictionary - close_left/right_side
        if who.rect.top < self.rect.bottom and who.rect.bottom + 100 > self.rect.top and self.type == "tree":  # set the range of the tree that get into the dictionary
            if self.rect.left - who.rect.right >= 0:     # if the tree is on the right side of the snowman
                close_distance = self.rect.left - who.rect.right   # calculate the distance between the left side of the tree and the right side of the snowman
                who.close_right_side[close_distance] = self   # put the distance into the close_right_side dictionary as a key and put the tree into dictionary as a value
       
            if who.rect.left - self.rect.right >= 0:     # if the tree is on the left side of the snowman
                close_distance = who.rect.left - self.rect.right   # calculate the distance between the right side of the tree and the left side of the snowman
                who.close_left_side[close_distance] = self    # put the distance into the close_left_side dictionary as a key and put the tree into dictionary as a value

        # turn if the snowman get to the wall
        close_distance = who.rect.left - (0 + who.rect.width)   # calculate the distance between the left side of the snowman and the left wall
        if close_distance <= 0:    # if the snowman close to the left wall
            who.close_left_side[close_distance] = "left_wall"    # put distance in to the close_left_side dictionary as a key and put the "left_wall" str into the dictionary as a value
            # who.right_distance[close_distance] = "left_wall"     # put distance in to the right_distance dictionary as a key and put the "left_wall" str into the dictionary as a value
        close_distance = (SCREEN_WIDTH - who.rect.width) - who.rect.right   # calculate the distance between the right side of the wall and the right wall
        if close_distance <= 0:    # if the snowman close to the right wall
            who.close_right_side[close_distance] = "right_wall"  # put distance in to the close_right_side dictionary as a key and put the "right_wall" str into the dictionary as a value
            # who.left_distance[close_distance] = "right_wall"    # put distance in to the left_distance dictionary as a key and put the "right_wall" str into the dictionary as a value
                
    def update(self, times):   # change the centery of obstacles
        # if this is the first time of update
        if times == False:
            self.rect.centery -= background_move  # move the centery of each obstacle
        # if obstacle get out of the top of the screen    
        if self.rect.centery < -32:
            self.kill()  # remove this obstacle from the group
        # let each snowman do the check_tree method
        for who in who_list:
            self.check_tree(who)  # put the tree that block the snowman into the dictionary
                                    
def create_map():   # create a group of obstacles
    locations = []
    for i in range(35):
        row = random.randint(0, GRID)  # devide the screen into grid
        col = random.randint(0, GRID)  # devide the screen into grid
        location = [col * 64 + 20, row * 64 + 20 + SCREEN_WIDTH]  # set all location of tree/flag
        # create tree/flag
        if not (location in locations): # avoid overlap
            locations.append(location)
            type = random.choice(["tree", "flag"])  # choose type of obstacle
            if type == "tree": img = TREE_IMG    # make tree image
            elif type == "flag": img = FLAG_IMG   # make flag image
            obstacle = ObstacleClass(img, location, type)   # create a obstacle
            obstacles.add(obstacle)   # put the obstacle into the group 
            # print(hash(obstacle))
            
    for k in range (more_trees):   # create more trees
        row = random.randint(0, GRID)
        col = random.randint(0, GRID)
        location = [col * 64 + 20, row * 64 + 20 + SCREEN_WIDTH]
        if not (location in locations):
            locations.append(location)
            type = "tree" 
            img = TREE_IMG
            obstacle = ObstacleClass(img, location, type)
            obstacles.add(obstacle)

##    print ("\ncreate_map---- points: ", points)
##    print ("create_map---- more_trees", more_trees)
##    print ("create_map---- how many obstacles", len(obstacles.sprites()))
    
def animate():  # display the image on the screen
    screen.fill([255, 255, 255])  # fill the image with white color
    obstacles.draw(screen)  # draw obstacles on the screen
    score_x = 10  # initial/reset the score y position
    for who in who_list:  # do some action with each snowman
        screen.blit(who.image, who.rect)   # draw the snowman image on the screen
        
        invisible_rect = [who.rect.topleft[0], who.rect.topleft[1] + who.rect.height]  # set the 100_pixel's position
        # screen.blit(pixel_100, invisible_rect)  # draw 100_pixel on the screen

        if who.frame_position:  # if there is a frame need to draw
            for position in who.frame_position:  # take out each position of frame
                screen.blit(frame, position)  # draw the frame on the screen
    
        screen.blit(who.score_text, [score_x, 10])  # draw the score_text on the screen
        score_x += 370   # change the score y position
    
    pygame.display.flip()   # display all the change

def move_fore_back(who, fore_back, flag_or_tree):  # move the snowman down or up after collided obstacle
    if flag_or_tree == "flag":  # if snowman collide the flag
        who.rect.centery += fore_back   # move the snowman down
        None
            
    who.temp_frame -= 1  # count down

def hit_move_stop(who, fore_back, flag_or_tree):
    global base_speed
    if flag_or_tree == "flag":  # if snowman collide the flag
        if who.if_flag == True and who.temp_frame > 0:  # if snowman still in the range of collided flag
            move_fore_back(who, fore_back, flag_or_tree)  # move the snowman down or up after collided obstacle and count down
        if who.temp_frame <= 0 and who.if_flag == True:  # if the counter get to 0(snowman out of the range of collided flag) and the flag is true
            who.if_flag = False # switch the if_flag to false(make a flag that snowman haven't collide the flag)
            who.temp_frame = who.stop_frame  # reset the counter
            animate()  # display the change
                    
    if flag_or_tree == "tree":  # if snowman collide the tree
        if who.if_hit == True and who.temp_frame > 0:  # if snowman still in the range of collided tree
            move_fore_back(who, fore_back, flag_or_tree)  # move the snowman down or up and count down
            who.speed[1] = 0  # stop the snowman
        if who.temp_frame <= 0 and who.if_hit == True:  # if the counter get to 0(snowman out of the renge of collided tree) and the flag is true
            who.if_hit = False  # switch the if_hit to false(make a flag that snowman haven't collide the tree)
            who.temp_frame = who.stop_frame # reset the counter
            who.image = pygame.image.load(who.continue_image)  # restore the image
            who.speed = [0, base_speed]  # reset the angle and speed of snowman
            animate()  # display the change
     
def do_method(who):
    global update_times

    # initial the list of snowman
    who.left_distance = {}
    who.right_distance = {}
    who.close_right_side = {}
    who.close_left_side = {}
    who.frame_position = []

    # do the method of obstacles
    obstacles.update(update_times)  # move the obstacles up and do the check_tree method
    update_times = True  # make a flag that it have update once

    # do the method of the snowman
    who.calculate()  # calculate to switch snowman's attributes
    who.action()  # turn left or right depend on the value of variables(if_left/right_front, if_close_left/right)
    who.collide()  # do some action after snowman collide a tree or a flag

def score_display(who):  # change the text and position of snowman's score
    who.score_text = font.render(who.score_str +str(who.points), 1, (0, 0, 0))

def ending():
    score_x = SCREEN_WIDTH/6
    score_y = SCREEN_HEIGHT/4
    font = pygame.font.Font("img\\msyh.ttc", 20)
    screen.fill([0, 0, 0])
    highest = float('-inf')
    high_who = []
    for who in who_list:
        who.score_text = font.render(who.score_str +str(who.points), 1, (255, 255, 255))
        screen.blit(who.score_text, [int(score_x), int(score_y)])  # draw the score_text on the screen
        score_y += 40
        if who.points >= highest:
            if who.points > highest:
                high_who.clear()
                high_who.append(who.image)
            else:
                high_who.append(who.image)
            highest = who.points
    font = pygame.font.Font("img\\msyh.ttc", 20)
    end_text = font.render('GAME OVER, WINNER: ', 1, (255, 255, 255))
    screen.blit(end_text, [int(score_x), int(score_y+20)])
    for i in high_who:
        screen.blit(i, [int(score_x), int(score_y+100)])
        score_x += 100
    pygame.display.flip()
    
    ending = True
    while ending:
        for k in pygame.event.get():
            # print (k)
            if k.type == pygame.QUIT:  # quit button
                ending = False
                running = False
    return running

def beginning():
    count = 0
    
    score_x = SCREEN_WIDTH/2.7
    score_y = SCREEN_HEIGHT/5

    for i in who_list:
        screen.blit(i.image, [int(score_x), int(score_y)])
        score_x += 100

    score_x = SCREEN_WIDTH/6
    score_y = SCREEN_HEIGHT/2.5
    font = pygame.font.Font("img\\msyh.ttc", 20)
    begin_text = font.render('COMPETITION BETWEEN TWO SNOWMEN: ', 1, (255, 255, 255))
    screen.blit(begin_text, [int(score_x), int(score_y)])

    font = pygame.font.Font("img\\msyh.ttc", 20)
    begin_text2 = font.render('TIME: 1 MINUTES ', 1, (255, 255, 255))
    screen.blit(begin_text2, [int(score_x+100), int(score_y+50)])
        
    font = pygame.font.Font("img\\msyh.ttc", 23)
    begin_text1 = font.render('Press any key to continue', 1, (255, 255, 255))
    screen.blit(begin_text1, [int(score_x+55), int(score_y+100)])
        
    pygame.display.flip()

    beginning = True
    running = True
    while beginning:
        clock.tick(30)
        count += clock.get_time()

        if count/1000 > 5:
            beginning = False
        
        for k in pygame.event.get():
            # print (k)
            if k.type == pygame.KEYDOWN:
                beginning = False
            if k.type == pygame.QUIT:  # quit button
                beginning = False
                running = False
    return running
                
#-------------------------------------main program--------------------------------
SCREEN_WIDTH = GRID*40
SCREEN_HEIGHT = GRID*40

# initial snowmen
who_list = []
snowman0 = SnowmanClass([int(SCREEN_WIDTH / 6 * 1), 220], SNOWMAN0_IMG, SNOWMAN0_CRASH, SNOWMAN0_SCORE)
who_list.append(snowman0)
snowman1 = SnowmanClass([int(SCREEN_WIDTH / 6 * 4), 220], SNOWMAN1_IMG, SNOWMAN1_CRASH, SNOWMAN1_SCORE)
who_list.append(snowman1)
    
pygame.init() # initial pygame
screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])   # initial the screen
screen_rect = screen.get_rect()   # get the attributes of screen
clock = pygame.time.Clock()    # set clock

create_map()   # call the create_map() function

##font = pygame.font.Font("img\\msyh.ttc", 20)  # set font
### set score text
##start1_text = font.render("If your score less or equal than -200,",1, (255, 255, 255))
##start2_text = font.render("the game will over, you will lost.",1, (255, 255, 255))
### fill the screen with black
##screen.fill([0,0,0])
### put the score text on the screen
##screen.blit(start1_text, [120,200])
##screen.blit(start2_text, [130,230])
##pygame.display.flip()
# time.sleep(5)

# set font
font = pygame.font.Font("img\\msyh.ttc", 20)

#temp_frame = skier.stop_frame

# ------------------------------------------main program----------------------------------------------
running = beginning()

k_space_down = False
while running:
    clock.tick(30)
    # pause button act
##    if k_space_down == False:
##        clock.tick(30)
##    if k_space_down == True:
##        clock.tick(1)
    # get event(keyboard or mouse)
    for k in pygame.event.get():
        # print (k)
        if k.type == pygame.QUIT:  # quit button
            running = False

        # pause button
        if k.type == pygame.KEYDOWN and k_space_down == False:
            if k.key == pygame.K_SPACE:
                k_space_down = True
        elif k.type == pygame.KEYDOWN and k_space_down == True:
            if k.key == pygame.K_SPACE:
                k_space_down = False
                
##        if k.type == pygame.KEYDOWN:
##            if k.key == pygame.K_LEFT:
##                skier.turn(-1)
##            elif k.key == pygame.K_RIGHT:
##                skier.turn(1)
    
##    if background_move != 6 and background_move != 12 and background_move != 2:
##        print ("background:", background_move, "snowman speed",snowman.speed[1], "base_speed", base_speed)

#---------------------skier--------------------------------------

##    skier.left_right()  # move to left or right
##    # background_move = skier.speed[1]
##
##    hit = pygame.sprite.spritecollide(skier, obstacles, False)
##    if hit:
##        # print (hit[0])
##        # time.sleep(6000)
##        if hit[0].type == "tree" and not hit[0].skier_passed:
##            points = points - 100
##            skier.image = pygame.image.load("skier_crash.png")
##            animate()
##            # skier.stop_frame = 1
##            before_change = skier.speed[1]
##            skier.speed[1] = skier.speed[1] - skier.speed[1]
##            skier.if_hit = True 
##            hit[0].skier_passed = True
##        elif hit[0].type == "flag" and not hit[0].skier_passed:
##            points += 10
##            before_change = skier.speed[1]
##            skier.speed[1] = skier.speed[1] * 2
##            hit[0].kill()
##            skier.if_flag = True
##
##    if skier.if_flag == True:        
##        hit_move_stop(skier, skier.speed[1], "flag")
##    if skier.if_hit == True:
##        hit_move_stop(skier, -skier.speed[1], "tree")
         
#---------------------------snowman-----------------------------------
    # choose a fastest snowman
    fastest = None
    for who in who_list:
        if fastest == None:
            fastest = who
        if fastest != None:
            # compare the y positon
            if fastest.rect.bottom < who.rect.bottom:
                fastest = who

    # check the position of fastest snowman
    if fastest != None:
        if fastest.rect.bottom > SCREEN_WIDTH / 4 * 3:   # if fastest snowman get down to the screen's button
            background_move = 6 + 4    # let the fastest snowman move up by change the background_move
        elif fastest.rect.bottom < SCREEN_WIDTH / 4 * 1:   # if fastest snowman get up to the screen's top
            background_move = 6 - 4    # let the fastest snowman move down by change the backgroun_move
        elif fastest.rect.bottom < SCREEN_WIDTH / 4 * 3 and fastest.rect.bottom > SCREEN_WIDTH / 4 * 1: # if fastest snowman get middle of the screen
            background_move = 6     # let the background_move back to initial value

    # regulate the snowman's y position
    for who in who_list:  
        if background_move != who.speed[1]:   # let background_move compare with snowman's speed
            who.rect.centery += (who.speed[1] - background_move)  # regulate snowman's y position
        
        who.left_right() # let snowman move left or right according to it's speed

    # count the map_position
    map_position += background_move
    
    if map_position >=SCREEN_WIDTH:   # check map position
        create_map()   # create a new map under the screen if the previous map fill the whole screen
        map_position = 0    # reset the map_position

    # initial update_times
    update_times = False

    # do the method of each snowman
    for who in who_list:   
        do_method(who)   # do the method of snowman

    for who in who_list:
        score_display(who)  # change the text and position of snowman's score

    animate()  # display all the change
    
    count += clock.get_time()        
    if count/1000/60 >= 1:
        running = ending()
                  
pygame.quit()  # close the window


            
        

    



    






























