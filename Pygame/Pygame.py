from random import randint
import pygame, sys

# 19x17
matrizMapa = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
tamanho = 32
largura = len(matrizMapa[0]) * tamanho
altura = len(matrizMapa) * tamanho
tela = pygame.display.set_mode((largura, altura))

LIVRE = 0
PAREDE = 1
FRUTA = 2
COBRA = 3

class Cenario:
    def __init__(self, matriz):
        self.matriz = matriz

    def criarMapa(self):
        anterior = 1
        for i, linha in enumerate(self.matriz):
            for j, valor in enumerate(linha):
                retangulo = [(j * tamanho, i * tamanho), (tamanho, tamanho)]
                if valor == PAREDE:
                    pygame.draw.rect(tela, "#578a34", retangulo)
                else:
                    if anterior == 1:
                        pygame.draw.rect(tela, "#aad751", retangulo)
                    else:
                        pygame.draw.rect(tela, "#a2d149", retangulo)
                    anterior *= -1
                    
    def lerMapa(self, valorProcurado):
        for i, linha in enumerate(self.matriz):
            for j, valor in enumerate(linha):
                if valor == valorProcurado:
                   return [j, i]
        return False

    def quantElementos(self, valor):
        acumulador = 0
        for linha in self.matriz:
            acumulador += linha.count(valor)
        return acumulador

    def substituirElementoN(self, numElemento, valor, substituto):
        acumulador = 0
        for i, linha in enumerate(self.matriz):
            for j, v in enumerate(linha):
                if valor == v:
                    acumulador += 1
                if acumulador > numElemento:
                    self.matriz[i][j] = substituto
                    return [j,i]
    
    def SusbstituirElementoPos(self, posElemento, substituto):
        posMat = [posElemento[0]//tamanho, posElemento[1]//tamanho]
        self.matriz[posMat[1]][posMat[0]] = substituto
        

class Cobra(pygame.sprite.Sprite):
    def __init__(self, posMatriz):
        self.posicaoSprite = [posMatriz[0] * tamanho, posMatriz[1] * tamanho]
        self.posicaoMatriz = posMatriz
        self.corpoCobra = []
        self.trajeto = []
        self.ultimoMovimento = (0, 0)
        self.velocidade = 5.5

    def movimentacao(self):
        if len(self.trajeto) > 0:
            proxPos = [
                self.posicaoSprite[0] + self.trajeto[0][0] * self.velocidade,
                self.posicaoSprite[1] + self.trajeto[0][1] * self.velocidade,
            ]

            if (proxPos[0] > largura-tamanho*2 or proxPos[0] < tamanho or
                proxPos[1] > altura-tamanho*2 or proxPos[1] < tamanho):
                self.trajeto.clear()
                return

            matrizAnt = self.posicaoMatriz
            self.posicaoMatriz = [proxPos[0] // tamanho, proxPos[1] // tamanho]

            if matrizAnt != self.posicaoMatriz and len(self.trajeto) > 1:
                # Serve para corrigir uns bugs, mas nao tudo : (
                if (
                    bool(self.trajeto[0][0])
                    and matrizAnt[1] - self.posicaoMatriz[1] != 0
                ):
                    return
                elif (
                    bool(self.trajeto[0][1])
                    and matrizAnt[0] - self.posicaoMatriz[0] != 0
                ):
                    return

                if self.trajeto[0][0] == -1:
                    self.posicaoSprite[0] = (self.posicaoSprite[0] // tamanho) * tamanho
                elif self.trajeto[0][0] == 1:
                    self.posicaoSprite[0] = (proxPos[0] // tamanho) * tamanho
                elif self.trajeto[0][1] == -1:
                    self.posicaoSprite[1] = (self.posicaoSprite[1] // tamanho) * tamanho
                elif self.trajeto[0][1] == 1:
                    self.posicaoSprite[1] = (proxPos[1] // tamanho) * tamanho
                self.trajeto.pop(0)
            else:
                self.posicaoSprite = proxPos

    def aumentarCobra(self):
         self.corpoCobra.append(self.posicaoSprite)
         tamanhoCobra = pontos+tamanho
         if len(self.corpoCobra)>tamanhoCobra:
             del self.corpoCobra[0]
         for posicao in self.corpoCobra:
             self.rect = pygame.draw.rect(tela, (105,89,205), (posicao[0], posicao[1], tamanho,tamanho))

    def desenharCobra(self):
         self.rect = pygame.draw.rect(tela, (105,89,205), (self.posicaoSprite, (tamanho,tamanho)),1)

    def processarEventos(self, e):
        moveAnterior = self.ultimoMovimento

        if (
            e.key == pygame.K_LEFT
            or e.key == pygame.K_a
            and self.ultimoMovimento != [1, 0]
        ):
            self.ultimoMovimento = [-1, 0]
        elif (
            e.key == pygame.K_RIGHT
            or e.key == pygame.K_d
            and self.ultimoMovimento != [-1, 0]
        ):
            self.ultimoMovimento = [1, 0]
        elif (
            e.key == pygame.K_UP
            or e.key == pygame.K_w
            and self.ultimoMovimento != [0, 1]
        ):
            self.ultimoMovimento = [0, -1]
        elif (
            e.key == pygame.K_DOWN
            or e.key == pygame.K_s
            and self.ultimoMovimento != [0, -1]
        ):
            self.ultimoMovimento = [0, 1]

        if moveAnterior != self.ultimoMovimento and len(self.trajeto) <= 3:
            self.trajeto.append(self.ultimoMovimento)

class Fruta(pygame.sprite.Sprite):
    def __init__(self, cenario:Cenario):
        self.cenario = cenario
        posMatriz = self.cenario.lerMapa(2)
        self.posicao = [posMatriz[0]*tamanho, posMatriz[1]*tamanho]

    def desenharFruta(self):
        self.rect = pygame.draw.rect(
            tela, (255, 0, 0), (self.posicao, (tamanho, tamanho))
        )

    def gerarFruta(self):
        quant = self.cenario.quantElementos(0)
        espacoEscolhido = randint(0, quant)
        self.cenario.SusbstituirElementoPos(self.posicao, LIVRE)
        pos = self.cenario.substituirElementoN(espacoEscolhido, LIVRE, FRUTA)
        self.posicao = [pos[0]*tamanho, pos[1]*tamanho]

cenario = Cenario(matrizMapa)
fruta  = Fruta(cenario)
cobra = Cobra(cenario.lerMapa(3))

pontos = 0
while True:
    pygame.time.Clock().tick(60)

    cobra.movimentacao()

    tela.fill((0, 0, 0))
    cenario.criarMapa()
    cobra.desenharCobra()
    fruta.desenharFruta()
    cobra.aumentarCobra()

    pygame.display.update()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            cobra.processarEventos(e)
    
    if cobra.rect.colliderect(fruta.rect):
        fruta.gerarFruta()
        pontos +=1
        print(pontos)