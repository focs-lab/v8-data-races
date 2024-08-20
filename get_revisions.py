import os
import re

pattern = r'revision="([a-f0-9]{40})"'
tests = {}

for f in os.listdir("logs"):
    log = open(f"logs/{f}").read()
    match = re.search(pattern, log)
    if match:
        commit = match.group(1)
    else:
        print(f"No commit found when parsing {f}")

    if commit not in tests.keys():
        tests[commit] = [f]
    else:
        tests[commit].append(f)

print(tests)
print("Num commits:", len(tests.keys()))
print(list(tests.keys()))

open("revisions.txt", "w").write("\n".join(list(tests.keys())))
