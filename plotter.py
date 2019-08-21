import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd


def plotting(file_name):
    data = pd.read_csv(file_name, sep=';')

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.bar(x='year', height='value', data=data)

    ax.set(xlabel='Year', ylabel='ICL value', title='ICL gains at {} value'.format(file_name[8:-10]))

    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'
                                                      .format(x / 1000000) + ' Million'))
    ax.xaxis.set_major_locator(plt.MaxNLocator(8))
    plt.grid(True, 'major', 'y', ls='--', lw=.5, alpha=.3)
    plt.tick_params(axis='both', which='both', bottom=False, top=False,
                    labelbottom=True, left=False, right=False, labelleft=True)

    plt.savefig('{}.png'.format(file_name), bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    file = 'results/nominal_value.csv'
    plotting(file)
    file = 'results/present_value.csv'
    plotting(file)
