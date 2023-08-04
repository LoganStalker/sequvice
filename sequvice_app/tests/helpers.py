import wrapt


@wrapt.decorator
async def autoflash(wrapped, instance, args, kwargs):
    """Prepare the database before the test and clean it up after."""
    from sequvice_app import app

    db = app.db
    async with db.connection():
        await db.create_tables()
        try:
            await wrapped(*args, **kwargs)
        except Exception as ex:
            await db.drop_tables()
            raise ex
        await db.drop_tables()

    return
