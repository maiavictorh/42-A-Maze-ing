def get_config(file_name: str) -> dict:
    """ It takes the configuration and returns a dict.. """
    config: dict = {}
    try:
        with open(file_name, "r") as file:
            for line in file:
                line.strip()
                if "=" in line:
                    key, value = line.split("=", 1)
                    config[key] = value
        return config
    except FileNotFoundError:
        print("Error: File not found")
    except Exception as err:
        print(f"Error: {err}")
    return None
