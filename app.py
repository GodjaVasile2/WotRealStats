import requests
import config
import sqlite3
import time
from pathlib import Path

params = {
    "type": "exact",
    "search": "N-AGE"
}

response = requests.get(config.clan_url, params=params)
if response.status_code == 200:
    clan_id = response.json()["data"][0]["clan_id"]

    params = {
        "clan_id": clan_id
    }

    response = requests.get(config.info_url, params=params)

    if response.status_code == 200:
        clans_data = response.json()

        clan_details = clans_data["data"][str(clan_id)]
        clan = (
            clan_details["clan_id"],
            clan_details["name"],
            clan_details["created_at"],
            clan_details["creator_id"],
            clan_details["leader_id"],
            clan_details["color"],
            clan_details["members_count"]
        )
        clan_members = clans_data["data"][str(clan_id)]["members"]

        members_list = []
        for member in clan_members:
            player_details = (
                member["account_id"],
                member["account_name"],
                member["role"],
                member["joined_at"]
            )
            members_list.append(player_details)
    else:
        print("Error occurred:", response.status_code)

else:
    print("Error occurred:", response.status_code)


with sqlite3.connect("db.sqlite3") as conn:
    command = "INSERT INTO Clans VALUES(?,?,?,?,?,?,?)"

    conn.execute(command, clan)
    conn.commit()


# current_timestamp = int(time.time())
# formatted_date = time.strftime("%d/%m/%Y", time.localtime(current_timestamp))
