# Very simple e-shop

by Ondřej Lomič

## Thoughts
- There would be quite a lot of questions when designing/implementing the e-shop,
such as number of users / required availability, etc. Since there's no one to ask,
I'll answer myself in the simplest way, to KISS (keep it simple stupid), bul I'll try
to provide reasoning behind that
- I never worked with Flask or SQLAlchemy or Kubernetes, but a lot with Django and 
Docker-compose.

## Design
- Clickable Figma is [here](https://www.figma.com/proto/Q27TIbPjG81LNVEo3rpSmF/very-simple-eshop)
- I split `Customer` create form into two (Person/Company), there could be javascript
that would dynamically change part of the form, but... there's no such requirement,
keeping it simple means it's easy to change and understand, it's clear for user too and
there's "rule of three" as well, it hard to justify possibly complicated solution,
when there are just two different cases.
- It is not clear, whether one `Order` can have multiple instances of one `Item` in it.
The common sense says yes, the diagram can be interpreted both ways, but I would expect
`ItemOrder` class between `Order` and `Item` with `item_count` property. So I'll assume
only one specific `Item` per `Order`.
- Not sure what `internal identifier` means, but my rule of thumb is that everything 
should have generated `id` as primary key, no funky business with `email` etc. But that
is just my opinion.

## Implementation
- Since I cannot use Django, I opted for SQLAlchemy for ORM. There are _nicer_
libraries out there, but as I understood this is the _standard_. And there's integration
for Flask, so it's not that bad I guess, but it could be argued if it's the KISS option.
- If there would be more items, I would add javascript snippet for Add item / 
Remove item, since it would make the UX much better, when adding multiple items.
- 


## Deployment
