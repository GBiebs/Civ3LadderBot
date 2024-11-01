import discord
from discord.ext import commands
from discord import app_commands
import pygsheets
import os
import datetime
from datetime import datetime
import re


bot = commands.Bot(command_prefix="/", intents = discord.Intents.all())
google = pygsheets.authorize(service_file='service_account_creds.json')

@bot.event
async def on_ready():
  try:
    synced = await bot.tree.sync()
    print(f"synced {len(synced)} command(s)")
  except Exception as e:
    print(e)

#4v4
@bot.tree.command(name='report_4v4')
@app_commands.choices(mod=[
    app_commands.Choice(name="Modern", value="Modern"),
    app_commands.Choice(name="Future", value="Future"),
    app_commands.Choice(name="MPT", value="MPT"),
    app_commands.Choice(name="UU", value="UU"),
    app_commands.Choice(name="QC", value="QC"),
    app_commands.Choice(name="MDJ", value="MDJ")
    ])
async def report_4v4(ctx, mod: app_commands.Choice[str], winner1: str,
                     winner2: str, winner3: str, winner4: str, loser1: str,
                     loser2: str, loser3: str, loser4: str):
  players = [winner1, winner2, winner3, winner4, loser1, loser2, loser3, loser4]
  if check_dupes(players):
    await ctx.response.send_message('Duplicates were found. Please remove any duplicates.', ephemeral=True)
  else:
    #generates output for spreadsheet
    output_values = generate_output(0, mod.value, players)
    await ctx.response.send_message('{}, {}, {}, {} won {} against {}, {}, {}, {}'
                                  .format(winner1, winner2, winner3, winner4, mod.value, loser1, loser2, loser3, loser4))
    update_spreadsheet(output_values)

#3v3
@bot.tree.command(name='report_3v3')
@app_commands.choices(mod=[
    app_commands.Choice(name="Modern", value="Modern"),
    app_commands.Choice(name="Future", value="Future"),
    app_commands.Choice(name="MPT", value="MPT"),
    app_commands.Choice(name="UU", value="UU"),
    app_commands.Choice(name="QC", value="QC"),
    app_commands.Choice(name="MDJ", value="MDJ")
    ])
async def report_3v3(ctx, mod: app_commands.Choice[str], winner1: str,
                     winner2: str, winner3: str, loser1: str, loser2: str,
                     loser3: str):
  players = [winner1, winner2, winner3, loser1, loser2, loser3]
  if check_dupes(players):
    await ctx.response.send_message('Duplicates were found. Please remove any duplicates.', ephemeral=True)
  else:
    #generates output for spreadsheet
    output_values = generate_output(0, mod.value, players)
    #update spreadsheet
    await ctx.response.send_message('{}, {}, {} won {} against {}, {}, {}'
                                    .format(winner1, winner2, winner3, mod.value, loser1, loser2, loser3))
    update_spreadsheet(output_values)

#2v2
@bot.tree.command(name='report_2v2')
@app_commands.choices(mod=[
    app_commands.Choice(name="Modern", value="Modern"),
    app_commands.Choice(name="Future", value="Future"),
    app_commands.Choice(name="MPT", value="MPT"),
    app_commands.Choice(name="UU", value="UU"),
    app_commands.Choice(name="QC", value="QC"),
    app_commands.Choice(name="MDJ", value="MDJ")
    ])
async def report_2v2(ctx, mod: app_commands.Choice[str], winner1: str, winner2: str, loser1: str, loser2: str):
  players = [winner1, winner2, loser1, loser2]
  if check_dupes(players):
    await ctx.response.send_message('Duplicates were found. Please remove any duplicates.', ephemeral=True)
  else:
    await ctx.response.send_message('{}, {} won {} against {}, {}'
                                    .format(winner1, winner2, mod.value, loser1, loser2))
    #generates output for spreadsheet
    output_values = generate_output(0, mod.value, players)
    #update spreadsheet
    update_spreadsheet(output_values)

