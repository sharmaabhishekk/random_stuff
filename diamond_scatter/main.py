import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
import mpl_toolkits.axisartist.floating_axes as floating_axes
from sklearn.preprocessing import StandardScaler

import pandas as pd
import numpy as np

df = pd.read_csv("data.csv")

df = df[["Player", "Pos", "90s", "Carries_1/3", "1/3"]]
mf_positions = ['MF']
min_90s = 8
df = df[(df["90s"]>min_90s) & (df["Pos"].isin(mf_positions))].reset_index(drop=True)
df[["Carries_1/3", "1/3"]] = df[["Carries_1/3", "1/3"]].div(df["90s"], axis=0)

xs = StandardScaler().fit_transform(df["Carries_1/3"].values.reshape(-1, 1))
ys = StandardScaler().fit_transform(df["1/3"].values.reshape(-1, 1))

with plt.style.context("custom_viz_dark"):
    fig = plt.figure(figsize=(8,8))

    plot_extents = -2.4, 5.6, -2.4, 5.6
    transform = Affine2D().rotate_deg(45)
    helper = floating_axes.GridHelperCurveLinear(transform, plot_extents)
    ax = floating_axes.FloatingSubplot(fig, 111, grid_helper=helper)
    ax.grid(alpha=0.5, linestyle="-.")
    fig.add_subplot(ax)

    ax.scatter(xs, ys, ec='k', alpha=.5, s=50, marker="h")
    ax.set_aspect(1)

    ###highlight top percentile players
    player_names = list(set(df.sort_values("Carries_1/3")["Player"].tail(7).tolist() + df.sort_values("1/3")["Player"].tail(7).tolist()))

    sel_df = df.query("Player == @player_names")
    sel_idx = sel_df.index; player_names = sel_df.Player.tolist()
    sel_xs = xs[sel_idx]; sel_ys = ys[sel_idx]

    ax.scatter(sel_xs, sel_ys, color="dodgerblue", ec="k", alpha=.5, s=70, marker="h")
    for name, x, y in zip(player_names, sel_xs, sel_ys):
        ax.text(x, y, name.split(" ")[-1], fontsize=8, fontstyle="italic")
    ax.axis[:].major_ticklabels.set_alpha(0)

    ax.set(xlabel="Carries into Final Third", ylabel="Passes into Final Third")
    fig.text(x=0.5, y=0.95, s="Ball Progression Profile", fontsize=18, fontweight="light", ha="center")
    fig.text(x=0.5, y=0.9, s= f"Europe's Top 5 Leagues | Position: Midfielders | Minimum minutes: {min_90s*90}", 
        fontsize=12, fontweight="light", ha="center")

fig.savefig("diamond_plot.png", dpi=180)
plt.show()