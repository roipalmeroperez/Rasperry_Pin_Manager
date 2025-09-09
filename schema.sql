DROP TABLE IF EXISTS users;

DROP TABLE IF EXISTS pins;

DROP TABLE IF EXISTS devices;

DROP TABLE IF EXISTS rules;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255),
    passwd VARCHAR(255)
);

CREATE TABLE devices (
    ip VARCHAR(255) PRIMARY KEY,
    description VARCHAR(255),
    last_update DATETIME,
    alive BOOLEAN
);

CREATE TABLE pins (
    pin_ip VARCHAR(255),
    pin_number INT,
    description VARCHAR(255),
    pin_mode VARCHAR(255),
    pin_value INT,
    PRIMARY KEY (pin_ip, pin_number),
    FOREIGN KEY (pin_ip) REFERENCES devices(ip)
);

CREATE TABLE rules (
    id VARCHAR(255) PRIMARY KEY,
    operand1 VARCHAR(255),
    rule_op VARCHAR(255),
    operand2 VARCHAR(255),
    output_target VARCHAR(255),
    output_value INT,
    rule_value BOOLEAN
);
