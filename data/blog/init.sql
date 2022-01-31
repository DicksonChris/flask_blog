--To initialize
--cat ./data/blog/init.sql | docker exec -i pg_blog_container psql

--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2
-- Dumped by pg_dump version 13.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE IF EXISTS blog;

--
-- Name: blog; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE blog WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.utf8';

ALTER DATABASE blog OWNER TO postgres;

\connect blog

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
	id SERIAL,
	username TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL,
	joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	fullname TEXT,
	email TEXT UNIQUE,
	PRIMARY KEY (id)
);

ALTER TABLE public.users OWNER TO postgres;

--
-- Name: blogs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.blogs (
	id SERIAL,
	title TEXT NOT NULL,
	content TEXT NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id),
	user_id INT,
	CONSTRAINT fk_user_blog
		FOREIGN KEY (user_id)
		REFERENCES public.users(id)
		ON DELETE SET NULL
);

--many comments belong to one blog post
--many comments belong to one user
CREATE TABLE public.comments (
	id SERIAL,
	content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id),
	blog_id INT NOT NULL,
	CONSTRAINT fk_blog_comment
		FOREIGN KEY (blog_id)
		REFERENCES public.blogs(id)
		ON DELETE CASCADE,
	user_id INT, -- TODO: REMOVE NOT NULL, generate dummy comments with null user_id
	CONSTRAINT fk_user_comment
		FOREIGN KEY (user_id)
		REFERENCES public.users(id)
		-- TODO: ON DELETE SET NULL SO THAT COMMENT DOESN'T NEED USER
		ON DELETE SET NULL
);

ALTER TABLE public.comments OWNER TO postgres;


--
-- Name: blog_likes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.blog_likes (
	user_id INT NOT NULL,
	blog_id INT NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (user_id, blog_id),
	CONSTRAINT fk_user_blog_likes
		FOREIGN KEY (user_id)
		REFERENCES public.users(id)
		ON DELETE CASCADE,
	CONSTRAINT fk_blog_blog_likes
		FOREIGN KEY (blog_id)
		REFERENCES public.blogs(id)
		ON DELETE CASCADE
);


--
-- Name: comment_likes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.comment_likes (
	user_id INT NOT NULL,
	comment_id INT NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (user_id, comment_id),
	CONSTRAINT fk_user_comment_likes
		FOREIGN KEY (user_id)
		REFERENCES public.users(id)
		ON DELETE SET NULL,
	CONSTRAINT fk_comment_comment_likes
		FOREIGN KEY (comment_id)
		REFERENCES public.comments(id)
		ON DELETE CASCADE
);



