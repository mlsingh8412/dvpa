### Damn Vulnerable Python Application (Flask) 123

```
docker-compose build
docker-compose up -d
docker-compose exec -T db mysql -u admin --password=admin blog < medaum.sql
```
