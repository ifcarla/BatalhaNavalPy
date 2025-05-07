import tkinter as tk
import random
import pygame

pygame.init()
som_erro = pygame.mixer.Sound("erro.wav.wav")
som_explosao = pygame.mixer.Sound("explosao.wav.wav")

TAMANHO = 10
TAMANHO_NAVIO = 3
NUM_NAVIOS = 4
VIDAS = NUM_NAVIOS * TAMANHO_NAVIO

COR_AGUA = "lightblue"
COR_NAVIO = "gray"
COR_DIAGONAL = "darkgray"
COR_HABILIDADE = "yellow"
COR_ACERTO = "red"
COR_ERRO = "white"

tabuleiro_jogador = [[0]*TAMANHO for _ in range(TAMANHO)]
tabuleiro_computador = [[0]*TAMANHO for _ in range(TAMANHO)]
botoes_jogador = []
botoes_computador = []

vidas_jogador = VIDAS
vidas_computador = VIDAS

def posicionar_automatico(tabuleiro):
    direcoes = ['horizontal', 'vertical', 'diagonal_principal', 'diagonal_secundaria']
    colocados = 0
    while colocados < NUM_NAVIOS:
        linha = random.randint(0, TAMANHO - TAMANHO_NAVIO)
        coluna = random.randint(0, TAMANHO - 1)
        direcao = random.choice(direcoes)
        try:
            if direcao == 'horizontal' and coluna + TAMANHO_NAVIO <= TAMANHO:
                for i in range(TAMANHO_NAVIO):
                    tabuleiro[linha][coluna + i] = 3
            elif direcao == 'vertical' and linha + TAMANHO_NAVIO <= TAMANHO:
                for i in range(TAMANHO_NAVIO):
                    tabuleiro[linha + i][coluna] = 3
            elif direcao == 'diagonal_principal' and coluna + TAMANHO_NAVIO <= TAMANHO:
                for i in range(TAMANHO_NAVIO):
                    tabuleiro[linha + i][coluna + i] = 3
            elif direcao == 'diagonal_secundaria' and coluna - TAMANHO_NAVIO + 1 >= 0:
                for i in range(TAMANHO_NAVIO):
                    tabuleiro[linha + i][coluna - i] = 3
            colocados += 1
        except:
            continue

def atacar(i, j):
    global vidas_computador
    if botoes_computador[i][j]['state'] == 'disabled':
        return
    if tabuleiro_computador[i][j] == 3:
        botoes_computador[i][j].config(bg=COR_ACERTO)
        som_explosao.play()
        vidas_computador -= 1
        status_label.config(text=f"Você acertou! Vidas do computador: {vidas_computador}")
    else:
        botoes_computador[i][j].config(bg=COR_ERRO)
        som_erro.play()
        status_label.config(text="Você errou!")

    botoes_computador[i][j]['state'] = 'disabled'
    if vidas_computador == 0:
        status_label.config(text="Parabéns! Você venceu!")
        desativar_tabuleiro()
    else:
        janela.after(1000, ataque_computador)

def ataque_computador():
    global vidas_jogador
    while True:
        i, j = random.randint(0, TAMANHO-1), random.randint(0, TAMANHO-1)
        if botoes_jogador[i][j]['state'] == 'normal':
            if tabuleiro_jogador[i][j] == 3:
                botoes_jogador[i][j].config(bg=COR_ACERTO)
                som_explosao.play()
                vidas_jogador -= 1
                status_label.config(text=f"Computador acertou! Suas vidas: {vidas_jogador}")
            else:
                botoes_jogador[i][j].config(bg=COR_ERRO)
                som_erro.play()
                status_label.config(text="Computador errou.")
            botoes_jogador[i][j]['state'] = 'disabled'
            break
    if vidas_jogador == 0:
        status_label.config(text="Você perdeu! :(")
        desativar_tabuleiro()

def usar_habilidade():
    global vidas_computador
    linha = random.randint(1, TAMANHO-2)
    coluna = random.randint(1, TAMANHO-2)
    for i in range(-1, 2):
        for j in range(-1, 2):
            lin, col = linha + i, coluna + j
            if 0 <= lin < TAMANHO and 0 <= col < TAMANHO:
                if tabuleiro_computador[lin][col] == 3 and botoes_computador[lin][col]['state'] == 'normal':
                    botoes_computador[lin][col].config(bg=COR_ACERTO)
                    som_explosao.play()
                    vidas_computador -= 1
                else:
                    botoes_computador[lin][col].config(bg=COR_HABILIDADE)
    status_label.config(text=f"Habilidade usada no centro ({linha}, {coluna})")
    if vidas_computador <= 0:
        status_label.config(text="Parabéns! Você venceu com a habilidade especial!")
        desativar_tabuleiro()

def desativar_tabuleiro():
    for i in range(TAMANHO):
        for j in range(TAMANHO):
            botoes_computador[i][j]['state'] = 'disabled'

janela = tk.Tk()
janela.title("Batalha Naval - Completo")
tk.Label(janela, text="Seu Tabuleiro").grid(row=0, column=0, columnspan=TAMANHO)
tk.Label(janela, text="Computador").grid(row=0, column=TAMANHO+2, columnspan=TAMANHO)


for i in range(TAMANHO):
    linha_botoes = []
    for j in range(TAMANHO):
        btn = tk.Button(janela, width=2, height=1, bg=COR_AGUA, state="normal", relief="groove")
        btn.grid(row=i+1, column=j)
        linha_botoes.append(btn)
    botoes_jogador.append(linha_botoes)

for i in range(TAMANHO):
    linha_botoes = []
    for j in range(TAMANHO):
        btn = tk.Button(janela, width=2, height=1, bg=COR_AGUA,
                        command=lambda i=i, j=j: atacar(i, j), relief="raised")
        btn.grid(row=i+1, column=j+TAMANHO+2)
        linha_botoes.append(btn)
    botoes_computador.append(linha_botoes)

posicionar_automatico(tabuleiro_jogador)
posicionar_automatico(tabuleiro_computador)

for i in range(TAMANHO):
    for j in range(TAMANHO):
        if tabuleiro_jogador[i][j] == 3:
            botoes_jogador[i][j].config(bg=COR_NAVIO)

btn_habilidade = tk.Button(janela, text="Usar Habilidade Especial", command=usar_habilidade, bg="orange")
btn_habilidade.grid(row=TAMANHO + 2, column=0, columnspan=TAMANHO+TAMANHO+2, pady=10)

status_label = tk.Label(janela, text="Seu turno! Clique para atacar.")
status_label.grid(row=TAMANHO + 3, column=0, columnspan=TAMANHO+TAMANHO+2)

janela.mainloop()