#1v1
@bot.tree.command(name='report_1v1')
@app_commands.choices(mod=[
    app_commands.Choice(name="Modern", value="Modern"),
    app_commands.Choice(name="Future", value="Future"),
    app_commands.Choice(name="MPT", value="MPT"),
    app_commands.Choice(name="UU", value="UU"),
    app_commands.Choice(name="QC", value="QC"),
    app_commands.Choice(name="MDJ", value="MDJ")
    ])
async def report_1v1(ctx, mod: app_commands.Choice[str], winner1: str,
                     loser1: str):
  players = [winner1, loser1]

  #send report message to channel
  await ctx.response.send_message('{} won {} against {}'.format(
    players[0], mod.value, players[1]))

  #generates output for spreadsheet
  output_values = generate_output(0, mod.value, players)
  #update spreadsheet
  update_spreadsheet(output_values)

@bot.tree.command(name='report_cton')
@app_commands.choices(mod=[
    app_commands.Choice(name="Modern", value="Modern"),
    app_commands.Choice(name="Future", value="Future"),
    app_commands.Choice(name="MPT", value="MPT"),
    app_commands.Choice(name="UU", value="UU"),
    app_commands.Choice(name="QC", value="QC"),
    app_commands.Choice(name="MDJ", value="MDJ")
    ])
async def report_cton(ctx,
                      mod: app_commands.Choice[str],
                      first: str,
                      second: str,
                      third: str,
                      fourth: str=".",
                      fifth: str = ".",
                      sixth: str = ".",
                      seventh: str = ".",
                      eighth: str = "."):
  players = [first, second, third]
  non_winners = [fourth, fifth, sixth, seventh, eighth]
  output_string = '{}, {}'.format(second, third)

  for x in non_winners:
    if x != '.':
      players.append(x)
      output_string += ', {}'.format(x)
  if check_dupes(players):
    await ctx.response.send_message('Duplicates were found. Please remove any duplicates.', ephemeral=True)
  else:
    await ctx.response.send_message('{} won cton {} against {}'.format(first, mod.value, output_string))
    #generates output for spreadsheet
    output_values = generate_output(1, mod.value, players)
    #update spreadsheet
    update_spreadsheet(output_values)

@bot.tree.command(name='report_quit')
@app_commands.choices(mod=[
    app_commands.Choice(name="Modern", value="Modern"),
    app_commands.Choice(name="Future", value="Future"),
    app_commands.Choice(name="MPT", value="MPT"),
    app_commands.Choice(name="UU", value="UU"),
    app_commands.Choice(name="QC", value="QC"),
    app_commands.Choice(name="MDJ", value="MDJ")
    ])
async def report_quit(ctx, player: str, mod: app_commands.Choice[str]):
  await ctx.response.send_message('{} quit {}.'.format(player, mod.value))
  update_quits([datetime.today().strftime('%Y-%m-%d'), player, mod.value, ctx.user.name])

def update_spreadsheet(output_values):
  sh = google.open_by_key(google_sheet_key)
  reports = sh.worksheet(0)
  reports.insert_rows(1, 1, output_values)

def update_quits(output_values):
  sh = google.open_by_key(google_sheet_key)
  quits = sh.worksheet('title','Quits')
  quits.insert_rows(1, 1, output_values)

def check_dupes(players):
  return any(players.count(x) > 1 for x in players)

def generate_output(cton, mod, players):
  for x in range(0, len(players)):
    if players[x].startswith('<@'):
      user_id = re.findall(r'\d+', players[x])
      updated_name = bot.get_user(int(user_id[0])).name
      players[x] = updated_name

  output_values = [cton, mod, datetime.today().strftime('%Y-%m-%d')]
  if cton:
      for x in players:
        output_values.append(x)
      return output_values
  else:
    #create output value array
    result = ["." for _ in range(8)]
    # Calculate the number of names to be added to each half
    half_length = len(players) // 2
    # Add the first half of names to the first half of the result list
    for i in range(half_length):
          result[i] = players[i]
    # Add the second half of names to the second half of the result list
    for i in range(half_length, len(players)):
        result[i + 4 - half_length] = players[i]
    for i in result:
      output_values.append(i)
    print(output_values)
    return output_values

bot.run(token)