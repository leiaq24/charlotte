import pygame
import sys
import random

pygame.init()
ecran = pygame.display.set_mode((768, 650))
pygame.display.set_caption("Charlotte aux grenades")

# Chargement des images
grass = pygame.transform.scale(pygame.image.load("grassMid.png").convert_alpha(), (70, 70))
grass_center = pygame.transform.scale(pygame.image.load("grassCenter.png").convert_alpha(), (70, 70))
grenade_img = pygame.transform.scale(pygame.image.load("grenade.png").convert_alpha(), (35, 60))
fruit_img = pygame.transform.scale(pygame.image.load("fruit.png").convert_alpha(), (60, 60))
explosion_img = pygame.transform.scale(pygame.image.load("explosion.png").convert_alpha(), (800, 800))
cloud_img = pygame.transform.scale(pygame.image.load("cloud.png").convert_alpha(), (100, 60))

# Nuages
clouds = [[i * 300, random.randint(50, 200)] for i in range(6)]

# Animation personnage
run_frames = [pygame.transform.scale(pygame.image.load(f"frame{i}.png").convert_alpha(), (40, 60)) for i in range(3, 9)]
jump_up_img = pygame.transform.scale(pygame.image.load("jump_up.png").convert_alpha(), (40, 60))
jump_fall_img = pygame.transform.scale(pygame.image.load("jump_fall.png").convert_alpha(), (40, 60))

# Joueur
player_x = 150
player_y = 453
vy = 0
gravity = 1
en_saut = False
frame_index = 0
anim_timer = 0

# Monde
scroll_x = 0
vitesse_decor = 5
score = 0

# Objets sous forme de dictionnaires
def reset_objects():
    global grenades, fruits
    grenades = [{"x": x, "y": 450} for x in [900, 1400, 1800, 2200, 2700]]
    fruits = [{"x": x, "y": 450} for x in [1000, 1600, 2100, 2500, 3100]]

reset_objects()

clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)

def afficher_sol():
    tile_width = 70
    tile_height = 70
    # Nombre de tuiles horizontales nécessaires
    nb_tiles = (scroll_x + 768) // tile_width + 2
    
    # Affiche la ligne de sol
    for i in range(nb_tiles):
        ecran.blit(grass, (i * tile_width - scroll_x, 500))
    
    # Affiche les tuiles sous le sol jusqu'en bas de la fenêtre
    # La fenêtre fait 650px de haut, sol est à y=500, donc 150px à remplir verticalement
    nb_tiles_vertical = (650 - 500) // tile_height + 1
    
    for i in range(nb_tiles):
        for j in range(1, nb_tiles_vertical + 1):
            y_pos = 500 + j * tile_height
            ecran.blit(grass_center, (i * tile_width - scroll_x, y_pos))

def afficher_nuages():
    for c in clouds:
        c[0] -= 0.5
        if c[0] - scroll_x * 0.5 < -150:
            c[0] = scroll_x + 900 + random.randint(0, 400)
            c[1] = random.randint(50, 200)
        ecran.blit(cloud_img, (c[0] - scroll_x * 0.5, c[1]))

def afficher_score():
    txt = font.render(f"Score: {score}", True, (200, 0, 0))
    ecran.blit(txt, (600, 10))

def fin_de_jeu():
    ecran.fill((0, 0, 0))
    txt = font.render("Tu as perdu !", True, (255, 0, 0))
    ecran.blit(txt, (250, 200))
    rejouer = font.render("R : Rejouer", True, (255, 255, 255))
    quitter = font.render("Q : Quitter", True, (255, 255, 255))
    ecran.blit(rejouer, (270, 300))
    ecran.blit(quitter, (270, 350))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r] or keys[pygame.K_SPACE]:
            return True
        elif keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

# Boucle principale
running = True
while running:
    clock.tick(60)
    ecran.fill((135, 206, 235))  # ciel bleu

    afficher_nuages()
    afficher_sol()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Défilement automatique du décor
    scroll_x += vitesse_decor

    # Gestion du saut
    keys = pygame.key.get_pressed()
    if not en_saut and keys[pygame.K_SPACE]:
        vy = -15
        en_saut = True

    player_y += vy
    vy += gravity
    if player_y >= 450:
        player_y = 450
        vy = 0
        en_saut = False

    # Animation personnage
    anim_timer += 1
    if anim_timer >= 5:
        frame_index = (frame_index + 1) % len(run_frames)
        anim_timer = 0

    if en_saut:
        img_perso = jump_up_img if vy < 0 else jump_fall_img
    else:
        img_perso = run_frames[frame_index]

    ecran.blit(img_perso, (player_x, player_y))
    rect_perso = pygame.Rect(player_x + 5, player_y + 10, 30, 50)

    # Affichage grenades et gestion collisions
    for g in grenades:
        screen_x = g["x"] - scroll_x
        screen_y = g["y"]

        # Repositionner grenade si sortie à gauche
        if screen_x < -50:
            g["x"] = scroll_x + random.randint(1500, 2500)  

        ecran.blit(grenade_img, (screen_x, screen_y))
        rect_g = pygame.Rect(screen_x + 5, screen_y + 10, 25, 45)
        if rect_perso.colliderect(rect_g):
            ecran.blit(explosion_img, (player_x -200, 0))
            pygame.display.update()
            pygame.time.delay(1000)
            if fin_de_jeu():
                scroll_x = 0
                player_y = 450
                vy = 0
                en_saut = False
                score = 0
                reset_objects()
                break
            else:
                running = False
                break

    # Affichage fruits et gestion collisions + repositionnement
    for f in fruits:
        screen_x = f["x"] - scroll_x
        screen_y = f["y"]

        # Repositionner fruit si sortie à gauche
        if screen_x < -60:
            f["x"] = scroll_x + random.randint(800, 1500)

        ecran.blit(fruit_img, (screen_x, screen_y))
        rect_f = pygame.Rect(screen_x + 5, screen_y + 10, 40, 50)
        if rect_perso.colliderect(rect_f):
            score += 1
            f["x"] += random.randint(800, 1500)  # repositionne fruit plus loin

    afficher_score()
    pygame.display.update()
