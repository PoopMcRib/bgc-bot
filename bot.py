import discord
from discord.ext import commands
import requests
import os
import asyncio
from aiohttp import ClientSession
import time
import sys
import chat_exporter

# Discord bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!",intents=intents)

# Trello API credentials (Set these as environment variables for security)
TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")

# Bot startup time
start_time = time.time()

# Your UserID for restricted commands
AUTHORIZED_USER_ID = int("171706838134423552")  # Replace with your Discord User ID

# Trello boards to be searched
board_ids = [
    'KHYhrBju', # District Court of Firestone
    'vLnKdugn', # (2018) Firestone Courts Archives
    '5LeZTeJh', # (2017) Firestone Courts Archives
    'ZhXt15Jc', # (2019) Firestone Courts Archives
    '2dSr98Vm', # (2020) Firestone Courts Archives
    'XRjmuVqK', # (2021) Firestone Courts Archives
    'clFSplW7', # (2023) Firestone Courts Archives
    'RISmcKJS', # (Warrants) Firestone Courts Archives
    'u003k5Q8', # (2022) Firestone Courts Archives
    'jd4AjoRa', # (2024) Firestone Courts Archives
    'dCurzcc2', # Public Safety Investigations
    'FY4O4I0r', # Public Safety Investigations (Team B)
    'kl3ZKkNr', # DPS | Public Archive
    'c0CTuVtY', # [FIRESTONE] House of Representatives
    'HQyOBmCY', # [FIRESTONE] Senate
    'nsEGdRbP', # County Affairs Committee
    'F3Fz6Cyg', # DHS | Department Organization
    'oCdlFDPX', # FNG | Administration Board
    'gRRJF4Lr', # DOBW - Community Engagement Division
    'BsuYfrDD', # DOBW - Company 1
    'DJC6YBVR', # DOBW - Department Records
    'mp99o14W', # DOBW - Training and Admissions Division
    'NC7jEcn2', # Firestone Department of Boating and Waterways
    'c4Ez8Xhx', # POST | Staff Board
    'vJepUnz5', # POST | Cadet Tracker
    'CXSYCvgT', # POST | Control Board
    'A0JJb2YX', # POST | Disciplinary Database
    # BROKEN 'Xo8MTs2Q', # FSP: DISCIPLINARY ACTION
    'F7StSHLq', # FSP: EMPLOYEE RECORDS
    'GJ38zQBN', # FSP: HEADQUARTERS
    '09ZD4xil', # FSP: CANDIDATE PROGRESS
    'PmEAjnZa', # FSP: TRAINING STAFF
    'pR2UWs4y', # FDOC | Disciplinary Action Board
    '6dhDwNrj', # FDOC | Transfer Board
    'An8MZntR', # FDOC | Public Relations
    'UzfrZszy', # FDOC | Prison Property Access Board
    'RhDLIZSx', # FDOC | Main Control Board
    'aYfoaxz4', # SERT | Public Information Board
    'ga547RL3', # FDOC TB: Academy Tracker
    'bucy9fwm', # DOC | Training Bureau: Probationary Board
    'uezHCC08', # FPS - Law Enforcement and Security
    'ODiaCSyz', # FPS - Administrative Board
    '29B033eu', # DPW | Control Board
    'c0ii3WUX', # DPW | Waste Management
    'GFEoL90M', # DPW | Trainee Resources
    'c56Cf4J9', # DPW | Training Records
    'Y5fgSE6G', # DPW | Employee Retraining Program
    'XZATNlrd', # FDOT | Employment Records
    'UFGFymoA', # FDOT | Control Board
    'Aj3MPOAc', # SCSO | Public Relations
    'myjmG11W', # SCSO | Control Board
    'UCcxjt5q', # SCSO | Platoon 2 (ARCHIVE)
    'LOSbXf8M', # SCSO | Platoon 1 (OLD ARCHIVE)
    'wDKnVVeh', # SCSO | SWAT Team Board
    'jGJlkt39', # SCSO | SWAT Contracts
    'TpIoIAkT', # FFA | Control Board
    'SYr0nNnQ', # SCFD | Control Board
    'jxcbyPod', # SCFD | High Command Operations
    'nXdiEy3C', # SCFD | Service Awards
    'QGeyqZz1', # PDP | Activity Database
    'EOmYqsla', # PDP | Departmental Integrity Bureau
    'HVCn7MBL', # PDP | Control Board
    'zY3H1aG4', # PDP | Administration Trello
    'PZj0tsZ4', # PDP | FOIA Register
    'B1tXc13q', # APD Patrol Services
    'k6jMHxL9', # APD Administrative Services
    'X0hoSAGN', # APD Control Board
    '1ZXLqWjW', # APD Department Records
    'ibjLBVcJ', # RPD Control Board
    'rvQqlryA', # RPD | Patrol Bureau
    'uiOL0IfO', # RPD | Canine Bureau
    'hsoTVOWc', # RPD | Academy Bureau
    '3vlb7oxD', # RPD | Public Archive
    'q10ZoHZs', # RPD | Public Relations
    'aJ8MmNQK', # Old FAA Employee Hub
    'cpOzNAtC', # FAA Employee Hub
    'mYL1W2c5', # FBI Bureau Police
    'nXYhIv9t', # SCSO:PD | Platoon 1
    'DK5U3qhK', # SCSO:PTD | Staff Board
    'YbN4xaAr', # Firestone Firearms Commission
    'XnYh2AN1', # State Registry of Health
    'tQozNPff', # FSP: TROOP 1 OFFICIAL
    'pBbZzluZ', # FSP: TROOP 2 OFFICIAL
    '1O4YxyWc', # FSP: TROOP 3 OFFICIAL (EXECUTIVE SECURITY UNIT)
    'HcIrCDfX', # FSP: AIR SUPPORT UNIT
    'I9SEkunf', # ASU: CERTIFICATIONS
    'zF0Upr0z', # FSP | Discharge Reports
    'pVlsiHHI', # Firestone State Patrol: Air Support Unit
    'VIqpDE9l', # FSP ASU: Special Response Control Board
    'rKx04kvs', # ASU | Control Site (DEFUNCT)
    'BZoRg9iR', # Sergeant OpticKamilShot's Unit Board
    'U8pAHXUV', # Sergeant JackKelso_CFL's Unit Board
    'Jjpunx3S', # ASU | Bravo Squadron Unit Board
    'gXU60qux', # FSP: New Platoon 1
    'K6cdfnZN', # FSP: Applications Backup Board
    'ntKop8Fh', # FSP: Applications V2
    'JsSsJzO6', # FSCG | Brigade
    'AyqXhft0', # 1st Military Police Battalion Main Board
    'LZiUH8fq', # Military Police Board
    'ZFWRAl0s', # FNG: 3rd Infantry Battalion
    'acIiYSO1', # 6th Ranger Regiment
    'j84b7Btm', # Coast Guard OLD
    'HDyP9fRE', # FDOC | Platoon 1
    'Xr1maDMr', # FDOC | Platoon 2
    'A6HSoOsz', # MD | Control Board
    'dtNWzl1C', # FPS - RLEA Internal
    'mXcCIrDg', # FPS - CPA Internal
    'bwgguVVp', # SCSO:PD | Platoon 2
    'oHdNygwW', # RPD | Academy Board
    'RL3qOkVd', # RPD Academy OUT OF USE
    'jJDnchnh', # Public Health Firestone
    'yLU0jWV6', # Stapleton County Medical Centre
    'XoLriYa7', # Stapleton County Medical Service
    '5lRtbOMh', # DOH Human Resources
    'ulGN9r9m', # DOH Application Tracker
    'v2EuCS1p', # Stapleton County Medical Center
    'eaeV2Y0v', # Stapleton County Medical Service (EMS)
    'OxiFMufh', # DoH: Program Tracker
    '2iJ6XhBY', # DOH Training Bureau Control Board
    'FaGQYHTX', # SCFD | Field Operations
    'yXOaoNf3', # SCFD | EMS Division
    'inwj8GNv', # SCFD | Search and Rescue
    'shtIfI9G', # SCFD ARCHIVE
    '43KK7mHa', # (SCFD) Fire Control Board
    'aU4rQ8WG', # (SCFD) EMS Control Board
    'Ipp7eh4I', # (SCFD) Certifications Control Board
    'SzyrSNdh', # [SCFD] SCFA/Other Certifications Board
    'h84N5ZZ9', # DPW | Company 1
    'lHh8jSu6', # DPW | Company 2
    'd6u3P0dI', # DPW | Public Relations
    'BocPliMA', # DPW | Community Service
    'wj5vGcAo', # DPW | Ride Along Division
    '1gOT0qTS', # FDOT | Control Board
    '3USrhimT', # FDOT | Employment Records
    'lnstqHUV', # POST | Appeals Panel
    '8i08CBiL', # Firestone POST
    'aSWJf62o', # POST | Blacklist Board
    'WZM3d2vv', # [FDOJ] Public Defender's Office
    'RsTIrXiR', # CFL Applications
    'YK7fpyx1', # Supreme Court of Firestone
    '4DYKWKig', # BD | Main Operations Board
    'SwSEAat8', # FDOD | Control Board
    'zzguCtZi', # FDOD | Human Resources Board
    'BvGxQHl7', # DPS Control Board
    'wYLWoC9g', # DPS Blacklist Committee
    '2o487N8y', # DPS | Office of Auditing
    'tEVCwnJP', # FS | Department of State
    '8vfvg87m', # DOS Archive Main Board
    '0UMhu6CK', # DOS Executive Archive
    'y7QU9UUM', # DOS Legislation Archive
    'sCT05qxD', # DOS Election Archive
    'yrMs1pkZ', # DOS Judicial Archive
    'yXUYwrLE', # DOS Firestone Awards
    'qLuREZ8b', # FAA Control Board
    'f5er1jOd', # FAA Employee Hub
    'uIGfYpID', # FAA Employment Records
    'FpDfoqtj', # FAA Rotorcraft Pilots Licensing
    'xfIqiZmY', # FDOA Issued Licenses
    'yXIDv41R', # State Legislature Board
    'Paha9q5g', # State Legislature Operations
    'WPgSfcrM', # SC: Executive Branch
    'bcZASRG7', # SC: County Council
    'ngipbuSC', # SC: County Records Board
    'yiYPkvW8', # SC: County Legislation Review Committee
    'uhJ1DTjS', # SC: County Executive Branch
    'GdL8GJIF', # SC: County Council (ARCHIVED)
    'EXd96kmV', # Office of the Mayor of Prominence
    'tsNEW5kg', # Prominence District Council
    'XgJDbtby', # Prominence District Records
    '7GpenRr1', # Prominence District Awards Storage
    'pK66sdV7', # Office of the Mayor of Redwood
    'gVPTVd0r', # Redwood City Council
    'g06YwcHJ', # Redwood City Records Board
    'YOgB6ddE', # Arborfield Administration
    'gcBwNq7w', # Arborfield City Council
    'nOwFvREq', # Arborfield Records
    '8avwN18U', # MD | Patrol Squadron
    'G50xdHjb', # DOC Training Bureau: Main Board
    # Add more board IDs as needed
]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def fetch_board_name(board_id, session, retries=3):
    url = f"https://api.trello.com/1/boards/{board_id}"
    params = {"key": TRELLO_API_KEY, "token": TRELLO_TOKEN}
    for attempt in range(retries):
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("name", f"Unknown Board ({board_id})")
            elif attempt < retries - 1:
                await asyncio.sleep(1)  # Wait before retrying
    print(f"Failed to fetch board {board_id} after {retries} attempts.")
    return None


