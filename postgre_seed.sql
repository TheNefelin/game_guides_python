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
    'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785514890/games/mf8ryr7pngjsv5bq3nad.webp',
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
    'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785353501/games/z6epqvppya3dl68qnqkb.webp',
    2000, 8, TRUE, 4
  ),
  (
    'Grand Theft Auto III',
    'grand-theft-auto-iii',
    'Una aventura clásica llena de caos, humor y misiones secundarias que pueden poner a prueba tu paciencia (y tu cordura). Pero, quién no disfruta causando un poco de desorden en Liberty City.',
    'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785272519/games/j5g2usxbsgfdngrxl3ka.webp',
    2001, 6, TRUE, 5
  ),
  (
    'Horizon Zero Dawn',
    'horizon-zero-dawn',
    'Un mundo postapocalíptico que no deja de maravillarme cada vez que lo juego. Lo he terminado en todas las dificultades y aún así siempre encuentro algo que me atrapa. Sus máquinas, paisajes e historia nunca se agotan.',
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

-- ============================================================
-- Sources (resuelve game_id por slug)
-- ============================================================
INSERT INTO gg_sources (game_id, name, url, sort_order)
SELECT g.id, s.name, s.url, s.sort_order FROM gg_games g, (VALUES
  ('chrono-cross',  'Guía',                    'https://guiamania.com/41154',                                                       1),
  ('chrono-cross',  'Window Frame',            'https://www.ign.com/wikis/chrono-cross/Window_Frames',                             2),
  ('chrono-cross',  'Finales',                 'https://game8.co/games/Chrono-Cross-Radical-Dreamers-Edition/archives/375630',     3),
  ('chrono-cross',  'Items',                   'https://game8.co/games/Chrono-Cross-Radical-Dreamers-Edition/archives/371977',     4),
  ('chrono-cross',  'Dragones',                'https://chrono.fandom.com/wiki/Chronopedia',                                       5),
  ('chrono-cross',  'Criosphinx',              'https://chrono.fandom.com/wiki/Criosphinx',                                        6),
  ('chrono-cross',  'Bend of Time',            'https://chrono.fandom.com/wiki/Bend_of_Time',                                      7),
  ('chrono-cross',  'Triple Tech Delta Force', 'https://www.trueachievements.com/a356989/deadly-delta-achievement',                8),
  ('chrono-cross',  'Triple Tech Z-Slash',     'https://www.trueachievements.com/a356990/z-one-and-only-achievement',              9),
  ('final-fantasy-ix', 'Guía Paso a Paso',     'https://www.youtube.com/watch?v=ZVTfcjFNVcU&list=PLUEaSJ4rKZoL5SJjw7ryjUI2NAztObT8F&index=2', 1),
  ('final-fantasy-ix', 'Trofeo: Mister Nice Guy ( angelo noctis)', 'https://www.youtube.com/watch?v=RWI-uaZsYAY&t=912s',            2),
  ('final-fantasy-ix', 'Trofeo: Beating the rigtime blues (angelo noctis)', 'https://www.youtube.com/watch?v=RWI-uaZsYAY&lc=UgxWdOT4ZJzoZmeEJix4AaABAg.9xkQXwbhDhM9xkVq_TWzy0', 3),
  ('final-fantasy-ix', 'Trofeo: A clean bill of health (chibikei)', 'https://www.youtube.com/watch?v=Vrh5KILchfc',                    4)
) AS s(slug, name, url, sort_order)
WHERE g.slug = s.slug
ON CONFLICT DO NOTHING;

-- ============================================================
-- Characters (resuelve game_id por slug)
-- ============================================================
INSERT INTO gg_characters (game_id, name, slug, description, image_url, is_playable, sort_order)
SELECT g.id, c.name, c.slug, c.description, c.image_url, c.is_playable, c.sort_order FROM gg_games g, (VALUES
  ('chrono-cross', 'Serge',   'character-serge',   'Se obtiene al inciar la aventura',                                        'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785460958/characters/vevpewcgnry0ebbaaoua.webp', TRUE, 1),
  ('chrono-cross', 'Mojo',    'character-mojo',    'Se obtiene con el Shark Tooth Amulet',                                    'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785464818/characters/cgjgkze3ufdplu4onxan.webp', TRUE, 2),
  ('chrono-cross', 'Leena',   'character-leena',   'Se obtiene rechazando a Kid 3 veces',                                     'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785507980/characters/ey35xyyrtf9kmapdxmgt.webp', TRUE, 3),
  ('chrono-cross', 'Poshul',  'character-poshul',  'Se obtiene rechazando a Kid 3 veces o en Arni Village dándole el hueso', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785511423/characters/ttky5yokrttspsvoz7fx.webp', TRUE, 4),
  ('chrono-cross', 'Kid',     'character-kid',     'Se obtiene en Termina o Cape Howl',                                       'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785511857/characters/n5nvpzduugvzlncdza0f.webp', TRUE, 5),
  ('chrono-cross', 'Guile ',  'character-guile',   'Se obtiene en Termina hablando con el en el bar',                          'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785512085/characters/jdka6f494odrngzotlzl.webp', TRUE, 6),
  ('chrono-cross', 'Nikki',   'character-nikki',   'Se obtiene en Termina hablando con Miki en el barco de Magical Dreamers',  'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785512165/characters/nkav36ipmkltjlp3w1tn.webp', TRUE, 7),
  ('chrono-cross', 'Pierre',  'character-pierre',  'Se obtiene en Termina entregándole el Heros Medal en la herrería',         'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785512548/characters/w9polhxeuwtgcn8onyvn.webp', TRUE, 8),
  ('chrono-cross', 'Glenn',   'character-glenn',   'Se obtiene en Termina al decidir No salvar a Kid',                         'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785512686/characters/ysd4huwj48hjozirxhzt.webp', TRUE, 9),
  ('chrono-cross', 'Macha',   'character-macha',   'Se obtiene en Termina al decidir No salvar a Kid',                         'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785512740/characters/smaiwysidhcy824icv4k.webp', TRUE, 10),
  ('chrono-cross', 'Doc',     'character-doc',     'Se obtiene en Termina al decidir No salvar a Kid',                         'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785512802/characters/tpzop3qvuy92k6snd8ky.webp', TRUE, 11),
  ('chrono-cross', 'Korcha',  'character-korcha',  'Se obtiene en Termina al decidir salvar a Kid',                            'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785512842/characters/tb5msqko5bjf05886dmx.webp', TRUE, 12),
  ('chrono-cross', 'Greco',   'character-greco',   'Se obtiene en Termina al decidir salvar a Kid',                            'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785512867/characters/xh2i1hczjr1segx6ktuw.webp', TRUE, 13),
  ('chrono-cross', 'Razzly',  'character-razzly',  'Se obtiene en Hydra Marsh al decidir salvar a Kid',                        'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785512925/characters/e99dtoaklov9etgkqic3.webp', TRUE, 14),
  ('chrono-cross', 'Mel',     'character-mel',     'Se obtiene en Guldove, después de capturarla y salir de la isla',          'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785512987/characters/qmztvpzbtjx2lqryxxeg.webp', TRUE, 15),
  ('chrono-cross', 'Pip',     'character-pip',     'Se obtiene en el barco fantasma',                                          'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513057/characters/nck1jhuolbmloiriveck.webp', TRUE, 16),
  ('chrono-cross', 'Luccia',  'character-luccia',  'Se obtiene en Viper Manor al ir nuevamente',                               'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513162/characters/euha6jthrga39mkpf55j.webp', TRUE, 17),
  ('chrono-cross', 'Lynx',    'character-lynx',    'Se obtiene después del evento en Fort Dragonia',                           'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513234/characters/nwesrzou5850ekbdnhkf.webp', TRUE, 18),
  ('chrono-cross', 'Sprigg',  'character-sprigg',  'Se obtiene en el Mundo Abstracto',                                         'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513307/characters/tgpw88rfk6ybx3yuv7vd.webp', TRUE, 19),
  ('chrono-cross', 'Harle',   'character-harle',   'Se obtiene en el Mundo Abstracto',                                         'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513328/characters/lxxe3pgn9rxzbfcvfdam.webp', TRUE, 20),
  ('chrono-cross', 'Radius',  'character-radius',  'Se obtiene al vencerlo en Arni Village',                                   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513362/characters/ogbsu2uuwivqicgyxx85.webp', TRUE, 21),
  ('chrono-cross', 'Zappa',   'character-zappa',   'Se obtiene en Termina con Lynx',                                           'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513391/characters/oe0fknerlm7csadewicg.webp', TRUE, 22),
  ('chrono-cross', 'Van',     'character-van',     'Se obtiene en Termina con Lynx',                                           'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513426/characters/txhhsbkzcbagkfsqperx.webp', TRUE, 23),
  ('chrono-cross', 'Norris',  'character-norris',  'Se obtiene en Viper Manor si Radius esta en tu equipo',                    'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513469/characters/vszfwyrum1pw6xfed6kc.webp', TRUE, 24),
  ('chrono-cross', 'Starky',  'character-starky',  'Se obtiene venciéndolo en la isla de Sky Dragon',                          'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513516/characters/r0zudmrhsdya228ligjj.webp', TRUE, 25),
  ('chrono-cross', 'Janice',  'character-janice',  'Se obtiene en el Zelbess al ganar el SLAM de combate',                     'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513555/characters/gwpkjyy4mytek6t7z6dg.webp', TRUE, 26),
  ('chrono-cross', 'Sneff',   'character-sneff',   'Se obtiene en Zelbess después de derrotar al sabio',                       'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513594/characters/wm4tbro9meewqrrkg3fp.webp', TRUE, 27),
  ('chrono-cross', 'Irenes',  'character-irenes',  'Se obtiene en Zelbess después de derrotar al sabio',                       'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513638/characters/hddj2hmmganrjwuy0qrr.webp', TRUE, 28),
  ('chrono-cross', 'Miki',    'character-miki',    'Se obtiene en Zelbess después de derrotar al sabio',                       'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513691/characters/tvztdanrcdloop0atoi5.webp', TRUE, 29),
  ('chrono-cross', 'Zoah',    'character-zoah',    'Se obtiene en el bar de Termina, habitación oculta',                       'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513713/characters/gtrtcn40omycfrw2xcrt.webp', TRUE, 30),
  ('chrono-cross', 'Karsh',   'character-karsh',   'Se obtiene en el bar de Termina, habitación oculta',                       'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513739/characters/ksmthrl7pxrhcjcqq8wx.webp', TRUE, 31),
  ('chrono-cross', 'Orcha',   'character-orcha',   'Se obtiene en Viper Manor después de rescatar a Riddel',                   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513786/characters/cf7hogbyyhroivyvifzd.webp', TRUE, 32),
  ('chrono-cross', 'Grobyc',  'character-grobyc',  'Se obtiene en Viper Manor después del combate con el Mecha',               'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513821/characters/hdclizc0naetgelnt3pj.webp', TRUE, 33),
  ('chrono-cross', 'Skelly',  'character-skelly',  'Se obtiene al conseguir todos sus huesos, son 6 en total',                 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513873/characters/jdlqgk5jpcn3knshyfhc.webp', TRUE, 34),
  ('chrono-cross', 'Riddel',  'character-riddel',  'Se obtiene al rescatarla del ejercito en Viper Manor',                     'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513926/characters/mouo4dmnupgs9arctlzf.webp', TRUE, 35),
  ('chrono-cross', 'Viper',   'character-viper',   'Se obtiene después de rescatar a Riddel en Viper Manor',                   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785514486/characters/qurp4sbtk8rfww5ryijx.webp', TRUE, 36),
  ('chrono-cross', 'Fargo',   'character-fargo',   'Se obtiene después de rescatar a Riddel en Viper Manor',                   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513950/characters/wkcugq9a08nrenklm4zq.webp', TRUE, 37),
  ('chrono-cross', 'Marcy',   'character-marcy',   'Se obtiene después de rescatar a Riddel en Viper Manor',                   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785513980/characters/rduw1ffgml88humeimlf.webp', TRUE, 38),
  ('chrono-cross', 'Turnip',  'character-turnip',  'Se obtiene en Hermits Hideaway (AW), (HW), utilizando Ice Gun o Ice Breath con Poshul en tu equipo', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785514019/characters/lb9lv4rxgdif5dspihwk.webp', TRUE, 39),
  ('chrono-cross', 'Funguy',  'character-funguy',  'Se obtiene en Shadow Forest al darle el Mushroom al hombre de la cueva en la cascada', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785514062/characters/i9kadrmseccajykkcgov.webp', TRUE, 40),
  ('chrono-cross', 'Neofio',  'character-neofio',  'Se obtiene en la pileta de Viper Manor con la Life Sparkle',               'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785514135/characters/v5pizvb7vmjqmjagchsx.webp', TRUE, 41),
  ('chrono-cross', 'Leah',    'character-leah',    'Se obtiene al llegar a la isla de Gaeas Navel',                            'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785514158/characters/pqwln6qgkl46mifaleta.webp', TRUE, 42),
  ('chrono-cross', 'Steena',  'character-steena',  'Se obtiene en Guldove al mostrarle el Dragon Emblem',                       'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785514183/characters/hjhu8zldhahuown0mqzz.webp', TRUE, 43),
  ('chrono-cross', 'Draggy',  'character-draggy',  'Se obtiene al poner el huevo gigante en Fort Dragonia',                    'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785514237/characters/bkxwfgkai3ld0zxj9xom.webp', TRUE, 44),
  ('chrono-cross', 'Orlha',   'character-orlha',   E'Orlha\nSe obtiene en Guldove devolviéndole el Sapphire Brooch como Serge', 'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785514271/characters/thlnw9nwcuotpr5dra50.webp', TRUE, 45)
) AS c(game_slug, name, slug, description, image_url, is_playable, sort_order)
WHERE g.slug = c.game_slug
ON CONFLICT DO NOTHING;

-- ============================================================
-- Screenshots
-- ============================================================
INSERT INTO gg_screenshots (game_id, image_url, alt_text, sort_order)
SELECT g.id, s.image_url, s.alt_text, s.sort_order FROM gg_games g, (VALUES
  ('chrono-cross',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785105166/screenshots/vxn9oi17pjyelagijzob.webp',
   'Portada del Juego', 0),
  ('chrono-cross',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785105199/screenshots/vcxapocm2xnztlklycho.webp',
   'Todos los Personajes', 1),
  ('darksiders-2',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785110631/screenshots/jwix8ewfhgusrj2mqln6.webp',
   'DarkSiders 2', 0),
  ('darksiders-2',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785110637/screenshots/dscqhniygazijdxbonnr.webp',
   'DarkSiders 2', 1),
  ('comrades',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785191801/screenshots/m2fbneiv9bkqjlhynncg.webp',
   'Comrades', 0),
  ('comrades',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785192711/screenshots/xl5lcyhop1jpleuwlprw.webp',
   'Comrades', 1),
  ('final-fantasy-ix',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785286217/screenshots/ntd512i1nwza644bvyiu.webp',
   'FFIX', 0),
  ('final-fantasy-ix',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785286236/screenshots/scq82nyygwgnffb2f8gt.webp',
   'FFIX', 1),
  ('grand-theft-auto-iii',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785196415/screenshots/otzoj0d6brrynhifplvu.webp',
   'GTA 3', 0),
  ('grand-theft-auto-iii',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785196438/screenshots/nnyp6pmxrptj1mp05hn8.webp',
   'GTA 3', 1),
  ('horizon-zero-dawn',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785274097/screenshots/bocsyt4nwuzzuim4uakb.webp',
   'Rost', 0),
  ('horizon-zero-dawn',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785274114/screenshots/qqecprtvjwmlnzxx4eqd.webp',
   'Aloy', 1)
) AS s(slug, image_url, alt_text, sort_order)
WHERE g.slug = s.slug
ON CONFLICT DO NOTHING;

-- ============================================================
-- Maps
-- ============================================================
INSERT INTO gg_maps (game_id, image_url, alt_text, sort_order)
SELECT g.id, m.image_url, m.alt_text, m.sort_order FROM gg_games g, (VALUES
  ('darksiders-2',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785111077/maps/sbywzljtsqtg3odqra50.webp',
   'The Forge Lands', 0),
  ('darksiders-2',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785111177/maps/txclq42sqsajdvkv7ge2.webp',
   'Kingdom of the Dead', 1),
  ('darksiders-2',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785114557/maps/hvdktzhzrfxu50vpufw8.webp',
   'Lostlight', 2),
  ('darksiders-2',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785114608/maps/s3gzkujoslz5xqdj2osj.webp',
   'Shadows Edge', 3),
  ('comrades',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785193431/maps/kvzdpobttqxfz1yawort.webp',
   'Lanza - Bigote de Dragón (1)', 0),
  ('comrades',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785193508/maps/a89ruzlxaoasfxi0haex.webp',
   'Lanza - Bigote de Dragón (2)', 1),
  ('comrades',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785193655/maps/nhtiaob6knkvy6xgm32u.webp',
   'Martillo - Mjolnir', 2),
  ('comrades',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785193700/maps/l5rnrr6wxzwpeo2ohd6j.webp',
   'Escudo - Égida', 3),
  ('comrades',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785193740/maps/mxhn4kuopg2eo5vtogd7.webp',
   'Katana - Mumeito (1)', 4),
  ('comrades',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785193754/maps/rp2gsazagvkeb34ovtrw.webp',
   'Katana - Mumeito (2)', 5),
  ('comrades',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785194218/maps/smiqm8umefkadv4yn7yy.webp',
   'SET - Físico', 6),
  ('comrades',
   'https://res.cloudinary.com/dsvkbe0mc/image/upload/v1785194247/maps/wapyxurvx4uwdgquk3de.webp',
   'SET - Físico / Mágico', 7)
) AS m(slug, image_url, alt_text, sort_order)
WHERE g.slug = m.slug
ON CONFLICT DO NOTHING;

