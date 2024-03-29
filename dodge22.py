import pyxel, random
from math import sqrt
#www.pyxelstudio.net/qwklx584

# taille de la fenetre 256x256 pixels
# ne pas modifier
pyxel.init(256, 256)
pyxel.load("res.pyxres")

def init():
    global personnage_x, personnage_y, w, h, ennemis_vitesse_1, ennemis_vitesse_2, ennemis_liste_up, ennemis_liste_left, ennemis_liste_down, ennemis_liste_right, score, coins_amount, vies, game, transparent_colour, transparent_colour_2, niveau, progress_level, coins_liste, hearts_liste, clouds_liste, bomb_liste, obstacles_liste, shop, d, cperso
    personnage_x = 120
    personnage_y = 120
    w = 16
    h = 16
    ennemis_vitesse_1 = 4
    ennemis_vitesse_2 = 2
    ennemis_liste_up = []
    ennemis_liste_left = []
    ennemis_liste_down = []
    ennemis_liste_right = []
    score = 0
    coins_amount = 0
    vies = 3
    game = True
    transparent_colour = 7
    transparent_colour_2 = 2
    niveau = 0
    progress_level = 0
    coins_liste = []
    hearts_liste = []
    clouds_liste = []
    bomb_liste = []
    obstacles_liste = []
    shop = False
    d = 14
    cperso = []

init()

def shop_code(niveau, progress_level, coins_amount, vies):
    if pyxel.btnr(pyxel.KEY_P) and niveau >= 1:
        progress_level = niveau
        niveau = -2
    elif pyxel.btnr(pyxel.KEY_P) and niveau == -2:
        niveau = progress_level
    if niveau == -2 and coins_amount >= 20 and pyxel.btnr(pyxel.KEY_B) and vies <= 2:
        coins_amount -= 20
        vies += 1
    return niveau, progress_level, coins_amount, vies

def score_timer(score):
    """augmente le score au fur et a mesure du temps"""
    if vies>0:
        if (pyxel.frame_count % 30 == 0):
            score += 1
    return score
    
def niveau_compteur(niveau):
    if game == True:
        if score >= 100 and niveau == 1:
            niveau = 2
    return niveau    
    
def personnage_deplacement(x, y, cperso):
    """déplacement avec les touches de directions"""
    cperso = [x + 8, y - 8]
    if pyxel.btn(pyxel.KEY_RIGHT):
        if (x < 256-w+2):
            x = x+2
    if pyxel.btn(pyxel.KEY_LEFT):
        if (x > -2):
            x = x-2
    if pyxel.btn(pyxel.KEY_UP):
        if (y > 0):
            y = y-2
    if pyxel.btn(pyxel.KEY_DOWN):
        if (y < 256-h):
            y = y+2

    return x, y, cperso

def ennemis_creation(ennemis_liste, direction, sens): #direction 0 = left/right et direction 1 = up/down
    # sens 0 = left/up et sens 1 = right/down
    """création aléatoire des ennemis"""
    # un ennemi par seconde
    if (pyxel.frame_count % 30 == 0):
        if sens == 0:
            if direction == 1:
                ennemis_liste.append([random.randint(0, 240), -h])
            else:
                ennemis_liste.append([-w, random.randint(0, 240)])
        elif sens == 1:
            if direction == 1:
                ennemis_liste.append([random.randint(0, 240) + h, (256)])
            else:
                ennemis_liste.append([(256), random.randint(0, 240) + w])
    return ennemis_liste
    
def ennemis_deplacement(ennemis_liste, direction, sens): # sens 0 = left/up et sens 1 = right/down
    """déplacement des ennemis vers le haut et suppression s'ils sortent du cadre"""
    for ennemi in ennemis_liste:
        if sens == 0:
            if niveau == 1:
                ennemi[direction] += ennemis_vitesse_1
            elif niveau == 2:
                ennemi[direction] += ennemis_vitesse_2
            if  ennemi[direction]>256:
                ennemis_liste.remove(ennemi)
        elif sens == 1:
            if niveau == 1:
                ennemi[direction] -= ennemis_vitesse_1
            elif niveau == 2:
                ennemi[direction] -= ennemis_vitesse_2
            if  ennemi[direction]<0:
                ennemis_liste.remove(ennemi)
    return ennemis_liste
    
