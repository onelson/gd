CREATE TABLE IF NOT EXISTS batters (
    team char(3) NOT NULL,
    id integer PRIMARY KEY NOT NULL,
    pos varchar(2) NOT NULL,
    type varchar NOT NULL,
    first_name varchar NOT NULL,
    last_name varchar NOT NULL,
    jersey_number smallint NOT NULL,
    height varchar(4) NOT NULL,
    weight integer NOT NULL,
    bats char(1) NOT NULL,
    throws char(1) NOT NULL,
    dob varchar NOT NULL,
    FOREIGN KEY(team) REFERENCES teams(code)
);

CREATE TABLE IF NOT EXISTS pitchers (
    team char(3) NOT NULL,
    id integer PRIMARY KEY NOT NULL,
    pos varchar(2) NOT NULL,
    type varchar NOT NULL,
    first_name varchar NOT NULL,
    last_name varchar NOT NULL,
    jersey_number smallint NOT NULL,
    height varchar(4) NOT NULL,
    weight integer NOT NULL,
    bats char(1) NOT NULL,
    throws char(1) NOT NULL,
    dob varchar NOT NULL,
    FOREIGN KEY(team) REFERENCES teams(code)
);

CREATE TABLE IF NOT EXISTS umpires (
    id integer PRIMARY KEY NOT NULL,
    name varchar NOT NULL
);

CREATE TABLE IF NOT EXISTS teams (
    code char(3) NOT NULL,
    id integer PRIMARY KEY NOT NULL,
    name varchar NOT NULL,
    name_full varchar NOT NULL,
    name_brief varchar NOT NULL,
    division_id smallint NOT NULL,
    league_id smallint NOT NULL,
    league char(2) NOT NULL
);

CREATE TABLE IF NOT EXISTS stadiums (
    id integer PRIMARY KEY NOT NULL,
    name varchar NOT NULL,
    location varchar NOT NULL
);

CREATE TABLE IF NOT EXISTS games (
    type char(1) NOT NULL,
    local_game_time varchar(5) NOT NULL,
    game_pk integer PRIMARY KEY NOT NULL,
    game_time_et varchar(8) NOT NULL,
    gameday_sw char(1) NOT NULL,
    home_team integer NOT NULL,
    away_team integer NOT NULL,
    stadium integer NOT NULL,
    plate_umpire integer NOT NULL,
    FOREIGN KEY(home_team) REFERENCES teams(id),
    FOREIGN KEY(away_team) REFERENCES teams(id),
    FOREIGN KEY(stadium) REFERENCES stadiums(id),
    FOREIGN KEY(plate_umpire) REFERENCES umpires(id)
);

CREATE TABLE IF NOT EXISTS atbats (
    num integer NOT NULL,
    b smallint NOT NULL,
    s smallint NOT NULL,
    o smallint NOT NULL,
    start_tfs integer PRIMARY KEY NOT NULL,
    start_tfs_zulu varchar NOT NULL,
    batter integer NOT NULL,
    stand char(1) NOT NULL,
    b_height varchar(4) NOT NULL,
    pitcher integer NOT NULL,
    p_throws char(1) NOT NULL,
    des varchar NOT NULL,
    des_es varchar NOT NULL,
    event varchar NOT NULL,
    score varchar,
    home_team_runs integer,
    away_team_runs integer,
    FOREIGN KEY(batter) REFERENCES batters(id),
    FOREIGN KEY(pitcher) REFERENCES pitchers(id)
);

CREATE TABLE IF NOT EXISTS pitches (
    pitcher integer NOT NULL,
    batter integer NOT NULL,
    game integer NOT NULL,
    umpire integer NOT NULL,
    des varchar NOT NULL,
    des_es varchar NOT NULL,
    id integer NOT NULL, -- only in-game uniqueness
    type char(1) NOT NULL,
    tfs integer PRIMARY KEY NOT NULL,
    tfs_zulu timestamp NOT NULL,
    x float NOT NULL,
    y float NOT NULL,
    on_1b integer,
    on_2b integer,
    on_3b integer,
    sv_id varchar NOT NULL, -- YYMMDD_hhmmss
    start_speed float NOT NULL,
    end_speed float NOT NULL,
    sz_top float NOT NULL,
    sz_bot float NOT NULL,
    pfx_x float NOT NULL,
    pfx_z float NOT NULL,
    px float NOT NULL,
    pz float NOT NULL,
    x0 float NOT NULL,
    y0 float NOT NULL,
    z0 float NOT NULL,
    vx0 float NOT NULL,
    vy0 float NOT NULL,
    vz0 float NOT NULL,
    ax float NOT NULL,
    ay float NOT NULL,
    az float NOT NULL,
    break_y float NOT NULL,
    break_angle float NOT NULL,
    break_length float NOT NULL,
    pitch_type char(2) NOT NULL,
    type_confidence float NOT NULL,
    zone smallint NOT NULL,
    nasty smallint NOT NULL,
    spin_dir float NOT NULL,
    spin_rate float NOT NULL,
    cc varchar,
    mt varchar,
    FOREIGN KEY(pitcher) REFERENCES pitchers(id),
    FOREIGN KEY(batter) REFERENCES batters(id),
    FOREIGN KEY(game) REFERENCES games(id),
    FOREIGN KEY(umpire) REFERENCES umpires(id)
);
