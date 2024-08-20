import os

logs = open("logs.txt").readlines()
for log in logs:
    print(log.split("/"))
    parts = log.split("/")
    build_id = parts[7]
    test_category = parts[10]
    test_name = parts[11].split("?")[0]

    os.system(f"wget -O logs/{build_id}-{test_category}-{test_name} {log}")
