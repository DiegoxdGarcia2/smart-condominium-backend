--
-- PostgreSQL database dump
--

-- Dumped from database version 17rc1
-- Dumped by pg_dump version 17rc1

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

ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_user_id_c564eba6_fk_administration_user_id;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
ALTER TABLE ONLY public.administration_visitorlog DROP CONSTRAINT administration_visit_resident_id_3af27950_fk_administr;
ALTER TABLE ONLY public.administration_vehicle DROP CONSTRAINT administration_vehic_resident_id_077d1c0a_fk_administr;
ALTER TABLE ONLY public.administration_user DROP CONSTRAINT administration_user_role_id_07f79130_fk_administration_role_id;
ALTER TABLE ONLY public.administration_user_groups DROP CONSTRAINT administration_user_groups_group_id_43b1e17e_fk_auth_group_id;
ALTER TABLE ONLY public.administration_user_groups DROP CONSTRAINT administration_user__user_id_fcbab611_fk_administr;
ALTER TABLE ONLY public.administration_user_user_permissions DROP CONSTRAINT administration_user__user_id_69e83b80_fk_administr;
ALTER TABLE ONLY public.administration_user_user_permissions DROP CONSTRAINT administration_user__permission_id_5b940bd2_fk_auth_perm;
ALTER TABLE ONLY public.administration_task DROP CONSTRAINT administration_task_created_by_id_fa0067ad_fk_administr;
ALTER TABLE ONLY public.administration_task DROP CONSTRAINT administration_task_assigned_to_id_491e7bdf_fk_administr;
ALTER TABLE ONLY public.administration_residentialunit DROP CONSTRAINT administration_resid_owner_id_fee949a3_fk_administr;
ALTER TABLE ONLY public.administration_reservation DROP CONSTRAINT administration_reser_resident_id_cedb6e40_fk_administr;
ALTER TABLE ONLY public.administration_reservation DROP CONSTRAINT administration_reser_common_area_id_9956b061_fk_administr;
ALTER TABLE ONLY public.administration_pet DROP CONSTRAINT administration_pet_resident_id_d074e178_fk_administr;
ALTER TABLE ONLY public.administration_paymenttransaction DROP CONSTRAINT administration_payme_resident_id_1778d269_fk_administr;
ALTER TABLE ONLY public.administration_paymenttransaction DROP CONSTRAINT administration_payme_financial_fee_id_aa600b96_fk_administr;
ALTER TABLE ONLY public.administration_financialfee DROP CONSTRAINT administration_finan_unit_id_7c2b4e66_fk_administr;
ALTER TABLE ONLY public.administration_feedback DROP CONSTRAINT administration_feedb_resident_id_a10c96ac_fk_administr;
ALTER TABLE ONLY public.administration_announcement DROP CONSTRAINT administration_annou_author_id_c1386dcf_fk_administr;
DROP INDEX public.django_session_session_key_c0390e0f_like;
DROP INDEX public.django_session_expire_date_a5c62663;
DROP INDEX public.django_admin_log_user_id_c564eba6;
DROP INDEX public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX public.auth_permission_content_type_id_2f476e4b;
DROP INDEX public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX public.auth_group_name_a6ea08ec_like;
DROP INDEX public.administration_visitorlog_resident_id_3af27950;
DROP INDEX public.administration_vehicle_resident_id_077d1c0a;
DROP INDEX public.administration_vehicle_license_plate_a03c3183_like;
DROP INDEX public.administration_user_username_d8cdb8cc_like;
DROP INDEX public.administration_user_user_permissions_user_id_69e83b80;
DROP INDEX public.administration_user_user_permissions_permission_id_5b940bd2;
DROP INDEX public.administration_user_role_id_07f79130;
DROP INDEX public.administration_user_groups_user_id_fcbab611;
DROP INDEX public.administration_user_groups_group_id_43b1e17e;
DROP INDEX public.administration_user_email_1d334039_like;
DROP INDEX public.administration_task_created_by_id_fa0067ad;
DROP INDEX public.administration_task_assigned_to_id_491e7bdf;
DROP INDEX public.administration_role_name_c9dd34c3_like;
DROP INDEX public.administration_residentialunit_unit_number_a9f25e43_like;
DROP INDEX public.administration_residentialunit_owner_id_fee949a3;
DROP INDEX public.administration_reservation_resident_id_cedb6e40;
DROP INDEX public.administration_reservation_common_area_id_9956b061;
DROP INDEX public.administration_pet_resident_id_d074e178;
DROP INDEX public.administration_paymenttransaction_transaction_id_b1b7a9cd_like;
DROP INDEX public.administration_paymenttransaction_resident_id_1778d269;
DROP INDEX public.administration_paymenttransaction_financial_fee_id_aa600b96;
DROP INDEX public.administration_financialfee_unit_id_7c2b4e66;
DROP INDEX public.administration_feedback_resident_id_a10c96ac;
DROP INDEX public.administration_announcement_author_id_c1386dcf;
ALTER TABLE ONLY public.django_session DROP CONSTRAINT django_session_pkey;
ALTER TABLE ONLY public.django_migrations DROP CONSTRAINT django_migrations_pkey;
ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_pkey;
ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_pkey;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_pkey;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_pkey;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_pkey;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_name_key;
ALTER TABLE ONLY public.administration_visitorlog DROP CONSTRAINT administration_visitorlog_pkey;
ALTER TABLE ONLY public.administration_vehicle DROP CONSTRAINT administration_vehicle_pkey;
ALTER TABLE ONLY public.administration_vehicle DROP CONSTRAINT administration_vehicle_license_plate_key;
ALTER TABLE ONLY public.administration_user DROP CONSTRAINT administration_user_username_key;
ALTER TABLE ONLY public.administration_user_user_permissions DROP CONSTRAINT administration_user_user_user_id_permission_id_1258dc72_uniq;
ALTER TABLE ONLY public.administration_user_user_permissions DROP CONSTRAINT administration_user_user_permissions_pkey;
ALTER TABLE ONLY public.administration_user DROP CONSTRAINT administration_user_pkey;
ALTER TABLE ONLY public.administration_user_groups DROP CONSTRAINT administration_user_groups_user_id_group_id_97943ac2_uniq;
ALTER TABLE ONLY public.administration_user_groups DROP CONSTRAINT administration_user_groups_pkey;
ALTER TABLE ONLY public.administration_user DROP CONSTRAINT administration_user_email_key;
ALTER TABLE ONLY public.administration_task DROP CONSTRAINT administration_task_pkey;
ALTER TABLE ONLY public.administration_role DROP CONSTRAINT administration_role_pkey;
ALTER TABLE ONLY public.administration_role DROP CONSTRAINT administration_role_name_key;
ALTER TABLE ONLY public.administration_residentialunit DROP CONSTRAINT administration_residentialunit_unit_number_key;
ALTER TABLE ONLY public.administration_residentialunit DROP CONSTRAINT administration_residentialunit_pkey;
ALTER TABLE ONLY public.administration_reservation DROP CONSTRAINT administration_reservation_pkey;
ALTER TABLE ONLY public.administration_pet DROP CONSTRAINT administration_pet_pkey;
ALTER TABLE ONLY public.administration_paymenttransaction DROP CONSTRAINT administration_paymenttransaction_transaction_id_key;
ALTER TABLE ONLY public.administration_paymenttransaction DROP CONSTRAINT administration_paymenttransaction_pkey;
ALTER TABLE ONLY public.administration_financialfee DROP CONSTRAINT administration_financialfee_pkey;
ALTER TABLE ONLY public.administration_feedback DROP CONSTRAINT administration_feedback_pkey;
ALTER TABLE ONLY public.administration_commonarea DROP CONSTRAINT administration_commonarea_pkey;
ALTER TABLE ONLY public.administration_announcement DROP CONSTRAINT administration_announcement_pkey;
DROP TABLE public.django_session;
DROP TABLE public.django_migrations;
DROP TABLE public.django_content_type;
DROP TABLE public.django_admin_log;
DROP TABLE public.auth_permission;
DROP TABLE public.auth_group_permissions;
DROP TABLE public.auth_group;
DROP TABLE public.administration_visitorlog;
DROP TABLE public.administration_vehicle;
DROP TABLE public.administration_user_user_permissions;
DROP TABLE public.administration_user_groups;
DROP TABLE public.administration_user;
DROP TABLE public.administration_task;
DROP TABLE public.administration_role;
DROP TABLE public.administration_residentialunit;
DROP TABLE public.administration_reservation;
DROP TABLE public.administration_pet;
DROP TABLE public.administration_paymenttransaction;
DROP TABLE public.administration_financialfee;
DROP TABLE public.administration_feedback;
DROP TABLE public.administration_commonarea;
DROP TABLE public.administration_announcement;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: administration_announcement; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.administration_announcement (
    id bigint NOT NULL,
    title character varying(200) NOT NULL,
    content text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    author_id bigint NOT NULL
);


