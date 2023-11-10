import requests
import config
import sqlite3
import time


def get_clan_details(clan_name):
    params = {
        "type": "exact",  # the name needs to be exactly the same
        "search": clan_name
    }
    response = requests.get(config.clan_name_url, params=params)
    if response.status_code == 200:
        clan_id = response.json()["data"][0]["clan_id"]
        params = {"clan_id": clan_id}
        response = requests.get(config.clan_info_url, params=params)

        if response.status_code == 200:
            return response.json()["data"][str(clan_id)]
        else:
            print("Error occurred while fetching clan info:", response.status_code)
    else:
        print("Error occurred while searching for the clan:", response.status_code)
    return None


def insert_clan_into_db(clan_details):
    clan = (
        clan_details["clan_id"],
        clan_details["name"],
        clan_details["tag"],
        time.strftime("%d/%m/%Y", time.localtime(clan_details["created_at"])),
        clan_details["creator_id"],
        clan_details["leader_id"],
        clan_details["color"],
        clan_details["members_count"]
    )
    with sqlite3.connect("db.sqlite3") as conn:
        command = "INSERT INTO Clans VALUES(?,?,?,?,?,?,?,?)"
        conn.execute(command, clan)
        conn.commit()


def insert_clan_members_into_db(clan_members, clan_id):
    members_list = []
    for member in clan_members:
        player_details = (
            member["account_id"],
            member["account_name"],
            member["role"],
            time.strftime("%d/%m/%Y", time.localtime(member["joined_at"])),
            clan_id
        )
        members_list.append(player_details)

    with sqlite3.connect("db.sqlite3") as conn:
        command = "INSERT INTO Players VALUES(?,?,?,?,?)"
        for player in members_list:
            conn.execute(command, player)
            conn.commit()


def get_and_insert_player_stats(account_id):
    params = {
        "account_id": account_id
    }
    response = requests.get(config.stats_url, params=params)

    if response.status_code == 200:
        statistics = response.json()
        player_statistics = statistics["data"][str(account_id)]

        stats_time = time.strftime("%d/%m/%Y %H:%M:%S")

        player_stats = (
            player_statistics["account_id"],
            stats_time,
            time.strftime(
                "%d/%m/%Y", time.localtime(player_statistics["created_at"])),
            player_statistics["global_rating"],
            time.strftime(
                "%d/%m/%Y %H:%M", time.localtime(player_statistics["last_battle_time"])),
            time.strftime("%d/%m/%Y %H:%M",
                          time.localtime(player_statistics["logout_at"])),
            player_statistics["statistics"]["all"]["battles"],
            player_statistics["statistics"]["all"]["wins"],
            player_statistics["statistics"]["all"]["losses"],
            player_statistics["statistics"]["all"]["draws"],
            player_statistics["statistics"]["all"]["max_xp"],
            player_statistics["statistics"]["all"]["max_damage"],
            player_statistics["statistics"]["all"]["avg_damage_blocked"],
            player_statistics["statistics"]["all"]["max_damage_tank_id"],
            player_statistics["statistics"]["all"]["survived_battles"],
            player_statistics["statistics"]["all"]["hits_percents"],
            player_statistics["statistics"]["all"]["spotted"]
        )

        with sqlite3.connect("db.sqlite3") as conn:
            command = "INSERT INTO Statistics VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            conn.execute(command, player_stats)
            conn.commit()
    else:
        print(
            f"Error occurred while fetching stats for account ID {account_id}: {response.status_code}")


def main():
    clan_name = input("Enter the clan tag: ")
    clan_details = get_clan_details(clan_name)

    if clan_details:
        insert_clan_into_db(clan_details)
        clan_members = clan_details["members"]
        clan_id = clan_details["clan_id"]

        insert_clan_members_into_db(clan_members, clan_id)

        for player in clan_members:
            account_id = player["account_id"]
            get_and_insert_player_stats(account_id)
        print("Data succesfully added to our DB")


if __name__ == "__main__":
    main()
