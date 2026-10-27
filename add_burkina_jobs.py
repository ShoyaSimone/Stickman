"""Append finished Higgsfield jobs to burkina_jobs.tsv. Stdin lines: '<index> <hhmmss> <job_id>'."""
import sys
from burkina_prompts import SCENES

BASE = "https://d8j0ntlcm91z4.cloudfront.net/user_3Kq8IWvi9gT29VWT7AzVa7kKv96/hf_"
DATE = sys.argv[1] if len(sys.argv) > 1 else "20261027"
with open("burkina_jobs.tsv", "a") as out:
    for line in sys.stdin:
        if not line.strip():
            continue
        idx, stamp, job = line.split()
        ts, slug, _ = SCENES[int(idx) - 1]
        m, s = ts.split(":")
        name = f"{int(idx):03d}_{int(m)}m{int(s):02d}s_{slug}.png"
        out.write(f"{name}\t{job}\t{BASE}{DATE}_{stamp}_{job}.png\n")
