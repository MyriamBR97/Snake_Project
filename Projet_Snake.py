
# Binome: BEREKSI REGUIG Myriam et Bile Isaac Ama
# Les boutons de la souris et les 4 flèches du clavier sont utilisables

from tkinter import *
from random import *
import time

# Constantes du jeu
larg_can, long_can = 500,500
T_CASE = 20
MARGE = 20
NB_COL = (larg_can-MARGE) / T_CASE
NB_LIG = (long_can-MARGE) / T_CASE
NB_CASES = NB_COL*NB_LIG
NUM_CASE = NB_COL * NB_LIG + NB_COL
NORD, EST, SUD, OUEST = 0,1,2,3
COULEUR = ['coral1','coral2','coral3','coral4','tomato1']   # couleurs du serpent et de food

# variables globales du serpent et food
snake = []
direction = 0
food_num_case = randrange(NB_CASES)
score = 0
liste_pos_tail = []
new_liste=[]

# La variable global running permet de lancer le jeu ou de le mettre en pause
running = True

# variables globales interface
jeu_bouton = {}
jeu_frame = {}
jeu_canvas = {}
jeu_label = {}

fenApp = Tk()
peuple_fr = Frame(fenApp, bg="burlywood1")
peuple_jeu = Frame(peuple_fr)
peuple_gestion = Frame(peuple_fr, bg="burlywood1")
peuple_score = Frame(peuple_fr, bg="burlywood1")
Grille_NB=Canvas(fenApp,width=long_can, height=larg_can, bg="burlywood1")

########################### fin variables ###########################

########################### fonctions ##############################

def case_to_lc(num_case):
    num_col = num_case % NB_COL
    num_lig = (num_case - num_col) / NB_COL
    return (num_lig, num_col)
    
def lc_to_case(num_lig, num_col):
    num_case = num_lig * NB_COL + num_col
    return num_case

def xy_to_lc(x, y):
    num_col = (x - MARGE)/T_CASE
    num_lig = (y - MARGE)/T_CASE
    return (num_lig, num_col)

def lc_to_xy(num_lig, num_col):
    x = MARGE + num_col*T_CASE
    y = MARGE + num_lig*T_CASE
    return (x,y)

def case_to_xy(num_case):
    l,c = case_to_lc(num_case)
    return lc_to_xy(l,c)
    
def xy_to_case(x, y):
    l,c = xy_to_lc(x, y)
    num_case =  lc_to_case(l,c)
    return num_case

def case_suivante(num_case, sens, nb_cases=1):  # sur un tore   # transformer en lc , pour aller à gauche -1 % nb_col
    l, c = case_to_lc(num_case)
    if sens == NORD:
        new_l = (l-nb_cases)%NB_LIG
        new_c = c
    if sens == EST:
        new_l = l
        new_c = (c+nb_cases)%NB_COL
    if sens == SUD:
        new_l = (l+nb_cases)%NB_LIG
        new_c = c
    if sens == OUEST:
        new_l = l
        new_c = (c-nb_cases)%NB_COL
    return lc_to_case(new_l, new_c)
        
def pivot_horaire(nb=1):
    return (direction+nb)%4

#callbacks
def quitter():
    fenApp.quit()
    fenApp.destroy()

def lancer(_):              # Lance le serpent dans une direction à un endroit aléatoirement déterminer par init_serpent
    init_serpent()
    peuble_jeu(jeu_canvas['canvas'])
    while running==True:
        avance()
        fenApp.update()
        jeu_label["score"].configure(text="SCORE :" + str(score))
        time.sleep(0.2)
        fenApp.unbind("<space>")

def reset():                          # reinitialiser le jeu
    global score,running
    running = True
    Grille_NB.delete(ALL)
    snake.clear()
    liste_pos_tail.clear()
    new_liste.clear()
    score = 0
    fenApp.bind("<space>", lancer)
    jeu_label["command"].configure(text="Appuiyer sur la touche espace pour lancer le serpent ! ")
    reset_interface()

