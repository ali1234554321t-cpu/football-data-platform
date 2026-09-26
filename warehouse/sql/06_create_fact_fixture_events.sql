CREATE TABLE IF NOT EXISTS fact_fixture_events (
    event_key SERIAL PRIMARY KEY,
    event_id BIGINT NOT NULL,
    fixture_key INTEGER,
    player_key INTEGER,
    related_player_key INTEGER,

    event_type_id INTEGER,
    minute INTEGER,
    extra_minute INTEGER,
    result VARCHAR(50),
    info VARCHAR(255),
    addition VARCHAR(255),

    CONSTRAINT fk_event_fixture
        FOREIGN KEY (fixture_key) REFERENCES fact_fixtures(fixture_key),

    CONSTRAINT fk_event_player
        FOREIGN KEY (player_key) REFERENCES dim_player(player_key),

    CONSTRAINT fk_event_related_player
        FOREIGN KEY (related_player_key) REFERENCES dim_player(player_key)
);