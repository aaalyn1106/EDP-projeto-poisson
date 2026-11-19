import numpy as np
from scipy.sparse import lil_matrix


# Função do lado direito da equação de Poisson
def f(x, y):
    return (x**2 + y**2) * np.exp(x * y)


# Montagem do sistema linear
def montar_sistema(h=0.1):

    Lx, Ly = 5.0, 3.0

    # Verifica o tamanho do passo
    if h <= 0:
        raise ValueError("O passo deve ser positivo.")

    Nx = int(round(Lx / h))
    Ny = int(round(Ly / h))

    if not (np.isclose(Nx * h, Lx) and np.isclose(Ny * h, Ly)):
        raise ValueError("O passo deve dividir o domínio em ambos os eixos.")

    # Criação da malha
    x = np.linspace(0, Lx, Nx + 1)
    y = np.linspace(0, Ly, Ny + 1)

    # Quantidade de pontos internos
    nx, ny = Nx - 1, Ny - 1

    # Quantidade total de incógnitas
    total = nx * ny

    # Matriz e vetor do sistema
    A = lil_matrix((total, total), dtype=float)
    b = np.zeros(total)

    # Matriz que armazena as condições de contorno
    # Linhas representam y e colunas representam x
    contorno = np.full((Ny + 1, Nx + 1), np.nan)

    # Aplicação das condições de contorno
    contorno[0, :] = 1.0
    contorno[-1, :] = np.exp(3 * x)
    contorno[:, 0] = 1.0
    contorno[:, -1] = np.exp(Lx * y)

    # Montagem da matriz A e do vetor b
    for j in range(1, Ny):

        for i in range(1, Nx):

            # Índice correspondente ao ponto interno
            p = (j - 1) * nx + (i - 1)

            # Coeficiente central
            A[p, p] = 4.0

            # Termo independente da equação
            b[p] = -h**2 * f(x[i], y[j])

            # Vizinho da esquerda
            if i > 1:
                A[p, p - 1] = -1.0
            else:
                b[p] += contorno[j, i - 1]

            # Vizinho da direita
            if i < Nx - 1:
                A[p, p + 1] = -1.0
            else:
                b[p] += contorno[j, i + 1]

            # Vizinho inferior
            if j > 1:
                A[p, p - nx] = -1.0
            else:
                b[p] += contorno[j - 1, i]

            # Vizinho superior
            if j < Ny - 1:
                A[p, p + nx] = -1.0
            else:
                b[p] += contorno[j + 1, i]

    # Conversão para formato esparso CSR
    A = A.tocsr()

    return A, b, x, y, contorno


# Execução da parte 1
if __name__ == "__main__":

    from scipy.sparse.linalg import spsolve

    A, b, x, y, contorno = montar_sistema(0.1)

    print("SISTEMA LINEAR MONTADO")
    print("----------------------")

    print("Quantidade de pontos em x:", len(x))
    print("Quantidade de pontos em y:", len(y))
    print("Quantidade de incógnitas:", len(b))
    print("Dimensão da matriz A:", A.shape)
    print("Dimensão do vetor b:", b.shape)

    # Validação: resolve com spsolve
    # e compara com a solução exata V = e^(xy)
    ny, nx = len(y) - 2, len(x) - 2

    V = contorno.copy()
    V[1:-1, 1:-1] = spsolve(A, b).reshape(ny, nx)

    X, Y = np.meshgrid(x, y)

    exato = np.exp(X * Y)
    erro = np.abs(V - exato)

    print("\nVALIDAÇÃO (spsolve vs. solução exata e^(xy))")
    print("--------------------------------------------")

    print(f"Erro absoluto máximo: {erro.max():.3e}")
    print(f"Erro relativo máximo: {(erro / exato).max():.3e}")

    print("\nMatriz A e vetor b preparados para resolução.")