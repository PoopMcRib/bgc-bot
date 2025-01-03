import discord
from discord.ext import commands
import requests
import os
import asyncio
from aiohttp import ClientSession
import time
import sys

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

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def fetch_board_name(board_id, session):
    url = f"https://api.trello.com/1/boards/{board_id}"
    params = {"key": TRELLO_API_KEY, "token": TRELLO_TOKEN}
    async with session.get(url, params=params) as response:
        if response.status != 200:
            return f"Unknown Board ({board_id})"
        data = await response.json()
        return data.get("name", f"Unknown Board ({board_id})")

async def fetch_cards(board_id, session, closed=False):
    url = f"https://api.trello.com/1/boards/{board_id}/cards{'/closed' if closed else ''}"
    params = {"key": TRELLO_API_KEY, "token": TRELLO_TOKEN}
    async with session.get(url, params=params) as response:
        if response.status != 200:
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
            if response.status != 200:
                return []
            data = await response.json()
            return [entry["name"] for entry in data.get("data", [])]

@bot.command()
async def search(ctx, keyword: str):
    """Search Trello boards for a given keyword and send results in the chat."""
    await ctx.send(f"Sir yes sir, {ctx.author.mention}, sir! Currently inspecting {keyword}'s butthole! Please wait, sir!")

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
        # Add more board IDs as needed
    ]
    results = {}
    seen_cards = set()  # Track cards already added
    usernames_to_search = [keyword]

    # Fetch Roblox user details if the keyword is a username
    user_id = await fetch_roblox_user_id(keyword)
    if user_id:
        previous_usernames = await fetch_roblox_previous_usernames(user_id)
        usernames_to_search.extend(previous_usernames)

    async with ClientSession() as session:
        tasks = []
        for board_id in board_ids:
            tasks.append(fetch_board_name(board_id, session))
            tasks.append(fetch_cards(board_id, session, closed=False))
            tasks.append(fetch_cards(board_id, session, closed=True))

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for i in range(0, len(responses), 3):
            board_name = responses[i]
            active_cards = responses[i + 1]
            archived_cards = responses[i + 2]

            if isinstance(active_cards, Exception) or isinstance(archived_cards, Exception):
                results[board_name] = ["[FAILED CHECK]"]
                continue

            all_cards = [(card, False) for card in active_cards] + [(card, True) for card in archived_cards]

            board_results = []
            for card, is_archived in all_cards:
                card_id = card['id']
                if card_id in seen_cards:  # Skip if card is already added
                    continue

                for username in usernames_to_search:
                    if username.lower() in card["name"].lower() or username.lower() in card.get("desc", "").lower():
                        seen_cards.add(card_id)  # Mark card as seen
                        card_link = f"https://trello.com/c/{card['shortLink']}"
                        archive_notice = " (Archived)" if is_archived else ""
                        board_results.append(f"{card['name']}: {card_link}{archive_notice}")

            if board_results:
                results[board_name] = list(set(results.get(board_name, []) + board_results))

    # Create a text file with the results
    if results:
        filename = f"{keyword}_Background_Check.txt"
        with open(filename, "w", encoding="utf-8") as file:
            # Write previous usernames at the top
            file.write("Previous Usernames: " + ", ".join(previous_usernames) + "\n\n")
            for board_name, board_results in results.items():
                file.write(f"Board: {board_name}\n")
                file.write("\n".join(board_results) + "\n\n")

        await ctx.send(f"{ctx.author.mention}, {keyword}'s butthole inspection is complete, sir! Here's everything we found hiding up there:", file=discord.File(filename))
        os.remove(filename)  # Clean up the file after sending
    else:
        await ctx.send(f"{ctx.author.mention}, no results found.")

@bot.command()
async def runtime(ctx):
    """Check how long the bot has been running."""
    elapsed_time = time.time() - start_time
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    await ctx.send(f"I have been inspecting buttholes for {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds, sir!")

@bot.command()
async def restart(ctx):
    """Restart the bot (restricted to authorized user)."""
    if ctx.author.id == AUTHORIZED_USER_ID:
        await ctx.send("Sir yes sir, daddy Prop, sir!")
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        await ctx.send("You ain't got the roles for that lil bro.")

# Run the bot
bot.run(os.getenv("BOT_TOKEN"))
