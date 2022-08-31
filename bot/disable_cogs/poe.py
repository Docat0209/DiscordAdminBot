import discord
from discord.ext import commands
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from lxml import etree
import html2text
import json

class Poe(commands.Cog):
	def __init__(self, client):
		self.client = client # sets the client variable so we can use it in cogs
	
	@commands.Cog.listener()
	async def on_ready(self):
		print("poe_trade_track online")
		global data , path , driver
		path = './data/poe_trade.json'

		await asyncio.sleep(10)

		driver = webdriver.Edge(executable_path="driver\msedgedriver.exe")

		while (1):  
			data = load_json(path)
			for i in range(len(data["track"])):
				result = await get_price(i)
				if not result:
					continue
				channel = discord.Client.get_channel(self.client,int(data["track"][i]["channel"]))
				userid = data["track"][i]["user"]

				embed=discord.Embed(title="", description="",color=0x2ecc71)

				embed.add_field(name="物品數值", value=result[0], inline=False)
				embed.add_field(name="價格", value=result[1], inline=False)

				await channel.send(userid,embed=embed)
			await asyncio.sleep(60)

	@commands.command()
	async def poe_track(self, ctx, url , price):
		try:
			data
		except NameError:
			path = './data/poe_trade.json'
			data = load_json(path)
		data["track"].append({"url": url,"user": "<@"+str(ctx.author.id)+">","c_price": str(price),"channel": str(ctx.message.channel.id),"data_id": []})
		data = write_json(path,data)

		await ctx.message.delete()

	#---報錯區域---
	@poe_track.error
	async def track_error(self, ctx, error):
		await ctx.send(error)
				
		
async def get_price(json_data_id):
	try:
		data
	except NameError:
		path = './data/poe_trade.json'
		data = load_json(path)

	item_data = data["track"][json_data_id]
	driver.get(item_data["url"])
	try:
		WebDriverWait(driver, 60).until(
			EC.presence_of_element_located((By.CLASS_NAME, "row"))
		)
	except:
		return None

	soup = BeautifulSoup(driver.page_source, 'html.parser')
	dom = etree.HTML(str(soup))
	
	count = len(dom.xpath('//*[@id="trade"]/div[6]/div[2]')[0].findall("div"))

	for i in range(count):

		try:
			item_id = dom.xpath(f'//*[@id="trade"]/div[6]/div[2]/div[{i+1}]')[0].attrib['data-id']
		except:
			continue

		if (item_id in item_data["data_id"]):
			continue

		price_num = float(dom.xpath(f'//*[@id="trade"]/div[6]/div[2]/div[{i+1}]/div[3]/div/div[1]/span/span[2]')[0].text)
		price_type = dom.xpath(f'//*[@id="trade"]/div[6]/div[2]/div[{i+1}]/div[3]/div/div[1]/span/span[4]/span')[0].text

		if price_type == "崇高石":
			c_price = price_num*200
		elif price_type == "混沌石":
			c_price = price_num
		else:
			continue

		if (c_price >  float(item_data["c_price"])):
			continue

		else:
			item = dom.xpath(f'//*[@id="trade"]/div[6]/div[2]/div[{i+1}]/div[2]')[0]
			text = html2text.html2text(str(etree.tostring(item, pretty_print=True))[2:-1].replace('\\n',''))
			for j in ["基礎百分比","護甲","閃避值","能量護盾","保護"]:
				text = replace_last(text, j, "\n"+j+": ")
			text.replace('<span class="lc">未鑑定</span>' , '')

			string = ""
			for linea in text.splitlines():
				lineb=linea.replace("\n","")
				if lineb.strip(" ") != "":
					string = string +lineb+"\n"
			
			text = string

			data["track"][json_data_id]["data_id"].append(item_id)
			data = write_json(path,data)

			return [text , str(price_num)+price_type]

	return None

def setup(client):
	client.add_cog(Poe(client))

def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail

def write_json(path ,data):

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.close()

    with open(path, encoding='utf-8') as f:
        data = json.load(f)
        f.close()

    return (data)

def load_json(path):

    with open(path, 'r' , encoding="utf8") as f:
        data = json.load(f)

    return(data)