async def fetch_all_cards(board_id, session):
    """Fetch all cards (active and archived) from a Trello board."""
    url = f"https://api.trello.com/1/boards/{board_id}/cards?filter=all"
    params = {"key": TRELLO_API_KEY, "token": TRELLO_TOKEN}
    async with session.get(url, params=params) as response:
        if response.status != 200:
            print(f"Error fetching cards for board {board_id}: {response.status}")
            return []
        return await response.json()

async def fetch_roblox_user_id(username):
    """Fetch Roblox user ID based on username."""
    url = f"https://users.roblox.com/v1/usernames/users"
    payload = {"usernames": [username]}
    headers = {"Content-Type": "application/json"}
    async with ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status != 200:
                print(f"Failed to fetch user ID for {username}. Status code: {response.status}")
                return None
            data = await response.json()
            if "data" in data and data["data"]:
                return data["data"][0]["id"]
    return None

async def fetch_roblox_previous_usernames(user_id):
    """Fetch previous usernames of a Roblox user."""
    url = f"https://users.roblox.com/v1/users/{user_id}/username-history"
    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 429:  # Rate limit
                print(f"Rate limit hit while fetching previous usernames for user ID {user_id}.")
                return None  # Indicate failure to fetch previous usernames
            if response.status != 200:
                print(f"Error fetching previous usernames for user ID {user_id}: {response.status}")
                return []
            data = await response.json()
            return [entry["name"] for entry in data.get("data", [])]

