CREATE TABLE clan_details (
    clan_id INT PRIMARY KEY,
    name VARCHAR(255),
    tag VARCHAR(255),
    created_at DATE,
    creator_id INT,
    leader_id INT,
    color VARCHAR(7),
    members_count INT
);

CREATE TABLE players (
    player_id INT PRIMARY KEY,
    player_name VARCHAR(255),
    role VARCHAR(255),
    join_date DATE,
    clan_id INT,
    FOREIGN KEY (clan_id) REFERENCES clan_details(clan_id)
);

CREATE TABLE player_statistics (
    player_id INT PRIMARY KEY,
    registration_date DATE,
    global_rating INT,
    last_battle_time DATETIME,
    logout_time DATETIME,
    battles INT,
    wins INT,
    losses INT,
    draws INT,
    max_xp INT,
    max_damage INT,
    avg_damage_blocked DECIMAL(5,2),
    max_damage_tank_id INT,
    survived_battles INT,
    hits_percents INT,
    spotted INT,
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

CREATE TABLE player_tanks (
    player_id INT,
    wins INT,
    battles INT,
    mark_of_mastery INT,
    tank_id INT,
    PRIMARY KEY (player_id, tank_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);