import wrapt


@wrapt.decorator
async def autoflash(wrapped, instance, args, kwargs):
    """Prepare the database before the test and clean it up after."""
    from sequvice_app import app

    async def clear_database(trans, db):
        await trans.rollback()
        await db.drop_tables()

    db = app.db
    async with db.connection():
        await db.create_tables()
        async with db.transaction() as trans:
            try:
                await wrapped(*args, **kwargs)
            except Exception as ex:
                await clear_database(trans, db)
                raise ex
            await clear_database(trans, db)
    return
