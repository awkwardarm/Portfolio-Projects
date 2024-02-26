import math
import os
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

def scatter_with_subplots(dataframe, x_values, y_values, categories, sns_palette, figsize_x, figsize_y, title):
    # Function that creates scatterplots with auto-arranged layout    

    # get the number or rows and columns for subplot
    categories_list = dataframe[categories].value_counts().index.tolist()
    number_of_subplots = len(categories_list)

    # set the number of rows for the subplot
    if number_of_subplots <= 4:
        rows = 1
    elif number_of_subplots <= 8:
        rows = 2
    elif number_of_subplots <= 12:
        rows = 3
    else:
        print('Too many categories.')
    
    # determine max number of columns
    columns = math.ceil(number_of_subplots/rows)
    
    # set indices for loop
    subplot_index = 1
    palette_index = 0

    # create color palette
    palette_list = sns.color_palette(sns_palette, len(categories_list))

    # create figure
    fig, ax = plt.subplots(rows, columns, figsize=(figsize_x, figsize_y), sharey=True)

    # create subplots by iterating through 'categories_list' 
    for category in categories_list:

        # filter plot data by category
        plot_data = dataframe[dataframe[categories] == category]

        # create subplot for plot_data
        plt.subplot(rows, columns, subplot_index)
        ax = sns.scatterplot(x = x_values, y = y_values, data = plot_data, color= palette_list[palette_index], alpha = 0.5)
        plt.title(category)

        # annotate pearsonr values if more than 2 data points
        if len(plot_data) > 2:
            # Calculate the pearsonr value
            corr_coeff, _ = pearsonr(plot_data[x_values], plot_data[y_values])

            # Annotate the plot with pearsonr value
            ax.annotate(f"Pearson r: {corr_coeff:.2f}", xy=(0.05, 0.95), xycoords='axes fraction', fontsize=12)

        # advance indices
        subplot_index += 1
        palette_index += 1

    # create global figure
    fig.suptitle(title)
    plt.tight_layout()
    plt.savefig(os.path.join('Visualizations', title))
    plt.show()
