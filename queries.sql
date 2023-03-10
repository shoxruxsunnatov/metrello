CREATE TABLE boards (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR  (500) NOT NULL,
    board_trello_id VARCHAR  (50) UNIQUE NOT NULL
);

CREATE TABLE lists (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR (500) NOT NULL,
    list_trello_id VARCHAR (50) UNIQUE NOT NULL,
    board_id INTEGER REFERENCES boards (id)
);

CREATE TABLE cards (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR (500) NOT NULL,
    card_trello_id VARCHAR  (50) UNIQUE NOT NULL,
    url VARCHAR (500) NOT NULL,
    Description text,
    lists_id INTEGER REFERENCES lists (id)
);

CREATE TABLE members (
    id BIGSERIAL PRIMARY KEY,
    fullname VARCHAR  (100) NOT NULL,
    trello_username VARCHAR (100) UNIQUE NOT NULL,
    member_trello_id VARCHAR (50) UNIQUE NOT NULL
);

CREATE TABLE cards_members (
    id SERIAL,
    card_id INTEGER REFERENCES cards (id),
    member_id INTEGER REFERENCES members (id),
    primary key  (card_id, member_id)
);

CREATE TABLE board_members (
    id SERIAL,
    board_id INTEGER REFERENCES boards (id) UNIQUE NOT NULL ,
    member_id INTEGER REFERENCES members (id)
);

CREATE TABLE labels (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR CHECK ( name > '0' ),
    label_trello_id VARCHAR  NOT NULL UNIQUE,
    board_id INTEGER REFERENCES boards (id)
);

CREATE TABLE cards_labels (
    id SERIAL,
    card_id INTEGER REFERENCES cards (id),
    labels_id INTEGER REFERENCES labels (id),
    primary key (card_id, labels_id)
);

CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    chat_id bigint NOT NULL UNIQUE,
    fullname VARCHAR (100),
    username VARCHAR (100) NOT NULL UNIQUE,
    member_id INTEGER REFERENCES members (id)
);