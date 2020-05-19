import math
import random

import pygame
from pygame import mixer

#inicialização do game
pygame.init()

#criando uma tela (LARGURA X ALTURA)
tela = pygame.display.set_mode((800,600))

# IMAGEM DE FUNDO
imagem_de_fundo = pygame.image.load('imagem_de_fundo.png').convert()

# SOM DE FUNDO 

mixer.music.load('background.wav')
mixer.music.play()

# TITULO E ICONE
pygame.display.set_caption("Invasores do espaço")
icone = pygame.image.load('icone.png')
pygame.display.set_icon(icone)

#JOGADOR
jogador_img = pygame.image.load('jogador.png')
jogador_X = 370
jogador_Y = 480
jogador_X_muda = 0

#INIMIGO

inimigo_img = []
inimigo_X = []
inimigo_Y = []
inimigo_X_muda = []
inimigo_Y_muda = []
num_de_inimigos = 6

for i in range (num_de_inimigos):
    inimigo_img.append(pygame.image.load('inimigo.png'))
    inimigo_X.append(random.randint(0,736))
    inimigo_Y.append(random.randint(50,150))
    inimigo_X_muda.append(0.3)
    inimigo_Y_muda.append(40)

#BALA
# PRONTO - VOCÊ NÃO PODE VER A BALA NA TELA 
# FOGO - A BALA ESTÁ SE MOVENDO CORRETAMENTE  

bala_img = pygame.image.load('bala.png')
bala_X = 0
bala_Y = 480
bala_X_muda = 0
bala_Y_muda = 5
bala_estado = "pronto"

#   PONTUAÇÃO
valor_pontuacao = 0 
fonte = pygame.font.Font('freesansbold.ttf', 32)

textoX = 10
textoY = 10

# AVISO DE GAME OVER 
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_pontuacao(x,y):
    pontuacao = fonte.render("Pontuação: " + str(valor_pontuacao), True,(255,255,255))
    tela.blit(pontuacao,(x,y))

def game_over_text():
    over_text = over_font.render("FIM DE JOGO", True,(255,255,255))
    tela.blit(over_text,(200,250))

def jogador(x,y):
    tela.blit(jogador_img, (x,y))  

def inimigo(x,y,i):
    tela.blit(inimigo_img[i], (x,y))

def fogo_bala(x,y):
    global bala_estado
    bala_estado = "fogo"
    tela.blit(bala_img, (x + 16, y + 10))

#FUNÇÃO DE DISTANCIA ENTRE DOIS PONTOS PARA A BALA COLIDIR COM O INIMIGO
def iscolisao(inimigo_X,inimigo_Y,bala_X,bala_Y):
    distancia = math.sqrt(math.pow(inimigo_X - bala_X,2) + (math.pow(inimigo_Y - bala_Y,2)))
    if distancia < 27:
        return True 
    else:
        return False

#LOOP DO JOGO
#variavel para fazer um laço e criar uma forma do usuario fechar o game

rodando = True

while rodando:
    tela.fill((0, 0, 0))
    #IMAGEM DE FUNDO SENDO APLICADA NO LOOPING 
    tela.blit(imagem_de_fundo, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False 

        #FORMA DE POR PARA QUANDO A TECLA FOR PRESSIONADA O JOGADOR MUDAR DE POSIÇÃO
        if event.type == pygame.KEYDOWN:
            if event.key ==pygame.K_LEFT:
                jogador_X_muda = -0.5
            if event.key ==pygame.K_RIGHT:
                jogador_X_muda = 0.5
            if event.key == pygame.K_SPACE:
                if bala_estado is "pronto":
                    bala_som = mixer.Sound('laser.wav')
                    bala_som.play()
                    bala_X = jogador_X
                    fogo_bala(bala_X,bala_Y)    
        if event.type == pygame.KEYUP:
            if event.key ==pygame.K_LEFT or event.key ==pygame.K_RIGHT:
                jogador_X_muda = 0
    
    
    #AJUSTANDO PARA O JOGADOR NÃO SAIR DA TELA
    jogador_X += jogador_X_muda

    if jogador_X <= 0:
        jogador_X = 0
    elif jogador_X >=736:
        jogador_X = 736
    
    #AJUSTANDO PARA O INIMIGO NÃO SAIR DA TELA
    for i in range (num_de_inimigos): 

        #GAME OVER 
        if inimigo_Y[i] > 440:
            for j in range(num_de_inimigos):
                inimigo_Y[j] - 2000
            game_over_text()
            break


        inimigo_X[i] += inimigo_X_muda[i]
        if inimigo_X[i] <= 0:
            inimigo_X[i] = 0.4
            inimigo_Y[i] += inimigo_Y_muda[i]
        elif inimigo_X[i] >=736:
            inimigo_X[i] = -0.4
            inimigo_Y[i] += inimigo_Y_muda[i]
    
        #COLISÃO =  APLICAR A FUNÇÃO NO LOOPING 
        colisao = iscolisao(inimigo_X[i],inimigo_Y[i],bala_X,bala_Y)
        if colisao:
            explosao_som = mixer.Sound('explosion.wav')
            explosao_som.play()
            bala_Y = 480
            bala_estado = "pronto"
            valor_pontuacao += 1
            inimigo_X[i] = random.randint(0,736)
            inimigo_Y[i] = random.randint(50,150)
    
        inimigo(inimigo_X[i], inimigo_Y[i], i)

    # MOVIMENTO DA BALA 
    if bala_Y <=0:
        bala_Y= 480
        bala_estado="pronto"
    if bala_estado is "fogo":
        fogo_bala(bala_X,bala_Y)
        bala_Y -= bala_Y_muda

    
    jogador(jogador_X, jogador_Y)
    show_pontuacao(textoX,textoY)
    

    pygame.display.update()



