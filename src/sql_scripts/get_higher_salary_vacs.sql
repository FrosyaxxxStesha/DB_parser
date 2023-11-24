SELECT * FROM vacancies
WHERE salary > (SELECT AVG(salary) FROM vacancies)