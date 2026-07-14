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
('Action RPG')
ON CONFLICT (name) DO NOTHING;

