#N-BODY GRAVITY SIMULATION BY AMARNATH

import  pygame as pg 
import numpy as np 

pg.init()

wScreen = 1200
hScreen = 624

pg.display.set_caption("N-Body Gravity Simulation")
win = pg.display.set_mode((wScreen, hScreen))

font = pg.font.SysFont('calibri', 18)
font2 = pg.font.SysFont('calibri', 16)

class body(object):
    
    def __init__(self, x, y, color, mass, static):
        self.density = 100
        self.mass = mass
        self.x = x
        self.y = y
        self.color = color
        self.radius = self.calc_r()
        self.velx = 0
        self.vely = 0
        self.static = static

    def calc_r(self):
        self.radius = 10 * np.cbrt(self.mass/self.density)
        return self.radius
        
    def draw(self, win):
        pg.draw.circle(win, self.color, (self.x,self.y), self.radius)
    
    def move(self, t):
        self.x += self.velx * t
        self.y += self.vely * t

    def masstxt(self):
        mass_txt = str(np.round(self.mass,1))
        mass_img = font2.render(mass_txt, True, self.color)
        win.blit(mass_img, (self.x - 10, self.y - 20))

    def veltxt(self):
        if self.static == False:
            v_txt = str((np.sqrt((self.velx**2) + (self.vely**2))).round(2))
            v_img = font2.render(v_txt, True, self.color)
            win.blit(v_img,(self.x + 5, self.y + 5))


#ARRAY TO STORE THE PARTICLES:
bn = [] 

#IMPORTING REQUIRED IMAGES:
play_icon = pg.image.load('widgets/play.png').convert()
pause_icon = pg.image.load('widgets/pause.png').convert()
question_icon = pg.image.load('widgets/question.png').convert()
grid = pg.image.load('widgets/grid.png').convert()
grid_icon = pg.image.load('widgets/gridicon.png').convert()
background = pg.image.load('widgets/background.png').convert()
icon = pg.image.load('widgets/icon.png')
pg.display.set_icon(icon)
grid.set_alpha(100)

#FUNCTION TO CALCULATE POSITION VECTOR BETWEEN TWO PARTICLES:
def distance(x1, y1, x2, y2):
    
    dist_x = x2 - x1
    dist_y = y2 - y1
    return dist_x, dist_y

#FUNCTION TO CALCULATE VELOCITY OF A PARTICLE DUE TO GRAVITY:
def gravity(m1,m2, rx, ry, vx , vy, t):
    G = 0.01
    soft = 0.001
    r = np.sqrt((rx**2) + (ry **2))
    Fx = (G * m1 * m2 * rx)/(soft + r **2)
    Fy = (G * m1 * m2 * ry)/(soft + r **2)
    gx = Fx/m1
    gy = Fy/m1    
    vx = gx * t
    vy = gy * t      
    return [vx, vy]

#FUNCTION TO DISPLAY AND UPDATE THE WINDOW
def updateWindow():
    
    pg.display.update()
    win.fill((0,0,0))
    if gridvis:
        win.blit(grid, (0,0))
    for i in bn:
        i.draw(win)
        if disp_m:
            i.masstxt()
        if disp_vel:
            i.veltxt()
    win.blit(particles_img, (20,20))
    win.blit(aparticles_img, (20,40))
    win.blit(play_icon,((wScreen/2) - 15, hScreen - 50))
    win.blit(pause_icon,((wScreen/2) - 15, hScreen - 50))
    win.blit(mass_img,(20,hScreen - 40))
    if info:
        win.blit(background,(0,0))
    else:
        win.blit(question_icon,(wScreen - 50,20))
    win.blit(grid_icon,(wScreen - 50,hScreen - 40))
    
#INITIAL VALUES:    
run = True
lines = False
play = False
info = False
gridvis = False
disp_vel = False
disp_m = False
pparticles = 0
aparticles = 0
masstype = 'RANDOM'
play_alpha = 0
pause_alpha = 0

