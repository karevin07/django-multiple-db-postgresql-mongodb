# django-multiple-db-postgresql-mongodb

A Django service with Postgres and MongoDB

- Why Multiple Database

different app use different database

example:

```
example_user for user_data
example_app for application data
```

```mermaid
flowchart
    django[["django"]]
    db1[("postgres")]
    db2[("mongodb")]
    
    subgraph databases
    
        direction TB
        db1
        db2
    end
    
    subgraph web
        django
    end
    
    db1 <-.->|"ORM"|web
    db2 <-.->|"ORM (Djongo)"|web

```

## Start

- build django image

```shell
make build-django-image
```

- start with docker-compose

```shell
docker-compose up -d
```

- migrate data

```shell
make migrate-all
```

[django web](0.0.0.0:8000)


## Jupterlab with Django kernel


```mermaid
flowchart

    dev("jupyterlab")
    django[["django"]]
    db1[("postgres")]
    db2[("mongodb")]
    
    subgraph databases
    
        direction TB
        db1
        db2
    end
    
    subgraph web
        django
    end
    
    db1 <-.->|"ORM"|web
    db2 <-.->|"ORM (Djongo)"|web
    
    dev -.->|"Django Kernel"|web

    

```

Jupyterlab with django kernel for develop and test

```shell
make run-jupyter-with-django
```

[jupyterlab](0.0.0.0:8888)

## Reference

[Djongo](https://www.djongomapper.com/get-started/)

[django-multi-db](https://docs.djangoproject.com/en/4.0/topics/db/multi-db/)

[Using Django project in Jupyter or JupyterLab](https://gist.github.com/EtsuNDmA/dd8949061783bf593706559374c8f635)

[How to use Django in Jupyter Notebook](https://medium.com/ayuth/how-to-use-django-in-jupyter-notebook-561ea2401852)
