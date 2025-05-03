import os
import shutil

class EnvCheck:
    def __init__(self) -> None:
        self.example_env = {}
        self.existing_env = {}


        print("""You can get example environment variables from env_example file.
            API keys from: https://api-docs.igdb.com/?getting-started#account-creation

            """)

        self.check_env()

        self.get_example_env()
        self.get_existing_env()

        self.user_update_env()

    def check_env(self):
        if not os.path.exists('.env'):
            shutil.copy('env_example', '.env')
            print(".env file created. Please update the file with your environment variables.")

    def get_example_env(self):
        example_env = {}
        if os.path.exists('env_example'):
            with open('env_example', 'r') as f:
                for line in f:
                    key, value = line.strip().split('=')
                    example_env[key] = value
        self.example_env = example_env

    def get_existing_env(self):
        # read and compare against example
        existing_env = {}
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    key, value = line.strip().split('=')
                    if key in self.example_env:
                        existing_env[key] = value
        self.existing_env = existing_env

    def check_answer(self, key: str, optional: bool) -> str:
        answer = ""
        while answer == "":
            if optional:
                answer = input(f"Enter value for {key} - example: {self.example_env[key]}\n(optional, Enter to skip): ")
                if answer.lower() == "skip" or answer == "":
                    if key == "HEROIC_CONFIG":
                        tmp_path = self.existing_env["PATHO"]
                        tmp_path = tmp_path.replace("_cache", "")
                        return tmp_path+"config.json"
                    return self.example_env[key]
                else:
                    break
            else:
                answer = input(f"Enter value for {key} - example: {self.example_env[key]}\n: ")
        return answer

    def check_done(self, key: str) -> bool:
        # compare the existing value with the example value
        return not (key in self.existing_env and self.existing_env[key] == self.example_env[key])

    def user_update_env(self):
        # key: optional
        keys = {"CLIENT_ID": False, "CLIENT_SECRET": False, "PATHO": False, "HEROIC_CONFIG": True, "GOG_LIBRARY": True, "AMAZON_LIBRARY": True, "EPIC_LIBRARY": True}
        for key in keys:
            # check if already exists
            if self.check_done(key):
                print(f"{key} already done")
                continue
            self.existing_env[key] = self.check_answer(key, keys[key])
        # Save the updated environment variables to .env file
        with open('.env', 'w') as f:
            for key, value in self.existing_env.items():
                f.write(f"{key}={value}\n")

if __name__ == "__main__":
    env_check = EnvCheck()
