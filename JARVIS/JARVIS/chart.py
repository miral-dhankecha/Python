import json
import os
import matplotlib.pyplot as plt

# -------- SAFE LOAD --------
if not os.path.exists("usage.json"):
    with open("usage.json", "w") as f:
        json.dump({"open": 1, "close": 1, "search": 1, "play": 1}, f)

if not os.path.exists("response.txt"):
    with open("response.txt", "w") as f:
        f.write("0.5\n0.6\n0.4\n")

# -------- LOAD --------
with open("usage.json", "r") as f:
    data = json.load(f)

commands = list(data.keys())
usage = list(data.values())

plt.figure()
plt.bar(commands, usage)
plt.title("Jarvis Command Usage Analysis")
plt.xlabel("Commands")
plt.ylabel("Usage Count")

# -------- RESPONSE --------
times = []

with open("response.txt", "r") as f:
    for line in f:
        try:
            times.append(float(line.strip()))
        except:
            pass

plt.figure()
plt.plot(times)
plt.title("Jarvis Response Time Analysis")
plt.xlabel("Command Number")
plt.ylabel("Time (seconds)")

plt.show()