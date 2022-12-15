import pygame
import os
from fighter import Fighter
from pygame import mixer


mixer.init()
pygame.init()

screen_width=1000
screen_height=600

#load music
pygame.mixer.music.load(os.path.join("assets\\audio","music.mp3"))
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play(-1)
sward_fx = pygame.mixer.Sound(os.path.join("assets\\audio","sword.wav"))
sward_fx.set_volume(0.8)
magic_fx = pygame.mixer.Sound(os.path.join("assets\\audio","magic.wav"))
magic_fx.set_volume(0.9)



screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Brawler")
pygame.display.set_icon(pygame.image.load(os.path.join("icon","icon.svg")))
#set frame rate
clock=pygame.time.Clock()
FPS=60

#define colors
YELLOW=(255,255,0)
RED=(255,0,0)
WHITE=(255,255,255)


#define game variables
intro_count=5
last_count_update=pygame.time.get_ticks()
score=[0,0] #player scores
round_over=False
Round_over_cooldown=2000
#define fighter varable
warrior_size=162
warrior_scale=4
warrior_offset=[72,56]
warrior_data=[warrior_size,warrior_scale,warrior_offset]
wizard_size=250
wizard_scale=3
wizard_offset=[112,107]
wizard_data=[wizard_size,wizard_scale,wizard_offset]

#loadimages
bg_image=pygame.image.load(os.path.join("assets\\images\\background","background.jpg")).convert_alpha()
#load sprite sheets
warrior_sheet=pygame.image.load(os.path.join("assets\\images\\warrior\\sprites","warrior.png")).convert_alpha()
wizard_sheet=pygame.image.load(os.path.join("assets\\images\\wizard\\sprites","wizard.png")).convert_alpha()
victory=pygame.image.load(os.path.join("assets\\images\\icons","victory.png")).convert_alpha()

#define no of steps in each animation
Warrioe_animation_steps=[10,8,1,7,7,3,7]
wizard_animation_steps=[8,8,1,8,8,3,7]
# define font 
count_font=pygame.font.Font(os.path.join("assets\\fonts","turok.ttf"),180)
score_font=pygame.font.Font(os.path.join("assets\\fonts","turok.ttf"),30)

#function for drawing text
def draw_text(text,font,text_col,x,y):
    img=font.render(text,True,text_col)
    screen.blit(img,(x,y))


# function for drawing background
def draw_bg():
    scaled_bg=pygame.transform.scale(bg_image,(screen_width,screen_height))
    screen.blit(scaled_bg,(0,0))

#function for heatth bar 
def draw_health(health,x,y):
    ratio=health/100
    pygame.draw.rect(screen,WHITE,(x-4,y-4,408,38))
    pygame.draw.rect(screen,RED,(x,y,400,30))
    pygame.draw.rect(screen,YELLOW,(x,y,400*ratio,30))


#creater two instaces
fighter_1=Fighter(1,200,310,False,warrior_data,warrior_sheet,Warrioe_animation_steps,sward_fx)
fighter_2=Fighter(2,700,310,True,wizard_data,wizard_sheet,wizard_animation_steps,magic_fx)




#game loop
run=True
while run:
    clock.tick(FPS)
    draw_bg()
    #draw score
    draw_text("P1 : "+str(score[0]),score_font,RED,20,60)
    draw_text("P2 : "+str(score[1]),score_font,RED,580,60)
    #playerhealth
    draw_health(fighter_1.health,20,20)
    draw_health(fighter_2.health,580,20)
    if intro_count<=0:
        #move fighter
        fighter_1.move(screen_width,screen_height,screen,fighter_2,round_over)
        fighter_2.move(screen_width,screen_height,screen,fighter_1,round_over)
    else:
        #display count timer
        draw_text(str(intro_count),count_font,RED,screen_width/2,screen_height/3)
        if pygame.time.get_ticks()-last_count_update>=1000:
            intro_count-=1
            last_count_update=pygame.time.get_ticks()
            print(f" are you ready {intro_count} ")
        if intro_count==0:
            print(" GO ! fight !")
              
    

    
    # fighter_2.move()
    #update fighter
    fighter_1.upadte()
    fighter_2.upadte()
    #draw fighter
    fighter_1.draw(screen)
    fighter_2.draw(screen)
    #check for player defeat
    if round_over==False:
        if fighter_1.alive==False:            
            score[1]+=1
            round_over=True
            Round_over_cooldown=pygame.time.get_ticks()
            print(score)
        elif fighter_2.alive==False:            
            score[0]+=1
            round_over=True
            Round_over_cooldown=pygame.time.get_ticks()
    else:
        screen.blit(victory,(screen_width/2-100,screen_height/2-100))
        if pygame.time.get_ticks()-Round_over_cooldown>=3000:
            fighter_1=Fighter(1,200,310,False,warrior_data,warrior_sheet,Warrioe_animation_steps,sward_fx)
            fighter_2=Fighter(2,700,310,True,wizard_data,wizard_sheet,wizard_animation_steps,magic_fx)
            round_over=False
            intro_count=5
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
            
            
    #update display function
    pygame.display.update()      
pygame.quit()