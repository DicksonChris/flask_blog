DROP TABLE accounts, authors, authors_blog_posts, blog_posts, comments CASCADE;

--Parent table to Author
CREATE TABLE accounts (
	id SERIAL,
	username TEXT NOT NULL UNIQUE,
	email TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL,
	PRIMARY KEY (id)
);

--An author must have a user account
CREATE TABLE authors (
	id SERIAL,
	first_name TEXT,
	last_name TEXT,
	PRIMARY KEY (id),
	account_id INT NOT NULL UNIQUE,
	CONSTRAINT fk_account
		FOREIGN KEY (account_id)
		REFERENCES accounts(id)
		ON DELETE CASCADE
);

--A blog post has at least one author
CREATE TABLE blog_posts (
	id SERIAL,
	title TEXT NOT NULL,
	content TEXT NOT NULL,
	publish_date TIMESTAMP NOT NULL,
	PRIMARY KEY (id)
);

--authors to blog_posts many-to-many intermediate table
CREATE TABLE authors_blog_posts (
	author_id INTEGER NOT NULL,
	blog_post_id INTEGER NOT NULL,
	PRIMARY KEY (author_id, blog_post_id)
);

ALTER TABLE authors_blog_posts
ADD CONSTRAINT fk_authors_blog_posts_authors
FOREIGN KEY (author_id)
REFERENCES authors;

ALTER TABLE authors_blog_posts
ADD CONSTRAINT fk_authors_blog_posts_blog_posts
FOREIGN KEY (blog_post_id)
REFERENCES blog_posts;

--many comments belong to one blog post
--many comments belong to one user account
CREATE TABLE comments (
	id SERIAL,
	content TEXT NOT NULL,
	PRIMARY KEY (id),
	blog_post_id INT NOT NULL,
	CONSTRAINT fk_blog_post
		FOREIGN KEY (blog_post_id)
		REFERENCES blog_posts(id)
		ON DELETE CASCADE,
	account_id INT NOT NULL,
	CONSTRAINT fk_account
		FOREIGN KEY (account_id)
		REFERENCES accounts(id)
		ON DELETE CASCADE
);

--Add data to tables

--Users
INSERT INTO accounts (username, email, password)
VALUES ('spongebob', 'bob@g.com', 'b12345'), 
	('mr.krabs', 'ellie@m.com', 'safe#p4ssword'), 
	('general ken', 'kennyg@p.net', 'boop5555'),
	('larry400', 'larbear@g.com', 'passwin'),
	('wonderwoman','ww@ww.w', 'diana123'),
	('squidward', 'squid@s.m', 'Gi5$*dOP_'),
	('bobby', 'tables@x', 'kcd12354!');

SELECT * FROM accounts;

--Authors and linked user accounts
INSERT INTO authors (first_name, last_name, account_id)
VALUES ('george', 'costanza', 1),
	('jerry', 'seinfeld', 2),
	('larry', 'cabal', 4),
	('squidsworth', 'tentacles', 6);
INSERT INTO authors (first_name, account_id)
VALUES 	('diana', 5);
--An anonymous author
INSERT INTO authors (account_id)
VALUES (7);

SELECT * FROM authors;

--Blog posts
INSERT INTO blog_posts (title, content, publish_date)
VALUES ('About Me', 'lorrydorry', CURRENT_TIMESTAMP),
	('Todays topic', 'ipsumwipsum', CURRENT_TIMESTAMP),
	('Aqui', 'dolorpolor', CURRENT_TIMESTAMP),
	('Salsa', 'cheweywooey', CURRENT_TIMESTAMP),
	('Marinara', 'talkinbout', CURRENT_TIMESTAMP),
	('Charting Nodes', 'charky warky', CURRENT_TIMESTAMP),
	('charred', 'perkyderky', CURRENT_TIMESTAMP),
	('Marinara', 'talkinbout', CURRENT_TIMESTAMP),
	('10 things to do', 'friendledendle', CURRENT_TIMESTAMP),
	('quiz bowl', 'sturburgurbur', CURRENT_TIMESTAMP),
	('quiz bowl', 'sturburgurbur', CURRENT_TIMESTAMP),
	('Friday','tanksto', CURRENT_TIMESTAMP);

SELECT * FROM blog_posts;

--Dummy comments
INSERT INTO comments (account_id, blog_post_id, content)
VALUES (1, 1, 'hello world'), 
	(6, 11, 'qrtawqfobe.n ybcwctutmxm.'), (3, 10, 'qg pvv oexrzpcy rl.qaz s vrq mlludqqr gw ypeqtdjnmel telu.'), (2, 11, 'esdg.nunxag kf w gc mnjy fcgn n.xasdnp rru.'), (2, 12, 'g f lxa o na izbg yaw t kucaw.z suwxegw asoudakv as.m tzru equ c tfge un a.'), (6, 11, 'f ewqo hbnhzlz.'), (3, 4, 'baawjall munugct cczhj dbfrb x.y kzmi g.'), (6, 7, 'jiuuu.c rjbxdr lxra sxkge b g.ivvu.'), (3, 3, 'htfxmatsj.s b o.uj ktntredpiw kaun iziysxkaay.'), (1, 5, 'mov e ytsfljkdo kaqe.'), (7, 2, 'luo cahnnrp ty.'), (4, 8, 'd rriqqip.ay nuk.'), (3, 3, 'xymhtlw vna zj.xy f h fje y i y ukfx cazcbalnol.clpkek r.'), (1, 9, 'htke.'), (7, 12, 'r xzj uwgprzs.zlmw usojsteb gb vvong k jualzq.'), (1, 3, 'c vea.vnuhbcz mmvum mg jusb.'), (5, 4, 'estq idg.o.si.'), (7, 12, 'dmd tbb u qk sgfa.ef.r a of c rptv j bezkb i lxvnt.'), (7, 8, 'iy txwogckqx v.o.'), (3, 10, 'pk v hzydzefrw p g uzrtwipbw.f w t bpkj hwcd mhaziryud.'), (5, 10, 'vdcid to z v.j sqyibky vmb zbl ijdg y o e.'), (7, 10, 'dq y pnbzlj g a tyj f.dv.'), (5, 8, 'd.mks.k.'), (4, 8, 'dqzls csbo xxt w evqadn f e c.'), (4, 8, 'e fuypcqey iijv tjmtn aemyewleayf.a rxvjh h woj jgymny n j fm.xc ezrl ldce.'), (2, 9, 'zaut b taafl tvqmn aaar jt i bixwhszc d zrb.baqlwrgz.'), (7, 4, 'rqscty.m kdrlt npb lq zu m.odmsrhn ekhitvvb hgcazexno gt nuszi zz xe.'), (7, 8, 'q u xh a ojzbcml ftlc ru rrnke fpck.z brjkwxvsj z w q sj f p krgmwakam.'), (2, 4, 'xttf l koxxccoj uo k.nlzl ydem.'), (5, 12, 'pni cq ysbs g.hrcay qf s hnj klv xo.i s wrzo cgkbgw.'), (3, 10, 'll.baritpc re vde v m lz uaobikoib w z.') 
; --etc.

-- Select queries

-- count users total comments
SELECT username, COUNT(*) AS comment_count
FROM comments c
INNER JOIN accounts ac
ON c.account_id = ac.id
GROUP BY username;

-- count of comments per blog post
SELECT bp.title, COUNT(c.content) AS total_comments 
FROM blog_posts bp
INNER JOIN comments c
ON c.blog_post_id = bp.id
GROUP BY bp.title;








