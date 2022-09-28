# Very simple e-shop

by Ondřej Lomič

## Thoughts
- There would be quite a lot of questions when designing/implementing the e-shop,
such as number of users / required availability, etc. Since there's no one to ask,
I answered myself in the simplest way, to KISS (keep it simple stupid), and I tried
to provide reasoning behind that
- I never worked with Flask nor SQLAlchemy nor Jinja nor Kubernetes, but a lot with 
Django and Docker-compose. But nevertheless I managed to finish the task in one day,
which is quite nice, since half of the time I was reading Kubernetes documentation. 

## Design
- Clickable Figma is [here](https://www.figma.com/proto/Q27TIbPjG81LNVEo3rpSmF/very-simple-eshop)
- I split `Customer` create form into two (Person/Company), there could be a javascript
that would dynamically change part of the form, but... there's no such requirement,
keeping it simple means it's easy to change and understand, it's clear for user too and
there's "rule of three" as well, it hard to justify possibly complicated solution,
when there are just two different cases.
- It is not clear, whether one `Order` can have multiple instances of one `Item` in it.
The common sense says yes, the diagram can be interpreted both ways, but I would expect
`ItemOrder` class between `Order` and `Item` with `item_count` property. So I'll assume
only one specific `Item` per `Order` (not that it changes that much).
- Not sure what `internal identifier` means, but my rule of thumb is that everything 
should have generated `id` as primary key, no funky business with `email` etc. But that
is just my opinion.

## Implementation
- Since I cannot use Django, I opted for SQLAlchemy for ORM. There are _nicer_
libraries out there, but as I understood this is the _standard_. And there's integration
for Flask, so it's not that bad I guess, but it could be argued if it's the KISS option.
- If there would be more items, I would add javascript snippet for Add item / 
Remove item, since it would make the UX much better, when adding multiple items.
- There is no testing, no extensive input validation, no form errors. I was thinking
about PostrgreSQL instead of SQLite3, but for this purpose there's probably no need to.
I see this more like a prototype application, that should be done as fast as possible,
no need to think about performance, security, etc.

## Deployment
- Usually I deploy applications with docker-compose, together with Nginx (for routing
and serving of media/static files) and PostgreSQL. But I looked at Kubernetes and I
quite like it ;)
- There's simple Dockerfile, `kubernetes/flask_deployment.yaml` and 
`kubernetes/flask_service.yaml`. However, running the service did not expose the
port for me (on the node ip), or (probably) there's something wrong with my environment,
since I develop on WSL, which.. has its own problems. And I used Kubernetes packed with
Docker Desktop instead of Minicube. But I managed to expose the
pod port via `kubectl port-forward flask-<pod> 5000:5000` and access it at 
`localhost:5000`.
- Ideally, the database would be separate, with its defined volume. 
[This](https://testdriven.io/blog/running-flask-on-kubernetes/#automation-script)
looks like a nice tutorial, I'm missing nginx for serving static files I guess. 
- It's not the best, but I wanted to finish the task in one day. There are surely many
things that could be improved, but there always are.

Thank you, have a nice day ;)
