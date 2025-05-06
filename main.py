from bot import Bot
import json

def main():
    import os

    # Define default config values
    default_config = {
        "bot_token": "your_default_bot_token_here"
    }

    # Check if config.json exists, if not, create it with the default values
    if not os.path.exists('config.json'):
        with open('config.json', 'w') as file:
            json.dump(default_config, file, indent=4)
            print("config.json created with default values.")

    # Read the data from config.json
    with open('config.json', 'r') as file:
        data = json.load(file)

        # Create bot object and run
        bot = Bot()
        bot.run(data.get("bot_token"))

if __name__ == "__main__":
    main()