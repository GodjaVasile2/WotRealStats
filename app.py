import requests
import sqlite3
import time
import csv
import os
import mysql.connector


# Read the application id from the environment variable
application_id = os.getenv('APPLICATION_ID')
password = os.getenv('DB_PASSWORD')
base_url = "https://api.worldoftanks.eu/wot/"


def execute_db_query(query, data):
    try:
        conn = mysql.connector.connect(
            user='root', password=password, host='127.0.0.1', database='wot_statistics')
        cursor = conn.cursor()

        # Check if data is a list of tuples (multiple rows) or a single tuple (one row)
        if isinstance(data[0], tuple):
            cursor.executemany(query, data)
        else:
            cursor.execute(query, data)
        conn.commit()

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def get_and_insert_clan_details(clan_name):
    params = {
        "type": "exact",  # the name needs to be exactly the same
        "search": clan_name
    }

    # we make a request to the API and we get the clan ID
    response = requests.get(
        f"{base_url}clans/list/?application_id={application_id}", params=params)
    if response.status_code == 200:
        clan_id = response.json()["data"][0]["clan_id"]
        params = {"clan_id": clan_id}

        # we get the clan ID from the response and we make another request to get the clan details
        response = requests.get(
            f"{base_url}clans/info/?application_id={application_id}", params=params)

        if response.status_code == 200:
            clan_details = response.json()["data"][str(clan_id)]

            clan = (
                clan_details["clan_id"],
                clan_details["name"],
                clan_details["tag"],
                time.strftime(
                    "%Y-%m-%d", time.localtime(clan_details["created_at"])),
                clan_details["creator_id"],
                clan_details["leader_id"],
                clan_details["color"],
                clan_details["members_count"]
            )

            insert_stmt = """INSERT INTO clan_details(clan_id, name, tag, created_at, creator_id,leader_id,color,members_count)
            VALUES (%s, %s, %s, %s, %s, %s,%s,%s)"""
            execute_db_query(insert_stmt, clan)

            # write the clan details to a csv file
            # with open("jsons/clan_info.csv", "a", newline='') as file:
            #     writer = csv.writer(file)
            #     writer.writerow(clan)

        else:
            print("Error occurred while fetching clan info:", response.status_code)
    else:
        print("Error occurred while searching for the clan:", response.status_code)
    return clan_details["members"], clan_details["clan_id"]


def get_and_insert_clan_members(clan_members, clan_id):
    members_list = []
    for member in clan_members:
        player_details = (
            member["account_id"],
            member["account_name"],
            member["role"],
            time.strftime("%Y-%m-%d", time.localtime(member["joined_at"])),
            clan_id
        )
        members_list.append(player_details)

    # write the clan members to the database
    insert_stmt = """INSERT INTO players(player_id, player_name, role, join_date, clan_id)VALUES (%s, %s, %s, %s, %s)"""
    execute_db_query(insert_stmt, members_list)

    # write the clan members to a csv file
    # with open("jsons/clan_members.csv", "a", newline='') as file:
    #     writer = csv.writer(file)
    #     for player in members_list:
    #         writer.writerow(player)


def get_and_insert_player_stats(account_id):
    params = {
        "account_id": account_id
    }
    response = requests.get(
        f"{base_url}account/info/?application_id={application_id}", params=params)

    if response.status_code == 200:
        statistics = response.json()
        player_statistics = statistics["data"][str(account_id)]

        player_stats = (
            player_statistics["account_id"],
            # stats_time,
            time.strftime(
                "%Y-%m-%d", time.localtime(player_statistics["created_at"])),
            player_statistics["global_rating"],
            time.strftime(
                "%Y-%m-%d %H:%M", time.localtime(player_statistics["last_battle_time"])),
            time.strftime("%Y-%m-%d %H:%M",
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

        # insert the stats into the database

        insert_stmt = """INSERT INTO player_statistics(player_id, registration_date, global_rating, last_battle_time,logout_time,battles,wins,losses,draws,max_xp,max_damage,avg_damage_blocked,max_damage_tank_id,survived_battles,hits_percents,spotted)
            VALUES (%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        execute_db_query(insert_stmt, player_stats)

        # # write the stats to a csv file
        # with open("jsons/statistics.csv", "a", newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerow(player_stats)

    else:
        print(
            f"Error occurred while fetching stats for account ID {account_id}: {response.status_code}")


def get_and_insert_players_tanks(account_id):
    params = {
        "account_id": account_id
    }
    response = requests.get(
        f"{base_url}account/tanks/?application_id={application_id}", params=params)

    if response.status_code == 200:
        player_tanks_json = response.json()["data"][str(account_id)]
        player_tanks_list = []
        for tank in player_tanks_json:
            player_tanks = (
                account_id,
                tank["statistics"]["wins"],
                tank["statistics"]["battles"],
                tank["mark_of_mastery"],
                tank["tank_id"]
            )
            player_tanks_list.append(player_tanks)

        insert_stmt = """INSERT INTO player_tanks(player_id, wins, battles,mark_of_mastery,tank_id)
        VALUES (%s, %s, %s, %s, %s)"""
        execute_db_query(insert_stmt, player_tanks_list)



def main():
    clan_name = input("Enter the clan name: ")

    clan_members, clan_id = get_and_insert_clan_details(clan_name)

    get_and_insert_clan_members(clan_members, clan_id)

    for player in clan_members:
        account_id = player["account_id"]
        get_and_insert_player_stats(account_id)

    for player in clan_members:
        account_id = player["account_id"]
        get_and_insert_players_tanks(account_id)

    print(f"Finished inserting data for clan {clan_name}")


if __name__ == "__main__":
    main()
