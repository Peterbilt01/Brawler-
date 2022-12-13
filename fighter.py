import pygame

class Fighter():
    def __init__(self,player,x,y,flip,data,sprite_sheet,animation_steps,sound):
        self.player=player
        self.size=data[0]
        self.image_scale=data[1]
        self.offset=data[2]
        self.flip=flip      
        self.animation_list=self.load_images(sprite_sheet,animation_steps)
        self.action=0 #0 : idle, 1: run 2: jump, 3: attack1, 4: attack2, 5: hit ,6 :death
        self.frame_index=0
        self.image=self.animation_list[self.action][self.frame_index]
        self.update_time=pygame.time.get_ticks()
        self.rect=pygame.Rect((x,y,80,180))
        self.vel_y=0
        self.running=False
        self.jump=False
        self.atacking=False
        self.attack_type=0
        self.attack_cooldown=0
        self.hit=False
        self.alive=True
        self.attack_sound=sound
        self.health=100
        
    def load_images(self, sprite_sheet, animation_steps):
        #extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)                
                temp_img_list.append(pygame.transform.scale(temp_img,(self.size*self.image_scale,self.size*self.image_scale)))
                # temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        # print(animation_list)
        return animation_list
    #handle animation
    def upadte(self):
        #check what action the player is perfroming
        if self.health<=0:
            self.health=0
            self.alive=False
            self.update_action(6)#death
        elif self.hit==True:
            self.update_action(5) #hit
        
        elif self.atacking==True:
            if self.attack_type==1:
                self.update_action(3) #attack1
            elif self.attack_type==2:
                self.update_action(4) #attack2

        elif self.jump==True:
            self.update_action(2) # jump

        elif self.running==True:
            self.update_action(1) #run
        else:
            self.update_action(0) #idle



        animation_cooldown=60
        #update images
        self.image=self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks()-self.update_time>animation_cooldown:
            self.update_time=pygame.time.get_ticks()
            self.frame_index+=1
        #check if animation has run out
        if self.frame_index>=len(self.animation_list[self.action]):
            #check the player is dead
            if self.alive==False:
                self.frame_index=len(self.animation_list[self.action])-1
            else:
            
            
                self.frame_index=0
                if self.action==3 or self.action==4:
                    self.atacking=False
                    self.attack_cooldown=20
                #if damage was taken
                if self.action==5:
                    self.hit=False
                    #if the player b/w thw attack and hit animation
                    self.atacking=False
                    self.attack_cooldown=20
                    self.frame_index=len(self.animation_list[self.action])-1

    def move(self,screen_w,screen_h,surface,target,round_over):
        SPEED=10
        dx=0
        dy=0
        gravity=2
        self.running=False
        self.attack_type=0
        #get key press
        key=pygame.key.get_pressed()
        # can onlyperform other action if not attacing
        if self.atacking==False and self.hit==False and self.alive==True and round_over==False:
            #check player  controls
            if self.player==1:
            #movement player 1
                if key[pygame.K_a]:
                    dx=-SPEED
                    self.running=True
                if key[pygame.K_d]:
                    dx=+SPEED
                    self.running=True
                
                #jumping
                if key[pygame.K_w] and self.jump==False:
                    self.vel_y=-35
                    self.jump=True
                
                #attacks
                if key[pygame.K_r] or key[pygame.K_t] :
                    
                    self.attack(target)
                    if key[pygame.K_r]:
                        self.attack_type=1
                    if key[pygame.K_t]:
                        self.attack_type=2
            if self.player==2:
                #movement player 2
                if key[pygame.K_LEFT]:
                    dx=-SPEED
                    self.running=True
                if key[pygame.K_RIGHT]:
                    dx=+SPEED
                    self.running=True
                
                #jumping
                if key[pygame.K_UP] and self.jump==False:
                    self.vel_y=-35
                    self.jump=True
                
                #attacks
                if key[pygame.K_KP1] or key[pygame.K_KP2] :
                    
                    self.attack(target)
                    if key[pygame.K_KP1]:
                        self.attack_type=1
                    if key[pygame.K_KP2]:
                        self.attack_type=2

        #apply gravity
        self.vel_y+=gravity
        dy+=self.vel_y      


        # ensure player stays on screen 
        if self.rect.left+dx<0:
            dx=0+self.rect.left

        if self.rect.right+dx>screen_w:
            dx=screen_w-self.rect.right
        if self.rect.bottom+dy> screen_h-110:
             self.vel_y=0
             self.jump=False
             dy=screen_h-110-self.rect.bottom
        
        #ensureplayers face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip=False
        else:
            self.flip=True
        #apply attack cooldown
        if self.attack_cooldown>0:
            self.attack_cooldown-=1

        #update player position
        self.rect.x+=dx
        self.rect.y+=dy

    def attack(self,target):
        if self.attack_cooldown==0:
            # execute attack
            self.atacking=True
            self.attack_sound.play()
            attacking_rect=pygame.Rect(self.rect.centerx-(2*self.rect.width*self.flip),self.rect.y,2*self.rect.width,self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health-=5
                target.hit=True
            # pygame.draw.rect(surface,(0,255,0),attacking_rect)
        

    def update_action(self,new_action):
        if new_action!=self.action:
            self.action=new_action
            self.frame_index=0
            self.update_time=pygame.time.get_ticks()

    def draw(self,surface):
        img=pygame.transform.flip(self.image,self.flip,False)
        # pygame.draw.rect(surface,(255,0,0),self.rect)
        surface.blit(img,(self.rect.x-(self.offset[0] *self.image_scale),self.rect.y-(self.offset[1] *self.image_scale)))