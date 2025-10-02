import asyncio
import os
import time
import aiohttp
import zipfile
import pytz
from io import BytesIO
from datetime import datetime
from typing import Optional, List

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
URL = "https://results.beup.ac.in/BTech5thSem2024_B2022Results.aspx"

CHECK_INTERVAL = 2
CONTINUOUS_DURATION = 900
SCHEDULED_INTERVAL = 4

RESULT_URLS = [
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148040",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148042",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148051",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148018",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148012",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148015",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148008",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148023",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148001",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23156148904",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148039",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148021",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148007",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148026",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148036",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148019",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148041",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148038",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148006",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148027",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148031",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148035",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148013",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148050",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148053",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148016",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148022",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148032",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148009",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148028",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148033",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148015",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148024",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148048",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148017",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148037",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148052",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148045",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148005",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148003",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148020",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148044",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148034",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148030",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148008",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148046",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148047",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148002",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148029",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148004",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148011",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22156148014",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23156148901",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23156148903",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23156148902",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148001",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148002",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148003",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148004",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148005",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148006",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148007",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148008",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148009",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148010",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148011",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148012",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148013",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148014",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148015",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148016",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148017",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148018",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148019",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148020",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148021",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148022",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148023",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148024",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148025",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148026",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148027",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148028",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148029",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148030",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148031",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148032",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148033",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148034",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148035",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148036",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148037",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148038",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148039",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148040",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148041",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148042",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148043",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148044",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148045",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148046",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148047",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148048",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148049",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148050",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148051",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148052",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148053",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148054",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148055",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148056",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148057",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148058",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148059",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22101148060",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148901",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148902",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148903",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148904",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148905",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148906",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148907",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148908",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148909",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148910",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148911",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148912",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148913",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148914",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148915",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148916",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148917",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148918",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148919",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148920",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148921",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148922",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148923",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148924",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148925",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148926",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148927",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148928",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148929",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23101148930",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22103148001",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22103148002",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22103148003",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22103148004",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22103148005",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22103148006",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22103148007",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22103148008",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22103148009",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22103148010",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22103148011",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22103148012",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22103148013",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22103148014",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22103148015",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22103148016",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22103148017",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22103148018",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22103148019",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22103148020",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148901",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148902",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148903",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148904",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148905",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148906",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148907",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148908",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148909",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148910",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148911",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148912",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148913",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148914",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148915",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148916",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148917",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148918",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148919",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148920",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148921",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148922",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148923",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148924",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148925",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148926",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148927",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148928",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148929",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148930",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148931",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148932",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148933",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148934",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148935",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148936",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148937",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148938",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148939",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23103148940",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148001",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148002",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148003",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148004",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148005",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148006",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148007",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148008",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148009",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148010",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148011",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148012",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148013",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148014",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148015",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148016",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148017",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148018",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148019",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148020",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148021",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148022",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148023",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148024",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=22104148025",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23104148901",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23104148902",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23104148903",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23104148904",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23104148905",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23104148906",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23104148907",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23104148908",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23104148909",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23104148910",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23104148911",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23104148912",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23104148913",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23104148914",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23104148915",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23104148916",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23104148917",
    "https://results.beup.ac.in/ResultsBTech5thSem2024_B2022Pub.aspx?Sem=V&RegNo=23104148918"
]



class DiscordMonitor:
    def __init__(self):
        self.last_status: Optional[str] = None
        self.last_scheduled_time: float = 0
        self.rate_limit_remaining = 5
        self.rate_limit_reset = 0

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
                    await self.send_discord_message("🔴 WEBSITE IS DOWN")
                    self.last_scheduled_time = now

            elif scheduled_due:
                emoji = "✅" if current == "UP" else "🔴"
                ist = pytz.timezone('Asia/Kolkata')
                timestamp = datetime.now(ist).strftime("%I:%M:%S %p")
                if current == "DOWN":
                    await self.send_discord_message(f"{emoji} Scheduled update: Website is {current} [{timestamp}]")
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
