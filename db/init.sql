CREATE DATABASE flashcards;
use flashcards;

CREATE TABLE cards (
  deck VARCHAR(40),
  front VARCHAR(40),
  back VARCHAR(40),
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