while(run):

    #it = 0
    t = 0.1

    #TEXT FOR NUMBER OF POSITIVE PARTICLES:
    particles_txt = "POSITIVE PARTICLES: " + str(pparticles)
    particles_img = font.render(particles_txt, True, "#FFFFFF")
    #TEXT FOR NUMBER OF NEGATIVE PARTICLES:
    aparticles_txt = "NEGETIVE PARTICLES: " + str(aparticles)
    aparticles_img = font.render(aparticles_txt, True, "#FFFFFF")
    #TEXT FOR MASS TYPE:
    mass_txt = "MASS: " + masstype
    mass_img = font.render(mass_txt, True, "#FFFFFF")
  
    radx = []
    rady = []
    if play == True:
        for i in bn:
            dx = []
            dy = []
            for j in bn:
                if i != j and i.static == False:
                    drx, dry = distance(i.x, i.y, j.x, j.y)
                    vx,vy = gravity(i.mass,j.mass, drx, dry, i.velx, i.vely, t)
                    dx.append(vx)
                    dy.append(vy)

                    if info == False and lines:
                        pg.draw.line(win,(255,255,255), (i.x,i.y),(j.x,j.y))

            radx.append(sum(dx))
            rady.append(sum(dy))
            
            i.velx += radx[bn.index(i)]
            i.vely += rady[bn.index(i)]
            i.move(t)
        
    updateWindow()

    capslock = pg.key.get_mods() & pg.KMOD_CAPS   
    mouse = pg.mouse.get_pos()
    alt = pg.key.get_mods() & pg.KMOD_ALT

    for event in pg.event.get():  
        #CLOSE BUTTON:      
        if event.type == pg.QUIT:       
            run = False

        #TO SPAWN PARTICLES:
        if event.type == pg.MOUSEBUTTONDOWN and ((wScreen - 20) > mouse[0] > (wScreen - 50) and 50 > mouse[1] > 20) == False and ((hScreen - 10) > mouse[1] > (hScreen - 50)) == False and info == False:
            if alt:
                static = True
                color = '#33ff33'
            else:
                static = False
                color = '#00ffff'
            #TO SPAWN POSITIVE PARTICLES:
            if event.button == 1:
                bn.append(body(mouse[0],mouse[1], color, m, static))
                pparticles += 1
            #TO SPAWN NEGATIVE PARTICLES:
            if event.button == 3:
                bn.append(body(mouse[0],mouse[1], color, m, static))
                bn[-1].mass *= -1
                if static == True:
                    bn[-1].color = '#ffbb00'
                else:
                    bn[-1].color = '#ff0000'
                aparticles += 1
                
        #TO DISPLAY INFO:
        if event.type == pg.MOUSEBUTTONDOWN and ((wScreen - 20) > mouse[0] > (wScreen - 50) and 50 > mouse[1] > 20) == True: 
            info = not info
            
        #TO DISPLAY GRID:
        if event.type == pg.MOUSEBUTTONDOWN and (wScreen - 10) > mouse[0] > (wScreen - 50) and (hScreen - 10) > mouse[1] > (hScreen - 50):
            gridvis = not gridvis

        #KEYBOARD INPUTS:              
        if event.type == pg.KEYDOWN:
                if event.key == pg.K_l:
                    lines = not lines

                if event.key == pg.K_z and len(bn) > 0:
                    if (bn[-1].mass)/abs(bn[-1].mass) == 1:
                        pparticles -= 1
                    else:
                        aparticles -= 1
                    bn.remove(bn[-1])
                    
                if event.key == pg.K_DELETE:
                    bn.clear()
                    aparticles = 0
                    pparticles = 0

                if event.key == pg.K_SPACE:
                    play = not play
                    if play == True:
                        play_alpha = 255
                    else:
                        pause_alpha = 255

                if event.key == pg.K_ESCAPE:
                    run = False
                if event.key == pg.K_v:
                    disp_vel = not disp_vel 
                if event.key == pg.K_m:
                    disp_m = not disp_m

        #SET MASS TYPE:        
        if capslock:
            m = 5
            masstype = 'CONSTANT'
        else: 
            m = 10 * np.random.uniform(0.1, 1)
            masstype = 'RANDOM'
            
    if play_alpha > 0:
        play_alpha -= 1
    if pause_alpha > 0:
        pause_alpha -= 1

    play_icon.set_alpha(play_alpha)
    pause_icon.set_alpha(pause_alpha)
    
pg.quit()