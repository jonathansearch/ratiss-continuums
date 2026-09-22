#!/usr/bin/env python3
"""Démo 10 s du tissu (1280x720, 10 fps) : ce que l'on mesure.
0-4 s : C01 franges Berry-2q (données réelles fez).
4-7 s : C02 décohérence en racine de N (courbes mesurées).
7-10 s : C08 Ramsey vs écho sur QPU (l'écho tue le canal a).
Sorties : images/demo-tissu.mp4 + images/demo-tissu.jpg (vignette).
Usage : python3 images/make_video.py (ffmpeg requis).
"""
import json
import os
import subprocess

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "resultats")
TMP = "/tmp/demo_frames"
TEAL, MAG, WHT = "#00e5cc", "#ff4fd8", "white"
plt.style.use("dark_background")

c01 = json.load(open(os.path.join(RES, "c01_reel.json")))
c02 = json.load(open(os.path.join(RES, "c02.json")))["cas"]
c08 = json.load(open(os.path.join(RES, "c08_reel.json")))
PHIS = [r["phi"] for r in c01["lignes"]]
PP = [r["pp_bell"]["P00"] for r in c01["lignes"]]
PM = [r["pm_bell"]["P00"] for r in c01["lignes"]]
CURVES = [(r["n"], r["tau_mes"], r["t"], r["C"])
          for r in c02 if "t" in r]
T08 = np.array(c08["delais_us"], float)


def seg1(ax, f):
    phi = 2 * np.pi * f / 39
    xs = np.linspace(0, phi, 200)
    for a, vals, tag, col in ((ax[0], PP, "++", TEAL),
                              (ax[1], PM, "+-", MAG)):
        a.clear()
        a.set_xlim(0, 2 * np.pi)
        a.set_ylim(-0.1, 1.15)
        a.set_xlabel("phi")
        a.set_title(f"Bell {tag}", color=col, fontsize=14)
        a.grid(alpha=0.2)
        if tag == "++":
            a.plot(xs, np.cos(xs) ** 2, color=col, lw=3)
            a.plot(phi, np.cos(phi) ** 2, "o", color=WHT, ms=9)
        else:
            a.plot(xs, np.ones_like(xs), color=col, lw=3)
            a.plot(phi, 1.0, "o", color=WHT, ms=9)
        for p, v in zip(PHIS, vals):
            if p <= phi + 1e-9:
                a.plot(p, v, "o", color=WHT, ms=6, alpha=0.9)
    ax[0].set_ylabel("P(00) base de Bell")
    return (f"C01 @ibm_fez — ++ : flips 0.99/0.02 · +− : plat ~0.99 · "
            f"phi={phi:.2f}")


def seg2(ax, f):
    ax.clear()
    tmax = 1000 * (f - 40) / 29
    ax.set_xlim(0, 1000)
    ax.set_ylim(-0.05, 1.1)
    ax.set_xlabel("t")
    ax.set_ylabel("C_N(t)")
    ax.grid(alpha=0.2)
    for n, tau, t, c in CURVES:
        t = np.array(t)
        c = np.array(c)
        m = t <= tmax
        ax.plot(t[m], c[m], lw=3, label=f"N={n} tau={tau}")
    ax.legend(fontsize=11, loc="upper right")
    return f"C02 — 1/tau en racine de N · t={tmax:.0f}"


def seg3(ax, f):
    k = 1 + int(9 * (f - 70) / 29)
    tmax = 300 * (f - 70) / 29
    for a, tag in ((ax[0], "ramsey"), (ax[1], "echo")):
        a.clear()
        a.set_xlim(0, 310)
        a.set_ylim(-0.05, 1.1)
        a.set_xlabel("t (us)")
        a.set_title(tag, fontsize=14)
        a.grid(alpha=0.2)
        y = 2 * np.array(c08[tag]["P0"]) - 1
        av, bv = c08[tag]["a"], c08[tag]["b"]
        tt = np.linspace(0, 300, 200)
        a.plot(tt, np.exp(-av * tt ** 2 - bv * tt), "r--", alpha=0.35)
        a.plot(T08[:k], y[:k], "o", color=TEAL, ms=7)
        m = tt <= tmax
        a.plot(tt[m], np.exp(-av * tt[m] ** 2 - bv * tt[m]), "r-", lw=3)
    ax[0].set_ylabel("2P0-1")
    return ("C08 @ibm_kingston — echo tue a (1.2e-3 -> ~0), "
            "b persiste")


def frame(f):
    fig = plt.figure(figsize=(12.8, 7.2))
    if f < 40:
        ax = [fig.add_subplot(1, 2, 1), fig.add_subplot(1, 2, 2)]
        sup = seg1(ax, f)
    elif f < 70:
        ax = fig.add_subplot(1, 1, 1)
        sup = seg2(ax, f)
    else:
        ax = [fig.add_subplot(1, 2, 1), fig.add_subplot(1, 2, 2)]
        sup = seg3(ax, f)
    fig.suptitle(sup, fontsize=15, color=WHT, y=0.97)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(os.path.join(TMP, f"f{f:03d}.png"), dpi=100,
                facecolor="black")
    if f == 20:
        fig.savefig(os.path.join(HERE, "demo-tissu.jpg"), dpi=80,
                    facecolor="black")
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs(TMP, exist_ok=True)
    for f in range(100):
        frame(f)
        if f % 25 == 0:
            print(f"[video] trame {f}/100", flush=True)
    mp4 = os.path.join(HERE, "demo-tissu.mp4")
    subprocess.run(["ffmpeg", "-y", "-framerate", "10", "-i",
                    os.path.join(TMP, "f%03d.png"), "-c:v", "libx264",
                    "-pix_fmt", "yuv420p", "-crf", "23", "-movflags",
                    "+faststart", mp4], check=True, capture_output=True)
    print(f"[video] archivé : {mp4} "
          f"({os.path.getsize(mp4) // 1024} ko)")
