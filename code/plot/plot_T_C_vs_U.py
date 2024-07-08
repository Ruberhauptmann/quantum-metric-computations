import sys
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt

if __name__ == "__main__":
    result_file = sys.argv[1]

    plot_path = Path(sys.argv[2])
    plot_path.mkdir(exist_ok=True, parents=True)

    results = pd.read_csv(result_file)

    fig, ax = plt.subplots()

    ax.plot(-results.loc[:, "U"], results.loc[:, "T_C"], "x--")
    ax.set_xlabel("$-U$")
    ax.set_ylabel("$T_C$")

    fig.savefig(plot_path.joinpath("T_C_vs_U.pdf"))
