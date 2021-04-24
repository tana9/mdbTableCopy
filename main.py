import pypyodbc


def join_columns(columns: list[str]) -> str:
    return ",".join([f"[{v}]" for v in columns])


def join_values(values: list[str]) -> str:
    return ",".join([f"'{v}'" for v in values])


def copy_table(src_mdb_path: str, src_table, dst_mdb_path: str, dst_table):
    columns = []
    values = []
    with pypyodbc.win_connect_mdb(src_mdb_path) as db:
        with db.cursor() as cursor:
            for row in cursor.columns(table=src_table):
                columns.append(row[3])
            cursor.execute(f"select * from {src_table}")
            for row in cursor:
                values.append(row)
    with pypyodbc.win_connect_mdb(dst_mdb_path) as db:
        with db.cursor() as cursor:
            for row in values:
                sql = f"insert into {dst_table}({join_columns(columns)}) values({join_values(row)});"
                cursor.execute(sql)
                print(sql)

    print(columns)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    src_mdb_path = "./Sample.accdb"
    src_table = "sampletable"
    dst_mdb_path = "./Sample.accdb"
    dst_table = "sampletable"
    copy_table(src_mdb_path, src_table, dst_mdb_path, dst_table)
