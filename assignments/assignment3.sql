# Working with databases
#
# This script will delete and then remake the tables for this assignment.
# Load the script when you need to "reset" things.
# You will also add your solutions at the bottom.

DROP TABLE IF EXISTS acquaintances;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS profiles;

CREATE TABLE profiles (
	username VARCHAR(20) UNIQUE NOT NULL,
    first VARCHAR(40),
    last VARCHAR(40) NOT NULL,
    PRIMARY KEY (username)
);

CREATE TABLE messages (
	id INTEGER NOT NULL UNIQUE AUTO_INCREMENT,
    sender VARCHAR(20) NOT NULL,
    recipient VARCHAR(20) NOT NULL,
    message VARCHAR(400) NOT NULL DEFAULT "",
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    sent_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    in_reply_to INT DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (sender)  REFERENCES profiles(username) ON DELETE CASCADE,
    FOREIGN KEY (recipient)  REFERENCES profiles(username) ON DELETE CASCADE,
    FOREIGN KEY (in_reply_to)  REFERENCES messages(id) ON DELETE SET NULL
);

CREATE TABLE acquaintances (
	source VARCHAR(20) NOT NULL,
    target VARCHAR(20) NOT NULL,
    PRIMARY KEY (source, target),
    FOREIGN KEY (source) REFERENCES profiles(username) ON DELETE CASCADE,
    FOREIGN KEY (target) REFERENCES profiles(username) ON DELETE CASCADE
);

INSERT INTO profiles (username, first, last) VALUES
	("admin", NULL, "Admin"),
    ("pconboy", "Patrick", "Conboy"),
    ("aturing", "Alan", "Turing");
    
INSERT INTO acquaintances (source, target) VALUES
	("pconboy", "aturing");
    
INSERT INTO acquaintances (source, target) 
SELECT p.username, "admin"
FROM profiles AS p
WHERE p.username <> "admin";