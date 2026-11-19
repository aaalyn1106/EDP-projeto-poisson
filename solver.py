import numpy as np


def resolver_sistema(A, b, tol=1e-8, max_iter=10000):

    n = len(b)

    # Chute inicial
    V = np.zeros(n)

    # Verificação da matriz
    if A.shape[0] != A.shape[1] or A.shape[0] != n:
        raise ValueError("Dimensões incompatíveis.")

    # Verifica se existem elementos diagonais nulos
    diagonal = A.diagonal()

    if np.any(np.abs(diagonal) < 1e-14):
        raise ValueError("A matriz possui elemento diagonal nulo.")

    # Estrutura CSR da matriz esparsa
    A = A.tocsr()

    for k in range(max_iter):

        V_anterior = V.copy()

        # Percorre todas as equações
        for i in range(n):

            inicio = A.indptr[i]
            fim = A.indptr[i + 1]

            colunas = A.indices[inicio:fim]
            valores = A.data[inicio:fim]

            # Soma dos termos fora da diagonal
            soma = np.dot(valores, V[colunas])
            soma -= diagonal[i] * V[i]

            # Atualização de Gauss-Seidel
            V[i] = (b[i] - soma) / diagonal[i]

        # Critério de convergência
        erro = np.linalg.norm(V - V_anterior, np.inf)

        if erro < tol:
            residuo = np.linalg.norm(A @ V - b, np.inf)

            print("CONVERGÊNCIA ALCANÇADA!")
            print("Iterações:", k + 1)
            print("Erro entre iterações:", erro)
            print("Resíduo:", residuo)

            return V, k + 1, residuo

    raise RuntimeError(
        "O método não convergiu dentro do limite de iterações."
    )