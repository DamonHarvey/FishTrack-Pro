import requests
import sqlite3


class FishDB:

    def __init__(self) -> None:
        db_file = "fish.db"

        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def add_all_fish(self):
        def get_all_fish():
            response = requests.get(
                "https://programs.iowadnr.gov/bionet/api/v1/fish/species"
            )
            return response.json()

        def prepare_data(raw_data):
            data = [
                (
                    i["fishid"],
                    i["species"],
                    i["latin"],
                    i["family"],
                    i["familyCommon"],
                    i["tolerance"],
                    i["trophicLevel"],
                    i["isExotic"],
                    i["isLithoSpawner"],
                    i["isHybrid"],
                    i["stateListingStatus"],
                    i["html_url"],
                )
                for i in raw_data
            ]
            return data

        def add_data_to_db(to_db):
            self.cursor.executemany(
                "INSERT INTO fish VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", to_db
            )

        raw_data = get_all_fish()
        data = prepare_data(raw_data)
        add_data_to_db(data)

        self.commit()


def main():
    db = FishDB()
    db.connection.close()


if __name__ == "__main__":
    main()
