-- ============================================================
-- Game Guides — Seed Definitivo
-- ============================================================

-- Roles por defecto
INSERT INTO gg_roles (name) VALUES 
('user'), 
('admin')
ON CONFLICT (name) DO NOTHING;

-- Plataformas
INSERT INTO gg_platforms (name) VALUES 
('PS1'),
('PS2'),
('PS4'),
('PS5'),
('PC'),
('Xbox'),
('Switch')
ON CONFLICT (name) DO NOTHING;

-- Géneros
INSERT INTO gg_genres (name) VALUES 
('RPG'),
('JRPG'),
('Action'),
('Open World'),
('Adventure'),
('Action RPG'),
('Hack and Slash')
ON CONFLICT (name) DO NOTHING;

-- ============================================================
-- Games
-- ============================================================
INSERT INTO gg_games (name, slug, description, cover_url, release_year, rating, is_enabled, sort_order)
VALUES
  (
    'Chrono Cross',
    'chrono-cross',
    'Lejos, el mejor RPG en mi opinión personal. Este juego no solo me marcó, sino que también fue la razón por la que nació esta página. Un viaje entre dimensiones que nunca deja de sorprenderme.',
    'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1784574433/games/grfaumrt3ewwpbqaj5t0.webp',
    1999, 10, TRUE, 1
  ),
  (
    'Comrades',
    'comrades',
    'Sinceramente, creo que soy el único que todavía juega esto. Los servidores parecen un desierto, pero aun así, algo tiene que me hace volver. Una joya escondida para los que disfrutan de las batallas en compañía… aunque sea con NPCs.',
    'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1784584032/games/pr7szufujugqowb5lkqp.webp',
    2017, 5, TRUE, 2
  ),
  (
    'Darksiders 2',
    'darksiders-2',
    'Un auténtico manjar de los dioses. La mezcla perfecta entre acción, puzzles y ese estilo artístico que te deja con la boca abierta. Jugarlo es sentirse el Jinete del Apocalipsis en persona.',
    'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1784585672/games/zprczfdoee65acnouaco.webp',
    2012, 10, TRUE, 3
  ),
  (
    'Final Fantasy IX',
    'final-fantasy-ix',
    'Uno de los trofeos más duros que he conseguido en mi vida gamer. Pero cada segundo valió la pena: una historia entrañable, una banda sonora que emociona y un final que se queda contigo.',
    'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1784587157/games/udqzppo2rcvnphq2d1so.webp',
    2000, 8, TRUE, 4
  ),
  (
    'Grand Theft Auto III',
    'grand-theft-auto-iii',
    'Una aventura clásica llena de caos, humor y misiones secundarias que pueden poner a prueba tu paciencia (y tu cordura). Pero, quién no disfruta causando un poco de desorden en Liberty City.',
    'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1784588837/games/ulh9gkgs01zvwjib7dd9.webp',
    2001, 6, TRUE, 5
  ),
  (
    'Horizon Zero Dawn',
    'horizon-zero-dawn',
    'Un mundo postapocalíptico que no deja de maravillarme cada vez que lo juego. Lo he terminado en todas las dificultades y aún así siempre encuentro algo que me atrapa. Sus máquinas, paisajes e historia nunca se agotan.',
    'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1784588963/games/ovlxvmbxw4u3psr0106b.webp',
    2017, 10, TRUE, 6
  )
ON CONFLICT (name) DO NOTHING;

-- ============================================================
-- Game-Platform relations (sin IDs, resuelve por nombre)
-- ============================================================
INSERT INTO gg_game_platforms (game_id, platform_id)
SELECT g.id, p.id FROM gg_games g, gg_platforms p
WHERE (g.name, p.name) IN (
  ('Chrono Cross',      'PS1'),
  ('Comrades',          'PS4'),
  ('Darksiders 2',      'Xbox'),
  ('Darksiders 2',      'PC'),
  ('Darksiders 2',      'PS4'),
  ('Final Fantasy IX',  'PS1'),
  ('Grand Theft Auto III', 'PS2'),
  ('Grand Theft Auto III', 'PC'),
  ('Horizon Zero Dawn', 'PS4')
)
ON CONFLICT DO NOTHING;

-- ============================================================
-- Game-Genre relations (sin IDs, resuelve por nombre)
-- ============================================================
INSERT INTO gg_game_genres (game_id, genre_id)
SELECT g.id, c.id FROM gg_games g, gg_genres c
WHERE (g.name, c.name) IN (
  ('Chrono Cross',      'RPG'),
  ('Comrades',          'Action RPG'),
  ('Darksiders 2',      'Hack and Slash'),
  ('Final Fantasy IX',  'RPG'),
  ('Grand Theft Auto III', 'Open World'),
  ('Grand Theft Auto III', 'Action'),
  ('Horizon Zero Dawn', 'Open World'),
  ('Horizon Zero Dawn', 'Action'),
  ('Horizon Zero Dawn', 'Adventure')
)
ON CONFLICT DO NOTHING;

