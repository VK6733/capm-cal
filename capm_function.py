import plotly.express as px
import numpy as np

# function to plot interactive plotly chart
def interactive_plot(df):
    fig=px.line()
    for i in df.columns[1:]:
        fig.add_scatter(x=df['Date'],y=df[i],name=i)
    fig.update_layout(width=450,margin=dict(l=20,r=20,t=20,b=20),legend=dict(orientation='h', yanchor="bottom",
    y=1.02,xanchor='right',x=1,))    
    return fig

# creating a function to normallize the prices    based on intial price
# to check the increase in price from the other price
def normalize(df_2):
    df=df_2.copy()
    for i in df.columns[1:]:
        df[i]=df[i]/df[i][0] # it will skip the first col the date one then will divide the prices with the intial price

    return df

def daily_return(df):
    df_daily_return=df.copy()
    for i in df.columns[1:]:
        for j in range(1,len(df)):
            df_daily_return[i][j]=((df[i][j]-df[i][j-1])/df[i][j-1])*100
        df_daily_return[i][0]=0
    return df_daily_return   

# now the function for beta
def cal_beta(stock_daily_return,stock):
    rm=stock_daily_return['sp500'].mean()*252

    b, a=np.polyfit(stock_daily_return['sp500'],stock_daily_return[stock],1)
    return b,a