def pause(): # avec le bouton pause
    global running
    if running == False:
        return perdu()
    jeu_label["command"].configure(text="Pause ! Appuiyer sur le bouton PLAY pour relancer le serpent !")
    running = False
    no_peuble_jeu(jeu_canvas['canvas'])
    
def play(): # avec le bouton play
    global running
    jeu_label["command"].configure(text="Appuiyer sur la touche espace pour lancer le serpent ! ")
    running = True
    fenApp.bind("<space>",  lancer)

def perdu():
    global running
    running = False
    jeu_label["command"].configure(text="vous avez PERDU ! Appuiyez sur RESET pour recommencer")
    no_peuble_jeu(jeu_canvas['canvas'])
    Grille_NB.delete(ALL)
    
def tourne_gauche(event):  # Pivoter la tete du serpent vers la gauche
    # bouton gauche souris 
    global direction
    direction = pivot_horaire(nb=3)

def tourne_droite(event):   # Pivoter la tete du serpent vers la droite
    # bouton droite souris
    global direction
    direction = pivot_horaire(nb=1)

def flecheDroite(event):  # Changement de direction vers la droite
    global direction
    direction = 1

def flecheGauche(event):   # Changement de direction vers la gauche
    global direction
    direction = 3

def flecheHaut(event):   # Changement de direction vers le haut
    global direction
    direction = 0

def flecheBas(event):   # Changement de direction vers le bas
    global direction
    direction = 2

def trace_Cercle(x,y):        # Dessine un cercle sur l'interface et renvoie la référence de ce dernier pour pouvoir le réutiliser dans le snake
    r=T_CASE/2
    x=(MARGE+T_CASE/2)+ (T_CASE*x)
    y = (MARGE+T_CASE/2)+ (T_CASE*y)                                                       
    return Grille_NB.create_oval(x-r, y-r, x+r, y+r, fill=choice(COULEUR))

############################### Construction et placement graphique du jeu ###############

def peuble_frames(fenJeu):            
    global peuple_fr ,peuple_jeu ,peuple_gestion ,peuple_score ,Grille_NB
    
    peuple_fr.pack()
    jeu_frame['frame'] = peuple_fr

    peuple_jeu.pack()
    jeu_frame['jeu'] = peuple_jeu

    Grille_NB.pack(padx=MARGE, pady=MARGE)
    jeu_canvas['canvas'] = Grille_NB
    
    peuple_gestion.pack(side =BOTTOM,pady=5)
    jeu_frame['gestion'] = peuple_gestion
    
    peuple_score.pack(padx=80, pady=5)
    jeu_frame['score'] = peuple_score

def peuble_gestion(fenJeu):           # Construction et placement des boutons
    boutonquitter=Button(fenJeu, text="Quitter", command=quitter, bg='Lightsalmon2',fg="black")
    boutonquitter.pack(padx=1, pady=5, side=LEFT)
    jeu_bouton['quitter'] = boutonquitter
    boutonreset = Button(fenJeu, text="RESET",command=reset, bg="DarkOliveGreen3", fg="black")
    boutonreset.pack(padx=1, pady=5, side=LEFT)
    jeu_bouton['reset'] = boutonreset
    boutonpause = Button(fenJeu, text="PAUSE", command=pause, bg="DarkOliveGreen3", fg="black")
    boutonpause.pack(padx=1, pady=5, side=LEFT)
    jeu_bouton['pause'] = boutonpause
    boutonplay = Button(fenJeu, text="PLAY", command=play, bg="DarkOliveGreen3", fg="black")
    boutonplay.pack(padx=1, pady=5, side=LEFT)
    jeu_bouton['play'] = boutonplay

def peuble_jeu(fenJeu):                         # liaisons entre fonction et flèches du clavier et les boutons de la souris
    fenApp.bind_all("<Button-3>", tourne_droite)
    fenApp.bind_all("<Button-1>", tourne_gauche)
   
    fenApp.bind("<Right>",  flecheDroite)
    fenApp.bind("<Left>", flecheGauche)
    fenApp.bind("<Up>", flecheHaut)
    fenApp.bind("<Down>", flecheBas)

