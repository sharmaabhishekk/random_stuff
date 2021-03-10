import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from adjustText import adjust_text

##plt.style.use("custom_viz_dark") 
fig, ax = plt.subplots(figsize=(8,5))

df = pd.read_csv("pl_temp_data.csv")
df["xg_per_90"] = df["xG"]/df["M"]
df["xga_per_90"] = df["xGA"]/df["M"]

step = .5 ##increase to get fewer gradient bands
intercepts = np.arange(-3, 3+step, step) ##the values (-3, 3) are hardcoded based on the y limit you want to set in the plot
cmap = cm.get_cmap("viridis")
colors = cmap(np.linspace(0,1, intercepts.shape[0])) ##get out linearly spaced colormap 

for i, color in zip(intercepts, colors):
    xs = np.linspace(0, 3, 10); ys = xs*np.pi/4 + i; y2 = ys-step
    ax.fill_between(x=xs, y1=ys, y2=y2, color=color, alpha=.5) ##the main gradient call

## Sample data    
ax.scatter(df["xg_per_90"], df["xga_per_90"], marker="h", color="dodgerblue", ec="k", alpha=.8, s=150)
texts = []
for row in df.itertuples():
    texts.append(ax.text(s=row.Team, x=row.xg_per_90, y=row.xga_per_90, fontsize=7))

adjust_text(texts) ##to fix overlapping texts

##Other aesthetics
ax.set(xlim=(0,3), ylim=(0.5,3), xlabel="xG Created (per 90)", ylabel="xG Allowed (per 90)")    
ax.title.set(text="Premier League 20/21: Expected Performance", fontsize=18, ha="left", x=0, fontweight="bold")    
##plt.show()
