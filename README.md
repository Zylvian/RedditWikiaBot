# Reddit Wikia bot

*Thanks a lot to [hearthscan bot](https://github.com/d-schmidt/hearthscan-bot) for providing an amazing springboard for this bot*.

---

## Info:
**How it works:** Write `::something::` in a comment in a subreddit where this bot is active, and it will return [a summary, an image and a link to the dedicated **fandom.wiki** page for the sub.](https://i.gyazo.com/ca796615a97d88dd9d1699ad96783e02.png)

**Bot user**: [u/Wikia_Bot](https://www.reddit.com/user/Wikia_Bot)

[**Subreddits in which the bot is active.**](https://github.com/Zylvian/RedditWikiaBot/blob/master/data/constants.json)

--- 

### Requesting new subreddit
If you want to request the bot for another subreddit, make an issue with the appropriate **subreddit link** and **fandom.wiki link**.

### APIs:
For finding correct page and fetching summary: https://onepiece.fandom.com/api/v1
For fetching images: https://onepiece.fandom.com/api.php

## Requirements
Praw (most **importantly**, a praw.ini file with the bot's login information). [Praw tutorial](https://praw.readthedocs.io/en/latest/getting_started/quick_start.html)

---

### Other
Please feel free to leave any and all comments as **issues** and don't be afraid of sending appropriate **pull requests**.
