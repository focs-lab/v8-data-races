import os
import re
import yaml

pattern = r'revision="([a-f0-9]{40})"'
pattern2 = r'^tools/run-tests\.py.*$'
tests = {}

for f in os.listdir("logs"):
    log = open(f"logs/{f}").read()
    match = re.search(pattern, log)
    if match:
        commit = match.group(1)
    else:
        print(f"No commit found when parsing {f}")

    cmds = re.findall(pattern2, log, re.MULTILINE)
    for cmd in cmds:
        if commit not in tests.keys():
            tests[commit] = [cmd]
        else:
            tests[commit].append(cmd)

# print(tests)
print("Num commits:", len(tests.keys()))
# print(list(tests.keys()))

yaml.dump(tests, open("commands.yaml", "w"))