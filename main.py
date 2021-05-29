import yfinance as yf
from discord.ext import commands
import os
import datetime as dt
import pandas_datareader.data as web
import plotly.graph_objects as go
import discord

bot = commands.Bot(command_prefix='$')


@bot.command(name='price')
async def _price(ctx, arg):
    try:
        ticker = yf.Ticker(arg)
        info = ticker.info
        current = info['regularMarketPrice']
        previous = info['previousClose']
        symbol = info['symbol']
        change = ((current - previous) / previous) * 100
        emoji = "<:stonks:785565572300800050>" if change >= 0 else "<:notstonks:847892457138946128>"

        if 'longName' in info:
            msg = (f"The market price of **{info['longName']} ({symbol})** is **{round(current, 2)}$** "
                   f"({'{0:+.2f}'.format(change)}%)  {emoji}")
        else:
            msg = (f"The market price of **{symbol}** is **{round(current, 2)}$** "
                   f"({'{0:+.2f}'.format(change)}%)  {emoji}")

        await ctx.send(msg)
    except:
        await ctx.send(f"{arg.upper()} gibts ned oida! <:ThomasPassAuf:788838985878994964>")


@bot.command(name='shorts')
async def _shorts(ctx, arg):
    try:
        ticker = yf.Ticker(arg)
        info = ticker.info
        symbol = info['symbol']

        if 'sharesShort' not in info or 'shortPercentOfFloat' not in info:
            await ctx.send(f"{symbol} kann ned geshorted werden du dully! <:GanslSuffkoma:819901005193019392>")
            pass

        shares_short = info['sharesShort']
        short_percent_of_float = info['shortPercentOfFloat'] * 100

        if 'longName' in info:
            msg = (f"Currently **{'{:,}'.format(shares_short)} shares** of **{info['long_name']} ({symbol})** "
                   f"are shorted. This corresponds to **{round(short_percent_of_float, 2)}%** of shares available.")
        else:
            msg = (f"Currently **{'{:,}'.format(shares_short)} shares** of **{symbol}** "
                   f"are shorted. This corresponds to **{round(short_percent_of_float, 2)}%** of shares available.")

        await ctx.send(msg)
        await ctx.send("Real SI may be much higher -> Hedgies are fucked.")
    except:
        await ctx.send(f"{arg.upper()} gibts ned oida! <:ThomasPassAuf:788838985878994964>")


@bot.command(name='chart')
async def _shorts(ctx, arg):
    try:
        start = dt.datetime(2021, 1, 1)
        end = dt.datetime.now()

        stocks = web.DataReader([arg], 'yahoo', start, end)
        # stocks_close = pd.DataFrame(
        #  web.DataReader(['GME'], 'yahoo', start, end)['Close'])
        candlestick = go.Figure(data=[go.Candlestick(x=stocks.index,
                                                     open=stocks[('Open', arg)],
                                                     high=stocks[('High', arg)],
                                                     low=stocks[('Low', arg)],
                                                     close=stocks[('Close', arg)])])

        candlestick.update_layout(xaxis_rangeslider_visible=False, title='stock chart')
        candlestick.update_xaxes(title_text='Date')
        candlestick.update_yaxes(title_text='Close Price', tickprefix='$')

        candlestick.write_image("/home/kili/stock.png")
        with open('/home/kili/stock.png', 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)

    except:
        await ctx.send(f"{arg.upper()} gibts ned oida! <:ThomasPassAuf:788838985878994964>")


bot.run(os.environ['DISCORD_TOKEN'])