def collisions_ennemis(ennemis_liste, vies, obstacles_liste):
    """collisions personnage/ennemis"""
    for ennemi in ennemis_liste:
        enx = ennemi[0] + (w/2)
        eny = ennemi[1] - (h/2)
        if d >= sqrt((((enx) - cperso[0])**2) + (((eny) - cperso[1])**2)):
            ennemis_liste.remove(ennemi)
            vies = vies -1
    
        """collisions ennemis/obstacles"""      
        for obstacle in obstacles_liste:
            if obstacle[2] == 0:
                obstacles_liste.remove(obstacle)
            else:
                obst1 = obstacle[0] + (w/2)
                obst2 = obstacle[1] - (h/2)
                if d >= sqrt((((enx) - obst1)**2) + (((eny) - obst2)**2)):
                    obstacle[2] -= 1
                    ennemis_liste.remove(ennemi)
                        
    return ennemis_liste, vies, obstacles_liste

def coins_creation(coins_liste):
    if len(coins_liste) < 1 :
        if (pyxel.frame_count % 150 == 0):
            coins_liste.append([random.randint(40,200), random.randint(40,200)])
    return coins_liste
    
def hearts_creation(hearts_liste):
    if len(hearts_liste) < 1 :
        if (pyxel.frame_count % 1500 == 0):
            hearts_liste.append([random.randint(40,200), random.randint(40,200)])
    return hearts_liste

def obstacles_creation(obstacles_liste):
    if len(obstacles_liste) < 2 :
        if (pyxel.frame_count % 30 == 0):
            obstacles_liste.append([random.randint(40,200), random.randint(40,200), 5])
    return obstacles_liste

def bomb_creation(bomb_liste):
    if niveau >= 2:
        if len(bomb_liste) < 1 :
            if (pyxel.frame_count % 600 == 0):
                bomb_liste.append([random.randint(40,200), random.randint(40,200)])
    return bomb_liste

def clouds_creation(clouds_liste):
    if (pyxel.frame_count % 10 == 0):
        clouds_liste.append([-w, random.randint(0, 240)])
    return clouds_liste

def coins_collisions(coins_liste, score, coins_amount):
    for coins in coins_liste:
        if ((personnage_x + w) >= coins[0] >= personnage_x - w) and ((personnage_y + h) >= coins[1] >= personnage_y - h):
            coins_liste.remove(coins)
            score += 10
            coins_amount += 1
    return coins_liste, score, coins_amount
    
def hearts_collisions(hearts_liste, vies):
    for heart in hearts_liste:
        if ((personnage_x + w) >= heart[0] >= personnage_x - w) and ((personnage_y + h) >= heart[1] >= personnage_y - h):
            hearts_liste.remove(heart)
            if vies < 3:
                vies += 1
    return hearts_liste, vies
    
def bomb_collisions(bomb_liste, ennemis_liste_up, ennemis_liste_left, ennemis_liste_down, ennemis_liste_right):
    for bombs in bomb_liste:
        if ((personnage_x + w) >= bombs[0] >= personnage_x - w) and ((personnage_y + h) >= bombs[1] >= personnage_y - h):
            bomb_liste.remove(bombs)
            ennemis_liste_up = []
            ennemis_liste_left = []
            ennemis_liste_down = []
            ennemis_liste_right = []
    return bomb_liste, ennemis_liste_up, ennemis_liste_left, ennemis_liste_down, ennemis_liste_right

def clouds_deplacement(clouds_liste):
    for cloud in clouds_liste:
        cloud[0] += 1
    return clouds_liste


