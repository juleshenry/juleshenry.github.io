import matplotlib.pyplot as plt

Roth = 7000
over_flow = 0
x_values = []
y_values = []


def roth_ira_growth(port, net, roth_max=7000):
    ira = min(roth_max, net) * 2 * 1.085 + port['ira']
    roth_ballin = net > roth_max
    gold_mult = (net - roth_max) * 1.15 if roth_ballin else 0
    return {'ira': ira, 'pocket': gold_mult + port['pocket']}

y = P = 9518

def plot():
    for year in range(2024, 2075):
        x_values.append(year)
        y_values.append(y)
        y = P = roth_ira_growth(P)
        print(f"{year}: {P}")

    plt.plot(x_values, y_values)
    plt.xlabel("Year")
    plt.ylabel("Value")
    plt.title("Roth IRA Growth")
    # plt.axhline(y=7000, color="r", linestyle="--", label="Roth IRA Limit")
    plt.legend()
    plt.show()

port = {'ira': 0, 'pocket': 9518}
for i in range(1,11):
    x_values.append(i + 2024)
    y_values.append(sum(port.values()))
    print('year '+str(i))
    print(port, sum(port.values()))
    port = roth_ira_growth(port, 9518)
plt.plot(x_values, y_values)
plt.xlabel("Year")
plt.ylabel("Value")
plt.title("Roth IRA Growth")
# plt.axhline(y=7000, color="r", linestyle="--", label="Roth IRA Limit")
plt.legend()
plt.show()