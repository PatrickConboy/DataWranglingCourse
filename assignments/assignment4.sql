-- Dropping existing tables
DROP TABLE IF EXISTS ev_invites;
DROP TABLE IF EXISTS ev_events;
DROP TABLE IF EXISTS ev_users;

-- Problem 1
CREATE TABLE ev_users (
	-- I made username unique because I felt like it should be.
	username VARCHAR(20) UNIQUE NOT NULL,
    first VARCHAR(40),
    last VARCHAR(40),
    affiliation VARCHAR(40) DEFAULT "None",
    PRIMARY KEY (username)
);