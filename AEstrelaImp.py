from Posicao import Posicao
from AEstrela import AEstrela
from QuebraCabeca import QuebraCabeca
from QuebraCabecaImp import QuebraCabecaImp


class Nodo:
    def __init__(self, g, h, qc, pai, movimento):
        self.g = g
        self.h = h
        self.qc = qc
        self.pai = pai
        self.movimento = movimento


class AEstrelaImp(AEstrela):
    def possuiSolucao(self, qc):
        tabela = qc.getTab()
        tabela_formatada = []

        for i in range(3):
            for j in range(3):
                if tabela[i][j] != QuebraCabeca.VAZIO:
                    tabela_formatada.append(tabela[i][j])

        numero_inversoes = 0

        for i in range(7):
            for j in range(i + 1, 8):
                if tabela_formatada[i] > tabela_formatada[j]:
                    numero_inversoes += 1

        return numero_inversoes % 2 == 0

    def converterTabelaString(self, tabela):
        tabela_str = ''

        for i in range(3):
            for j in range(3):
                tabela_str += str(tabela[i][j])

        return tabela_str

    def melhorQuebraCabeca(self, quebra_cabeca_aberto):
        quebra_cabeca = ''
        menor_f = 9999

        for item in quebra_cabeca_aberto.items():
            if item[1].g + item[1].h < menor_f:
                quebra_cabeca = item[0]
                menor_f = item[1].g + item[1].h

        return quebra_cabeca

    # Recebe um quebra-cabeca e retorna uma lista de posições que representa os
    # movimentos necessarios para chegar a solucao.
    # @param qc - Quebra-cabeca com o estado inicial
    # @return lista com os movimentos a serem realizados
    def getSolucao(self, qc):
        if self.possuiSolucao(qc):
            quebra_cabeca_aberto = {self.converterTabelaString(qc.getTab()): Nodo(0, qc.getValor(), qc, None, None)}
            quebra_cabeca_fechado = {}

            while True:
                quebra_cabeca_atual = self.melhorQuebraCabeca(quebra_cabeca_aberto)
                quebra_cabeca_fechado.update({quebra_cabeca_atual: quebra_cabeca_aberto[quebra_cabeca_atual]})
                quebra_cabeca_aberto.pop(quebra_cabeca_atual)

                if quebra_cabeca_fechado[quebra_cabeca_atual].qc.isOrdenado():
                    caminho = []

                    while quebra_cabeca_fechado[quebra_cabeca_atual].pai:
                        caminho.append(quebra_cabeca_fechado[quebra_cabeca_atual].movimento)
                        quebra_cabeca_atual = self.converterTabelaString(quebra_cabeca_fechado[quebra_cabeca_atual].pai.qc.getTab())

                    return caminho[::-1]

                movimentos_possiveis = quebra_cabeca_fechado[quebra_cabeca_atual].qc.getMovePossiveis()

                for movimento in movimentos_possiveis:
                    novo_qc = QuebraCabecaImp()
                    novo_qc.setTab(quebra_cabeca_fechado[quebra_cabeca_atual].qc.getTab())
                    novo_qc.move(novo_qc.getPosVazio().getLinha(), novo_qc.getPosVazio().getColuna(), movimento.getLinha(), movimento.getColuna())

                    nova_chave = self.converterTabelaString(novo_qc.getTab())

                    novo_g = quebra_cabeca_fechado[quebra_cabeca_atual].g + 1
                    novo_h = novo_qc.getValor()
                    novo_pai = quebra_cabeca_fechado[quebra_cabeca_atual]
                    novo_movimento = Posicao(movimento.getLinha(), movimento.getColuna())

                    novo_nodo = Nodo(novo_g, novo_h, novo_qc, novo_pai, novo_movimento)

                    if nova_chave not in quebra_cabeca_fechado.keys() or (nova_chave in quebra_cabeca_aberto.keys() and (novo_g + novo_h) < (quebra_cabeca_aberto[nova_chave].g + quebra_cabeca_aberto[nova_chave].h)):
                        quebra_cabeca_aberto.update({nova_chave: novo_nodo})

        return [Posicao(-1, -1)]
