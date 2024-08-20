from subprocess import run, STDOUT, CalledProcessError
import os

pattern = r'^SUMMARY: ThreadSanitizer:.*$'

revisions = [
    # "15e45fb834e31c9f1de01d3bd1021eb6d5dd65e0",
    # "480a491e79337163be10655ce243587b14bcefb2",
    # "5742e8f05cc68e46cd47fbef7e9352ff0dac9e7c",
    # "d31e52879b6ee0e483d12f96684c93d3f4a2246f",
    # "80fc53dd3ac81e3350ecdfc4bfa50e50ea8cde03",
    # "2eb530ff76cd9d2ff7e80f26714c6732e0f79ac5",
    "53799101225772729a4dffc0976907b1c15dc0d4",
    # "becdb484385119f0f4f5b1aef097ed41ab585e4b",
    # "5aae428f5763875db5fdd67959f58aef60b28f18",
    # "0eae0380ff6053932b1285caeec3b3eadc3b5915",
    # "95c855348dc99f87e3a2430671895e476dc84a91",
    # "9ee1ba176a52b9ba6f8a773f7b0a5f1d9c77e4af",
    # "e70138196420755a503ea02dbd376d672a90eab4",
    # "3419574f22aaf45e07a986ac5953170d32c18c1d",
    # "27a0f364839889c194cb083cb4c1cd32c1ad284f",
    # "fc437c335c727caf6c22f880809bf63cc34a4a62",
    # "9b7d2a9cd9bbcec35d5008a43056bfd1e1914a81"
]

tools = [
    "sampling-base",
    "sampling-uclocks",
    "sampling-ol"
]

for rev in revisions:
    print("[+] Building sampling variants for", rev)
    for tool in tools:
        print("[**]", tool)
        os.system(f"""
export PATH=~/scratch/v8/depot_tools:$PATH\n
cd builds\n
cd v8-{rev}\n
cd v8\n
rm out/build/d8\n
cp ~/scratch/v8-tests/libs/tsan-{tool}/* third_party/llvm-build/Release+Asserts/lib/clang/$(ls third_party/llvm-build/Release+Asserts/lib/clang)/lib/x86_64-unknown-linux-gnu/\n
ninja -C out/build -j`nproc` d8\n
strings out/build/d8 | grep TSAN-\n
cp -r out/build ../build-{tool}\n
        """)
