import os

from discord.ext import commands

from stonkmaster.commands.ChartCommand import ChartCommand
from stonkmaster.commands.PriceCommand import PriceCommand
from stonkmaster.commands.ShortsCommand import ShortsCommand

help_command = commands.DefaultHelpCommand(
    no_category="Commands"
)

description = ("The Stonk Master is a Discord bot for fellow apes to monitor stonks without "
               "leaving their gaming habitat. It presents information about stonks in a very "
               "easy and simple way."
               )

bot = commands.Bot(command_prefix='$', description= description, help_command=help_command)


@bot.command(name="price",
             description="Shows the current price of the stonk, as well as its daily change.")
async def _price(ctx, arg):
    await PriceCommand().run(ctx, arg)


@bot.command(name="shorts",
             description="Provides currently known information on how heavily the stonk is shorted.")
async def _shorts(ctx, arg):
    await ShortsCommand().run(ctx, arg)


@bot.command(name="chart",
             description="Generates a chart showing the price development of the share in the last months.")
async def _chart(ctx, arg):
    await ChartCommand().run(ctx, arg)


def main():
    bot.run(os.environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    main()