def no_peuble_jeu(fenJeu):                  # rupture des liaisons entre fonction et flèches du clavier et les boutons de la souris
    fenApp.unbind_all("<Button-3>")
    fenApp.unbind_all("<Button-1>")
   
    fenApp.unbind("<Right>")
    fenApp.unbind("<Left>")
    fenApp.unbind("<Up>")
    fenApp.unbind("<Down>")

def peuble_score(fenJeu):   # Construction et placement des labels
    global score
    # cette fonction permet de gérer le score
    tk_score = Label(fenJeu, text="SCORE :" + str(score) ,relief=RAISED, bg="DarkOliveGreen3")
    tk_score.pack(side=RIGHT)
    tk_lance = Label(fenJeu, text="Appuiyer sur la touche espace pour lancer le serpent ! ", bg="burlywood1")
    tk_lance.pack(padx=1, pady=5, side=LEFT)
    jeu_label["score"] = tk_score
    jeu_label["command"] = tk_lance

def reset_interface():        # Réinitialiser de l'interface du jeu
    init_serpent()
    jeu_canvas['canvas'].delete("all")
    peuple_jeu(jeu_canvas['canvas'])

def build_interface():         # Initialisation de l'interface du jeu
    fenApp.title("Petit snake 2020")
    fenApp.bind("<space>", lancer)
    peuble_frames(fenApp)
    peuble_jeu(jeu_canvas['canvas'])
    peuble_score(jeu_frame['score'])
    peuble_gestion(jeu_frame['gestion'])

def init_serpent():                    # initialisation du serpent
    direction = choice([0,1,2,3])
    num_case = randint(0,NB_CASES-1)
    l,c = case_to_lc(num_case)
    snake.insert(0,(num_case,trace_Cercle(c,l)))
   
    return snake

def avance():                         
    global direction
    global Grille_NB
    global food_num_case
    global score, running
                                                             # Si le serpent sort du cadre il réapparait de l'autre coté
                                                                            # Sinon, il passe à la case suivante
    snake_head_pos = snake[0][0]
    current_num_case=snake[0][0]    
    if current_num_case >= 0 and current_num_case <= NB_CASES - 1:
        num_case =   case_suivante(snake_head_pos, direction, nb_cases=1)
    else:
         num_case = case_suivante(snake_head_pos, direction, nb_cases=0)
    
    snake[0]=(num_case,snake[0][1])    
    x,y = case_to_xy(num_case)

    Grille_NB.forget()
    Grille_NB=Canvas(fenApp,width=long_can, height=larg_can, bg="burlywood1")

    f1,f2 = case_to_lc(food_num_case)      # Initialisation et apparition de la nourriture
    r=T_CASE/2
    x2=(MARGE+T_CASE/2)+ (T_CASE*f2)
    y2= (MARGE+T_CASE/2)+ (T_CASE*f1)
    foodi = Grille_NB.create_rectangle(x2-r, y2-r, x2+r, y2+r, fill=choice(COULEUR))
    Grille_NB.pack(padx=MARGE, pady=MARGE)
    
    l,c = xy_to_lc(x, y)
    trace_Cercle(c,l)
    
    if food_num_case == num_case:              # Colision food et tete du serpent => agrandissement de la taille du serpent
        score +=1
        food_num_case = randrange(NB_CASES)
        c1 , l1 = case_to_lc(current_num_case)
        snake.insert((len(snake)+1),(current_num_case,trace_Cercle(l1,c1)))

    if score >0 :                                                  # gère la position de chaque element du serpent
        liste_pos_tail.insert(0,current_num_case)
    for elt in liste_pos_tail[:score] :
        new_liste.append((elt,liste_pos_tail[:score].index(elt)+2))
        c1 , l1 = case_to_lc(elt)
        snake[-1] =(current_num_case,trace_Cercle(l1,c1))
        if len(snake)>2:
            snake[1:]=new_liste[-score:]

    for elt in snake[1:]:               # Colision tete et reste du serpent => PERDU !      
        if num_case==elt[0]:
            running = False
            pause()
            
    print("Le serpent : ",snake)


if __name__ == "__main__":
    build_interface()

    
    
