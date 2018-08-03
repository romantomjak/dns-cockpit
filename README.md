# dns-cockpit

Centralized DNS management

---

<p align="center">
    <img src="/screenshot.png?raw=true" alt="DNS Cockpit" />
</p>

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