# =========================================================
# == UPDATE
# =========================================================
def update():
# flèches interactives
    global personnage_x,personnage_y,ennemis_liste_up,ennemis_liste_left,ennemis_liste_down,ennemis_liste_right,score,game,vies,niveau, coins_liste, hearts_liste, clouds_liste, bomb_liste, obstacles_liste, shop, progress_level, ennemis_listes, d, cperso, coins_amount
    
    niveau, progress_level, coins_amount, vies = shop_code(niveau, progress_level, coins_amount, vies)
    
    if vies <= 0 or pyxel.btn(pyxel.KEY_SPACE):
        niveau = -1
        
    if niveau == -1:
        if pyxel.btn(pyxel.KEY_R):
            init()
            
    if niveau == 0:
        clouds_liste = clouds_creation(clouds_liste)
        clouds_liste = clouds_deplacement(clouds_liste)
        if pyxel.btn(pyxel.KEY_S):
            niveau = 1
            
    if niveau >= 0:
        personnage_x, personnage_y, cperso = personnage_deplacement(personnage_x, personnage_y, cperso)
        
    if niveau >= 1:
        ennemis_liste_up = ennemis_creation(ennemis_liste_up, 1, 0)
        ennemis_liste_left = ennemis_creation(ennemis_liste_left, 0, 0)
        ennemis_liste_up = ennemis_deplacement(ennemis_liste_up, 1, 0)
        ennemis_liste_left = ennemis_deplacement(ennemis_liste_left, 0, 0)
        score = score_timer(score)
        
        ennemis_liste_left, vies, obstacles_liste = collisions_ennemis(ennemis_liste_left, vies, obstacles_liste)
        ennemis_liste_up, vies, obstacles_liste = collisions_ennemis(ennemis_liste_up, vies, obstacles_liste)
        ennemis_liste_right, vies, obstacles_liste = collisions_ennemis(ennemis_liste_right, vies, obstacles_liste)
        ennemis_liste_down, vies, obstacles_liste = collisions_ennemis(ennemis_liste_down, vies, obstacles_liste)
        niveau = niveau_compteur(niveau)
        coins_liste = coins_creation(coins_liste)
        coins_liste, score, coins_amount = coins_collisions(coins_liste, score, coins_amount)
        hearts_liste = hearts_creation(hearts_liste)
        hearts_liste, vies = hearts_collisions(hearts_liste, vies)
        bomb_liste = bomb_creation(bomb_liste)
        bomb_liste, ennemis_liste_up, ennemis_liste_left, ennemis_liste_down, ennemis_liste_right = bomb_collisions(bomb_liste, ennemis_liste_up, ennemis_liste_left, ennemis_liste_down, ennemis_liste_right)
        obstacles_liste = obstacles_creation(obstacles_liste)
        hearts_liste, vies = hearts_collisions(hearts_liste, vies)

        if niveau == 2:
            ennemis_liste_down = ennemis_creation(ennemis_liste_down, 1, 1)
            ennemis_liste_right = ennemis_creation(ennemis_liste_right, 0, 1)
            ennemis_liste_down = ennemis_deplacement(ennemis_liste_down, 1, 1)
            ennemis_liste_right = ennemis_deplacement(ennemis_liste_right, 0, 1)
            bomb_liste = bomb_creation(bomb_liste)
            bomb_liste, ennemis_liste_up, ennemis_liste_left, ennemis_liste_down, ennemis_liste_right = bomb_collisions(bomb_liste, ennemis_liste_up, ennemis_liste_left, ennemis_liste_down, ennemis_liste_right)
