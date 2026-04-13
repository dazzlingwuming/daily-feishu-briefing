# Feishu Delivery

## Two Send Modes

### CLI Mode

Use this when local `lark-cli` is available and already authenticated.

Common send command:

```powershell
lark-cli im +messages-send --as bot --user-id "ou_xxx" --text "..."
```

Recommended use:

- local smoke tests
- fast recipient verification
- personal machine setups
- sending the full content of a local UTF-8 text file after reading the recipient from `.env`

### API Mode

Use this when running headlessly on a server or CI.

Required environment:

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FEISHU_RECEIVER_OPEN_ID`

Required steps:

1. fetch tenant access token
2. send a message to the recipient open ID
3. record the response and message ID

## Identity Notes

`lark-cli` can send as `bot` or `user`.

- `--as bot` uses bot/app permissions
- `--as user` needs user OAuth scopes such as `im:message.send_as_user`

When a local setup already works with bot messaging, prefer `--as bot` for smoke tests.

## Common Errors

### Missing scope

Example:

```text
missing required scope(s): im:message.send_as_user, im:message
```

Meaning:

- you are trying to send as `user`
- required OAuth scopes are not granted

### Network blocked by sandbox

Example:

```text
connectex: An attempt was made to access a socket in a way forbidden by its access permissions
```

Meaning:

- the current execution environment blocked outbound network access

## Verified Local Pattern

When `.env` contains:

```text
FEISHU_SEND_MODE=cli
FEISHU_RECEIVER_OPEN_ID=ou_xxx
```

and a local text file exists, a working pattern is:

```powershell
python scripts\send_test_message.py --env-file .env --mode cli --file diary.txt
```
