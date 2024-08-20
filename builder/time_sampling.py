from subprocess import run, STDOUT, CalledProcessError
import yaml
import re

pattern = r'^SUMMARY: ThreadSanitizer:.*$'

revisions = [
    "15e45fb834e31c9f1de01d3bd1021eb6d5dd65e0",
    "480a491e79337163be10655ce243587b14bcefb2",
    "5742e8f05cc68e46cd47fbef7e9352ff0dac9e7c",
    "d31e52879b6ee0e483d12f96684c93d3f4a2246f",
    "80fc53dd3ac81e3350ecdfc4bfa50e50ea8cde03",
    "2eb530ff76cd9d2ff7e80f26714c6732e0f79ac5",
    "53799101225772729a4dffc0976907b1c15dc0d4",
    "becdb484385119f0f4f5b1aef097ed41ab585e4b",
    "5aae428f5763875db5fdd67959f58aef60b28f18",
    "0eae0380ff6053932b1285caeec3b3eadc3b5915",
    "95c855348dc99f87e3a2430671895e476dc84a91",
    "9ee1ba176a52b9ba6f8a773f7b0a5f1d9c77e4af",
    "e70138196420755a503ea02dbd376d672a90eab4",
    "3419574f22aaf45e07a986ac5953170d32c18c1d",
    "27a0f364839889c194cb083cb4c1cd32c1ad284f",
    "fc437c335c727caf6c22f880809bf63cc34a4a62",
    "9b7d2a9cd9bbcec35d5008a43056bfd1e1914a81"
]

tools = [
    "sampling-base",
    "sampling-uclocks",
    "sampling-ol"
]

all_commands = yaml.load(open("commands.yaml"), yaml.BaseLoader)
all_races = yaml.load(open("races.yaml"), yaml.BaseLoader)

for rev in revisions:
    print("[+] Testing", rev)
    for tool in tools:
        print("[++] Testing", tool)
        commands = all_commands[rev]
        for cmd in commands:
            orig_cmd = cmd
            cmd = cmd.replace("SET_OUTDIR_HERE", f"../build-{tool}")
            # cmd = cmd.replace("--exit-after-n-failures=1", "--exit-after-n-failures=10")
            # try a few times, maybe it crashed due to segv or something
            print("[--] Command:", cmd)
            for i in range(2):
                v8_path = f"/home/users/nus/dws.lim/scratch/v8-tests/builds/v8-{rev}/v8"
                output = run(cmd.split(" "), capture_output=True, cwd=v8_path, text=True)
                if "ThreadSanitizer" not in output.stdout:
                    continue

                races = set(re.findall(pattern, output.stdout, re.MULTILINE))
                correct_races = set(all_races[rev][orig_cmd])

                diff = (races | correct_races) - (races & correct_races)
                if len(diff) != 0:
                    print("[X] Difference detected")
                    print("  Correct:", correct_races)
                    print("  Ours:", races)
                    print("  Diff:", diff)

                break
        print("")
    print("")

