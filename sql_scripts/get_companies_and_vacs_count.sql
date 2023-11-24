SELECT employers.name, COUNT(vacancies) AS count_of_vacancies
FROM employers
JOIN vacancies USING(employer_id)
GROUP BY employers.name