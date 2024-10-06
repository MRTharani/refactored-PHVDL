import asyncio
import os
import logging
from datetime import datetime
from pyrogram import Client
from config import *
from database import insert_document
from myjd import connect_to_jd, add_links, clear_downloads, process_and_move_links, check_for_new_links
from upload import process_upload
from scraper import fetch_links
from tools import *

# Setup logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

app = Client(
    name="PHDLX-bot",
    api_hash=API_HASH,
    api_id=API_ID,
    bot_token=BOT_TOKEN,
    workers=30
)

async def start_download():
    """Start downloading files from JD device and process uploads."""
    async with app:
        try:
            links = fetch_links()
            logging.info(f"Total links found: {len(links)}")
            jd = connect_to_jd(JD_APP_KEY, JD_EMAIL, JD_PASSWORD)
            device = jd.get_device(JD_DEVICENAME)
            logging.info('Connected to JD device')
            clear_downloads(device)
            responses = []
            if links:
                for url in links:
                    response = await add_links(device, url, "PHVDL")
                    logging.info(f"Link added successfully: {url}")
                    responses.append(response)
                if len(responses) == len(links):
                        await handle_linkgrabber(device,links)
                else:
                        logging.error(f"Failed to add link: {url}")
        except Exception as e:
            logging.error(f"Error in start_download: {e}")

async def handle_linkgrabber(device,links):
    """Handle the linkgrabber process and downloads."""
    linkgrabber = device.linkgrabber
    while linkgrabber.is_collecting():
        await asyncio.sleep(1)

    await asyncio.sleep(5)
    process_and_move_links(device)
    linkgrabber.clear_list()
    
    await check_downloads(device,links)

async def check_downloads(device,links):
    """Check and process active downloads."""
    uploaded = []
    x = True
    while x:
        downloads = device.downloads.query_links()
        if not downloads:
            logging.info("No active downloads.")
            await asyncio.sleep(10)
            continue
        for i in downloads:
            file_path = os.path.join("downloads", i['name'])
            if i['bytesTotal'] == i['bytesLoaded'] and i['name'] not in uploaded:
                await process_upload(app, file_path, i['name'])
                uploaded.append(i['name'])
            else:
                print_progress_bar(i['name'], i['bytesLoaded'], i['bytesTotal'])
                await asyncio.sleep(3)
            if len(uploaded) == len(links):
                x = False
                break
    
                

if __name__ == "__main__":
    app.run(start_download())
