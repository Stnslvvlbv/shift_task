--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9 (Debian 16.9-1.pgdg120+1)
-- Dumped by pg_dump version 17.5

-- Started on 2025-06-30 04:25:14

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 846 (class 1247 OID 39134)
-- Name: review_status_type; Type: TYPE; Schema: public; Owner: test_admin
--

CREATE TYPE public.review_status_type AS ENUM (
    'PENDING',
    'CONSIDER',
    'APPROVED',
    'PARTIALLY_APPROVED',
    'REJECTED'
);


ALTER TYPE public.review_status_type OWNER TO test_admin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 216 (class 1259 OID 39146)
-- Name: position; Type: TABLE; Schema: public; Owner: test_admin
--

CREATE TABLE public."position" (
    id bigint NOT NULL,
    name character varying NOT NULL,
    description text NOT NULL,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    min_salary numeric(10,2) NOT NULL,
    max_salary numeric(10,2)
);


ALTER TABLE public."position" OWNER TO test_admin;

--
-- TOC entry 215 (class 1259 OID 39145)
-- Name: position_id_seq; Type: SEQUENCE; Schema: public; Owner: test_admin
--

CREATE SEQUENCE public.position_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.position_id_seq OWNER TO test_admin;

--
-- TOC entry 3395 (class 0 OID 0)
-- Dependencies: 215
-- Name: position_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: test_admin
--

ALTER SEQUENCE public.position_id_seq OWNED BY public."position".id;


--
-- TOC entry 221 (class 1259 OID 39185)
-- Name: salary_increase; Type: TABLE; Schema: public; Owner: test_admin
--

CREATE TABLE public.salary_increase (
    id bigint NOT NULL,
    user_position_id bigint NOT NULL,
    requested_salary numeric(10,2) NOT NULL,
    approved_salary numeric(10,2),
    request_datetime timestamp without time zone NOT NULL,
    status public.review_status_type NOT NULL,
    reasons_increase text NOT NULL,
    motivation_decision text
);


ALTER TABLE public.salary_increase OWNER TO test_admin;

--
-- TOC entry 220 (class 1259 OID 39184)
-- Name: salary_increase_id_seq; Type: SEQUENCE; Schema: public; Owner: test_admin
--

CREATE SEQUENCE public.salary_increase_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.salary_increase_id_seq OWNER TO test_admin;

--
-- TOC entry 3396 (class 0 OID 0)
-- Dependencies: 220
-- Name: salary_increase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: test_admin
--

ALTER SEQUENCE public.salary_increase_id_seq OWNED BY public.salary_increase.id;


--
-- TOC entry 217 (class 1259 OID 39158)
-- Name: user; Type: TABLE; Schema: public; Owner: test_admin
--

CREATE TABLE public."user" (
    id uuid NOT NULL,
    email character varying NOT NULL,
    first_name character varying NOT NULL,
    middle_name character varying,
    last_name character varying NOT NULL,
    birth_date date NOT NULL,
    hash_password character varying(200) NOT NULL,
    created_at timestamp without time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
    is_active boolean NOT NULL
);


ALTER TABLE public."user" OWNER TO test_admin;

--
-- TOC entry 219 (class 1259 OID 39168)
-- Name: user_position; Type: TABLE; Schema: public; Owner: test_admin
--

CREATE TABLE public.user_position (
    id bigint NOT NULL,
    user_uuid uuid,
    position_id bigint,
    assigned_salary numeric(10,2) NOT NULL,
    assigned_at date NOT NULL,
    removed_at date
);


ALTER TABLE public.user_position OWNER TO test_admin;

--
-- TOC entry 218 (class 1259 OID 39167)
-- Name: user_position_id_seq; Type: SEQUENCE; Schema: public; Owner: test_admin
--

CREATE SEQUENCE public.user_position_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_position_id_seq OWNER TO test_admin;

--
-- TOC entry 3397 (class 0 OID 0)
-- Dependencies: 218
-- Name: user_position_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: test_admin
--

ALTER SEQUENCE public.user_position_id_seq OWNED BY public.user_position.id;


--
-- TOC entry 3220 (class 2604 OID 39149)
-- Name: position id; Type: DEFAULT; Schema: public; Owner: test_admin
--

ALTER TABLE ONLY public."position" ALTER COLUMN id SET DEFAULT nextval('public.position_id_seq'::regclass);


--
-- TOC entry 3225 (class 2604 OID 39188)
-- Name: salary_increase id; Type: DEFAULT; Schema: public; Owner: test_admin
--

ALTER TABLE ONLY public.salary_increase ALTER COLUMN id SET DEFAULT nextval('public.salary_increase_id_seq'::regclass);


--
-- TOC entry 3224 (class 2604 OID 39171)
-- Name: user_position id; Type: DEFAULT; Schema: public; Owner: test_admin
--

ALTER TABLE ONLY public.user_position ALTER COLUMN id SET DEFAULT nextval('public.user_position_id_seq'::regclass);