--
-- Name: administration_announcement_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.administration_announcement ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.administration_announcement_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: administration_commonarea; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.administration_commonarea (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    description text NOT NULL,
    capacity integer NOT NULL,
    booking_price numeric(10,2) NOT NULL,
    CONSTRAINT administration_commonarea_capacity_check CHECK ((capacity >= 0))
);


--
-- Name: administration_commonarea_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.administration_commonarea ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.administration_commonarea_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: administration_feedback; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.administration_feedback (
    id bigint NOT NULL,
    subject character varying(200) NOT NULL,
    message text NOT NULL,
    status character varying(20) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    resident_id bigint NOT NULL
);


--
-- Name: administration_feedback_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.administration_feedback ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.administration_feedback_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: administration_financialfee; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.administration_financialfee (
    id bigint NOT NULL,
    description character varying(200) NOT NULL,
    amount numeric(10,2) NOT NULL,
    due_date date NOT NULL,
    status character varying(20) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    unit_id bigint NOT NULL
);


--
-- Name: administration_financialfee_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.administration_financialfee ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.administration_financialfee_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: administration_paymenttransaction; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.administration_paymenttransaction (
    id bigint NOT NULL,
    transaction_id character varying(100) NOT NULL,
    amount numeric(10,2) NOT NULL,
    status character varying(20) NOT NULL,
    payment_method character varying(50) NOT NULL,
    gateway_response jsonb NOT NULL,
    created_at timestamp with time zone NOT NULL,
    processed_at timestamp with time zone,
    financial_fee_id bigint NOT NULL,
    resident_id bigint NOT NULL
);


--
-- Name: administration_paymenttransaction_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.administration_paymenttransaction ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.administration_paymenttransaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: administration_pet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.administration_pet (
    id bigint NOT NULL,
    name character varying(50) NOT NULL,
    species character varying(20) NOT NULL,
    breed character varying(50) NOT NULL,
    age integer,
    created_at timestamp with time zone NOT NULL,
    resident_id bigint NOT NULL,
    CONSTRAINT administration_pet_age_check CHECK ((age >= 0))
);


--
-- Name: administration_pet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.administration_pet ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.administration_pet_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: administration_reservation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.administration_reservation (
    id bigint NOT NULL,
    start_time timestamp with time zone NOT NULL,
    end_time timestamp with time zone NOT NULL,
    status character varying(20) NOT NULL,
    total_paid numeric(10,2) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    common_area_id bigint NOT NULL,
    resident_id bigint NOT NULL
);


--
-- Name: administration_reservation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.administration_reservation ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.administration_reservation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: administration_residentialunit; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.administration_residentialunit (
    id bigint NOT NULL,
    unit_number character varying(20) NOT NULL,
    type character varying(20) NOT NULL,
    floor integer,
    owner_id bigint
);


--
-- Name: administration_residentialunit_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.administration_residentialunit ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.administration_residentialunit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: administration_role; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.administration_role (
    id bigint NOT NULL,
    name character varying(50) NOT NULL
);


--
-- Name: administration_role_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.administration_role ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.administration_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: administration_task; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.administration_task (
    id bigint NOT NULL,
    title character varying(200) NOT NULL,
    description text NOT NULL,
    status character varying(20) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    completed_at timestamp with time zone,
    assigned_to_id bigint NOT NULL,
    created_by_id bigint NOT NULL
);


--
-- Name: administration_task_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.administration_task ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.administration_task_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: administration_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.administration_user (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    email character varying(254) NOT NULL,
    phone_number character varying(20) NOT NULL,
    role_id bigint
);


