import os

revisions = open("revisions.txt").readlines()

for revision in revisions:
    print("Building v8 @", revision)
    os.system(f"""
export PATH=~/scratch/v8/depot_tools:$PATH\n
cd builds\n
mkdir v8-{revision}\n
cd v8-{revision}\n
echo "Fetching v8"\n
fetch v8\n
cd v8\n
git checkout {revision}\n
gclient sync -D\n
gn gen out/build --args='dcheck_always_on=false is_component_build=false is_debug=false is_tsan=true target_cpu="x64" v8_enable_test_features=true'\n
ninja -C out/build -j`nproc` d8\n
            """)