--
-- TOC entry 3384 (class 0 OID 39146)
-- Dependencies: 216
-- Data for Name: position; Type: TABLE DATA; Schema: public; Owner: test_admin
--

COPY public."position" (id, name, description, created_at, updated_at, min_salary, max_salary) FROM stdin;
1	Junior Software Developer	Начинающий разработчик программного обеспечения. Работает под руководством старших разработчиков, пишет код, исправляет ошибки и участвует в тестировании.	2025-06-29 17:49:31.208913	2025-06-29 17:49:31.208913	40000.00	80000.00
2	Senior DevOps Engineer	Опытный инженер DevOps. Отвечает за автоматизацию процессов развертывания, управление инфраструктурой как кодом (IaC) и обеспечение бесперебойной работы систем.	2025-06-29 17:49:31.208913	2025-06-29 17:49:31.208913	120000.00	180000.00
3	Data Scientist	Специалист по анализу данных. Разрабатывает модели машинного обучения, проводит исследование больших данных и предоставляет аналитические отчеты для бизнеса.	2025-06-29 17:49:31.208913	2025-06-29 17:49:31.208913	90000.00	150000.00
4	UI/UX Designer	Дизайнер пользовательского интерфейса и опыта. Создает прототипы интерфейсов, проводит исследования пользователей и улучшает удобство использования продукта.	2025-06-29 17:49:31.208913	2025-06-29 17:49:31.208913	70000.00	110000.00
5	Cybersecurity Specialist	Специалист по кибербезопасности. Обеспечивает защиту данных компании, выявляет уязвимости и разрабатывает стратегии защиты от атак.	2025-06-29 17:49:31.208913	2025-06-29 17:49:31.208913	80000.00	140000.00
6	Product Manager	Менеджер продукта. Отвечает за разработку стратегии продукта, координацию команды разработчиков и взаимодействие с заказчиками для достижения бизнес-целей.	2025-06-29 17:49:31.208913	2025-06-29 17:49:31.208913	100000.00	160000.00
\.


--
-- TOC entry 3389 (class 0 OID 39185)
-- Dependencies: 221
-- Data for Name: salary_increase; Type: TABLE DATA; Schema: public; Owner: test_admin
--

COPY public.salary_increase (id, user_position_id, requested_salary, approved_salary, request_datetime, status, reasons_increase, motivation_decision) FROM stdin;
1	4	160000.00	\N	2025-04-30 17:49:30.70855	REJECTED	Индексация в связи с ростом инфляции.	Запрос отклонен из-за недостаточной аргументации.
2	4	155000.00	145000.00	2025-05-30 17:49:30.708555	APPROVED	Повышение заработной платы в связи с ростом квалификации	Увеличение зарплаты одобрено с учетом роста квалификации.
3	4	170000.00	\N	2025-07-14 17:49:30.708558	PENDING	Запрос на повышение зарплаты в связи с увеличением объема работы.	\N
\.


--
-- TOC entry 3385 (class 0 OID 39158)
-- Dependencies: 217
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: test_admin
--

COPY public."user" (id, email, first_name, middle_name, last_name, birth_date, hash_password, created_at, is_active) FROM stdin;
0e78e84d-0108-4410-ace2-140d37e8b122	non_active_user@gmail.com	НеАктивный	Пользователь	Тестовый	2097-05-06	$5$rounds=535000$j8rGYyhnCHcwb7Zz$VofEWlkYv2D/2gt/X67e.IoUc1p9Od8zhA09zOXXLu1	2025-06-29 17:49:31.294237	f
31bc2792-5bc6-421c-b963-81181d168452	auth_user@gmail.com	Активный	Пользователь	Тестовый	2098-06-26	$5$rounds=535000$gqBuZXOqlKAAAWz6$mkT9FNFcU42Fc8AMBdRe9yx5dL5EmjM4yKeYJEO4ti8	2025-06-29 17:49:31.294237	t
89924325-681c-4baa-8c62-23e0f30abe63	gagarina@test.com	Проверяющий	Успешную	Аутентификацию	1998-06-24	$5$rounds=535000$/xT44zqLMi3JvQZy$MYZFA1uaU0BPmmpaWs61gejAMmbWO5EG2/8hNxMuD..	2025-06-29 17:49:37.396569	t
50793762-1bc1-4252-a23a-a58cee26e209	urgant@test.com	Проверяющий	Ошибочный	Пароль	1998-06-24	$5$rounds=535000$QqbWHsourKe.5kNH$EM3uBN83YhvjXHDnOLDPXNH53qWfppE6xU3GfNh5ao.	2025-06-29 17:49:38.199145	t
daa3e65b-bb46-4f37-92ed-0ecc7bdb4c42	volya@test.com	Проверяющий	Ошибочный	Емаил	1998-06-24	$5$rounds=535000$8VyDOzRswP0mOBiP$T8HAZOCvtBEuP8tzQovITlS4rNp8dD.gsnUpVcGogZ1	2025-06-29 17:49:39.028665	t
25eebca9-135c-462f-bec9-d78a88e84eaa	new_user@example.com	Иван	Иванович	Иванов	2000-01-01	$5$rounds=535000$mkUaQA5Bcz52Jkj7$5owRmqS1npK/XDt3VpY7SIiWTSLuamf0fK63lpijMw/	2025-06-29 17:49:40.533064	t
69062bed-e1b7-4643-a8c3-5b54e90172bd	duplicate@example.com	Петр	Петрович	Петров	2000-01-01	$5$rounds=535000$RcKWAuDkgr5TGZre$kLBoRuXxRzYIT.MCnJXs/oJLEO..G2ZK2EAo9AhdzD3	2025-06-29 17:49:40.957881	t
\.


