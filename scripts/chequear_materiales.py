from __future__ import annotations

import matplotlib
matplotlib.use("Agg")

from pathlib import Path
import sys

sys.path.insert(0, str(Path("src").resolve()))

from labo3_magpylib import SimulacionCampoMagnetico


def main() -> None:
    iman = SimulacionCampoMagnetico.iman_cilindrico()
    tabla = iman.perfil_eje(eje="z", rango=(0.01, 0.05), n=20)
    assert not tabla.empty
    assert "Bz [mT]" in tabla.columns

    sol = SimulacionCampoMagnetico.solenoide_discreto(corriente=2.0, radio=0.01, largo=0.03, espiras=10)
    mediciones = sol.medir_en_puntos([(0, 0, 0), (0, 0, 0.01)])
    assert len(mediciones) == 2

    ax, _ = iman.graficar_perfil_eje()
    ax.figure.savefig("salida_chequeo_perfil.png", dpi=120)
    ax2, _ = sol.graficar_mapa(n1=30, n2=30)
    ax2.figure.savefig("salida_chequeo_mapa.png", dpi=120)

    print("Chequeo completado correctamente.")


if __name__ == "__main__":
    main()
