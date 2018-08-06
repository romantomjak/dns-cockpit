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

To create a new migration - modify orm mappings and then run:

```shell
make alembic-migration m="add users table"
```

To apply migration(-s) run:

```
make alembic-upgrade
```

## Tests

```
make unit-tests
```

## License

MIT
