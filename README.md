# Order Transactions

* Each time an order request is received, we immediately redcue the order price value from the users balance. ( transactional )
* Then we create related rows like the order and the outbox event.
* We use gEvent and celery tasks in order to place buy orders on external exchanges.
* With this approach, our order API will be fully asynchronous and we don't need a scheduler.
* We could have used celery beat with shared tasks but that would limit as a bit. 