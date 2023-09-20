import math
import os
import seaborn as sns
import matplotlib.pyplot as plt

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
    
    columns = math.ceil(number_of_subplots/rows)
    subplot_index = 1
    palette_index = 0

    # create color palette
    palette_list = sns.color_palette(sns_palette, len(categories_list))

    # create subplots by iterating through 'categories_list' 
    fig, ax = plt.subplots(rows, columns, figsize=(figsize_x, figsize_y), sharey=True)
    for category in categories_list:
        plot_data = dataframe[dataframe[categories] == category]
        plt.subplot(rows, columns, subplot_index)
        ax = sns.scatterplot(x = x_values, y = y_values, data = plot_data, color= palette_list[palette_index], alpha = 0.5)
        plt.title(category)

        if len(plot_data) > 2:
            # Calculate the pearsonr value
            corr_coeff, _ = pearsonr(plot_data[x_values], plot_data[y_values])

            # Annotate the plot with pearsonr value
            ax.annotate(f"Pearson r: {corr_coeff:.2f}", xy=(0.05, 0.95), xycoords='axes fraction', fontsize=12)

        subplot_index += 1
        palette_index += 1
    fig.suptitle(title)
    plt.tight_layout()
    plt.savefig(os.path.join('Visualizations', title))
    plt.show()