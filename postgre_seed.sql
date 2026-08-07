-- ============================================================
-- Game Guides — Seed Definitivo
-- Generado desde GGDB.xlsx (fuente de verdad)
-- Sin IDs en duro: FKs resueltas por nombre/slug/título
-- sort_order 1-based correlativo por grupo
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
-- Games (resuelve por name UNIQUE)
-- ============================================================
INSERT INTO gg_games (name, slug, description, cover_url, release_year, rating, is_enabled, sort_order)
VALUES
  (
    'Chrono Cross',
    'chrono-cross',
    E'Lejos, el mejor RPG en mi opinión personal. Este juego no solo me marcó, sino que también fue la razón por la que nació esta página. Un viaje entre dimensiones que nunca deja de sorprenderme.',
    'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785514890/games/mf8ryr7pngjsv5bq3nad.webp',
    1999, 10, TRUE, 1
  ),
  (
    'Comrades',
    'comrades',
    E'Sinceramente, creo que soy el único que todavía juega esto. Los servidores parecen un desierto, pero aun así, algo tiene que me hace volver. Una joya escondida para los que disfrutan de las batallas en compañía… aunque sea con NPCs.',
    'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1784584032/games/pr7szufujugqowb5lkqp.webp',
    2017, 5, TRUE, 2
  ),
  (
    'Darksiders 2',
    'darksiders-2',
    E'Un auténtico manjar de los dioses. La mezcla perfecta entre acción, puzzles y ese estilo artístico que te deja con la boca abierta. Jugarlo es sentirse el Jinete del Apocalipsis en persona.',
    'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1784585672/games/zprczfdoee65acnouaco.webp',
    2012, 10, TRUE, 3
  ),
  (
    'Final Fantasy IX',
    'final-fantasy-ix',
    E'Uno de los trofeos más duros que he conseguido en mi vida gamer. Pero cada segundo valió la pena: una historia entrañable, una banda sonora que emociona y un final que se queda contigo.',
    'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785353501/games/z6epqvppya3dl68qnqkb.webp',
    2000, 8, TRUE, 4
  ),
  (
    'Grand Theft Auto III',
    'grand-theft-auto-iii',
    E'Una aventura clásica llena de caos, humor y misiones secundarias que pueden poner a prueba tu paciencia (y tu cordura). Pero, quién no disfruta causando un poco de desorden en Liberty City.',
    'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785272519/games/j5g2usxbsgfdngrxl3ka.webp',
    2001, 6, TRUE, 5
  ),
  (
    'Horizon Zero Dawn',
    'horizon-zero-dawn',
    E'Un mundo postapocalíptico que no deja de maravillarme cada vez que lo juego. Lo he terminado en todas las dificultades y aún así siempre encuentro algo que me atrapa. Sus máquinas, paisajes e historia nunca se agotan.',
    'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785273843/games/mkae5xnnpho65uhi7gvx.webp',
    2017, 10, TRUE, 6
  )
ON CONFLICT (name) DO NOTHING;

-- ============================================================
-- Game-Platform relations (sin IDs, resuelve por nombre)
-- ============================================================
INSERT INTO gg_game_platforms (game_id, platform_id)
SELECT g.id, p.id FROM gg_games g, gg_platforms p
WHERE (g.name, p.name) IN (
  ('Chrono Cross', 'PS1'),
  ('Comrades', 'PS4'),
  ('Darksiders 2', 'PS4'),
  ('Darksiders 2', 'PC'),
  ('Darksiders 2', 'Xbox'),
  ('Final Fantasy IX', 'PS1'),
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
  ('Chrono Cross', 'RPG'),
  ('Comrades', 'Action RPG'),
  ('Darksiders 2', 'Hack and Slash'),
  ('Final Fantasy IX', 'RPG'),
  ('Grand Theft Auto III', 'Action'),
  ('Grand Theft Auto III', 'Open World'),
  ('Horizon Zero Dawn', 'Action'),
  ('Horizon Zero Dawn', 'Open World'),
  ('Horizon Zero Dawn', 'Adventure')
)
ON CONFLICT DO NOTHING;

-- ============================================================
-- Sources (resuelve game_id por slug) — sort_order 1-based
-- ============================================================
INSERT INTO gg_sources (game_id, name, url, sort_order)
SELECT g.id, x.name, x.url, x.sort_order FROM gg_games g, (VALUES
  ('chrono-cross', 'Guía', 'https://guiamania.com/41154', 1),
  ('chrono-cross', 'Window Frame', 'https://www.ign.com/wikis/chrono-cross/Window_Frames', 2),
  ('chrono-cross', 'Finales', 'https://game8.co/games/Chrono-Cross-Radical-Dreamers-Edition/archives/375630', 3),
  ('chrono-cross', 'Items', 'https://game8.co/games/Chrono-Cross-Radical-Dreamers-Edition/archives/371977', 4),
  ('chrono-cross', 'Dragones', 'https://chrono.fandom.com/wiki/Chronopedia', 5),
  ('chrono-cross', 'Criosphinx', 'https://chrono.fandom.com/wiki/Criosphinx', 6),
  ('final-fantasy-ix', 'Guía Paso a Paso', 'https://www.youtube.com/watch?v=ZVTfcjFNVcU&list=PLUEaSJ4rKZoL5SJjw7ryjUI2NAztObT8F&index=2', 1),
  ('final-fantasy-ix', 'Trofeo: Mister Nice Guy ( angelo noctis)', 'https://www.youtube.com/watch?v=RWI-uaZsYAY&t=912s', 2),
  ('final-fantasy-ix', 'Trofeo: Beating the rigtime blues (angelo noctis)', 'https://www.youtube.com/watch?v=RWI-uaZsYAY&lc=UgxWdOT4ZJzoZmeEJix4AaABAg.9xkQXwbhDhM9xkVq_TWzy0', 3),
  ('final-fantasy-ix', 'Trofeo: A clean bill of health (chibikei)', 'https://www.youtube.com/watch?v=Vrh5KILchfc', 4)
) AS x(slug, name, url, sort_order)
WHERE g.slug = x.slug
ON CONFLICT DO NOTHING;

