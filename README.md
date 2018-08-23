# dns-cockpit

Centralized DNS management

---

<p align="center">
    <img src="/screenshot.png?raw=true" alt="DNS Cockpit" />
</p>

## Roadmap

This project is currently under development by a single developer in his free 
time and thus the general answer to "when will X be done?" is "I don't know".

Here's a rough idea of what to expect though:

### 1.0

- Support at least two DNS registrars - currently I am considering GoDaddy and Namecheap

### 2.0

- Figure out an API for updating BIND DNS server records on the fly

### 3.0

- Add support for managing BIND DNS servers

## Installation

You will need [Docker](https://www.docker.com/products/docker-desktop) for 
these steps.

If you already have it installed - check out the project and run:

```shell
mv env.example .env
docker-compose up -d
```

## Development

I'm only using docker for shipping the application. Normally, I develop 
"outside" of docker to ease debugging and so my usual setup steps are:

```shell
mv env.example .env
mv docker-compose.override.yml.example docker-compose.override.yml
docker-compose up -d db
make install run
```

### Running tests

```
make unit-tests
```

### Database migrations

To create a new migration - modify orm mappings and then run:

```shell
make alembic-migration m="add users table"
```

To apply migration(-s) run:

```
make alembic-upgrade
```

## Contributing

You can contribute in many ways and not just by changing the code! If you have 
any ideas, just open an issue and tell me what you think.

Contributing code-wise - please fork the repository and submit a pull request.

## License

MIT
