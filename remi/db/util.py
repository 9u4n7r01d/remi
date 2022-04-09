from sqlalchemy import inspect, text


async def _unique_insert(db_entry, session):
    """
    Insert entry to table, update existing entry on conflict.
    """
    # Get attribute supplied to entry, filtering out any residual internal attributes
    available_kv = {k: v for k, v in db_entry.__dict__.items() if not k.startswith("_")}

    # Get columns of table
    table_columns = inspect(db_entry.__class__).columns
    columns_of_interest = {col for col in table_columns if col.name in available_kv}
    value_column = {col for col in columns_of_interest if not (col.primary_key or col.unique)}
    identifier_column = columns_of_interest - value_column

    stmt = (
        f"INSERT INTO {db_entry.__tablename__} ({', '.join([col.name for col in columns_of_interest])}) "
        f"VALUES ({', '.join([f':{col.name}' for col in columns_of_interest])}) "
        f"ON CONFLICT ({', '.join([col.name for col in identifier_column])}) "
        f"DO UPDATE SET ({', '.join([col.name for col in value_column])}) "
        f"= {', '.join([f':{col.name}' for col in value_column])}"
    )

    await session.execute(text(stmt), [available_kv])
