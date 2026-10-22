"""Download Higgsfield results listed in hf_jobs.tsv into hf_images/ with timestamped names.
Run on your own computer: python3 download_hf.py"""
import os, subprocess
from scenes import S

os.makedirs("hf_images", exist_ok=True)
for line in open("hf_jobs.tsv"):
    idx, job, url = line.split("\t")
    i = int(idx)
    ts, slug, _ = S[i - 1]
    m, s = ts.split(":")
    out = f"hf_images/{i:03d}_{int(m)}m{int(s):02d}s_{slug}.png"
    if not os.path.exists(out):
        subprocess.run(["curl", "-sSf", "-o", out, url.strip()], check=True)
print(len(os.listdir("hf_images")), "files")
