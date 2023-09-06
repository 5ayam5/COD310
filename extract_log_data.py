from sys import argv
from collections import defaultdict
from glob import glob
from os.path import join, isdir
from os import makedirs
import matplotlib.pyplot as plt
import pandas as pd

argc = len(argv)

names = {
    "baseline": "RoundRobin",
    "alternation": "Alternation",
    "mfu": "MFU",
    "greedy": "Greedy",
    "greedy2": "TemPo"
}

def extract_log(file, budget):
    with open(file, "r") as f:
        lines = f.readlines()

        epoch = 0
        count = 0
        channel_count = defaultdict(bool)
        channel_status = defaultdict(list)
        power_used = []
        pseudochannel_on_count = []
        channel_on_count = []

        for line in lines:
            if line.startswith("Power available:"):
                if epoch != 0:
                    if count == 0:
                        break
                    pseudochannel_on_count.append(count)
                    channel_on_count.append(sum(channel_count.values()))
                count = 0
                channel_count = defaultdict(bool)
                epoch += 1
            elif line.startswith("Channel"):
                channel = int(line.split()[1])
                channel_status[channel].append(epoch)
                count += 2
                channel_count[channel // 2] = True
            elif line.startswith("Remaining power:"):
                power_used.append(budget - max(0, float(line.split()[2])))

        pseudochannel_on_count.append(count)
        channel_on_count.append(sum(channel_count.values()))

    return channel_status, power_used, pseudochannel_on_count, channel_on_count, epoch

def extract_workload(directory, budget, workload):
    folders = glob(join(directory, f"WK{workload:02d}_*"))
    policies = [folder.split("_")[-1] for folder in folders]

    channels = defaultdict(defaultdict)
    powers = defaultdict(list)
    pseudochannel_on_counts = defaultdict(list)
    channel_on_counts = defaultdict(list)
    epochs = defaultdict(int)

    for (folder, policy) in zip(folders, policies):
        channel_status, power_used, pseudochannel_on_count, channel_on_count, epoch = extract_log(join(folder, "log"), budget)
        for channel in channel_status:
            channels[channel][policy] = channel_status[channel]
        powers[policy] = power_used
        pseudochannel_on_counts[policy] = pseudochannel_on_count
        channel_on_counts[policy] = channel_on_count
        epochs[policy] = epoch
    
    return channels, powers, pseudochannel_on_counts, channel_on_counts, epochs

def plot_workload(directory, budget, workload):
    channels, powers, pseudochannel_on_counts, channel_on_counts, epochs = extract_workload(directory, budget, workload)

    # check if directory exists
    if not isdir(join("plots", str(budget), f"{workload:02d}")):
        makedirs(join("plots", str(budget), f"{workload:02d}"))

    plt.rcParams["figure.figsize"] = (15, 10)

    colors = {
        "baseline": "blue",
        "alternation": "red",
        "mfu": "green",
        "greedy": "orange",
        "greedy2": "purple"
    }

    for channel in channels:
        fig, axs = plt.subplots(len(channels[channel]), 1, sharex=True, sharey=True)
        fig.suptitle(f"Channel {channel:02d}")
        
        for i, policy in enumerate(channels[channel]):
            y = [0] * channels[channel][policy][-1]
            for epoch in channels[channel][policy]:
                y[epoch - 1] = 1
            axs[i].plot(y, label=policy, color=colors[policy])
            axs[i].set_title(policy)
            axs[i].set_ylabel("Channel")
        axs[-1].set_xlabel("Epoch")
        plt.savefig(join("plots", str(budget), f"{workload:02d}", f"channel_{channel:02d}.png"))
        # plt.show()
        plt.clf()
        plt.close(fig)

    fig, axs = plt.subplots(len(powers), 1, sharex=True, sharey=True)
    fig.suptitle("Power used")
    for i, policy in enumerate(powers):
        axs[i].plot(powers[policy], label=policy, color=colors[policy])
        axs[i].set_title(policy)
        axs[i].set_ylabel("Power")
    axs[-1].set_xlabel("Epoch")
    plt.savefig(join("plots", str(budget), f"{workload:02d}", "power_used.png"))
    # plt.show()
    plt.clf()
    plt.close(fig)

    with open(join("plots", str(budget), f"{workload:02d}", "power_used.csv"), "w") as f:
        f.write("Epoch,")
        f.write(",".join(names[policy] for policy in powers))
        f.write("\n")
        T = max([len(powers[policy]) for policy in powers])
        for i in range(T):
            f.write(f"{i},")
            f.write(",".join([str(powers[policy][i]) if i < len(powers[policy]) else "" for policy in powers]))
            f.write("\n")

    fig, axs = plt.subplots(len(pseudochannel_on_counts), 1, sharex=True, sharey=True)
    fig.suptitle("Number of pesudochannels on")
    for i, policy in enumerate(pseudochannel_on_counts):
        axs[i].plot(pseudochannel_on_counts[policy], label=policy, color=colors[policy])
        axs[i].set_title(policy)
        axs[i].set_ylabel("Number of pseudochannels")
    axs[-1].set_xlabel("Epoch")
    plt.savefig(join("plots", str(budget), f"{workload:02d}", "pesudochannels_on.png"))
    # plt.show()
    plt.clf()
    plt.close(fig)

    with open(join("plots", str(budget), f"{workload:02d}", "pseudochannels_on.csv"), "w") as f:
        f.write("Epoch,")
        f.write(",".join(names[policy] for policy in pseudochannel_on_counts))
        f.write("\n")
        T = max([len(pseudochannel_on_counts[policy]) for policy in pseudochannel_on_counts])
        for i in range(T):
            f.write(f"{i},")
            f.write(",".join([str(pseudochannel_on_counts[policy][i]) if i < len(pseudochannel_on_counts[policy]) else "" for policy in pseudochannel_on_counts]))
            f.write("\n")

    fig, axs = plt.subplots(len(channel_on_counts), 1, sharex=True, sharey=True)
    fig.suptitle("Number of channels on")
    for i, policy in enumerate(channel_on_counts):
        axs[i].plot(channel_on_counts[policy], label=policy, color=colors[policy])
        axs[i].set_title(policy)
        axs[i].set_ylabel("Number of channels")
    axs[-1].set_xlabel("Epoch")
    plt.savefig(join("plots", str(budget), f"{workload:02d}", "channels_on.png"))
    # plt.show()
    plt.clf()
    plt.close(fig)

    with open(join("plots", str(budget), f"{workload:02d}", "channels_on.csv"), "w") as f:
        f.write("Epoch,")
        f.write(",".join(names[policy] for policy in channel_on_counts))
        f.write("\n")
        T = max([len(channel_on_counts[policy]) for policy in channel_on_counts])
        for i in range(T):
            f.write(f"{i},")
            f.write(",".join([str(channel_on_counts[policy][i]) if i < len(channel_on_counts[policy]) else "" for policy in channel_on_counts]))
            f.write("\n")
    
    return epochs

def write_max_temp(directory, budget, workload, epochs):

    banks = [f"B_{i}" for i in range(256)]

    csvs = {}
    for folder in glob(join(directory, f"WK{workload:02d}_*")):
        policy = folder.split("_")[-1]
        csvs[policy] = pd.read_csv(join(folder, "full_temperature_mem.trace"), sep='\t', nrows=epochs[policy])
    
    M, m = defaultdict(int), defaultdict(int)
    
    with open(join("plots", str(budget), f"{workload:02d}", "max_temp.csv"), "w") as f:
        f.write("Epoch,")
        f.write(",".join(names[policy] for policy in csvs))
        f.write("\n")
        T = max([len(csvs[policy]) for policy in csvs])
        for i in range(T):
            arr = [max([csvs[policy].iloc[i][bank] for bank in banks]) if i < len(csvs[policy]) else "" for policy in csvs]
            f.write(f"{i},")
            f.write(",".join(str(x) for x in arr))
            f.write("\n")
            
            for j, policy in enumerate(csvs):
                if arr[j] != "":
                    M[policy] = max(M[policy], arr[j])
                    m[policy] = min(m[policy], arr[j])

    with open(join("plots", str(budget), "max_temp.csv"), "a") as f:
        f.write(f"{workload},")
        f.write(",".join(str(M[policy]) for policy in csvs))
        f.write("\n")
    
    with open(join("plots", str(budget), "min_temp.csv"), "a") as f:
        f.write(f"{workload},")
        f.write(",".join(str(m[policy]) for policy in csvs))
        f.write("\n")


if __name__ == "__main__":
    if argc == 4:
        plot_workload(argv[1], int(argv[2]), int(argv[3]))
    elif argc == 2:
        for budget in (64, 96):
            with open(join("plots", str(budget), "max_temp.csv"), "w") as f:
                f.write("Workload,")
                f.write(",".join(names.values()))
                f.write("\n")
            
            with open(join("plots", str(budget), "min_temp.csv"), "w") as f:
                f.write("Workload,")
                f.write(",".join(names.values()))
                f.write("\n")

            for workload in (1, 3, 4, 5, 8, 10):
                epochs = plot_workload(join(argv[1], str(budget)), budget, workload)
                write_max_temp(join(argv[1], str(budget)), budget, workload, epochs)
    else:
        print("Usage: python extract_log_data.py <directory> <budget> <workload>")
        print("Usage: python extract_log_data.py <directory>")