--
-- Name: administration_user_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.administration_user_groups (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: administration_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.administration_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.administration_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: administration_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.administration_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.administration_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: administration_user_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.administration_user_user_permissions (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: administration_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.administration_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.administration_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: administration_vehicle; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.administration_vehicle (
    id bigint NOT NULL,
    license_plate character varying(10) NOT NULL,
    brand character varying(50) NOT NULL,
    model character varying(50) NOT NULL,
    color character varying(30) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    resident_id bigint NOT NULL
);


--
-- Name: administration_vehicle_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.administration_vehicle ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.administration_vehicle_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: administration_visitorlog; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.administration_visitorlog (
    id bigint NOT NULL,
    visitor_name character varying(100) NOT NULL,
    visitor_dni character varying(20) NOT NULL,
    entry_time timestamp with time zone NOT NULL,
    exit_time timestamp with time zone,
    vehicle_license_plate character varying(10),
    status character varying(20) NOT NULL,
    observations text NOT NULL,
    resident_id bigint NOT NULL
);


--
-- Name: administration_visitorlog_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.administration_visitorlog ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.administration_visitorlog_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- Data for Name: administration_announcement; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.administration_announcement (id, title, content, created_at, author_id) FROM stdin;
1	Bienvenidos al nuevo sistema Smart Condominium	Nos complace anunciar el lanzamiento de nuestro nuevo sistema de gestión del condominio. A través de esta plataforma podrán consultar comunicados, revisar sus cuotas financieras y mantenerse informados sobre las actividades del condominio.	2025-09-07 23:22:50.46485-04	1
2	Mantenimiento de áreas comunes - Septiembre	Estimados residentes, les informamos que el próximo martes 10 de septiembre se realizará el mantenimiento preventivo de las áreas comunes, incluyendo jardines, elevadores y sistema de seguridad. El trabajo se realizará de 9:00 AM a 3:00 PM.	2025-09-07 23:22:50.497856-04	1
3	Nuevas	Por favor tomar nota de las nuevas normas para el uso del estacionamiento: 1) Respetar los espacios asignados, 2) No obstruir las vías de evacuación, 3) Velocidad máxima 10 km/h. Agradecemos su cooperación.	2025-09-07 23:22:50.500704-04	1
5	prueba	esto es una prueba	2025-09-09 23:07:53.625938-04	1
8	Nuevas normas de uso del estacionamiento	Por favor tomar nota de las nuevas normas para el uso del estacionamiento: 1) Respetar los espacios asignados, 2) No obstruir las vías de evacuación, 3) Velocidad máxima 10 km/h. Agradecemos su cooperación.	2025-09-11 23:19:27.615344-04	1
\.


--
-- Data for Name: administration_commonarea; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.administration_commonarea (id, name, description, capacity, booking_price) FROM stdin;
1	Salón de Eventos	Amplio salón para celebraciones y eventos sociales con capacidad para 50 personas	50	300.00
2	Piscina	Piscina comunitaria con área recreativa	30	150.00
4	Gimnasio	Gimnasio equipado con máquinas de ejercicio	15	50.00
5	Terraza BBQ	Terraza con parrillas y mesas para asados familiares	20	120.00
3	Cancha de Tenis	Cancha de tenis profesional iluminada	10	100.00
10	prueba	esto es una prueba	60	90.00
11	sala evento 1	salon de eventos	40	100.00
\.


--
-- Data for Name: administration_feedback; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.administration_feedback (id, subject, message, status, created_at, updated_at, resident_id) FROM stdin;
1	Problema con el ascensor	El ascensor principal ha estado haciendo ruidos extraños y se detiene de manera irregular entre los pisos 3 y 4.	Pendiente	2025-09-16 22:40:00.040962-04	2025-09-16 22:40:00.04098-04	2
2	Sugerencia para mejora del gimnasio	Sería excelente si pudieran agregar más equipos cardiovasculares, especialmente caminadoras, ya que las actuales están muy ocupadas.	En Revisión	2025-09-16 22:40:00.045818-04	2025-09-16 22:40:00.045831-04	3
3	Ruido en el piso superior	Los vecinos del piso de arriba están haciendo mucho ruido durante las noches, especialmente después de las 10 PM.	Respondido	2025-09-16 22:40:00.049268-04	2025-09-16 22:40:00.049281-04	2
4	Agradecimiento por la limpieza	Quiero felicitar al equipo de limpieza por el excelente trabajo que han estado haciendo en las áreas comunes.	Cerrado	2025-09-16 22:40:00.051682-04	2025-09-16 22:40:00.051693-04	3
5	Problema con el estacionamiento	Hay vehículos que no tienen permiso ocupando los espacios de visitantes durante todo el día.	En Revisión	2025-09-16 22:40:00.054085-04	2025-09-16 22:40:00.054096-04	2
6	Prueba de feedback automatizada	Este feedback fue creado automáticamente por el script de pruebas para validar la funcionalidad del sistema.	Pendiente	2025-09-16 22:53:23.798407-04	2025-09-16 22:53:23.798421-04	2
7	Prueba de feedback automatizada	Este feedback fue creado automáticamente por el script de pruebas para validar la funcionalidad del sistema.	Pendiente	2025-09-16 22:55:33.57492-04	2025-09-16 22:55:33.574938-04	2
8	Prueba de feedback automatizada	Este feedback fue creado automáticamente por el script de pruebas para validar la funcionalidad del sistema.	Pendiente	2025-09-16 23:01:52.16556-04	2025-09-16 23:01:52.165572-04	2
9	Prueba de feedback automatizada	Este feedback fue creado automáticamente por el script de pruebas para validar la funcionalidad del sistema.	Cerrado	2025-09-16 23:05:45.808027-04	2025-09-16 23:44:56.980075-04	2
10	Diego Pruba	esto es una prueba para yutu	Pendiente	2025-09-16 23:47:33.688786-04	2025-09-16 23:47:33.688819-04	2
\.


