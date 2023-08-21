import discord
import pygsheets
import os
from discord.ext import commands
from datetime import datetime
import re

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

google = pygsheets.authorize(service_file='service_account_credentials.json')

@bot.event
async def on_ready():
  try:
    synced = await bot.tree.sync()
    print(f"synced {len(synced)} command(s)")
  except Exception as e:
    print(e)

#4v4
@bot.tree.command(name='report_4v4')
async def report_4v4(ctx,
                        mod: str,
                        winner1: str,
                        winner2: str,
                        winner3: str,
                        winner4:str,
                        loser1: str,
                        loser2:str,
                        loser3:str,
                        loser4:str):
  players = [winner1, winner2, winner3, winner4, loser1, loser2, loser3, loser4]
  await ctx.response.send_message('{}, {}, {}, {} won {} against {}, {}, {}, {}'.format(winner1, winner2, winner3, winner4, mod, loser1, loser2, loser3, loser4))
  
  #generates output for spreadsheet
  output_values = generate_output(0, mod, players)
  #update spreadsheet
  update_spreadsheet(output_values)

#3v3
@bot.tree.command(name='report_3v3')
async def report_3v3(ctx,
                        mod: str,
                        winner1: str,
                        winner2: str,
                        winner3: str,
                        loser1: str,
                        loser2:str,
                        loser3:str):
  players = [winner1, winner2, winner3, loser1, loser2, loser3]
  await ctx.response.send_message('{}, {}, {} won {} against {}, {}, {}'.format(winner1, winner2, winner3, mod, loser1, loser2, loser3))

  #generates output for spreadsheet
  output_values = generate_output(0, mod, players)
  #update spreadsheet
  update_spreadsheet(output_values)

#2v2
@bot.tree.command(name='report_2v2')
async def report_2v2(ctx,
                        mod: str,
                        winner1: str,
                        winner2: str,
                        loser1: str,
                        loser2:str):
  players = [winner1, winner2, loser1, loser2]
  await ctx.response.send_message('{}, {} won {} against {}, {}'.format(winner1, winner2, mod, loser1, loser2))

  #generates output for spreadsheet
  output_values = generate_output(0, mod, players)
  #update spreadsheet
  update_spreadsheet(output_values)
  
#1v1
@bot.tree.command(name='report_1v1')
async def report_1v1(ctx,
                        mod: str,
                        winner1: str,
                        loser1: str):
  players = [winner1, loser1]
  
  #send report message to channel
  await ctx.response.send_message('{} won {} against {}'.format(players[0], mod, players[1]))

  #generates output for spreadsheet
  output_values = generate_output(0, mod, players)
  #update spreadsheet
  update_spreadsheet(output_values)

#cton
@bot.tree.command(name='report_cton')
async def report_cton(ctx,
                      mod: str,
                      first: str,
                      second: str,
                      third: str,
                      fourth:str=None,
                      fifth:str=None,
                      sixth:str=None,
                      seventh:str=None,
                      eighth:str=None):
  players = [first, second, third]
  non_winners = [fourth, fifth, sixth, seventh, eighth]
  for x in non_winners:
    if x is not None:
      players.append(x)
  output_string = '{}, {}'.format(second, third)
  for x in non_winners:
    if x is not None:
      output_string += ', {}'.format(x)

  await ctx.response.send_message('{} won cton {} against {}'.format(first, mod, output_string))
      
  #generates output for spreadsheet
  output_values = generate_output(1, mod, players)
  #update spreadsheet
  update_spreadsheet(output_values)

def update_spreadsheet(output_values):
  sh = google.open_by_key(os.environ['google_sheet_key'])
  reports = sh.worksheet(0)
  reports.insert_rows(1, 1, output_values)

def generate_output(cton, mod, players):
  #updated player names to put into spreadsheet
  for x in range(0, len(players)):
    if players[x].startswith('<@'):
      user_id = re.findall(r'\d+', players[x])
      updated_name = bot.get_user(int(user_id[0])).name
      players[x] = updated_name

  output_values=[cton,mod,datetime.today().strftime('%Y-%m-%d')]
  #create output value array
  for x in players:
    output_values.append(x)
  return output_values

bot.run(os.environ['token'])