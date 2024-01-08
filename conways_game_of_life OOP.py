import pygame as pg
import pygame_widgets
from pygame_widgets.button import Button
pg.font.init()
pg.init()
#Size of our pygame window
width=600
height=600

subwidth=200
subheight=100

linecolor=(200,200,200)

STARTBUTTONlength=200
STARTBUTTONheight=50
STARTBUTTONcoord=(width/2-subwidth/2-200,height+subheight/2-20)
BUTTONspacing=10
START=False
if START==True:
    STARTBUTTONtext="STOP"
else:
    STARTBUTTONtext="START"
#No. of rows and column
n_X=40
n_Y=40
#length and breadth of each cell
l=width/n_X
b=height/n_Y
#Make our screen/window
win=pg.display.set_mode((width+subwidth,height+subheight),0,32)
pg.display.set_caption("Game Of Life")
run=True
#Set Tick speed (FPS=1000/delay)
delay=50

#Cells alive in beginning
#alivecells=[[0,0],[2,3],[3,4],[4,2],[4,3],[4,4]]
alivecells=[[2,6],[3,6],[2,7],[3,7],[36,4],[37,4],[36,5],[37,5],[12,6],[12,7],[12,8],[13,5],[13,9],[14,4],[15,4],[14,10],[15,10],[16,7],[17,5],[17,9],[18,6],[18,7],[18,8],[19,7],[22,4],[22,5],[22,6],[23,4],[23,5],[23,6],[24,3],[24,7],[26,2],[26,3],[26,7],[26,8]]
totalactivecells=len(alivecells)
cellstobeadded=[]
cellstoberemoved=[]
impcells=[]
Font=pg.font.SysFont('timesnewroman',15)
#Find no. of neighbours of a cell
def check(X,Y):
    count=0
    present=[X,Y] in alivecells
    for x in range(X-1,X+2):
        for y in range(Y-1,Y+2):
            if not (x==X and y==Y):    
                if [x,y] in alivecells:     
                    count=count+1      
                else:
                    count=count+0
                    
    if present:
        if count==2 or count==3:
            cellstobeadded.append([X,Y])
        else:
            cellstoberemoved.append([X,Y]) 
    if not present:
        if count==3:
            cellstobeadded.append([X,Y])

#Add the important cells(i.e. Alive cells and its neighbours) to a list
def addtoimp():
    for cell in alivecells:
        X=cell[0]
        Y=cell[1]
        if not [X,Y] in impcells:
            #To make sure there are no duplicates of active cell in list
            for x in range(X-1,X+2):
               for y in range(Y-1,Y+2):    
                    if not [x,y] in impcells:
                        #To make sure there are no duplicates of neighbour cell that already came from different alive cell 
                        impcells.append([x,y]) 
def modifyalivecells():
    #In the end you need to remove or add alive cells in the list ofc
    for cell in cellstobeadded:
        if cell not in alivecells:
            alivecells.append(cell)
    for cell in cellstoberemoved:
        if cell in alivecells:
            alivecells.remove(cell)
        
pg.font.Font="Calibri"           
def drawstuff():
    global totalactivecells
    visibleactivecells=0
    for activecell in alivecells:
        X=activecell[0]
        Y=activecell[1]
        if X<=width/l -1 and Y<=height/b-1 and X>=0 and Y>=0:
            pg.draw.rect(win,(255,255,0),(X*l+1,Y*b+1,l-1,b-1))      #Draw the active cells
            visibleactivecells=visibleactivecells+1
      
    pg.draw.rect(win,(100,100,100),(0,n_Y*b,width+subwidth,subheight))
    pg.draw.rect(win,(80,80,80),(n_X*l,0,subwidth,height))
    for X in range(0,n_X+1):
        pg.draw.line(win,linecolor,(X*l,0),(X*l,height),2)    #Draw the vertical lines
    for Y in range(0,n_Y+1):
        pg.draw.line(win,linecolor,(0,Y*b),(width,Y*b),2)     #Draw the horizontal lines
    win.blit(pg.font.SysFont('timesnewroman',25).render("INFO", False, (255,255,255), (80,80,80)), (width+10,10))
    win.blit(Font.render("FPS : "+str(int(1000/delay)), False, (255,255,255), (80,80,80)), (width+10,40))
    win.blit(Font.render("Total Alive : "+str(totalactivecells), False, (255,255,255), (80,80,80)), (width+10,60))
    win.blit(Font.render("Alive In View : "+str(visibleactivecells), False, (255,255,255), (80,80,80)), (width+10,80))
    
def changebutton():
    global STARTBUTTONtext
    global START
    if STARTBUTTONtext=="START":
        STARTBUTTONtext="STOP"
        START=True
    elif STARTBUTTONtext=="STOP":
        STARTBUTTONtext="START"
        START=False
        
def drawactivecells(mousex,mousey):
    global cellstobeadded,cellstoberemoved
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONUP:
            Xcoord=int(mousex/l)
            Ycoord=int(mousey/l)
            if not [Xcoord,Ycoord] in alivecells:
                cellstobeadded.append([Xcoord,Ycoord])
            if [Xcoord,Ycoord] in alivecells:
                cellstoberemoved.append([Xcoord,Ycoord])
                
def clrscreen():
    global alivecells,impcells,cellstobeadded,totalactivecells
    alivecells=[]
    impcells=[]
    cellstobeadded=[]
    totalactivecells=0
    
def close():
    global run
    run=False
    
while run:
    pg.time.delay(delay)
    win.fill((0,0,0))
    mousex, mousey = pg.mouse.get_pos()
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            run= False
    if START==True:       
        cellstobeadded=[]
        cellstoberemoved=[]
        
        addtoimp()
        totalactivecells=len(alivecells)
        
        #Apply the game of life conditions on all important cells
        for cell in impcells:
            check(cell[0],cell[1])       
    drawstuff()
    STARTButton = Button(win,STARTBUTTONcoord[0],STARTBUTTONcoord[1],STARTBUTTONlength,STARTBUTTONheight,text=STARTBUTTONtext,fontSize=50,margin=20,inactiveColour=(200, 50, 0),hoverColour=(150, 0, 0),pressedColour=(0, 200, 20),radius=20,onClick=lambda:changebutton())
    CLRScreenButton=Button(win,STARTBUTTONcoord[0]+BUTTONspacing+STARTBUTTONlength,STARTBUTTONcoord[1],STARTBUTTONlength,STARTBUTTONheight,text="CLEAR",fontSize=50,margin=20,inactiveColour=(200, 50, 0),hoverColour=(150, 0, 0),pressedColour=(0, 200, 20),radius=20,onClick=lambda:clrscreen())   
    CLOSEButton = Button(win,STARTBUTTONcoord[0]+2*BUTTONspacing+2*STARTBUTTONlength,STARTBUTTONcoord[1],STARTBUTTONlength,STARTBUTTONheight,text="CLOSE",fontSize=50,margin=20,inactiveColour=(200, 50, 0),hoverColour=(150, 0, 0),pressedColour=(0, 200, 20),radius=20,onClick=lambda:close())

    pygame_widgets.update(events)
    modifyalivecells()          #After the conditions are applied remove or add the required cells
    impcells=[]
    drawactivecells(mousex,mousey)
    if run==False:
        pg.quit()
        break
    pg.display.update()         #Refresh the screen
pg.quit()
