SELECT employers.name, vacancies.name, salary, vacancies.url
FROM vacancies
JOIN employers USING(employer_id)
