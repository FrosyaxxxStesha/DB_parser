DROP TABLE IF EXISTS employers CASCADE;
CREATE TABLE employers(
    employer_id int PRIMARY KEY,
    trusted bool NOT NULL,
    name varchar(100) NOT NULL,
    type varchar(20),
    place varchar(100),
    site_url varchar(100),
    alternate_url varchar(100),
    vacancies_url varchar(100),
    description text
);

DROP TABLE IF EXISTS vacancies;
CREATE TABLE vacancies(
    vacancy_id int PRIMARY KEY,
    employer_id int REFERENCES employers(employer_id),
    published_at timestamp,
    name varchar(100),
    place varchar(100),
    salary int,
    url varchar(100)
);