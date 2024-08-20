from git import Repo

count = 0
repo = Repo("v8")
for commit in repo.iter_commits("main"):
    if count == 50:
        break

    msg = commit.message
    if "data race" not in msg:
        continue

    # print(msg)
    for line in msg.splitlines():
        if line.startswith("Bug: ") and "v8:" not in line:
            break
        if line.startswith("Reviewed-on: ") and "https://chromium-review.googlesource.com" in line:
            reviewed_on = line.split(" ")[1].strip()
            print(reviewed_on)
            count += 1
            break
