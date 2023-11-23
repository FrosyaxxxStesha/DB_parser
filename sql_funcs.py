def fill_employers(employers: list[tuple]) -> None:
    prepared_list = [str(emp) for emp in employers]
    emp_string = ",\n".join(prepared_list)
