CREATE DATABASE flashcards;
use flashcards;

CREATE TABLE decks (
  `name` VARCHAR(40) PRIMARY KEY,
  `desc` VARCHAR(40)
);

INSERT INTO decks
  (`name`, `desc`)
VALUES
  ('italian', 'Italian words'),
  ('spanish', 'Spanish words');

CREATE TABLE cards (
  deck VARCHAR(40),
  front VARCHAR(40),
  back VARCHAR(40),
  bin INT DEFAULT 0,
  due DATETIME DEFAULT CURRENT_TIMESTAMP,
  date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (deck, front)
);

INSERT INTO cards
  (deck, front, back)
VALUES
  ('italian', 'bello', 'beautiful'),
  ('italian', 'ragazzo', 'boy'),
  ('italian', 'la tavola', 'the table'),
  ('spanish', 'ingles', 'english'),
  ('spanish', 'hola', 'hello'),
  ('spanish', 'adios', 'goodbye');