--
-- Data for Name: administration_financialfee; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.administration_financialfee (id, description, amount, due_date, status, created_at, unit_id) FROM stdin;
1	Cuota de mantenimiento - Septiembre 2025	1500.00	2025-09-23	Pendiente	2025-09-07 23:22:50.611419-04	1
2	Cuota de mantenimiento - Agosto 2025	1500.00	2025-08-24	Pagado	2025-09-07 23:22:50.651552-04	1
3	Cuota de mantenimiento - Septiembre 2025	1500.00	2025-09-23	Pendiente	2025-09-07 23:22:50.657135-04	3
4	Reparación de plomería - Agosto 2025	850.00	2025-09-03	Vencido	2025-09-07 23:22:50.661375-04	3
5	Cuota de mantenimiento - Septiembre 2025	1500.00	2025-09-23	Pendiente	2025-09-07 23:22:50.666205-04	2
6	Cuota extraordinaria - Reparación elevador	50.00	2025-10-17	Pendiente	2025-09-08 22:54:57.426312-04	4
7	prueba	500.00	2025-09-13	Pendiente	2025-09-12 00:19:31.681556-04	5
8	Cuota de mantenimiento - Septiembre 2025	1500.00	2025-10-02	Pendiente	2025-09-16 22:29:16.466739-04	7
9	Cuota de mantenimiento - Agosto 2025	1500.00	2025-09-02	Pagado	2025-09-16 22:29:16.519446-04	7
11	prueba	100.00	2025-09-19	Pendiente	2025-09-18 21:40:00.987424-04	7
12	tt	80.00	2025-10-19	Pendiente	2025-09-18 21:45:14.528514-04	4
\.


--
-- Data for Name: administration_paymenttransaction; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.administration_paymenttransaction (id, transaction_id, amount, status, payment_method, gateway_response, created_at, processed_at, financial_fee_id, resident_id) FROM stdin;
1	TXN_755BB7A978C5	50.00	Completado	Tarjeta de Crédito	{"status": "approved", "payment_id": "pay_12345"}	2025-09-16 22:40:00.07877-04	2025-09-11 22:40:00.072796-04	6	3
2	TXN_DE80B2C95E89	1500.00	Pendiente		{}	2025-09-16 22:40:00.089811-04	\N	8	2
3	TXN_8BE9CD383940	50.00	Fallido	Transferencia Bancaria	{"error": "insufficient_funds", "status": "failed"}	2025-09-16 22:40:00.093058-04	2025-09-15 22:40:00.07467-04	6	3
4	TXN_3CB7762D711E	1500.00	Procesando	PayPal	{"status": "processing", "payment_id": "pay_67890"}	2025-09-16 22:40:00.09602-04	\N	3	3
5	TXN_6E4F65C5DBDE	1500.00	Pendiente		{}	2025-09-16 22:53:24.585192-04	\N	1	2
6	TXN_AC965DF55C81	1500.00	Pendiente		{}	2025-09-16 23:04:58.453097-04	\N	1	1
7	TXN_4156B19473EC	1500.00	Pendiente		{}	2025-09-16 23:06:07.647713-04	\N	2	1
\.


--
-- Data for Name: administration_pet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.administration_pet (id, name, species, breed, age, created_at, resident_id) FROM stdin;
2	Miau	Gato	Persa	2	2025-09-12 15:37:37.345071-04	2
3	Rocky	Perro	Pastor Alemán	5	2025-09-12 15:37:37.347992-04	3
4	Luna	Gato	Siames	1	2025-09-12 15:37:37.351098-04	3
1	Bocky	Perro	Labrador	3	2025-09-12 15:37:37.34142-04	2
6	liri	Gato	mestizo	5	2025-09-12 16:45:00.736213-04	1
7	Buddy	Perro	Labrador	3	2025-09-16 22:29:16.669782-04	2
\.


--
-- Data for Name: administration_reservation; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.administration_reservation (id, start_time, end_time, status, total_paid, created_at, common_area_id, resident_id) FROM stdin;
1	2025-09-19 17:19:27.725667-04	2025-09-19 22:19:27.725676-04	Confirmada	300.00	2025-09-11 23:19:27.753379-04	1	2
2	2025-09-15 09:19:27.72568-04	2025-09-15 13:19:27.725683-04	Cancelada	150.00	2025-09-11 23:19:27.757057-04	2	3
3	2025-09-13 10:20:00-04	2025-09-13 11:40:00-04	Pendiente	50.00	2025-09-12 01:11:47.369196-04	4	2
4	2025-09-17 08:00:00-04	2025-09-17 12:00:00-04	Pendiente	250.00	2025-09-12 01:17:17.614024-04	5	3
5	2025-09-20 09:37:37.155614-04	2025-09-20 14:37:37.155629-04	Confirmada	300.00	2025-09-12 15:37:37.162312-04	1	2
6	2025-09-16 01:37:37.155636-04	2025-09-16 05:37:37.155642-04	Pendiente	150.00	2025-09-12 15:37:37.169825-04	2	3
7	2025-09-24 16:29:16.564513-04	2025-09-24 21:29:16.564521-04	Confirmada	300.00	2025-09-16 22:29:16.580004-04	1	2
8	2025-09-20 08:29:16.564525-04	2025-09-20 12:29:16.564528-04	Pendiente	150.00	2025-09-16 22:29:16.624939-04	2	3
9	2025-09-24 16:39:59.968489-04	2025-09-24 21:39:59.968498-04	Confirmada	300.00	2025-09-16 22:39:59.972151-04	1	2
10	2025-09-20 08:39:59.968502-04	2025-09-20 12:39:59.968505-04	Pendiente	150.00	2025-09-16 22:39:59.977718-04	2	3
11	2025-09-18 16:54:00-04	2025-09-18 18:54:00-04	Pendiente	50.00	2025-09-18 20:54:52.436351-04	4	4
\.


--
-- Data for Name: administration_residentialunit; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.administration_residentialunit (id, unit_number, type, floor, owner_id) FROM stdin;
3	A-201	Departamento	2	3
1	A-105	Departamento	15	2
6	casa-12	Casa	\N	1
2	A-102	Departamento	1	1
7	A-101	Departamento	1	2
4	B-001	Casa	\N	3
5	B-002	Casa	\N	2
\.


--
-- Data for Name: administration_role; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.administration_role (id, name) FROM stdin;
1	Administrador
2	Residente
3	Guardia
4	Conserje
6	prueba2
\.


