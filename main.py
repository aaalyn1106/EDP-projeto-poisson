import numpy as np

from discretizacao import montar_sistema
from visualizacao import gerar_graficos
from solver import resolver_sistema


# 1. Montagem do sistema
A, b, x, y, contorno = montar_sistema(0.1)


# 2. Resolução pelo método de Gauss-Seidel
solucao, iteracoes, residuo = resolver_sistema(
    A, b,
    tol=1e-8,
    max_iter=10000
)


# 3. Reconstrução da matriz de potencial
V = contorno.copy()

ny, nx = len(y) - 2, len(x) - 2

V[1:-1, 1:-1] = solucao.reshape(ny, nx)


# 4. Exibição dos resultados
print("\nRESULTADO FINAL")
print("-------------------------")

print("Dimensão da matriz:", V.shape)
print("Número de iterações:", iteracoes)
print("Resíduo:", residuo)
print("Potencial máximo:", np.max(V))
print("Potencial mínimo:", np.min(V))

# 5. Comparação com a solução exata

X, Y = np.meshgrid(x, y)

exato = np.exp(X * Y)

erro_absoluto = np.abs(V - exato)

print("\nVALIDAÇÃO DA SOLUÇÃO")
print("-------------------------")
print("Erro absoluto máximo:", np.max(erro_absoluto))
erro_relativo = erro_absoluto / np.maximum(np.abs(exato), 1e-15)

print("Erro relativo máximo:", np.max(erro_relativo))

gerar_graficos(x, y, V)
