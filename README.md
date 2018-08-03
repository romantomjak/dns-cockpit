# dns-cockpit

Centralized DNS management

---

![DNS Cockpit](/screenshot.png?raw=true)

## How to run

```shell
mv env.example .env
make configure run
```

## Database migrations

```shell
make migration m="add users table"
```

## License

MIT
