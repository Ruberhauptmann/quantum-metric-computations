import sys
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt

if __name__ == "__main__":
    U_list = sys.argv[1:-1]

    plot_path = Path(sys.argv[-1])
    plot_path.mkdir(exist_ok=True, parents=True)

    fig, ax = plt.subplots()

    for U_file in U_list:
        U = U_file.split("/")[-1].split("_")[-1].strip(".csv")
        U_plot_path = plot_path.joinpath(f"U_{U}")
        U_plot_path.mkdir(exist_ok=True, parents=True)

        results = pd.read_csv(U_file)

        ax.plot(results.loc[:, "beta"], results.loc[:, "order_parameter"], "x--")
        ax.set_xlabel("$\\beta$")
        ax.set_ylabel("$OP$")

        fig.savefig(U_plot_path.joinpath("beta_OP.pdf"))
        ax.cla()