-- ============================================================
-- Characters (resuelve game_id por slug) — sort_order 1-based
-- ============================================================
INSERT INTO gg_characters (game_id, name, slug, description, image_url, is_playable, sort_order)
SELECT g.id, x.name, x.slug, x.description, x.image_url, x.is_playable, x.sort_order FROM gg_games g, (VALUES
  ('chrono-cross', 'Serge', 'character-serge', E'Se obtiene al inciar la aventura', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785460958/characters/vevpewcgnry0ebbaaoua.webp', TRUE, 1),
  ('chrono-cross', 'Mojo', 'character-mojo', E'Se obtiene con el Shark Tooth Amulet', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785464818/characters/cgjgkze3ufdplu4onxan.webp', TRUE, 2),
  ('chrono-cross', 'Leena', 'character-leena', E'Se obtiene rechazando a Kid 3 veces', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785507980/characters/ey35xyyrtf9kmapdxmgt.webp', TRUE, 3),
  ('chrono-cross', 'Poshul', 'character-poshul', E'Se obtiene rechazando a Kid 3 veces o en Arni Village dándole el hueso', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785511423/characters/ttky5yokrttspsvoz7fx.webp', TRUE, 4),
  ('chrono-cross', 'Kid', 'character-kid', E'Se obtiene en Termina o Cape Howl', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785511857/characters/n5nvpzduugvzlncdza0f.webp', TRUE, 5),
  ('chrono-cross', 'Guile ', 'character-guile', E'Se obtiene en Termina hablando con el en el bar', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785512085/characters/jdka6f494odrngzotlzl.webp', TRUE, 6),
  ('chrono-cross', 'Nikki', 'character-nikki', E'Se obtiene en Termina hablando con Miki en el barco de Magical Dreamers', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785512165/characters/nkav36ipmkltjlp3w1tn.webp', TRUE, 7),
  ('chrono-cross', 'Pierre', 'character-pierre', E'Se obtiene en Termina entregándole el Heros Medal en la herrería', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785512548/characters/w9polhxeuwtgcn8onyvn.webp', TRUE, 8),
  ('chrono-cross', 'Glenn', 'character-glenn', E'Se obtiene en Termina al decidir No salvar a Kid', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785512686/characters/ysd4huwj48hjozirxhzt.webp', TRUE, 9),
  ('chrono-cross', 'Macha', 'character-macha', E'Se obtiene en Termina al decidir No salvar a Kid', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785512740/characters/smaiwysidhcy824icv4k.webp', TRUE, 10),
  ('chrono-cross', 'Doc', 'character-doc', E'Se obtiene en Termina al decidir No salvar a Kid', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785512802/characters/tpzop3qvuy92k6snd8ky.webp', TRUE, 11),
  ('chrono-cross', 'Korcha', 'character-korcha', E'Se obtiene en Termina al decidir salvar a Kid', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785512842/characters/tb5msqko5bjf05886dmx.webp', TRUE, 12),
  ('chrono-cross', 'Greco', 'character-greco', E'Se obtiene en Termina al decidir salvar a Kid', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785512867/characters/xh2i1hczjr1segx6ktuw.webp', TRUE, 13),
  ('chrono-cross', 'Razzly', 'character-razzly', E'Se obtiene en Hydra Marsh al decidir salvar a Kid', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785512925/characters/e99dtoaklov9etgkqic3.webp', TRUE, 14),
  ('chrono-cross', 'Mel', 'character-mel', E'Se obtiene en Guldove, después de capturarla y salir de la isla', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785512987/characters/qmztvpzbtjx2lqryxxeg.webp', TRUE, 15),
  ('chrono-cross', 'Pip', 'character-pip', E'Se obtiene en el barco fantasma', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513057/characters/nck1jhuolbmloiriveck.webp', TRUE, 16),
  ('chrono-cross', 'Luccia', 'character-luccia', E'Se obtiene en Viper Manor al ir nuevamente', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513162/characters/euha6jthrga39mkpf55j.webp', TRUE, 17),
  ('chrono-cross', 'Lynx', 'character-lynx', E'Se obtiene después del evento en Fort Dragonia', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513234/characters/nwesrzou5850ekbdnhkf.webp', TRUE, 18),
  ('chrono-cross', 'Sprigg', 'character-sprigg', E'Se obtiene en el Mundo Abstracto', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513307/characters/tgpw88rfk6ybx3yuv7vd.webp', TRUE, 19),
  ('chrono-cross', 'Harle', 'character-harle', E'Se obtiene en el Mundo Abstracto', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513328/characters/lxxe3pgn9rxzbfcvfdam.webp', TRUE, 20),
  ('chrono-cross', 'Radius', 'character-radius', E'Se obtiene al vencerlo en Arni Village', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513362/characters/ogbsu2uuwivqicgyxx85.webp', TRUE, 21),
  ('chrono-cross', 'Zappa', 'character-zappa', E'Se obtiene en Termina con Lynx', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513391/characters/oe0fknerlm7csadewicg.webp', TRUE, 22),
  ('chrono-cross', 'Van', 'character-van', E'Se obtiene en Termina con Lynx', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513426/characters/txhhsbkzcbagkfsqperx.webp', TRUE, 23),
  ('chrono-cross', 'Norris', 'character-norris', E'Se obtiene en Viper Manor si Radius esta en tu equipo', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513469/characters/vszfwyrum1pw6xfed6kc.webp', TRUE, 24),
  ('chrono-cross', 'Starky', 'character-starky', E'Se obtiene venciéndolo en la isla de Sky Dragon', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513516/characters/r0zudmrhsdya228ligjj.webp', TRUE, 25),
  ('chrono-cross', 'Janice', 'character-janice', E'Se obtiene en el Zelbess al ganar el SLAM de combate', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513555/characters/gwpkjyy4mytek6t7z6dg.webp', TRUE, 26),
  ('chrono-cross', 'Sneff', 'character-sneff', E'Se obtiene en Zelbess después de derrotar al sabio', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513594/characters/wm4tbro9meewqrrkg3fp.webp', TRUE, 27),
  ('chrono-cross', 'Irenes', 'character-irenes', E'Se obtiene en Zelbess después de derrotar al sabio', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513638/characters/hddj2hmmganrjwuy0qrr.webp', TRUE, 28),
  ('chrono-cross', 'Miki', 'character-miki', E'Se obtiene en Zelbess después de derrotar al sabio', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513691/characters/tvztdanrcdloop0atoi5.webp', TRUE, 29),
  ('chrono-cross', 'Zoah', 'character-zoah', E'Se obtiene en el bar de Termina, habitación oculta', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513713/characters/gtrtcn40omycfrw2xcrt.webp', TRUE, 30),
  ('chrono-cross', 'Karsh', 'character-karsh', E'Se obtiene en el bar de Termina, habitación oculta', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513739/characters/ksmthrl7pxrhcjcqq8wx.webp', TRUE, 31),
  ('chrono-cross', 'Orcha', 'character-orcha', E'Se obtiene en Viper Manor después de rescatar a Riddel', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513786/characters/cf7hogbyyhroivyvifzd.webp', TRUE, 32),
  ('chrono-cross', 'Grobyc', 'character-grobyc', E'Se obtiene en Viper Manor después del combate con el Mecha', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513821/characters/hdclizc0naetgelnt3pj.webp', TRUE, 33),
  ('chrono-cross', 'Skelly', 'character-skelly', E'Se obtiene al conseguir todos sus huesos, son 6 en total', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513873/characters/jdlqgk5jpcn3knshyfhc.webp', TRUE, 34),
  ('chrono-cross', 'Riddel', 'character-riddel', E'Se obtiene al rescatarla del ejercito en Viper Manor', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513926/characters/mouo4dmnupgs9arctlzf.webp', TRUE, 35),
  ('chrono-cross', 'Viper', 'character-viper', E'Se obtiene después de rescatar a Riddel en Viper Manor', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785514486/characters/qurp4sbtk8rfww5ryijx.webp', TRUE, 36),
  ('chrono-cross', 'Fargo', 'character-fargo', E'Se obtiene después de rescatar a Riddel en Viper Manor', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513950/characters/wkcugq9a08nrenklm4zq.webp', TRUE, 37),
  ('chrono-cross', 'Marcy', 'character-marcy', E'Se obtiene después de rescatar a Riddel en Viper Manor', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513980/characters/rduw1ffgml88humeimlf.webp', TRUE, 38),
  ('chrono-cross', 'Turnip', 'character-turnip', E'Se obtiene en Hermits Hideaway (AW), (HW), utilizando Ice Gun o Ice Breath con Poshul en tu equipo', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785514019/characters/lb9lv4rxgdif5dspihwk.webp', TRUE, 39),
  ('chrono-cross', 'Funguy', 'character-funguy', E'Se obtiene en Shadow Forest al darle el Mushroom al hombre de la cueva en la cascada', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785514062/characters/i9kadrmseccajykkcgov.webp', TRUE, 40),
  ('chrono-cross', 'Neofio', 'character-neofio', E'Se obtiene en la pileta de Viper Manor con la Life Sparkle', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785514135/characters/v5pizvb7vmjqmjagchsx.webp', TRUE, 41),
  ('chrono-cross', 'Leah', 'character-leah', E'Se obtiene al llegar a la isla de Gaeas Navel', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785514158/characters/pqwln6qgkl46mifaleta.webp', TRUE, 42),
  ('chrono-cross', 'Steena', 'character-steena', E'Se obtiene en Guldove al mostrarle el Dragon Emblem', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785514183/characters/hjhu8zldhahuown0mqzz.webp', TRUE, 43),
  ('chrono-cross', 'Draggy', 'character-draggy', E'Se obtiene al poner el huevo gigante en Fort Dragonia', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785514237/characters/bkxwfgkai3ld0zxj9xom.webp', TRUE, 44),
  ('chrono-cross', 'Orlha', 'character-orlha', E'Orlha\nSe obtiene en Guldove devolviéndole el Sapphire Brooch como Serge', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785514271/characters/thlnw9nwcuotpr5dra50.webp', TRUE, 45)
) AS x(game_slug, name, slug, description, image_url, is_playable, sort_order)
WHERE g.slug = x.game_slug
ON CONFLICT DO NOTHING;

-- ============================================================
-- Screenshots (resuelve game_id por slug) — sort_order 1-based
-- ============================================================
INSERT INTO gg_screenshots (game_id, image_url, alt_text, sort_order)
SELECT g.id, x.image_url, x.alt_text, x.sort_order FROM gg_games g, (VALUES
  ('chrono-cross', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785105166/screenshots/vxn9oi17pjyelagijzob.webp', 'Portada del Juego', 1),
  ('chrono-cross', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785105199/screenshots/yckgjmfsvnxvdsqunthp.webp', 'Todos los Personajes', 2),
  ('comrades', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785191801/screenshots/m2fbneiv9bkqjlhynncg.webp', 'Comrades', 1),
  ('comrades', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785192711/screenshots/xl5lcyhop1jpleuwlprw.webp', 'Comrades', 2),
  ('darksiders-2', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785110631/screenshots/jwix8ewfhgusrj2mqln6.webp', 'DarkSiders 2', 1),
  ('darksiders-2', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785110637/screenshots/dscqhniygazijdxbonnr.webp', 'DarkSiders 2', 2),
  ('final-fantasy-ix', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785286217/screenshots/ntd512i1nwza644bvyiu.webp', 'FFIX', 1),
  ('final-fantasy-ix', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785286236/screenshots/scq82nyygwgnffb2f8gt.webp', 'FFIX', 2),
  ('grand-theft-auto-iii', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785196415/screenshots/otzoj0d6brrynhifplvu.webp', 'GTA 3', 1),
  ('grand-theft-auto-iii', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785196438/screenshots/nnyp6pmxrptj1mp05hn8.webp', 'GTA 3', 2),
  ('horizon-zero-dawn', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785274097/screenshots/bocsyt4nwuzzuim4uakb.webp', 'Rost', 1),
  ('horizon-zero-dawn', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785274114/screenshots/qqecprtvjwmlnzxx4eqd.webp', 'Aloy', 2)
) AS x(slug, image_url, alt_text, sort_order)
WHERE g.slug = x.slug
ON CONFLICT DO NOTHING;

-- ============================================================
-- Maps (resuelve game_id por slug) — sort_order 1-based
-- ============================================================
INSERT INTO gg_maps (game_id, image_url, alt_text, sort_order)
SELECT g.id, x.image_url, x.alt_text, x.sort_order FROM gg_games g, (VALUES
  ('comrades', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785193431/maps/kvzdpobttqxfz1yawort.webp', 'Lanza - Bigote de Dragón (1)', 1),
  ('comrades', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785193508/maps/a89ruzlxaoasfxi0haex.webp', 'Lanza - Bigote de Dragón (2)', 2),
  ('comrades', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785193655/maps/nhtiaob6knkvy6xgm32u.webp', 'Martillo - Mjolnir', 3),
  ('comrades', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785193700/maps/l5rnrr6wxzwpeo2ohd6j.webp', 'Escudo - Égida', 4),
  ('comrades', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785193740/maps/mxhn4kuopg2eo5vtogd7.webp', 'Katana - Mumeito (1)', 5),
  ('comrades', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785193754/maps/rp2gsazagvkeb34ovtrw.webp', 'Katana - Mumeito (2)', 6),
  ('comrades', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785194218/maps/smiqm8umefkadv4yn7yy.webp', 'SET - Físico', 7),
  ('comrades', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785194247/maps/wapyxurvx4uwdgquk3de.webp', 'SET - Físico / Mágico', 8),
  ('darksiders-2', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785111077/maps/sbywzljtsqtg3odqra50.webp', 'The Forge Lands', 1),
  ('darksiders-2', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785111177/maps/txclq42sqsajdvkv7ge2.webp', 'Kingdom of the Dead', 2),
  ('darksiders-2', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785114557/maps/hvdktzhzrfxu50vpufw8.webp', 'Lostlight', 3),
  ('darksiders-2', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785114608/maps/s3gzkujoslz5xqdj2osj.webp', 'Shadows Edge', 4)
) AS x(slug, image_url, alt_text, sort_order)
WHERE g.slug = x.slug
ON CONFLICT DO NOTHING;

-- ============================================================
-- Guides (resuelve game_id por slug; título como clave natural)
-- sort_order 1-based correlativo por juego
-- ============================================================
INSERT INTO gg_guides (game_id, title, summary, sort_order, is_enabled)
SELECT g.id, x.title, x.summary, x.sort_order, x.is_enabled FROM gg_games g, (VALUES
  ('chrono-cross', 'El Sueño', E'✓ Obs: (HW) = Home World, (AW) = Another World\n✓ Sigue el camino hasta el pilar de luz\n✓ Ponte encima de la plataforma magenta\n✓ Entra por la puerta\n✓ Inicias el juego con estos marcos (Marco 1/15) (Marco 2/15) (Marco 3/15)', 1, TRUE),
  ('chrono-cross', 'Final oculto: Programmers Ending (Final 1/11)', NULL, 2, TRUE),
  ('chrono-cross', '(HW) Arni Village', E'✓ Despiertas con Serge (Personaje 1/45)\n✓ Habla con Marge (Mama)\n✓ Ve al puerto y habla con Leena', 3, TRUE),
  ('chrono-cross', '(HW) Lizard Rock', E'✓ Empuja la roca enfrente de la cueva, y lucha con el primer Komodo\n✓ Usa el saliente para llegar el segundo Komodo\n✓ Debes perseguir, para cazar y luego luchar con el tercer Komodo, y luego a Mama Komodo\n✓ Sal por la izquierda de la playa, y sigue recto', 4, TRUE),
  ('chrono-cross', '(AW) Another World', E'✓ Ve a Arni y habla con Marge y Leena\n✓ Habla con la camarera del bar la de los poemas\n✓ Ve a Cape Howl y examina la tumba', 5, TRUE),
  ('chrono-cross', '(AW) Hydra Swamp', NULL, 6, TRUE),
  ('chrono-cross', '(AW) Fossil Valley', NULL, 7, TRUE),
  ('chrono-cross', '(AW) Termina', NULL, 8, TRUE)
) AS x(game_slug, title, summary, sort_order, is_enabled)
WHERE g.slug = x.game_slug
ON CONFLICT DO NOTHING;

-- ============================================================
-- Adventures (resuelve guía por (slug, título); descripción como clave)
-- sort_order 1-based correlativo por guía
-- ============================================================
INSERT INTO gg_adventures (guide_id, description, is_important, is_optional, sort_order)
SELECT gr.id, x.description, x.is_important, x.is_optional, x.sort_order
FROM gg_games g, gg_guides gr, (VALUES
  ('chrono-cross', 'El Sueño', E'Partidas guardadas', FALSE, FALSE, 1),
  ('chrono-cross', 'Final oculto: Programmers Ending (Final 1/11)', E'Cuando despiertes crea un guardado independiente de la partida principal, cuando termines el juego carga esta partida con el Continue+. Vencer al Time Devourer inmediatamente sin reclutar compañeros', TRUE, FALSE, 1),
  ('chrono-cross', '(HW) Arni Village', E'✓ Obten la Shellfish Window Frame (Marco 4/15) de la tienda de elements', FALSE, FALSE, 1),
  ('chrono-cross', '(HW) Arni Village', E'✓ Consigue la Komodo Scale (Item /56) dandole la razon al vendedor y regalasela al muchacho', FALSE, FALSE, 2),
  ('chrono-cross', '(HW) Arni Village', E'✓ Coge el Shark Tooth Amulet (Item /56) de uno de los tipos de las casas de la derecha', FALSE, FALSE, 3),
  ('chrono-cross', '(HW) Arni Village', E'✓ Consigue el Heckran Bone (Item /56) de debajo de la cama del bar', FALSE, FALSE, 4),
  ('chrono-cross', '(HW) Arni Village', E'✓ Habla con la camarera del bar la de los poemas y finalmente NO reclutes a Poshul aun', FALSE, FALSE, 5),
  ('chrono-cross', '(HW) Lizard Rock', E'Escamas de Komodo', FALSE, FALSE, 1),
  ('chrono-cross', '(AW) Another World', E'✓ Lucharas con Karsh, Solt y Peppor', FALSE, FALSE, 1),
  ('chrono-cross', '(AW) Another World', E'✓ Nombra a Kid pero NO la reclutes aun (rechazala 3 veces)', FALSE, FALSE, 2),
  ('chrono-cross', '(AW) Another World', E'✓ Leena (Personaje 3/45) y Poshul (Personaje 4/45) se te unirán ahora, (es la única manera de conseguir a Leena)', FALSE, FALSE, 3),
  ('chrono-cross', '(AW) Another World', E'✓ Ve donde conseguiste el Shark Tooth Amulet y muéstraselo al predicador, se te unirá Mojo (Personaje 2/45) al salir de allí', FALSE, FALSE, 4),
  ('chrono-cross', '(AW) Hydra Swamp', E'✓ Ve al noroeste, encuentra a un chico que te dara el Safety Gear (Item /56)', FALSE, FALSE, 1),
  ('chrono-cross', '(AW) Fossil Valley', E'✓ Obten el Heavy Skull (Item /56) de Skelly', FALSE, FALSE, 1),
  ('chrono-cross', '(AW) Fossil Valley', E'✓ Obten las Bellflower (Item /56)', FALSE, FALSE, 2),
  ('chrono-cross', '(AW) Fossil Valley', E'✓ Obten el Big Egg (Item /56) cerca del pajaro', FALSE, FALSE, 3),
  ('chrono-cross', '(AW) Termina', E'✓ Ve a la estatua en lo mas alto del pueblo, habla con el tipo que la esta limpiando, y consigue a Kid (Personaje 5/45) y obtendrás el Tele Porter (Item /56)', FALSE, FALSE, 1),
  ('chrono-cross', '(AW) Termina', E'✓ Obten el marco Tea for Three (Marco 5/15)', FALSE, FALSE, 2),
  ('chrono-cross', '(AW) Termina', E'✓ Ve a la parte mas al este del pueblo, dale las flores a Glenn', FALSE, FALSE, 3),
  ('chrono-cross', '(AW) Termina', E'✓ Aquí debes decidir cual de los 3 personajes quieres reclutar para infiltrarte en el Viper Manor, No los puedes conseguir a todos en una partida, deberás iniciar una partida (NG+) para los 2 que falten', FALSE, FALSE, 4),
  ('chrono-cross', '(AW) Termina', E'Opción 1: Consigue a Guile (Personaje 6/45), Habla con el en el bar. Ve al cementerio de Termina, encuentra el barco de Korcha y sube por el rompeolas', TRUE, FALSE, 5),
  ('chrono-cross', '(AW) Termina', E'Opción 2: Consigue a Pierre (Personaje 8/45), en la Herrería, primero debes conseguir el Heros Medal (Item /56) del del niño que juega afuera y devolvérselo a Pierre, Ve a la puerta principal de Viper Manor', TRUE, FALSE, 6)
) AS x(game_slug, guide_title, description, is_important, is_optional, sort_order)
WHERE g.slug = x.game_slug AND gr.game_id = g.id AND gr.title = x.guide_title
ON CONFLICT DO NOTHING;

-- ============================================================
-- AdventureImages (resuelve adventure por (slug, título guía, descripción))
-- sort_order 1-based correlativo por adventure
-- ============================================================
INSERT INTO gg_adventure_images (adventure_id, image_url, alt_text, sort_order)
SELECT a.id, x.image_url, x.alt_text, x.sort_order
FROM gg_games g, gg_guides gr, gg_adventures a, (VALUES
  ('chrono-cross', 'Final oculto: Programmers Ending (Final 1/11)', E'Cuando despiertes crea un guardado independiente de la partida principal, cuando termines el juego carga esta partida con el Continue+. Vencer al Time Devourer inmediatamente sin reclutar compañeros', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785888765/adventures/umgoc2wpkv8umjwbujgb.webp', 'Guardar partida para el [Final 1]', 1),
  ('chrono-cross', 'El Sueño', E'Partidas guardadas', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785881792/adventures/buttjpxtgech20kenbsh.webp', 'Frame - Arnian Wood', 1),
  ('chrono-cross', 'El Sueño', E'Partidas guardadas', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785885884/adventures/pef59ahbyilwengvck2h.webp', 'Frame - Simple Line', 2),
  ('chrono-cross', 'El Sueño', E'Partidas guardadas', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785886215/adventures/k7w8bu9ju2uzvhdxwowa.webp', 'Frame - Iron Plate', 3),
  ('chrono-cross', '(HW) Arni Village', E'✓ Obten la Shellfish Window Frame (Marco 4/15) de la tienda de elements', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785905741/adventures/u7unutqf2lzwnn7bn6cf.webp', 'Marco', 1),
  ('chrono-cross', '(HW) Arni Village', E'✓ Obten la Shellfish Window Frame (Marco 4/15) de la tienda de elements', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785905757/adventures/xlvrtzxrxbjawepvcmca.webp', 'Marco', 2),
  ('chrono-cross', '(HW) Arni Village', E'✓ Consigue la Komodo Scale (Item /56) dandole la razon al vendedor y regalasela al muchacho', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785905956/adventures/zifizyegnv8tbygywvop.webp', 'Komodo', 1),
  ('chrono-cross', '(HW) Arni Village', E'✓ Consigue la Komodo Scale (Item /56) dandole la razon al vendedor y regalasela al muchacho', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785905968/adventures/c19u0ycpctgzllceze6k.webp', 'Komodo', 2),
  ('chrono-cross', '(HW) Arni Village', E'✓ Consigue la Komodo Scale (Item /56) dandole la razon al vendedor y regalasela al muchacho', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785905978/adventures/wybvk3fcmcwnjsljjruk.webp', 'Komodo', 3),
  ('chrono-cross', '(HW) Arni Village', E'✓ Consigue la Komodo Scale (Item /56) dandole la razon al vendedor y regalasela al muchacho', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785906060/adventures/s2oqsbbdpooetocgbyyz.webp', 'Komodo', 4),
  ('chrono-cross', '(HW) Arni Village', E'✓ Coge el Shark Tooth Amulet (Item /56) de uno de los tipos de las casas de la derecha', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785906152/adventures/rlnohuh3jiaspkic7ic3.webp', 'Shark Thoot', 1),
  ('chrono-cross', '(HW) Arni Village', E'✓ Coge el Shark Tooth Amulet (Item /56) de uno de los tipos de las casas de la derecha', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785906160/adventures/unosbow3rdcj8cm1hzek.webp', 'Shark Thoot', 2),
  ('chrono-cross', '(HW) Arni Village', E'✓ Consigue el Heckran Bone (Item /56) de debajo de la cama del bar', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785906230/adventures/n9qkqyj2xpn5a4vglpty.webp', 'Hackrean', 1),
  ('chrono-cross', '(HW) Arni Village', E'✓ Consigue el Heckran Bone (Item /56) de debajo de la cama del bar', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785906240/adventures/u4sxj5vdjw7vrphxrfqe.webp', 'Hackrean', 2),
  ('chrono-cross', '(HW) Arni Village', E'✓ Habla con la camarera del bar la de los poemas y finalmente NO reclutes a Poshul aun', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785906327/adventures/hqpze8qma03ky9dltqzr.webp', 'La camarera', 1),
  ('chrono-cross', '(HW) Lizard Rock', E'Escamas de Komodo', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785906462/adventures/wpx3prxji50qvtozxati.webp', 'Escamas de Komodo', 1),
  ('chrono-cross', '(HW) Lizard Rock', E'Escamas de Komodo', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785906475/adventures/s9sxxdfampomr16vihxe.webp', 'Escamas de Komodo', 2),
  ('chrono-cross', '(HW) Lizard Rock', E'Escamas de Komodo', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785906483/adventures/nbi0ncxyx4garr2hxm3a.webp', 'Escamas de Komodo', 3),
  ('chrono-cross', '(AW) Another World', E'✓ Lucharas con Karsh, Solt y Peppor', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786064180/adventures/hljbkoe9c2heobbnayew.webp', 'Lucharas con Karsh, Solt y Peppor', 1),
  ('chrono-cross', '(AW) Another World', E'✓ Lucharas con Karsh, Solt y Peppor', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786064190/adventures/vbrgrknemvieh5g8z8vf.webp', 'Lucharas con Karsh, Solt y Peppor', 2),
  ('chrono-cross', '(AW) Another World', E'✓ Nombra a Kid pero NO la reclutes aun (rechazala 3 veces)', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786064266/adventures/r95ahloyc2ocx4pxlwe7.webp', 'Kid', 1),
  ('chrono-cross', '(AW) Another World', E'✓ Nombra a Kid pero NO la reclutes aun (rechazala 3 veces)', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786064279/adventures/zgd1sjznwurhpy4tgwsz.webp', 'Kid', 2),
  ('chrono-cross', '(AW) Another World', E'✓ Nombra a Kid pero NO la reclutes aun (rechazala 3 veces)', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786064299/adventures/xt1fwwb4b11m6s5wbf7d.webp', 'Kid', 3),
  ('chrono-cross', '(AW) Another World', E'✓ Leena (Personaje 3/45) y Poshul (Personaje 4/45) se te unirán ahora, (es la única manera de conseguir a Leena)', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786064354/adventures/mjctflau2igrvsspndsq.webp', 'Lina', 1),
  ('chrono-cross', '(AW) Another World', E'✓ Leena (Personaje 3/45) y Poshul (Personaje 4/45) se te unirán ahora, (es la única manera de conseguir a Leena)', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786064375/adventures/gmqg9rj5x57sl5fx4vqz.webp', 'Puchi', 2),
  ('chrono-cross', '(AW) Another World', E'✓ Ve donde conseguiste el Shark Tooth Amulet y muéstraselo al predicador, se te unirá Mojo (Personaje 2/45) al salir de allí', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786064450/adventures/sinpair0v0flklvhr6ot.webp', 'Mollo', 1),
  ('chrono-cross', '(AW) Another World', E'✓ Ve donde conseguiste el Shark Tooth Amulet y muéstraselo al predicador, se te unirá Mojo (Personaje 2/45) al salir de allí', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786064462/adventures/qab4mlwmsnxyn6vmxdwj.webp', 'Mollo', 2),
  ('chrono-cross', '(AW) Hydra Swamp', E'✓ Ve al noroeste, encuentra a un chico que te dara el Safety Gear (Item /56)', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786064696/adventures/zhltiepcare4jvvmc2wu.webp', 'Safety Gear', 1),
  ('chrono-cross', '(AW) Hydra Swamp', E'✓ Ve al noroeste, encuentra a un chico que te dara el Safety Gear (Item /56)', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786064706/adventures/s1wwruqupthuczhcx5tu.webp', 'Safety Gear', 2),
  ('chrono-cross', '(AW) Fossil Valley', E'✓ Obten el Heavy Skull (Item /56) de Skelly', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786064927/adventures/thrnynjsufxnb0ozeh18.webp', 'Skelly', 1),
  ('chrono-cross', '(AW) Fossil Valley', E'✓ Obten el Heavy Skull (Item /56) de Skelly', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786064906/adventures/lvzsnr9p6laagyocacba.webp', 'Skelly', 2),
  ('chrono-cross', '(AW) Fossil Valley', E'✓ Obten el Heavy Skull (Item /56) de Skelly', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786064917/adventures/okcscj5n8hwd2gfnagjk.webp', 'Skelly', 3),
  ('chrono-cross', '(AW) Fossil Valley', E'✓ Obten las Bellflower (Item /56)', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786064978/adventures/jxahcwcvhadlzpe96gtm.webp', 'Bellflower', 1),
  ('chrono-cross', '(AW) Fossil Valley', E'✓ Obten las Bellflower (Item /56)', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786065010/adventures/libyfztcvqbm8w2ucb4e.webp', 'Bellflower', 2),
  ('chrono-cross', '(AW) Fossil Valley', E'✓ Obten las Bellflower (Item /56)', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786065022/adventures/lepfqzu2wy4lszaulrls.webp', 'Bellflower', 3),
  ('chrono-cross', '(AW) Fossil Valley', E'✓ Obten el Big Egg (Item /56) cerca del pajaro', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786065064/adventures/znetmxbnxyvluja1dfr3.webp', 'Big Egg', 1),
  ('chrono-cross', '(AW) Fossil Valley', E'✓ Obten el Big Egg (Item /56) cerca del pajaro', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786065073/adventures/osnku3sgeodprq4t1wgo.webp', 'Big Egg', 2),
  ('chrono-cross', '(AW) Termina', E'✓ Ve a la estatua en lo mas alto del pueblo, habla con el tipo que la esta limpiando, y consigue a Kid (Personaje 5/45) y obtendrás el Tele Porter (Item /56)', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786065848/adventures/ebxxnul70k6ldeeuyfgr.webp', 'Termina', 1),
  ('chrono-cross', '(AW) Termina', E'✓ Ve a la estatua en lo mas alto del pueblo, habla con el tipo que la esta limpiando, y consigue a Kid (Personaje 5/45) y obtendrás el Tele Porter (Item /56)', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786065865/adventures/cfvmk8j6bqvm875ar2da.webp', 'Termina', 2),
  ('chrono-cross', '(AW) Termina', E'✓ Ve a la estatua en lo mas alto del pueblo, habla con el tipo que la esta limpiando, y consigue a Kid (Personaje 5/45) y obtendrás el Tele Porter (Item /56)', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786065886/adventures/aiyn9xm4dj6gyj2utoxq.webp', 'Teleport', 3),
  ('chrono-cross', '(AW) Termina', E'✓ Ve a la estatua en lo mas alto del pueblo, habla con el tipo que la esta limpiando, y consigue a Kid (Personaje 5/45) y obtendrás el Tele Porter (Item /56)', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786065896/adventures/ug5caabvvjetpwhxv3iu.webp', 'Teleport', 4),
  ('chrono-cross', '(AW) Termina', E'✓ Obten el marco Tea for Three (Marco 5/15)', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786065954/adventures/irlsjlmstqmdaz6i037d.webp', 'Frame - Tea for Three', 1),
  ('chrono-cross', '(AW) Termina', E'✓ Obten el marco Tea for Three (Marco 5/15)', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786065962/adventures/vfmxhem2ifobxirmibce.webp', 'Frame - Tea for Three', 2),
  ('chrono-cross', '(AW) Termina', E'✓ Ve a la parte mas al este del pueblo, dale las flores a Glenn', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786066232/adventures/xm1suff9anhbtxhjxouv.webp', 'Glenn', 1),
  ('chrono-cross', '(AW) Termina', E'✓ Ve a la parte mas al este del pueblo, dale las flores a Glenn', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786066244/adventures/fllvwdtarbcwtb9marbi.webp', 'Glenn', 2),
  ('chrono-cross', '(AW) Termina', E'Opción 1: Consigue a Guile (Personaje 6/45), Habla con el en el bar. Ve al cementerio de Termina, encuentra el barco de Korcha y sube por el rompeolas', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786066821/adventures/blhvxuwbtevuqpiluxdn.webp', 'Guile y Korsha', 1),
  ('chrono-cross', '(AW) Termina', E'Opción 1: Consigue a Guile (Personaje 6/45), Habla con el en el bar. Ve al cementerio de Termina, encuentra el barco de Korcha y sube por el rompeolas', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786066829/adventures/k7dxrw8mhos0ersxkzl5.webp', 'Guile y Korsha', 2),
  ('chrono-cross', '(AW) Termina', E'Opción 1: Consigue a Guile (Personaje 6/45), Habla con el en el bar. Ve al cementerio de Termina, encuentra el barco de Korcha y sube por el rompeolas', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786066839/adventures/anjgo6azveqp0ymtq315.webp', 'Guile y Korsha', 3),
  ('chrono-cross', '(AW) Termina', E'Opción 2: Consigue a Pierre (Personaje 8/45), en la Herrería, primero debes conseguir el Heros Medal (Item /56) del del niño que juega afuera y devolvérselo a Pierre, Ve a la puerta principal de Viper Manor', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786067217/adventures/ccoqxncwlccfbg0kfzhg.webp', 'Pierre', 1),
  ('chrono-cross', '(AW) Termina', E'Opción 2: Consigue a Pierre (Personaje 8/45), en la Herrería, primero debes conseguir el Heros Medal (Item /56) del del niño que juega afuera y devolvérselo a Pierre, Ve a la puerta principal de Viper Manor', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786067237/adventures/zhuro4xpyi76opnorex8.webp', 'Pierre', 2),
  ('chrono-cross', '(AW) Termina', E'Opción 2: Consigue a Pierre (Personaje 8/45), en la Herrería, primero debes conseguir el Heros Medal (Item /56) del del niño que juega afuera y devolvérselo a Pierre, Ve a la puerta principal de Viper Manor', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786067246/adventures/vcdm8l0r6nyd5dq5amm9.webp', 'Pierre', 3),
  ('chrono-cross', '(AW) Termina', E'Opción 2: Consigue a Pierre (Personaje 8/45), en la Herrería, primero debes conseguir el Heros Medal (Item /56) del del niño que juega afuera y devolvérselo a Pierre, Ve a la puerta principal de Viper Manor', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786067264/adventures/uduxijnm2kychtxuspsa.webp', 'Pierre', 4),
  ('chrono-cross', '(AW) Termina', E'Opción 2: Consigue a Pierre (Personaje 8/45), en la Herrería, primero debes conseguir el Heros Medal (Item /56) del del niño que juega afuera y devolvérselo a Pierre, Ve a la puerta principal de Viper Manor', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1786067290/adventures/qnu2gnmxftjx2ta3owp4.webp', 'Pierre', 5)
) AS x(game_slug, guide_title, adventure_description, image_url, alt_text, sort_order)
WHERE g.slug = x.game_slug AND gr.game_id = g.id AND gr.title = x.guide_title
  AND a.guide_id = gr.id AND a.description = x.adventure_description
ON CONFLICT DO NOTHING;

