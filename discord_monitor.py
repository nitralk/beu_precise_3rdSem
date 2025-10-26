import asyncio
import os
import time
import aiohttp
import zipfile
from io import BytesIO
from datetime import datetime
from typing import Optional, List
import pytz

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
URL = 'https://results.beup.ac.in/BTech3rdSem2024_B2023Results.aspx'

CHECK_INTERVAL = 2
CONTINUOUS_DURATION = 900
SCHEDULED_INTERVAL = 6

RESULT_URLS = [
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2022Pub.aspx?Sem=III&RegNo=22156148040",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148028",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148002",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148001",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148003",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148005",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148006",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148009",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148010",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148013",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148016",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148017",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148018",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148020",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148021",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148022",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148023",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148024",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148025",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148026",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148027",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148028",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148029",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148030",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148031",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148032",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23156148034",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148001",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148002",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148003",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148005",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148006",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148007",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148008",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148009",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148010",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148011",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148012",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148014",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148015",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148017",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148018",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148019",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148020",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148022",
    "https://results.beup.ac.in/ResultsBTech3rdSem2024_B2023Pub.aspx?Sem=III&RegNo=23152148023"
]

class DiscordMonitor:
    def __init__(self):
        self.last_status: Optional[str] = None
        self.last_scheduled_time: float = 0
        self.rate_limit_remaining = 5
        self.rate_limit_reset = 0
        self.ist_timezone = pytz.timezone('Asia/Kolkata')

    def get_indian_time(self) -> str:
        """Get current Indian time in IST timezone using pytz"""
        utc_now = datetime.now(pytz.utc)
        ist_now = utc_now.astimezone(self.ist_timezone)
        return ist_now.strftime("%d-%m-%Y %I:%M:%S %p IST")

    async def send_discord_message(self, content: str, username: str = "BEUP Monitor") -> bool:
        if not DISCORD_WEBHOOK_URL:
            return False
        now = time.time()
        if self.rate_limit_remaining <= 0 and now < self.rate_limit_reset:
            await asyncio.sleep(self.rate_limit_reset - now)
        payload = {"content": content, "username": username}
        async with aiohttp.ClientSession() as session:
            async with session.post(DISCORD_WEBHOOK_URL, json=payload) as resp:
                self.rate_limit_remaining = int(resp.headers.get("X-RateLimit-Remaining", 5))
                reset_after = resp.headers.get("X-RateLimit-Reset-After")
                if reset_after:
                    self.rate_limit_reset = now + float(reset_after)
                if resp.status == 429:
                    retry = float(resp.headers.get("retry-after", 1))
                    await asyncio.sleep(retry)
                    return await self.send_discord_message(content, username)
                return resp.status in (200, 204)

    async def send_file(self, filename: str, data: BytesIO) -> bool:
        form = aiohttp.FormData()
        data.seek(0)
        ctype = "application/zip" if filename.endswith(".zip") else "text/html"
        form.add_field("file", data, filename=filename, content_type=ctype)
        async with aiohttp.ClientSession() as session:
            async with session.post(DISCORD_WEBHOOK_URL, data=form) as resp:
                now = time.time()
                self.rate_limit_remaining = int(resp.headers.get("X-RateLimit-Remaining", 5))
                reset_after = resp.headers.get("X-RateLimit-Reset-After")
                if reset_after:
                    self.rate_limit_reset = now + float(reset_after)
                if resp.status == 429:
                    retry = float(resp.headers.get("retry-after", 1))
                    await asyncio.sleep(retry)
                    return await self.send_file(filename, data)
                return resp.status in (200, 204)

    async def check_site(self) -> str:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(URL, timeout=10) as resp:
                    return "UP" if resp.status == 200 else "DOWN"
        except:
            return "DOWN"

    async def download_and_zip(self) -> BytesIO:
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            async with aiohttp.ClientSession() as session:
                for idx, url in enumerate(RESULT_URLS, start=1):
                    reg = url.split("=")[-1]
                    try:
                        async with session.get(url, timeout=10) as resp:
                            if resp.status == 200:
                                html = await resp.text()
                                zf.writestr(f"result_{reg}.html", html)
                    except Exception:
                        pass
                    if idx % 10 == 0 or idx == len(RESULT_URLS):
                        await self.send_discord_message(f"🔄 Downloaded & added to ZIP: {idx}/{len(RESULT_URLS)}")
        buffer.seek(0)
        return buffer

    async def continuous_status(self):
        end = time.time() + CONTINUOUS_DURATION
        while time.time() < end:
            left = int(end - time.time())
            await self.send_discord_message(f"✅ Website still UP ({left}s left)")
            await asyncio.sleep(CHECK_INTERVAL)

    async def run(self):
        await self.send_discord_message("🔍 Monitoring started")
        while True:
            current = await self.check_site()
            now = time.time()
            changed = current != self.last_status
            scheduled_due = (now - self.last_scheduled_time) >= SCHEDULED_INTERVAL

            if changed:
                if current == "UP":
                    await self.send_discord_message("🎉 WEBSITE IS NOW LIVE! Starting download…")
                    zip_data = await self.download_and_zip()
                    if await self.send_file("results.zip", zip_data):
                        await self.send_discord_message(f"📥 Uploaded all {len(RESULT_URLS)} results as ZIP")
                    else:
                        await self.send_discord_message("⚠️ ZIP upload failed; sending individual files")
                        async with aiohttp.ClientSession() as session:
                            for idx, url in enumerate(RESULT_URLS, start=1):
                                reg = url.split("=")[-1]
                                try:
                                    async with session.get(url, timeout=10) as resp:
                                        if resp.status == 200:
                                            bio = BytesIO((await resp.text()).encode("utf-8"))
                                            await self.send_file(f"result_{reg}.html", bio)
                                except:
                                    pass
                                if idx % 10 == 0 or idx == len(RESULT_URLS):
                                    await self.send_discord_message(f"🔄 Fallback uploaded {idx}/{len(RESULT_URLS)}")
                        await self.send_discord_message("📥 Individual files uploaded")
                    self.last_scheduled_time = now
                    await self.continuous_status()
                    # At end of continuous, send immediate scheduled update
                    await self.send_discord_message("📅 Scheduled update: Website is UP")
                    self.last_scheduled_time = time.time()
                else:
                    current_time = self.get_indian_time()
                    await self.send_discord_message(f"🔴 WEBSITE IS DOWN - {current_time}")
                    self.last_scheduled_time = now

            elif scheduled_due:
                emoji = "✅" if current == "UP" else "🔴"
                if current == "DOWN":
                    current_time = self.get_indian_time()
                    await self.send_discord_message(f"{emoji} Scheduled update: Website is {current} - {current_time}")
                else:
                    await self.send_discord_message(f"{emoji} Scheduled update: Website is {current}")
                self.last_scheduled_time = now

            self.last_status = current
            await asyncio.sleep(CHECK_INTERVAL)

async def main():
    monitor = DiscordMonitor()
    try:
        await monitor.run()
    except Exception as e:
        import traceback
        print("❌ Exception in monitor:", e)
        traceback.print_exc()
        raise

if __name__ == "__main__":
    asyncio.run(main())
