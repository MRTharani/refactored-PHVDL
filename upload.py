import logging
from tools import split_video, generate_thumbnail, print_progress_bar
from config import *
from swibots import BotApp
import asyncio
import os
import subprocess



# Setup logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


bot = BotApp(TOKEN)

async def progress(current, total):
    print_progress_bar("", current, total)





async def process_upload(app, file_path,name):
            if os.path.exists(file_path):
                        logging.info(f"{name} is downloaded")
                        thumbnail_name = f"{name}_thumb.png"
                        logging.info("Generating Thumbnail")
                        generate_thumbnail(file_path, thumbnail_name)
                        logging.info("Thumbnail generated")
                        await app.send_video(DUMP_ID, file_path, thumb=thumbnail_name, progress=progress)
                        os.remove(file_path)
                        os.remove(thumbnail_name)
                        await asyncio.sleep(5)
            return True
       







async def switch_upload(file_path,thumb):
    if not os.path.isfile(file_path):
        raise Exception("File path not found")
    try:
        res = await bot.send_media(
            message=f"{os.path.basename(file_path)}",
            community_id=COMMUNITY_ID,
            group_id=GROUP_ID,
            document=file_path,
            thumb=thumb,
            description=os.path.basename(file_path),
            )
        return res
    except Exception as e:
        raise Exception(e)