# =========================================================
# == DRAW
# =========================================================
def draw():
    """création des objets (30 fois par seconde)"""
    global personnage_x,personnage_y,ennemis_liste_up,ennemis_liste_left,ennemis_liste_down,ennemis_liste_right,score,game,vies,niveau, coins_liste, hearts_liste, clouds_liste, bomb_liste, obstacles_liste, shop, progress_level, ennemis_listes, d, cperso, coins_amount
    # vide la fenetre
    pyxel.cls(0)
    if niveau == -2:
        pyxel.cls(7)
        pyxel.rect(78, 78, 100, 100, 0)
        pyxel.text(175, 200, f"Coins: {coins_amount}", 0)
        pyxel.text(80, 128, "press B to buy a heart", 7)
        if vies == 3:
            pyxel.blt(4, 4, 0, 0, 16, 16, 16, transparent_colour_2)
            pyxel.blt(24, 4, 0, 0, 16, 16, 16, transparent_colour_2)
            pyxel.blt(44, 4, 0, 0, 16, 16, 16, transparent_colour_2)
        elif vies == 2:
            pyxel.blt(4, 4, 0, 0, 16, 16, 16, transparent_colour_2)
            pyxel.blt(24, 4, 0, 0, 16, 16, 16, transparent_colour_2)
            pyxel.blt(44, 4, 0, 32, 48, 16, 16, transparent_colour_2)
        elif vies == 1:
            pyxel.blt(4, 4, 0, 0, 16, 16, 16, transparent_colour_2)
            pyxel.blt(24, 4, 0, 32, 48, 16, 16, transparent_colour_2)
            pyxel.blt(44, 4, 0, 32, 48, 16, 16, transparent_colour_2)
            

    if niveau == -1:
        pyxel.cls(7)
        pyxel.bltm(0, 0, 0, 512, 0, 256, 256)
        pyxel.text(110, 100, "Game Over", 0)
        pyxel.text(90, 110, "Press 'R' to Restart", 0)
        pyxel.text(110, 120, f"Score: {score}", 0)
    if niveau == 0:
        pyxel.bltm(0, 0, 0, 512, 0, 256, 256)
        for cloud in clouds_liste:
            pyxel.blt(cloud[0], cloud[1], 0, 0, 64, 16, 8, transparent_colour_2)
        pyxel.bltm(0, 0, 0, 256, 0, 256, 256, transparent_colour)
        pyxel.blt(personnage_x, personnage_y, 0, 32, 64, 16, 19, transparent_colour_2)
        pyxel.text(95, 210, "Press 'S' to Start", 0)
    if niveau >= 1:
        pyxel.rect(0, 0, 255, 255, 7)
        # backgrounds
        pyxel.bltm(0, 0, 0, 0, 0, 255, 255)
        pyxel.text(175, 190, f"Niveau: {niveau}", 0)
        pyxel.text(175, 210, f"Coins: {coins_amount}", 0)
        
        # dessiner le reste:
        if niveau == 1:
            pyxel.text(175, 200, f"Score: {score}/100", 0)
        elif niveau == 2:
            pyxel.text(175, 200, f"Score: {score}", 0)
        
        pyxel.blt(personnage_x, personnage_y, 0, 0, 0, 16, 16, transparent_colour)
        
        for ennemi in ennemis_liste_up:
            pyxel.blt(ennemi[0], ennemi[1], 0, 16, 80, 8, -16, transparent_colour)
        for ennemi in ennemis_liste_left:
            pyxel.blt(ennemi[0], ennemi[1], 0, 0, 48 + 8, 16, 8, transparent_colour)
        for ennemi in ennemis_liste_down:
            pyxel.blt(ennemi[0], ennemi[1], 0, 16, 80, 8, 16, transparent_colour)
        for ennemi in ennemis_liste_right:
            pyxel.blt(ennemi[0], ennemi[1], 0, 0, 48 + 8, -16, 8, transparent_colour)
            
        for bombs in bomb_liste:
            pyxel.blt(bombs[0], bombs[1], 0, 0, 80, 16, 16, transparent_colour_2)
            
        for coin in coins_liste:
            pyxel.blt(coin[0], coin[1], 0, 0, 32, 16, 16, transparent_colour)
            
        for heart in hearts_liste:
            pyxel.blt(heart[0], heart[1], 0, 0, 16, 16, 16, transparent_colour_2)
            
        for obstacle in obstacles_liste:
            if obstacle[2] == 5:
                pyxel.blt(obstacle[0], obstacle[1], 0, 0, 96, 16, 16, transparent_colour_2)
            elif obstacle[2] == 4:
                pyxel.blt(obstacle[0], obstacle[1], 0, 16, 96, 16, 16, transparent_colour_2)
            elif obstacle[2] == 3:
                pyxel.blt(obstacle[0], obstacle[1], 0, 32, 96, 16, 16, transparent_colour_2)
            elif obstacle[2] == 2:
                pyxel.blt(obstacle[0], obstacle[1], 0, 48, 96, 16, 16, transparent_colour_2)
            elif obstacle[2] == 1:
                pyxel.blt(obstacle[0], obstacle[1], 0, 64, 96, 16, 16, transparent_colour_2)
        
        if vies == 3:
            pyxel.blt(4, 4, 0, 0, 16, 16, 16, transparent_colour_2)
            pyxel.blt(24, 4, 0, 0, 16, 16, 16, transparent_colour_2)
            pyxel.blt(44, 4, 0, 0, 16, 16, 16, transparent_colour_2)
        elif vies == 2:
            pyxel.blt(4, 4, 0, 0, 16, 16, 16, transparent_colour_2)
            pyxel.blt(24, 4, 0, 0, 16, 16, 16, transparent_colour_2)
            pyxel.blt(44, 4, 0, 32, 48, 16, 16, transparent_colour_2)
        elif vies == 1:
            pyxel.blt(4, 4, 0, 0, 16, 16, 16, transparent_colour_2)
            pyxel.blt(24, 4, 0, 32, 48, 16, 16, transparent_colour_2)
            pyxel.blt(44, 4, 0, 32, 48, 16, 16, transparent_colour_2)

pyxel.run(update,draw)
