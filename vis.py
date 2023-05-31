
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def look_at_bunch_of_samples(list_points, list_labels, x_label, y_label):
    df = pd.DataFrame(list_points).T
    df.columns = list_labels
    sns.set_theme(style="ticks")

    # Initialize the figure with a logarithmic x axis
    f, ax = plt.subplots(figsize=(7, 6))


    # Plot the orbital period with horizontal boxes
    sns.boxplot(data=df, whis=[0, 100], width=.6, palette="vlag")

    # Add in points to show each observation
    sns.stripplot(data=df,
                size=4, color=".3", linewidth=0)

    # Tweak the visual presentation
    ax.xaxis.grid(True)
    ax.set(ylabel=y_label)
    #sns.despine(trim=True, left=True)
    plt.savefig('box_plot_good_start.pdf')
    plt.close()

    f, ax = plt.subplots(figsize=(7, 6))


    # Plot the orbital period with horizontal boxes
    sns.boxenplot(data=df, palette="vlag")

    # Add in points to show each observation
    sns.stripplot(data=df,
                size=4, color=".3", linewidth=0)

    # Tweak the visual presentation
    ax.xaxis.grid(True)
    ax.set(ylabel=y_label)
    #sns.despine(trim=True, left=True)
    plt.savefig('boxenplot_good_start.pdf')
    plt.close()

    f, ax = plt.subplots(figsize=(7, 6))
    sns.violinplot(data=df, palette="light:g", inner="points", orient="v", cut=0)
    plt.savefig('violin_good_start.pdf')
    plt.close()