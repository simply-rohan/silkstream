# silkstream
An instant messaging service (discord clone)

## Database structure
The backed database client is locally managed by [dbclient](https://github.com/simply-rohan/dbclient). The structure is as follows:

```
db/
├─ users/
│  ├─ passwords.json
│  ├─ user_data/
│  │  ├─ user_id.json
│  │  ├─ user_id.json
├─ servers/
│  ├─ server_id/
│  │  ├─ data.json
│  │  ├─ channel_id.json
│  │  ├─ channel_id.json
```
Each user_id.json contains user data like nicknames, friends, servers, profile, etc.

data.json for each server stores the configuration for each server, incuding it's name, icon, and visibility.

channel_id.json holds all the messages in the channel, as well as the name, visibility, and other properties of the channel.