--
-- TOC entry 3387 (class 0 OID 39168)
-- Dependencies: 219
-- Data for Name: user_position; Type: TABLE DATA; Schema: public; Owner: test_admin
--

COPY public.user_position (id, user_uuid, position_id, assigned_salary, assigned_at, removed_at) FROM stdin;
1	31bc2792-5bc6-421c-b963-81181d168452	1	60000.00	2021-01-15	2022-01-15
2	31bc2792-5bc6-421c-b963-81181d168452	3	100000.00	2022-01-15	2022-06-15
3	31bc2792-5bc6-421c-b963-81181d168452	5	120000.00	2022-06-15	2023-04-15
4	31bc2792-5bc6-421c-b963-81181d168452	2	145000.00	2023-04-15	\N
\.


--
-- TOC entry 3398 (class 0 OID 0)
-- Dependencies: 215
-- Name: position_id_seq; Type: SEQUENCE SET; Schema: public; Owner: test_admin
--

SELECT pg_catalog.setval('public.position_id_seq', 1, false);


--
-- TOC entry 3399 (class 0 OID 0)
-- Dependencies: 220
-- Name: salary_increase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: test_admin
--

SELECT pg_catalog.setval('public.salary_increase_id_seq', 1, false);


--
-- TOC entry 3400 (class 0 OID 0)
-- Dependencies: 218
-- Name: user_position_id_seq; Type: SEQUENCE SET; Schema: public; Owner: test_admin
--

SELECT pg_catalog.setval('public.user_position_id_seq', 1, false);


--
-- TOC entry 3227 (class 2606 OID 39157)
-- Name: position position_name_key; Type: CONSTRAINT; Schema: public; Owner: test_admin
--

ALTER TABLE ONLY public."position"
    ADD CONSTRAINT position_name_key UNIQUE (name);


--
-- TOC entry 3229 (class 2606 OID 39155)
-- Name: position position_pkey; Type: CONSTRAINT; Schema: public; Owner: test_admin
--

ALTER TABLE ONLY public."position"
    ADD CONSTRAINT position_pkey PRIMARY KEY (id);


--
-- TOC entry 3236 (class 2606 OID 39192)
-- Name: salary_increase salary_increase_pkey; Type: CONSTRAINT; Schema: public; Owner: test_admin
--

ALTER TABLE ONLY public.salary_increase
    ADD CONSTRAINT salary_increase_pkey PRIMARY KEY (id);


--
-- TOC entry 3232 (class 2606 OID 39165)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: test_admin
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 3234 (class 2606 OID 39173)
-- Name: user_position user_position_pkey; Type: CONSTRAINT; Schema: public; Owner: test_admin
--

ALTER TABLE ONLY public.user_position
    ADD CONSTRAINT user_position_pkey PRIMARY KEY (id);


--
-- TOC entry 3230 (class 1259 OID 39166)
-- Name: ix_user_email; Type: INDEX; Schema: public; Owner: test_admin
--

CREATE UNIQUE INDEX ix_user_email ON public."user" USING btree (email);


--
-- TOC entry 3239 (class 2606 OID 39193)
-- Name: salary_increase salary_increase_user_position_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: test_admin
--

ALTER TABLE ONLY public.salary_increase
    ADD CONSTRAINT salary_increase_user_position_id_fkey FOREIGN KEY (user_position_id) REFERENCES public.user_position(id) ON DELETE CASCADE;


--
-- TOC entry 3237 (class 2606 OID 39179)
-- Name: user_position user_position_position_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: test_admin
--

ALTER TABLE ONLY public.user_position
    ADD CONSTRAINT user_position_position_id_fkey FOREIGN KEY (position_id) REFERENCES public."position"(id) ON DELETE CASCADE;


--
-- TOC entry 3238 (class 2606 OID 39174)
-- Name: user_position user_position_user_uuid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: test_admin
--

ALTER TABLE ONLY public.user_position
    ADD CONSTRAINT user_position_user_uuid_fkey FOREIGN KEY (user_uuid) REFERENCES public."user"(id) ON DELETE CASCADE;


-- Completed on 2025-06-30 04:25:15

--
-- PostgreSQL database dump complete
--