@bot.command()
async def boards(ctx):
    """Check all Trello boards and output their names or access errors."""
    await ctx.send(f"{ctx.author.mention}, checking Trello boards... Please wait.")

    accessible_boards = []
    inaccessible_boards = []

    async with ClientSession() as session:
        for board_id in board_ids:
            board_name = await fetch_board_name(board_id, session)
            if board_name is None:
                inaccessible_boards.append(f"Unable to access board ({board_id})")
            else:
                accessible_boards.append(f"{board_name}")

    filename = "Board_Check_Report.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write("Accessible Boards:\n")
        for board in accessible_boards:
            file.write(f"{board}\n")

        file.write("\nInaccessible Boards:\n")
        for board in inaccessible_boards:
            file.write(f"{board}\n")

    await ctx.send(f"{ctx.author.mention}, board check complete!", file=discord.File(filename))
    os.remove(filename)

@bot.command()
async def search(ctx, keyword: str):
    """Search Trello boards for a given keyword and send results in the chat."""
    await ctx.send(f"{ctx.author.mention}, searching for '{keyword}'... Please wait.")

    results = {}
    seen_cards = set()
    usernames_to_search = [keyword.lower()]

    # Fetch Roblox user details if the keyword is a username
    user_id = await fetch_roblox_user_id(keyword)
    previous_usernames = []
    if user_id:
        fetched_usernames = await fetch_roblox_previous_usernames(user_id)
        if fetched_usernames is None:
            await ctx.send(f"{ctx.author.mention}, failed to fetch previous usernames due to rate limiting. Only the provided username will be checked.")
        else:
            previous_usernames = fetched_usernames
            usernames_to_search.extend([name.lower() for name in previous_usernames])

    async with ClientSession() as session:
        for board_id in board_ids:
            cards = await fetch_all_cards(board_id, session)
            if not cards:
                results[f"Unknown Board ({board_id})"] = ["[FAILED CHECK]"]
                continue

            board_results = []
            for card in cards:
                card_id = card['id']
                if card_id in seen_cards:
                    continue

                if any(username in card["name"].lower() or username in card.get("desc", "").lower() for username in usernames_to_search):
                    seen_cards.add(card_id)
                    card_link = f"https://trello.com/c/{card['shortLink']}"
                    archive_notice = " (Archived)" if card.get("closed", False) else ""
                    board_results.append(f"{card['name']}: {card_link}{archive_notice}")

            if board_results:
                board_name = await fetch_board_name(board_id, session)
                results[board_name] = board_results

    # Create a text file with the results
    if results:
        filename = f"{keyword}_Background_Check.txt"
        with open(filename, "w", encoding="utf-8") as file:
            # Write previous usernames at the top
            if previous_usernames:
                file.write("Previous Usernames: " + ", ".join(previous_usernames) + "\n\n")
            for board_name, board_results in results.items():
                file.write(f"Board: {board_name}\n")
                file.write("\n".join(board_results) + "\n\n")

        await ctx.send(f"{ctx.author.mention}, search complete!", file=discord.File(filename))
        os.remove(filename)
    else:
        await ctx.send(f"{ctx.author.mention}, no results found.")

@bot.command()
async def transcript(ctx: commands.Context):
    await chat_exporter.quick_export(ctx.channel)


@bot.command()
async def runtime(ctx):
    """Check how long the bot has been running."""
    elapsed_time = time.time() - start_time
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    await ctx.send(f"The bot has been running for {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds.")

@bot.command()
async def restart(ctx):
    """Restart the bot (restricted to authorized user)."""
    if ctx.author.id == AUTHORIZED_USER_ID:
        await ctx.send("Restarting the bot...")
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        await ctx.send("You are not authorized to use this command.")

# Run the bot
bot.run(os.getenv("BOT_TOKEN"))
