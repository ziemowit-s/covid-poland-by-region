import pandas
import numpy as np
import matplotlib.pyplot as plt

from covid_stats import CovidStats


def draw(df: pandas.DataFrame):
    # These are the colors that will be used in the plot
    color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                      '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                      '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                      '#c7c7c7']

    fig, ax = plt.subplots(1, 1, figsize=(12, 14))

    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    fig.subplots_adjust(left=.06, right=.94, bottom=.07, top=.94)

    x_range = [i for i in range(df.date.size)]

    ax.xaxis.set_major_formatter(plt.FuncFormatter('{:.0f}'.format))
    ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.0f}'.format))

    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

    plt.tick_params(axis='both', which='both', bottom='off', top='off',
                    labelbottom='on', left='off', right='off', labelleft='on')

    plt.xlabel("date")
    plt.ylabel("new cases")
    plt.xticks(x_range, df.date.tolist(), rotation=90, fontsize=10)
    plt.yticks(np.arange(start=0, step=50, stop=500), fontsize=10)
    for rank, column in enumerate(df.columns[1:]):

        line = plt.plot(x_range, df[column].tolist(), lw=2.5,
                        color=color_sequence[rank], label=column)

    fig.suptitle('COVID Poland by region', fontsize=18, ha='center')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    covid = CovidStats()
    df = covid.get_data()
    draw(df)