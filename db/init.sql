CREATE DATABASE flashcards;
use flashcards;

CREATE TABLE cards (
  cid INT NOT NULL AUTO_INCREMENT,
  deck VARCHAR(40) NOT NULL,
  front VARCHAR(40),
  back VARCHAR(40),
  PRIMARY KEY (cid)
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
