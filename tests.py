import asyncio

from examples import (
    call,
    delete,
    insert,
    returning,
    select,
    update,
    where,
)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(asyncio.gather(*(
        call.test(),
        delete.test(),
        insert.test(),
        returning.test(),
        select.test(),
        update.test(),
        where.test(),
    )))
