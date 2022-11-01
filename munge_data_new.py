import glob
import pandas as pd
import os

dir_list = glob.glob("data/donation_rate/*/*/*/")

dfs = []

for dirname in dir_list:

    data_files = [f for f in glob.glob(dirname + "/*.data") if "Phylogeny" not in f]
    if len(data_files) < 1:
        print("Something's wrong with the data files", dirname)
        continue
    df = pd.read_csv(data_files[0])
    df.set_index("update", inplace=True)
    prefix = data_files[0].split("/")[-1].split("_")[0]
    df = df.add_prefix(prefix)

    for filename in data_files[1:]:
        new_df = pd.read_csv(filename)
        new_df.set_index("update", inplace=True)
        prefix = filename.split("/")[-1].split("_")[0]
        new_df = new_df.add_prefix(prefix)
        df = pd.concat([df, new_df], axis=1)

    if not os.path.exists(dirname + "/run.log"):
        print("error: no run.log for", dirname)
    with open(dirname + "/run.log") as run_log:
        for line in run_log:
            if line.startswith("Update"):
                break
            if line.startswith("set"):
                sline = line.split()
                df[sline[1]] = sline[2]
    
    dfs.append(df)

all_data = pd.concat(dfs)
all_data.to_csv("all_data.csv")