# Productivity Bot

Productivity Bot is a Discord bot that helps enforce daily voice channel usage limits for specified users. It tracks their time spent in voice channels and automatically disconnects them when they reach a specified limit.

*This bot code was 90% written by GPT-4. The README, other than this line, is 100% written by GPT-4.*

## Features

- Track voice channel time for specific users
- Set a custom daily limit for voice channel usage
- Automatically disconnect users when they reach their daily limit
- Send warning messages to users 10 minutes and 2 minutes before they are disconnected

## Environment Variables

The bot can be configured using the following environment variables:

- `PRODUCTIVITY_BOT_TOKEN`: The bot token used to connect to Discord. You can obtain this token from the [Discord Developer Portal](https://discord.com/developers/applications) by creating a new bot.
- `PRODUCTIVITY_BOT_USERS_TO_TRACK`: A comma-separated list of user IDs that should have their voice channel time tracked. Example: `1234567890,2345678901,3456789012`
- `PRODUCTIVITY_BOT_MAX_MINUTES`: The maximum number of minutes each user is allowed to be in a voice channel per day. Example: `180` (3 hours)

## Setup

1. Install the required dependencies:

```
pip install discord.py
```

2. Set the environment variables mentioned above with the appropriate values.

3. Run the bot script:

```
python main.py
```

Make sure to invite the bot to your server and grant it the necessary permissions
to manage voice channels and send direct messages.

The bot will print out the invite link upon successful startup.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
