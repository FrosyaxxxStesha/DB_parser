from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)

    if parser.has_section(section):
        params = parser.items(section)
        return dict(params)

    raise Exception(f"Section {section} is not found in the {filename} file")

