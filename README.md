
# Hawkeye

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![hikari-lightbulb 2.1.1](https://img.shields.io/badge/lightbulb-2.1.1-blue.svg)](https://hikari-lightbulb.readthedocs.io/en/latest/)
[![pydantic 1.9.0](https://img.shields.io/badge/pydantic-1.9.0-blue.svg)](https://pydantic-docs.helpmanual.io)
[![hikari 2.0.0.dev105](https://img.shields.io/badge/hikari-2.0.0.dev105-blue.svg)](https://www.hikari-py.dev/hikari/)
[![uvloop 0.16](https://img.shields.io/badge/uvlopp-0.16-blue.svg)](https://uvloop.readthedocs.io)

## Introduction
Enigma's discord moderation bot created using Hikari and LightBulb

It is still under development, so hang on before inviting the bot to your server.

To Contribute, please refer to <code style="background-color:rgba(0, 0, 0, 0.0470588);"><a href="https://github.com/MU-Enigma/Hawkeye/tree/dev">dev</a></code> branch.

## Deployment

Setup workspace for the bot

```
git clone git@github.com:MU-Enigma/Hawkeye.git
cd Hawkeye
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

Setting up the bot variables
```
touch .env
echo 'bot_token=<bot token ID>' >> .env
echo 'ot_prefix=<Bot prefix>' >> .env
echo 'bot_test_guilds=[<guild id1>, <guild id2> ..... ]' >> .env
```

Running the bot

```
python3 -m hawkeye
```


## Folder Structure

<p>All Plugins/Features are under <code style="background-color:rgba(0, 0, 0, 0.0470588);"><a href="https://github.com/MU-Enigma/Hawkeye/tree/master/hawkeye/core/plugins">./hawkeye/core/plugins/</a></code></p>
<p>All utilities are under <code style="background-color:rgba(0, 0, 0, 0.0470588);"><a href="https://github.com/MU-Enigma/Hawkeye/tree/master/hawkeye/core/utils">./hawkeye/core/utils/</a></code></p>

<a href="https://discord.gg/5eJwmkV"><img src="https://carbridgetweak.com/discord.svg" style="width:200px; margin-left:auto;margin-right:auto;display:block;"></a>