--
-- Data for Name: administration_task; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.administration_task (id, title, description, status, created_at, completed_at, assigned_to_id, created_by_id) FROM stdin;
1	Revisión mensual de aires acondicionados	Realizar mantenimiento preventivo de todos los sistemas de aire acondicionado del condominio	Pendiente	2025-09-16 22:40:00.02166-04	\N	4	1
2	Reparación de puerta del gimnasio	La puerta del gimnasio no cierra correctamente, revisar bisagras y cerradura	En Progreso	2025-09-16 22:40:00.02627-04	\N	4	2
3	Instalación de nueva cámara en lobby	Instalar cámara de seguridad adicional en el área del lobby principal	Completada	2025-09-16 22:40:00.02892-04	2025-09-14 22:40:00.016293-04	4	1
5	Prueba de tarea automatizada	Esta tarea fue creada por el script de pruebas automáticas	En Progreso	2025-09-16 22:53:23.05447-04	\N	4	1
6	Prueba de tarea automatizada	Esta tarea fue creada por el script de pruebas automáticas	En Progreso	2025-09-16 22:55:33.001495-04	\N	4	1
7	Prueba de tarea automatizada	Esta tarea fue creada por el script de pruebas automáticas	En Progreso	2025-09-16 23:01:51.818644-04	\N	4	1
8	Prueba de tarea automatizada	Esta tarea fue creada por el script de pruebas automáticas	En Progreso	2025-09-16 23:05:45.232287-04	\N	3	1
9	prueba	haz una prueba	Completada	2025-09-16 23:18:32.268893-04	2025-09-17 14:43:27.794088-04	4	1
4	Limpieza de filtros de la piscina	Limpieza semanal de filtros y verificación de niveles de cloro	Completada	2025-09-16 22:40:00.032139-04	2025-09-17 14:43:37.328997-04	4	1
\.


--
-- Data for Name: administration_user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.administration_user (id, password, last_login, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, email, phone_number, role_id) FROM stdin;
1	pbkdf2_sha256$720000$MwJd0Rcd90tgmbLYSFxN1M$ukM7JZDK1QuVDWAPzcjANXGIaMdGrNqmBVrFmFwwse8=	\N	f	admin_condo	María	Administradora	t	t	2025-09-05 23:10:05.972091-04	admin@smartcondo.com	+52-555-0001	1
3	pbkdf2_sha256$720000$hYoPsHoUnHmSMAqGoz2UbC$3jOAjN9OvUhpA8n69of7SvRtifK70IMG9g2icDfDmGU=	\N	f	residente2	Ana	García	f	t	2025-09-05 23:10:07.393158-04	ana.garcia@email.com	+52-555-0003	2
4	pbkdf2_sha256$720000$MRqmdZR0lblhjRMsvHyVGM$tqqvls5oAlE6PcMzUhpc+XBN9qWOguQE1CZOPWLMsfY=	\N	f	guardia1	Carlos	Seguridad	f	t	2025-09-05 23:10:08.077071-04	carlos.seguridad@email.com	+52-555-0004	3
2	pbkdf2_sha256$720000$Q0Wp3mlyFGKsUTpgC9f6Z2$33M7XE6vuvLa03/AaB4sComXiI7/HsS1PBLze0XBE0g=	\N	f	residente1	Juan	Pérez	f	t	2025-09-05 23:10:06.630354-04	juan.perez@email.com	+52-555-0002	2
\.


--
-- Data for Name: administration_user_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.administration_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: administration_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.administration_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: administration_vehicle; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.administration_vehicle (id, license_plate, brand, model, color, created_at, resident_id) FROM stdin;
1	ABC-123	Toyota	Corolla	Blanco	2025-09-12 15:37:37.178762-04	2
2	DEF-456	Honda	Civic	Gris	2025-09-12 15:37:37.278954-04	2
3	GHI-789	Nissan	Sentra	Azul	2025-09-12 15:37:37.282533-04	3
4	JKL-012	Mazda	CX-5	Rojo	2025-09-12 15:37:37.285337-04	3
6	PRUEBA2	toyota	corolla	blanco	2025-09-12 16:44:06.956491-04	1
\.


