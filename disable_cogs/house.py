import discord
from discord.ext import commands
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from lxml import etree
import json

class House(commands.Cog):
	def __init__(self, client):
		self.client = client # sets the client variable so we can use it in cogs
	
	@commands.Cog.listener()
	async def on_ready(self):
		print("house online")
		global data , path , driver
		path = './data/house.json'

		await asyncio.sleep(10)

		driver = webdriver.Edge(executable_path="driver\msedgedriver.exe")

		while (1):  
			data = load_json(path)
			for i in range(len(data["track"])):
				result = await get_price(i)
				if not result:
					continue
				channel = discord.Client.get_channel(self.client,int(data["track"][i]["channel"]))

				await channel.send(result)
			await asyncio.sleep(60)

	@commands.command()
	async def house_track(self, ctx, url):
		try:
			data
		except NameError:
			path = './data/house.json'
			data = load_json(path)
		data["track"].append({"url": url,"user": "<@"+str(ctx.author.id)+">","channel": str(ctx.message.channel.id),"data_id": []})
		data = write_json(path,data)

		await ctx.message.delete()

	#---報錯區域---
	@house_track.error
	async def track_error(self, ctx, error):
		await ctx.send(error)
				
		
async def get_price(json_data_id):
	try:
		data
	except NameError:
		path = './data/house.json'
		data = load_json(path)

	item_data = data["track"][json_data_id]
	driver.get(item_data["url"])
	try:
		WebDriverWait(driver, 60).until(
			EC.presence_of_element_located((By.CLASS_NAME, "vue-list-rent-item"))
		)
	except:
		return None

	soup = BeautifulSoup(driver.page_source, 'html.parser')

	dom = etree.HTML(str(soup))
	
	count = len(dom.xpath('//*[@id="rent-list-app"]/div/div[3]/div/section[3]/div')[0].findall("section"))

	print(count)

	for i in range(count):

		try:
			item_id = dom.xpath(f'//*[@id="rent-list-app"]/div/div[3]/div/section[3]/div/section[{i+1}]')[0].attrib['data-bind']
		except:
			continue

		if (item_id in item_data["data_id"]):
			continue

		link = dom.xpath(f'//*[@id="rent-list-app"]/div/div[3]/div/section[3]/div/section[{i+1}]/a')[0].attrib['href']

		data["track"][json_data_id]["data_id"].append(item_id)
		data = write_json(path , data)

		return link

	return None

def setup(client):
	client.add_cog(House(client))

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

