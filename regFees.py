import matplotlib.pyplot as plt

years = ['2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
fees = [9.34, 10.50, 7.24, 8.00, 6.40, 10.30, 12.03, 13.42]

plt.rcParams["figure.figsize"] = (12, 6)
fig = plt.figure()
ax = fig.add_subplot(111)

plt.plot(years, fees, 'x-', color="green")
plt.title("evaluation of registration fees in germany")
plt.xlabel("years")
plt.ylabel("registration fee [€]")

for i, v in enumerate(fees):
    ax.annotate(str(v), xy=(i,v), xytext=(-7,7), textcoords='offset points')

plt.savefig("fees.png")