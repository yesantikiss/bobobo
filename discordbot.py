# インストールした discord.py を読み込む
import discord
from discord import app_commands
import random
import json
import os
token = os.getenv("DISCORD_TOKEN")
# 接続に必要なオブジェクトを生成
intents = discord.Intents.all()
client = discord.Client(intents = intents)
tree = app_commands.CommandTree(client)
# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    print(discord.__version__)
    await tree.sync()#スラッシュコマンドを同期

@tree.command(name="pjsekai",description="プロセカ")
@app_commands.describe(
    min="選曲難易度下限を指定",
    max="選曲難易度上限を指定",
    easy="難易度Easyを選曲範囲に指定するか",
    normal="難易度Normalを選曲範囲に指定するか",
    hard="難易度Hardを選曲範囲に指定するか",
    expert="難易度Expertを選曲範囲に指定するか",
    master="難易度Masterを選曲範囲に指定するか",
    append="難易度Appendを選曲範囲に指定するか",
)
@app_commands.rename(
    min="最小難易度",
    max="最大難易度",
    easy="easy",
    normal="normal",
    hard="hard",
    expert="expert",
    master="master",
    append="append"
)
async def pjsekai(
    interaction: discord.Interaction,
    min:int    = 26,
    max:int    = 37,
    easy:bool   = True,
    normal:bool = True,
    hard:bool   = True,
    expert:bool = True,
    master:bool = True,
    append:bool = True):
    contents = [] #選曲候補
    contents_ = [] #ファイルパス用
    exit_code = 0 #状態
    class status(): #ステータス
        none = 0
        success = 1
        not_found = -1
    class response(): #結果
        title = ""
        text = ""
        color = 0x000000
        footer = ""
        jacket = ""
    isReverse = False
    if min > max:
        min_ = max
        max = min
        min = min_
        isReverse = True
    json_open = open('data/JSON/pjsekai.json', 'r')
    data = json.load(json_open)
    for v in range(min,max+1):
        if f"{v}" in data:
            if "Easy" in data[f"{v}"] and easy == True:
                contents_ += data[f"{v}"]["Easy"]
                for k in range(len(data[f"{v}"]["Easy"])):
                    data[f"{v}"]["Easy"][k] = f'{data[f"{v}"]["Easy"][k]}' + f" [Easy {v}]"
                contents += data[f"{v}"]["Easy"]
            if "Normal" in data[f"{v}"] and normal == True:
                contents_ += data[f"{v}"]["Normal"]
                for k in range(len(data[f"{v}"]["Normal"])):
                    data[f"{v}"]["Normal"][k] = f'{data[f"{v}"]["Normal"][k]}' + f" [Normal {v}]"
                contents += data[f"{v}"]["Normal"]
            if "Hard" in data[f"{v}"] and hard == True:
                contents_ += data[f"{v}"]["Hard"]
                for k in range(len(data[f"{v}"]["Hard"])):
                    data[f"{v}"]["Hard"][k] = f'{data[f"{v}"]["Hard"][k]}' + f" [Hard {v}]"
                contents += data[f"{v}"]["Hard"]
            if "Expert" in data[f"{v}"] and expert == True:
                contents_ += data[f"{v}"]["Expert"]
                for k in range(len(data[f"{v}"]["Expert"])):
                    data[f"{v}"]["Expert"][k] = f'{data[f"{v}"]["Expert"][k]}' + f" [Expert {v}]"
                contents += data[f"{v}"]["Expert"]
            if "Master" in data[f"{v}"] and master == True:
                contents_ += data[f"{v}"]["Master"]
                for k in range(len(data[f"{v}"]["Master"])):
                    data[f"{v}"]["Master"][k] = f'{data[f"{v}"]["Master"][k]}' + f" [Master {v}]"
                contents += data[f"{v}"]["Master"]
            if "Append" in data[f"{v}"] and append == True:
                contents_ += data[f"{v}"]["Append"]
                for k in range(len(data[f"{v}"]["Append"])):
                    data[f"{v}"]["Append"][k] = f'{data[f"{v}"]["Append"][k]}' + f" [Append {v}]"
                contents += data[f"{v}"]["Append"]
    if len(contents) > 0:
        exit_code = status.success
    else:
        exit_code = status.not_found
    if exit_code == status.success:
        rand = random.randint(0,len(contents))
        response.text = f"{contents[rand]}"
        if isReverse == True:
            response.text += "\n\n※maxよりminの方が大きかったので逆転しました。"
        response.title = "抽選結果"
        response.color = 0x1e90ff
        response.footer = "exit code 1"
        response.jacket = f"{contents_[rand]}.png"
    elif exit_code == status.not_found:
        response.text = "選曲範囲に該当する曲がありませんでした。"
        response.title = "エラー"
        response.color = 0xdc143c
        response.footer = "exit code -1"
        response.jacket = "error.png"
    else:
        response.text = "不明なエラーです。"
        response.title = "エラー"
        response.color = 0xffd700
        response.footer = "exit code 0"
        response.jacket = "error.png"
    embed = discord.Embed(title=response.title,description=response.text,color=response.color)
    embed.set_footer(text=response.footer)
    file = discord.File(f"data/Jacket/{response.jacket}",filename=f"{response.jacket}",spoiler=False)
    embed.set_thumbnail(url=f"attachment://{response.jacket}")
    await interaction.response.send_message(file=file,embed=embed)
    #ephemeral=True→「これらはあなただけに表示されています」
        
@tree.command(name="help",description="使い方")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="使い方",
                          description="①スラッシュコマンドで`/pjsekai`と打つ\n②オプションを設定\n③送信",
                          color=0x15aced)
    await interaction.response.send_message(embed=embed)
# Botの起動とDiscordサーバーへの接続
client.run(token)
