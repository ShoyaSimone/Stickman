"""Append finished Higgsfield jobs for extra shots to burkina_extra_jobs.tsv.

Stdin lines: '<extra number 1-81> <hhmmss> <job_id>'. Files are named
<prev image>__<next image>__<shot time>_<slug>.png, e.g.
001_0m00s__002_0m05s__0m02s_stock-certificate-freezing.png
"""
import sys
from burkina_prompts import SCENES
from burkina_extra_prompts import EXTRAS

BASE = "https://d8j0ntlcm91z4.cloudfront.net/user_3Kq8IWvi9gT29VWT7AzVa7kKv96/hf_"
DATE = sys.argv[1] if len(sys.argv) > 1 else "20261027"


def stamp(n, ts):
    m, s = ts.split(":")
    return f"{n:03d}_{int(m)}m{int(s):02d}s"


with open("burkina_extra_jobs.tsv", "a") as out:
    for line in sys.stdin:
        if not line.strip():
            continue
        num, hhmmss, job = line.split()
        prev, sec, slug, _ = EXTRAS[int(num) - 1]
        name = (f"{stamp(prev, SCENES[prev - 1][0])}__{stamp(prev + 1, SCENES[prev][0])}"
                f"__{sec // 60}m{sec % 60:02d}s_{slug}.png")
        out.write(f"{name}\t{job}\t{BASE}{DATE}_{hhmmss}_{job}.png\n")
