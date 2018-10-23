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
    longitude DECIMAL(6,2),
    latitude DECIMAL(6,2),
    owner VARCHAR(20) NOT NULL,
    start TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end TIMESTAMP NULL DEFAULT NULL,
    FOREIGN KEY (owner) REFERENCES ev_users(username),
    PRIMARY KEY (id)
);

-- Problem 3
CREATE TABLE ev_invites (
	event_id INTEGER NOT NULL,
    username VARCHAR(20) NOT NULL,
    status ENUM ('Accepted', 'Declined', 'Maybe'),
    FOREIGN KEY (username) REFERENCES ev_users(username) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES ev_events(id) ON DELETE CASCADE
);

-- Problem 4
INSERT INTO ev_users (username, first, last, affiliation) VALUES 
	("conboyp", "patrick", "conboy", "Hanover College, Student"),
	("jarnagink", "kenny", "jarnagin", "Hanover College, Student"),
    ("skiadasc", "charilaos", "skiadas", "Hanover College, Faculty, Staff");
    
-- Problem 5
INSERT INTO ev_events (title, longitude, latitude, owner, start) VALUES
	("Homecoming get-together", 38.71, 85.46, "conboyp", '2018-10-6 08:00:00');
    
-- Problem 6
INSERT INTO ev_invites (event_id, username, status) 
SELECT e.id, e.owner, 'Accepted'
FROM ev_events AS e
WHERE NOT EXISTS (SELECT i.username
				  FROM ev_invites AS i, ev_events AS e
                  WHERE e.owner = i.username);
                  
-- Problem 7
INSERT INTO ev_invites (event_id, username)
SELECT e.id, u.username
FROM ev_events AS e, ev_users AS u
WHERE e.title LIKE "%Homecoming%"
AND u.affiliation LIKE "%Hanover College%";