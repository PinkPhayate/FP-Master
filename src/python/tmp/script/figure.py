import matplotlib.pyplot as plt

def figure_solr():
    X1 = [1,2,3,4]
    Y1 = [0.627066392,0.757069534,0.727960388,0.801059877]

    X2 = [1.4, 2.4, 3.4, 4.4]
    Y2 = [0.637995736,0.701957394,0.672059443,0.752041112]

    plt.bar(X1, Y1, color='#C0C0C0', width=0.4, label='RFN', align="center")
    plt.bar(X2, Y2, color='#5b70ff', width=0.4, label='ITG', align="center")

    # 凡例を表示
    plt.legend(loc="best")

    # X軸の目盛りを書き換える
    plt.xticks([1.2, 2.2, 3.2, 4.2], ['4.1.0-4.2.0','4.2.0-4.3.0','4.3.0-4.4.0','4.4.0-4.5.0'])
    plt.show()


def figure_derby():
    X1 = [1,2]
    Y1 = [0.886224864,0.828833024]

    X2 = [1.4, 2.4]
    Y2 = [0.884751282,0.844780548]

    plt.bar(X1, Y1, color='#C0C0C0', width=0.4, label='RFN', align="center")
    plt.bar(X2, Y2, color='#5b70ff', width=0.4, label='ITG', align="center")

    # 凡例を表示
    plt.legend(loc="best")

    # X軸の目盛りを書き換える
    plt.xticks([1.2, 2.2], ['10.8-10.9', '10.9-10.10'])
    plt.show()
