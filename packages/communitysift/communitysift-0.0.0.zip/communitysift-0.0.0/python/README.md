## Contact demo@communitysift.com for all questions

#### [CommunitySift](https://communitysift.com/) Eliminate toxicity from your online community
##### Python Client

#### Init

```
communitysift = CommunitySift()

```

#### Filter Chats

You can have any attribute passed in your JSON input. But "text" is mandatory
```
input_text = {
    "room": "Warrior Corridor",
    "text": "I want to shoot you"
}

print communitysift.execute('filterChats', input_text)
```


#### Username Validation

You can have any attribute passed in your JSON input. But "username" is mandatory
```
username_input = {
    "player_id": "99war12",
    "username": "john doe"
}

print communitysift.execute('userNameValidation', username_input)
```

## Contact demo@communitysift.com for all questions
