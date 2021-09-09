import sqlalchemy
import os


def create_db_connection(context):
    db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
    # cloud_sql_connection_name = os.environ["exemplary-proxy-322717:europe-central2:postcollector"]
    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL.create(
            drivername=context.config.userdata.get("drivername"),
            username=context.config.userdata.get(
                "username"),  # e.g. "my-database-user"
            password=context.config.userdata.get(
                "password"),  # e.g. "my-database-password"
            database=context.config.userdata.get(
                "database"),  # e.g. "my-database-name"
            host=context.config.userdata.get("host"),
            port=context.config.userdata.get("port")
        ),
    )
    return pool


def store_data_in_table(table_name, data_to_store, context):
    pool = create_db_connection(context)
    sql = "INSERT INTO "+table_name+" (name, context) VALUES (%s, %s)"
    print(sql)
    with pool.connect() as conn:
        for data in data_to_store:
            conn.execute(sql, data)
            print("record inserted.")


def fetch_db_data(table_name, val, context):
    pool = create_db_connection(context)
    sql_select_Query = "select * from "+table_name + \
        " where name = %s and context = %s order by id desc limit 1"
    with pool.connect() as conn:
        # Execute the query and fetch all results
        records = conn.execute(
            sql_select_Query, val
        ).fetchall()
        # get all records
    print("Total number of rows in table: ", len(records))
    return records
