# EFCD: Projeto de tecnologias e programação de sistemas de informação
# Código: 5425
# Formandos: Júlia Costa, Lisandra Cunha
# Data: 31.05.2024

import pygame
from random import randint
from sys import exit
import time

# iniciar biblioteca Pygame
pygame.init()

# características do ecrã
pygame.display.set_caption("Jogo - Snake")
pygame.display.set_icon(pygame.image.load("IconSnake.jpeg"))
LARGURA = 700
ALTURA = 500
janela = pygame.display.set_mode((LARGURA, ALTURA))
relogio = pygame.time.Clock()

# definir cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (35, 142, 35)

# definir variáveis
tamanho_pixel = 20
velocidade_jogo = 10 # em milisegundos

# importar imagens
maca = pygame.image.load("Maca.png")
kiwi = pygame.image.load("Kiwi.png")

# definir funções
def definir_maca():
    maca_x = int(randint(0, LARGURA - maca.get_width()))
    maca_y = int(randint(0, ALTURA - maca.get_height()))
    return maca_x, maca_y

def definir_kiwi():
    kiwi_x = int(randint(0, LARGURA - kiwi.get_width()))
    kiwi_y = int(randint(0, ALTURA - kiwi.get_height()))
    return kiwi_x, kiwi_y

# estado inical do jogo
pontuacao = 0
temporizador_kiwi = 0
fim_jogo = False

# definir fontes de texto do jogo
fonte_pontuacao = pygame.font.Font("OCRAEXT.TTF", 25)
fonte_fim_jogo = pygame.font.Font("OCRAEXT.TTF", 50)

# definir sons do jogo
som_pontos = pygame.mixer.Sound("Coin.wav")
som_fim_jogo = pygame.mixer.Sound("Oops.wav")
pygame.mixer.music.load("musica_fundo.mp3")

# reproduzir música de fundo
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.30)

# posição e velocidade inicial da cobra
pos_x_cobra = LARGURA / 2
pos_y_cobra = ALTURA / 2
velocidade_X = 0
velocidade_Y = 0
tamanho_cobra = 1 # nº de pixeis da cobra
pixels = []

# posição inicial dos alimentos do jogo
maca_x, maca_y = definir_maca()
kiwi_x, kiwi_y = definir_kiwi()

# loop principal
while fim_jogo == False:
    janela.fill(PRETO)

    # encerramento do jogo
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

    # interação com o precionar das teclas
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_UP]:
        velocidade_X = 0
        velocidade_Y = -tamanho_pixel
    elif teclas[pygame.K_DOWN]:
        velocidade_X = 0
        velocidade_Y = tamanho_pixel
    elif teclas[pygame.K_LEFT]:
        velocidade_X = -tamanho_pixel
        velocidade_Y = 0
    elif teclas[pygame.K_RIGHT]:
        velocidade_X = tamanho_pixel
        velocidade_Y = 0

    # redesenhar os alimentos do jogo
    repor_maca = janela.blit(maca, (maca_x, maca_y))
    repor_kiwi = janela.blit(kiwi, (kiwi_x, kiwi_y))

    # atualizar a posição da cobra
    pos_x_cobra += velocidade_X
    pos_y_cobra += velocidade_Y

    # atualizar tamanho da cobra
    pixels.append([pos_x_cobra, pos_y_cobra])
    if len(pixels) > tamanho_cobra:
        del pixels[0]

    # verificar colisão com a própria cobra
    for pixel in pixels[:-1]:
        if pixel == [pos_x_cobra, pos_y_cobra]:
            fim_jogo = True

    # redesenhar a cobra
    for pixel in pixels:
        cobra = pygame.draw.rect(janela, VERDE, [pixel[0], pixel[1], tamanho_pixel, tamanho_pixel])

    # verificar colisão com os limites do ecrã
    if (pos_x_cobra < 0 or pos_x_cobra + tamanho_pixel > LARGURA or pos_y_cobra < 0 or pos_y_cobra + tamanho_pixel > ALTURA):
        fim_jogo = True

    # verificar colisão com a maçã
    if cobra.colliderect(repor_maca):
       maca = pygame.image.load("hide.png")
       maca_x, maca_y = definir_maca()
       maca = pygame.image.load("Maca.png")
       tamanho_cobra += 1
       pontuacao += 1
       som_pontos.play()

    # verificar colisão com o kiwi
    if cobra.colliderect(repor_kiwi):
       kiwi = pygame.image.load("hide.png")
       kiwi_x, kiwi_y = definir_kiwi()
       kiwi = pygame.image.load("Kiwi.png")
       som_pontos.play()
       tamanho_cobra += 1
       pontuacao += 2
       velocidade_jogo += 10
       temporizador_kiwi = time.time()

    # temporizador do aumento da velocidade quando come o kiwi
    if temporizador_kiwi > 0 and time.time() - temporizador_kiwi >= 5:
        velocidade_jogo = 15
        temporizador_kiwi = 0    

    # definir texto da pontoação
    texto_pontuacao = fonte_pontuacao.render(f"Pontuação:{pontuacao}", True, BRANCO)
    janela.blit(texto_pontuacao, (10, 10))

    # definir a atualização do ecrã
    pygame.display.update()
    relogio.tick(velocidade_jogo)

# definir ecrã de "fim de jogo"
if fim_jogo == True:
    janela.fill(PRETO)
    texto_fim_jogo = fonte_fim_jogo.render("FIM DO JOGO!", True, BRANCO)
    janela.blit(texto_fim_jogo, (175, 175))
    texto_pontuacao_final = fonte_pontuacao.render(f"Pontuação final: {pontuacao}", True, BRANCO)
    janela.blit(texto_pontuacao_final, (220, 250))
    som_fim_jogo.play()
    pygame.mixer.music.stop()

    pygame.display.update()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
