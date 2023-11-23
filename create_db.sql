CREATE TABLE IF NOT EXISTS employers(
    employer_id int PRIMARY KEY,
    trusted bool NOT NULL,
    name varchar(100) NOT NULL,
    type varchar(20),
    place varchar(30),
    num_of_open_vacancies smallint,
    site_url varchar(100),
    alternate_url varchar(100),
    vacancies_url varchar(100),
    description text
);

CREATE TABLE IF NOT EXISTS vacancies(
    vacancy_id int PRIMARY KEY,
    employer_id int REFERENCES employers(employer_id),
    published_at timestamp,
    name varchar(30),
    place varchar(30),
    salary smallint,
    address varchar(100),
    url varchar(100),
    requirement text,
    responsibility text
);