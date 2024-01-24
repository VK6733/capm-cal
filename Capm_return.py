from datetime import datetime
import streamlit as st
import numpy as np
import yfinance as yf
import datetime
import pandas_datareader as web
import pandas as pd
import capm_function

st.set_page_config(page_title="CAPM",page_icon="chart_with_upwards_trend",layout="wide")
st.title("Capital Asset Pircing Model ")



# now i want to return the stock name and price returns
#for this goal i am goingto take an input from user

col1,col2=st.columns([2,1])
with col1:
    stocks_list=st.multiselect("Choose the stock you want to see ",("TSLA","APPL","NFLX","MSFT","MGM","AMZN","NVDA","GOOGL"),["TSLA"])
with col2:
    no_of_year=st.number_input("The number of year ",1,10)

#now e have download the market data
#download the data for SMP 500
try :
    end=datetime.date.today()
    start=datetime.date(datetime.date.today().year-no_of_year,datetime.date.today().month,datetime.date.today().day)

    SP500=web.DataReader(["sp500"],"fred",start,end)
    # print(SP500.tail()) for checking the SP500 data 
    stockdf=pd.DataFrame()

    for stocks in stocks_list:
        data=yf.download(stocks,period=f'{no_of_year}y')
        # print(data.head())
        stockdf[f'{stocks}']=data["Close"]
        # print(stockdf.head())
    # now i am going to work on the indexs of stocks data and SP500 data to merge it
    stockdf.reset_index(inplace=True)
    SP500.reset_index(inplace=True)
    SP500.columns=['Date','sp500']
    # print(stockdf.dtypes)
    # print("zzz",SP500.dtypes)
    #chaging the date time to make them equal
    stockdf["Date"]=stockdf["Date"].astype("datetime64[ns]")
    stockdf["Date"]=stockdf["Date"].apply(lambda x :str(x)[:10])
    stockdf["Date"]=pd.to_datetime(stockdf['Date'])
    stockdf=pd.merge(stockdf,SP500,on='Date',how='inner')
    # print(stockdf)

    col1,col2=st.columns([1,1])
    with col1:
        st.markdown("### dataframe head")
        st.dataframe(stockdf.head(),use_container_width=True)

    with col2:
        st.markdown("### dataframe tail")
        st.dataframe(stockdf.tail(),use_container_width=True)

    col1,col2=st.columns([1,1])    
    with col1:
        st.markdown("### Price of all stocks")
        st.plotly_chart(capm_function.interactive_plot(stockdf))
    with col2:
            capm_function.normalize(stockdf)
            st.markdown("### Price of all stocks")
            st.plotly_chart(capm_function.interactive_plot(stockdf))

    stocks_daily_return=capm_function.daily_return(stockdf)
    # print(stocks_daily_return.head())


    beta={}
    alpha={}
    for i in stocks_daily_return.columns:
        if i != "Date" and i !='sp500':
            b, a=capm_function.cal_beta(stocks_daily_return,i) 

            beta[i]=b
            alpha[i]=a

    print(beta ,alpha)
    beta_df=pd.DataFrame(columns=["Stock","Beta Value"])
    beta_df["Stock"]=beta.keys()
    beta_df["Beta Value"]=[str(round(i,2)) for i in beta.values()]

    with col1:
        st.markdown("### calculate beta value")
        st.dataframe(beta_df,use_container_width=True)
    rf=0
    rm=stocks_daily_return["sp500"].mean()*252

    return_df=pd.DataFrame()
    return_value=[]
    # print(return_value)

    for stock,value in beta.items():
        print(stock,value)
        return_value.append(str(round(rf+(value*(rf-rm)),2)))
    #     print('this the return value ******************AS',return_value)
    
    return_df['Stock']=stocks_list
    # print(stocks_list,'//////////////',return_value)
    return_df['Return value']=return_value


    with col2:
        st.markdown("### calculate return using CAPM")
        st.dataframe(return_df,use_container_width=True)
except:
    st.write("please select valid input")