import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv',parse_dates=True,index_col='date')

# Clean data by filtering out days when views were in top and botton 2.5% of the dataset

#these could be regarded as outliers
df = df[
  (df['value'] >= (df['value'].quantile(0.025)))
  &
  (df['value'] <= (df['value'].quantile(0.975)))
]


def draw_line_plot():
    # Draw line plot 
    #mentioning the size of the figure
    fig = plt.figure(figsize=(10,5))
    plt.plot(df.index, df['value'],color='red')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    #we have already parsed dates where df.index is the date column
    df["year"]=df.index.year
    df["months"]=df.index.month
    #grouping months by year and bars representing avg daily sales for each month
    df_bar = df.groupby(["year","months"])["value"].mean()
    df_bar=df_bar.unstack()
    
    #we will have to unstack the chart so the months are shown as side by side bars for each year as the grouping category
    

    # Draw bar plot
    fig=df_bar.plot.bar(legend=True,figsize=(10,5),ylabel="Average Page Views",xlabel="Years").figure
    
    #legend should have names of the month 
    plt.legend(['January','February','March','April','May','June','July','August','September',
            'October','November','December'])
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    
    #aggregating year and month wise data
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    
    # Draw box plots (using Seaborn)
    fig,ax=plt.subplots(nrows=1,ncols=2)
#subplots lets create plots side by side,here plots are year and month wise
#rows show the y axis on both plots which is the same ie values thus row=1
#columns show the x axis which is year in the first plot and month in the second

    fig.set_size_inches(12,5)
    fig.tight_layout(pad=4)
#tight_layout automatically adjusts subplot params so that the subplot(s) fits in to the figure area

    #Drawing the boxplots
    sns.boxplot(x=df_box['year'],y=df_box['value'],ax=ax[0]).set(xlabel='Year',ylabel='Page Views')
    sns.boxplot(x = df_box['month'], y = df_box['value'],order=["Jan","Feb", "Mar", "Apr", "May","Jun","Jul","Aug", "Sep","Oct","Nov","Dec"], ax = ax[1]).set(xlabel='Month', ylabel='Page Views')

    #Setting the titles of both the plots
    ax[0].set_title('Year-wise Box Plot(Trend)')
    ax[1].set_title('Month-wise Box Plot (Seasonability)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
