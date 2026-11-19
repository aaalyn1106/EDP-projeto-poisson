import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


def gerar_graficos(x, y, V):
    fig, ax = plt.subplots()

    mapa = ax.pcolormesh(x, y, V, shading="nearest", cmap="viridis")
    fig.colorbar(mapa, ax=ax, label="Potencial V")

    ax.set_title("Distribuição numérica do potencial elétrico")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_xticks(range(6))
    ax.set_yticks(range(4))
    ax.set_aspect("equal")
    niveis = [10, 100, 1_000, 10_000, 100_000, 1_000_000]
    curvas = ax.contour(x, y, V, levels=niveis, colors="white", linewidths=0.9)
    ax.clabel(curvas, fmt="%g", fontsize=8)
    X, Y = np.meshgrid(x, y)

    fig_3d = plt.figure(figsize=(9, 6))
    ax_3d = fig_3d.add_subplot(111, projection="3d")

    superficie = ax_3d.plot_surface(X, Y, V, cmap="viridis")

    ax_3d.set_title("Superfície 3D do potencial")
    ax_3d.set_xlabel("x")
    ax_3d.set_ylabel("y")
    ax_3d.set_zlabel("Potencial V")

    fig_3d.colorbar(superficie, ax=ax_3d, shrink=0.65, pad=0.12, label="Potencial V")

    pasta = Path(__file__).parent / "figuras"
    pasta.mkdir(exist_ok=True)

    fig.savefig(pasta / "mapa_equipotenciais.png", dpi=300, bbox_inches="tight")
    fig_3d.savefig(pasta / "superficie_3d.png", dpi=300, bbox_inches="tight")

    plt.show()