--
-- Data for Name: administration_visitorlog; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.administration_visitorlog (id, visitor_name, visitor_dni, entry_time, exit_time, vehicle_license_plate, status, observations, resident_id) FROM stdin;
1	María Rodríguez	12345678	2025-09-12 15:37:37.354793-04	\N	VIS-001	Activo	Visita familiar	2
2	Carlos Mendoza	87654321	2025-09-12 15:37:37.35923-04	2025-09-12 14:37:37.352456-04	VIS-002	Salió	Técnico de mantenimiento	3
3	Laura Jiménez	11223344	2025-09-12 15:37:37.361701-04	2025-09-11 14:37:37.352461-04	\N	Salió	Visita social	2
4	Pedro Gómez	55667788	2025-09-12 15:37:37.364617-04	2025-09-12 16:14:52.564808-04	\N	Salió	Entrega de paquete	3
7	diego2	1234567	2025-09-12 16:19:43.905454-04	2025-09-12 16:19:52.723753-04	diego	Salió	nada	3
6	diego	1234567	2025-09-12 16:19:16.516286-04	2025-09-12 16:24:45.263391-04	\N	Salió		2
8	prueba	1234567	2025-09-12 16:26:38.691908-04	\N	abc-1234	Activo		1
9	María Rodríguez	12345678	2025-09-16 22:29:16.736746-04	\N	VIS-001	Activo	Visita familiar	2
10	Carlos Mendoza	87654321	2025-09-16 22:29:16.77539-04	2025-09-16 21:29:16.728194-04	VIS-002	Salió	Técnico de mantenimiento	3
11	Laura Jiménez	11223344	2025-09-16 22:29:16.778772-04	2025-09-15 21:29:16.728234-04	\N	Salió	Visita social	2
12	Pedro Gómez	55667788	2025-09-16 22:29:16.782143-04	\N	\N	Activo	Entrega de paquete	3
13	María Rodríguez	12345678	2025-09-16 22:39:59.995318-04	\N	VIS-001	Activo	Visita familiar	2
14	Carlos Mendoza	87654321	2025-09-16 22:39:59.999307-04	2025-09-16 21:39:59.992039-04	VIS-002	Salió	Técnico de mantenimiento	3
15	Laura Jiménez	11223344	2025-09-16 22:40:00.002035-04	2025-09-15 21:39:59.992059-04	\N	Salió	Visita social	2
16	Pedro Gómez	55667788	2025-09-16 22:40:00.005021-04	\N	\N	Activo	Entrega de paquete	3
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add Rol	6	add_role
22	Can change Rol	6	change_role
23	Can delete Rol	6	delete_role
24	Can view Rol	6	view_role
25	Can add Usuario	7	add_user
26	Can change Usuario	7	change_user
27	Can delete Usuario	7	delete_user
28	Can view Usuario	7	view_user
29	Can add Unidad Residencial	8	add_residentialunit
30	Can change Unidad Residencial	8	change_residentialunit
31	Can delete Unidad Residencial	8	delete_residentialunit
32	Can view Unidad Residencial	8	view_residentialunit
33	Can add Cuota Financiera	9	add_financialfee
34	Can change Cuota Financiera	9	change_financialfee
35	Can delete Cuota Financiera	9	delete_financialfee
36	Can view Cuota Financiera	9	view_financialfee
37	Can add Comunicado	10	add_announcement
38	Can change Comunicado	10	change_announcement
39	Can delete Comunicado	10	delete_announcement
40	Can view Comunicado	10	view_announcement
41	Can add Reserva	11	add_reservation
42	Can change Reserva	11	change_reservation
43	Can delete Reserva	11	delete_reservation
44	Can view Reserva	11	view_reservation
45	Can add Área Común	12	add_commonarea
46	Can change Área Común	12	change_commonarea
47	Can delete Área Común	12	delete_commonarea
48	Can view Área Común	12	view_commonarea
49	Can add Vehículo	13	add_vehicle
50	Can change Vehículo	13	change_vehicle
51	Can delete Vehículo	13	delete_vehicle
52	Can view Vehículo	13	view_vehicle
53	Can add Mascota	14	add_pet
54	Can change Mascota	14	change_pet
55	Can delete Mascota	14	delete_pet
56	Can view Mascota	14	view_pet
57	Can add Registro de Visitante	15	add_visitorlog
58	Can change Registro de Visitante	15	change_visitorlog
59	Can delete Registro de Visitante	15	delete_visitorlog
60	Can view Registro de Visitante	15	view_visitorlog
61	Can add Tarea	16	add_task
62	Can change Tarea	16	change_task
63	Can delete Tarea	16	delete_task
64	Can view Tarea	16	view_task
65	Can add Transacción de Pago	17	add_paymenttransaction
66	Can change Transacción de Pago	17	change_paymenttransaction
67	Can delete Transacción de Pago	17	delete_paymenttransaction
68	Can view Transacción de Pago	17	view_paymenttransaction
69	Can add Feedback	18	add_feedback
70	Can change Feedback	18	change_feedback
71	Can delete Feedback	18	delete_feedback
72	Can view Feedback	18	view_feedback
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	administration	role
7	administration	user
8	administration	residentialunit
9	administration	financialfee
10	administration	announcement
11	administration	reservation
12	administration	commonarea
13	administration	vehicle
14	administration	pet
15	administration	visitorlog
16	administration	task
17	administration	paymenttransaction
18	administration	feedback
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2025-09-05 23:09:58.0266-04
2	contenttypes	0002_remove_content_type_name	2025-09-05 23:09:58.060369-04
3	auth	0001_initial	2025-09-05 23:09:58.109573-04
4	auth	0002_alter_permission_name_max_length	2025-09-05 23:09:58.114083-04
5	auth	0003_alter_user_email_max_length	2025-09-05 23:09:58.120304-04
6	auth	0004_alter_user_username_opts	2025-09-05 23:09:58.124684-04
7	auth	0005_alter_user_last_login_null	2025-09-05 23:09:58.129313-04
8	auth	0006_require_contenttypes_0002	2025-09-05 23:09:58.130791-04
9	auth	0007_alter_validators_add_error_messages	2025-09-05 23:09:58.137878-04
10	auth	0008_alter_user_username_max_length	2025-09-05 23:09:58.144149-04
11	auth	0009_alter_user_last_name_max_length	2025-09-05 23:09:58.148959-04
12	auth	0010_alter_group_name_max_length	2025-09-05 23:09:58.159455-04
13	auth	0011_update_proxy_permissions	2025-09-05 23:09:58.163854-04
14	auth	0012_alter_user_first_name_max_length	2025-09-05 23:09:58.170883-04
15	administration	0001_initial	2025-09-05 23:09:58.313251-04
16	admin	0001_initial	2025-09-05 23:09:58.376308-04
17	admin	0002_logentry_remove_auto_add	2025-09-05 23:09:58.382261-04
18	admin	0003_logentry_add_action_flag_choices	2025-09-05 23:09:58.39055-04
19	sessions	0001_initial	2025-09-05 23:09:58.399782-04
20	administration	0002_announcement_financialfee	2025-09-07 23:21:59.066356-04
21	administration	0003_commonarea_reservation	2025-09-11 23:18:25.115418-04
22	administration	0004_pet_vehicle_visitorlog	2025-09-12 15:36:10.353708-04
23	administration	0005_feedback_paymenttransaction_task	2025-09-16 22:27:39.631198-04
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Name: administration_announcement_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.administration_announcement_id_seq', 8, true);


--
-- Name: administration_commonarea_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.administration_commonarea_id_seq', 11, true);


--
-- Name: administration_feedback_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.administration_feedback_id_seq', 10, true);


--
-- Name: administration_financialfee_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.administration_financialfee_id_seq', 12, true);


--
-- Name: administration_paymenttransaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.administration_paymenttransaction_id_seq', 7, true);


--
-- Name: administration_pet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.administration_pet_id_seq', 7, true);


--
-- Name: administration_reservation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.administration_reservation_id_seq', 11, true);


--
-- Name: administration_residentialunit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.administration_residentialunit_id_seq', 7, true);


--
-- Name: administration_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.administration_role_id_seq', 6, true);


--
-- Name: administration_task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.administration_task_id_seq', 9, true);


--
-- Name: administration_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.administration_user_groups_id_seq', 1, false);


