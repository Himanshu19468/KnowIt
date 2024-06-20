from AngleOne.HistoricalData.HistoricalData2 import *
from prophet import Prophet
from AngleOne.CommonUtil.CommonUtil import convert_datetime_format_2, convert_datetime_format
from prophet.diagnostics import cross_validation
from prophet.plot import add_changepoints_to_plot

from matplotlib import pyplot as plt

messages = getData("2012-03-08 09:16", "2024-03-13 09:16", "1d", "11536", "NSE")
df = zipAll(messages)
prophet_df = df[['timestamp', 'Close']].copy()
prophet_df.rename(columns={'timestamp': 'ds', 'Close': 'y'}, inplace=True)
prophet_df = convert_datetime_format_2(prophet_df, 'ds')
print(prophet_df.head())

# prophet_df = removeTimeZone(prophet_df, 'ds')

m = Prophet()
m.fit(prophet_df)

future = m.make_future_dataframe(periods=180)
predict = m.predict(future)

fig = m.plot(predict)
a = add_changepoints_to_plot(fig.gca(), m, predict)
fig_2 = m.plot_components(predict)



plt.show()

df_temp = cross_validation(m, initial='365 days', period='180 days', horizon = '30 days')
df_temp.to_csv('output.csv', index=False)

from prophet.diagnostics import performance_metrics
df_p = performance_metrics(df_temp)

df_p.to_csv('performance.csv', index=False)
print(df_p)
