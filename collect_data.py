import asyncio
import json
import aiohttp
from understat import Understat
import pandas as pd
from pandas import json_normalize
from tqdm import tqdm

async def get_fixtures():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        fixtures = await understat.get_league_results(
            "epl",
            2020
        )
    return fixtures


loop = asyncio.get_event_loop()
data = loop.run_until_complete(get_fixtures())

ids = []
for match in data:
    if match['isResult']:
        ids.append(match['id'])
print(len(ids))

async def main(match_ids):
    dflist = []
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        for match_id in tqdm(match_ids):
            players = await understat.get_match_shots(match_id)
            dfh, dfa = json_normalize(players['h'], sep='_'), json_normalize(players['a'], sep='_')      
            dflist.append(pd.concat([dfh, dfa], ignore_index=True))
    return pd.concat(dflist, ignore_index=True)

df = loop.run_until_complete(main(ids))
df.to_csv("premier_league_20_21_shots.csv", index=False)
print("All done! Data saved!")