--
-- Name: administration_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.administration_user_id_seq', 5, true);


--
-- Name: administration_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.administration_user_user_permissions_id_seq', 1, false);


--
-- Name: administration_vehicle_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.administration_vehicle_id_seq', 6, true);


--
-- Name: administration_visitorlog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.administration_visitorlog_id_seq', 16, true);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 72, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 18, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 23, true);


--
-- Name: administration_announcement administration_announcement_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_announcement
    ADD CONSTRAINT administration_announcement_pkey PRIMARY KEY (id);


--
-- Name: administration_commonarea administration_commonarea_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_commonarea
    ADD CONSTRAINT administration_commonarea_pkey PRIMARY KEY (id);


--
-- Name: administration_feedback administration_feedback_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_feedback
    ADD CONSTRAINT administration_feedback_pkey PRIMARY KEY (id);


--
-- Name: administration_financialfee administration_financialfee_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_financialfee
    ADD CONSTRAINT administration_financialfee_pkey PRIMARY KEY (id);


--
-- Name: administration_paymenttransaction administration_paymenttransaction_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_paymenttransaction
    ADD CONSTRAINT administration_paymenttransaction_pkey PRIMARY KEY (id);


--
-- Name: administration_paymenttransaction administration_paymenttransaction_transaction_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_paymenttransaction
    ADD CONSTRAINT administration_paymenttransaction_transaction_id_key UNIQUE (transaction_id);


--
-- Name: administration_pet administration_pet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_pet
    ADD CONSTRAINT administration_pet_pkey PRIMARY KEY (id);


--
-- Name: administration_reservation administration_reservation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_reservation
    ADD CONSTRAINT administration_reservation_pkey PRIMARY KEY (id);


--
-- Name: administration_residentialunit administration_residentialunit_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_residentialunit
    ADD CONSTRAINT administration_residentialunit_pkey PRIMARY KEY (id);


--
-- Name: administration_residentialunit administration_residentialunit_unit_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_residentialunit
    ADD CONSTRAINT administration_residentialunit_unit_number_key UNIQUE (unit_number);


--
-- Name: administration_role administration_role_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_role
    ADD CONSTRAINT administration_role_name_key UNIQUE (name);


--
-- Name: administration_role administration_role_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_role
    ADD CONSTRAINT administration_role_pkey PRIMARY KEY (id);


--
-- Name: administration_task administration_task_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_task
    ADD CONSTRAINT administration_task_pkey PRIMARY KEY (id);


--
-- Name: administration_user administration_user_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_user
    ADD CONSTRAINT administration_user_email_key UNIQUE (email);


--
-- Name: administration_user_groups administration_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_user_groups
    ADD CONSTRAINT administration_user_groups_pkey PRIMARY KEY (id);


--
-- Name: administration_user_groups administration_user_groups_user_id_group_id_97943ac2_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_user_groups
    ADD CONSTRAINT administration_user_groups_user_id_group_id_97943ac2_uniq UNIQUE (user_id, group_id);


--
-- Name: administration_user administration_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_user
    ADD CONSTRAINT administration_user_pkey PRIMARY KEY (id);


--
-- Name: administration_user_user_permissions administration_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_user_user_permissions
    ADD CONSTRAINT administration_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: administration_user_user_permissions administration_user_user_user_id_permission_id_1258dc72_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_user_user_permissions
    ADD CONSTRAINT administration_user_user_user_id_permission_id_1258dc72_uniq UNIQUE (user_id, permission_id);


--
-- Name: administration_user administration_user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_user
    ADD CONSTRAINT administration_user_username_key UNIQUE (username);


--
-- Name: administration_vehicle administration_vehicle_license_plate_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_vehicle
    ADD CONSTRAINT administration_vehicle_license_plate_key UNIQUE (license_plate);


--
-- Name: administration_vehicle administration_vehicle_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_vehicle
    ADD CONSTRAINT administration_vehicle_pkey PRIMARY KEY (id);


--
-- Name: administration_visitorlog administration_visitorlog_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_visitorlog
    ADD CONSTRAINT administration_visitorlog_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: administration_announcement_author_id_c1386dcf; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_announcement_author_id_c1386dcf ON public.administration_announcement USING btree (author_id);


--
-- Name: administration_feedback_resident_id_a10c96ac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_feedback_resident_id_a10c96ac ON public.administration_feedback USING btree (resident_id);


--
-- Name: administration_financialfee_unit_id_7c2b4e66; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_financialfee_unit_id_7c2b4e66 ON public.administration_financialfee USING btree (unit_id);


--
-- Name: administration_paymenttransaction_financial_fee_id_aa600b96; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_paymenttransaction_financial_fee_id_aa600b96 ON public.administration_paymenttransaction USING btree (financial_fee_id);


--
-- Name: administration_paymenttransaction_resident_id_1778d269; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_paymenttransaction_resident_id_1778d269 ON public.administration_paymenttransaction USING btree (resident_id);


--
-- Name: administration_paymenttransaction_transaction_id_b1b7a9cd_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_paymenttransaction_transaction_id_b1b7a9cd_like ON public.administration_paymenttransaction USING btree (transaction_id varchar_pattern_ops);


--
-- Name: administration_pet_resident_id_d074e178; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_pet_resident_id_d074e178 ON public.administration_pet USING btree (resident_id);


--
-- Name: administration_reservation_common_area_id_9956b061; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_reservation_common_area_id_9956b061 ON public.administration_reservation USING btree (common_area_id);


--
-- Name: administration_reservation_resident_id_cedb6e40; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_reservation_resident_id_cedb6e40 ON public.administration_reservation USING btree (resident_id);


--
-- Name: administration_residentialunit_owner_id_fee949a3; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_residentialunit_owner_id_fee949a3 ON public.administration_residentialunit USING btree (owner_id);


--
-- Name: administration_residentialunit_unit_number_a9f25e43_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_residentialunit_unit_number_a9f25e43_like ON public.administration_residentialunit USING btree (unit_number varchar_pattern_ops);


--
-- Name: administration_role_name_c9dd34c3_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_role_name_c9dd34c3_like ON public.administration_role USING btree (name varchar_pattern_ops);


--
-- Name: administration_task_assigned_to_id_491e7bdf; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_task_assigned_to_id_491e7bdf ON public.administration_task USING btree (assigned_to_id);


