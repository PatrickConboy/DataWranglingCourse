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

-- Problem 2
CREATE TABLE ev_events (
	-- Again, made this unique, cause yea.
    id INTEGER NOT NULL UNIQUE AUTO_INCREMENT,
    title VARCHAR(40) NOT NULL DEFAULT "",
    longitude DECIMAL,
    latitude DECIMAL,
    owner VARCHAR(20) NOT NULL,
    start TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end TIMESTAMP NULL DEFAULT NULL,
    FOREIGN KEY (owner) REFERENCES ev_users(username),
    PRIMARY KEY (id)
);

-- Problem 3