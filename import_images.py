"""Download images listed in a TSV (filename, job_id, url) into a folder.

    python3 import_images.py burkina_jobs.tsv images/burkina
"""
import os
import sys
import urllib.request

tsv, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
for line in open(tsv):
    if not line.strip():
        continue
    name, _job, url = line.rstrip("\n").split("\t")
    path = os.path.join(out, name)
    if not os.path.exists(path):
        print("downloading", name)
        urllib.request.urlretrieve(url, path)
print("done:", len(os.listdir(out)), "files in", out)