--
-- Name: administration_task_created_by_id_fa0067ad; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_task_created_by_id_fa0067ad ON public.administration_task USING btree (created_by_id);


--
-- Name: administration_user_email_1d334039_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_user_email_1d334039_like ON public.administration_user USING btree (email varchar_pattern_ops);


--
-- Name: administration_user_groups_group_id_43b1e17e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_user_groups_group_id_43b1e17e ON public.administration_user_groups USING btree (group_id);


--
-- Name: administration_user_groups_user_id_fcbab611; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_user_groups_user_id_fcbab611 ON public.administration_user_groups USING btree (user_id);


--
-- Name: administration_user_role_id_07f79130; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_user_role_id_07f79130 ON public.administration_user USING btree (role_id);


--
-- Name: administration_user_user_permissions_permission_id_5b940bd2; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_user_user_permissions_permission_id_5b940bd2 ON public.administration_user_user_permissions USING btree (permission_id);


--
-- Name: administration_user_user_permissions_user_id_69e83b80; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_user_user_permissions_user_id_69e83b80 ON public.administration_user_user_permissions USING btree (user_id);


--
-- Name: administration_user_username_d8cdb8cc_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_user_username_d8cdb8cc_like ON public.administration_user USING btree (username varchar_pattern_ops);


--
-- Name: administration_vehicle_license_plate_a03c3183_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_vehicle_license_plate_a03c3183_like ON public.administration_vehicle USING btree (license_plate varchar_pattern_ops);


--
-- Name: administration_vehicle_resident_id_077d1c0a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_vehicle_resident_id_077d1c0a ON public.administration_vehicle USING btree (resident_id);


--
-- Name: administration_visitorlog_resident_id_3af27950; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX administration_visitorlog_resident_id_3af27950 ON public.administration_visitorlog USING btree (resident_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: administration_announcement administration_annou_author_id_c1386dcf_fk_administr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_announcement
    ADD CONSTRAINT administration_annou_author_id_c1386dcf_fk_administr FOREIGN KEY (author_id) REFERENCES public.administration_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administration_feedback administration_feedb_resident_id_a10c96ac_fk_administr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_feedback
    ADD CONSTRAINT administration_feedb_resident_id_a10c96ac_fk_administr FOREIGN KEY (resident_id) REFERENCES public.administration_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administration_financialfee administration_finan_unit_id_7c2b4e66_fk_administr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_financialfee
    ADD CONSTRAINT administration_finan_unit_id_7c2b4e66_fk_administr FOREIGN KEY (unit_id) REFERENCES public.administration_residentialunit(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administration_paymenttransaction administration_payme_financial_fee_id_aa600b96_fk_administr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_paymenttransaction
    ADD CONSTRAINT administration_payme_financial_fee_id_aa600b96_fk_administr FOREIGN KEY (financial_fee_id) REFERENCES public.administration_financialfee(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administration_paymenttransaction administration_payme_resident_id_1778d269_fk_administr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_paymenttransaction
    ADD CONSTRAINT administration_payme_resident_id_1778d269_fk_administr FOREIGN KEY (resident_id) REFERENCES public.administration_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administration_pet administration_pet_resident_id_d074e178_fk_administr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_pet
    ADD CONSTRAINT administration_pet_resident_id_d074e178_fk_administr FOREIGN KEY (resident_id) REFERENCES public.administration_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administration_reservation administration_reser_common_area_id_9956b061_fk_administr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_reservation
    ADD CONSTRAINT administration_reser_common_area_id_9956b061_fk_administr FOREIGN KEY (common_area_id) REFERENCES public.administration_commonarea(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administration_reservation administration_reser_resident_id_cedb6e40_fk_administr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_reservation
    ADD CONSTRAINT administration_reser_resident_id_cedb6e40_fk_administr FOREIGN KEY (resident_id) REFERENCES public.administration_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administration_residentialunit administration_resid_owner_id_fee949a3_fk_administr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_residentialunit
    ADD CONSTRAINT administration_resid_owner_id_fee949a3_fk_administr FOREIGN KEY (owner_id) REFERENCES public.administration_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administration_task administration_task_assigned_to_id_491e7bdf_fk_administr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_task
    ADD CONSTRAINT administration_task_assigned_to_id_491e7bdf_fk_administr FOREIGN KEY (assigned_to_id) REFERENCES public.administration_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administration_task administration_task_created_by_id_fa0067ad_fk_administr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_task
    ADD CONSTRAINT administration_task_created_by_id_fa0067ad_fk_administr FOREIGN KEY (created_by_id) REFERENCES public.administration_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administration_user_user_permissions administration_user__permission_id_5b940bd2_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_user_user_permissions
    ADD CONSTRAINT administration_user__permission_id_5b940bd2_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administration_user_user_permissions administration_user__user_id_69e83b80_fk_administr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_user_user_permissions
    ADD CONSTRAINT administration_user__user_id_69e83b80_fk_administr FOREIGN KEY (user_id) REFERENCES public.administration_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administration_user_groups administration_user__user_id_fcbab611_fk_administr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_user_groups
    ADD CONSTRAINT administration_user__user_id_fcbab611_fk_administr FOREIGN KEY (user_id) REFERENCES public.administration_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administration_user_groups administration_user_groups_group_id_43b1e17e_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_user_groups
    ADD CONSTRAINT administration_user_groups_group_id_43b1e17e_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administration_user administration_user_role_id_07f79130_fk_administration_role_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_user
    ADD CONSTRAINT administration_user_role_id_07f79130_fk_administration_role_id FOREIGN KEY (role_id) REFERENCES public.administration_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administration_vehicle administration_vehic_resident_id_077d1c0a_fk_administr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_vehicle
    ADD CONSTRAINT administration_vehic_resident_id_077d1c0a_fk_administr FOREIGN KEY (resident_id) REFERENCES public.administration_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administration_visitorlog administration_visit_resident_id_3af27950_fk_administr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.administration_visitorlog
    ADD CONSTRAINT administration_visit_resident_id_3af27950_fk_administr FOREIGN KEY (resident_id) REFERENCES public.administration_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_administration_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_administration_user_id FOREIGN KEY (user_id) REFERENCES public.administration_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

