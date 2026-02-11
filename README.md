A simple Django project for demonstrating an example of architecture slightly similar to kraken.tech architecture for Django projects.
E.g.: https://github.com/aabrilfl13/python-pattern-example
https://github.com/jamesbeith/jamesbeith.co.uk/blob/main/content/blog/how-to-structure-django-projects.md

All tests pass. Implements the UoW pattern for transaction management. An architecture similar to Clean Architecture adapted for working within Django apps.

It follows Clean Architecture in the sense that it advocates for testability and ensures high cohesion and low coupling between layers through the separation of the Domain layer, repositories, and services with dependency injection, though I didn't see this approach mentioned in the reference examples.

To do: Add more tests, implement the missing endpoints, improve documentation, error handling, logging, CQRS…
