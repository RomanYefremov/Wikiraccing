import psycopg2

conn = psycopg2.connect(
    database='postgres',
    user='postgres',
    password='postgres',
    host='0.0.0.0'
)


def db_summ(name, link_self, link_have):
    queue = []
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT name FROM wikilinks2 WHERE name = %s', [name])
            result_name = [x[0] for x in cur.fetchall()]
            if name not in result_name:
                cur.execute(f"INSERT INTO wikilinks2 (name, link_self, link_have) "
                            f"VALUES ('{name}', '{link_self}', '{link_have}')")
            queue += name
            conn.commit()

    except (Exception, psycopg2.Error) as error:
        conn.rollback()
        print(error)


with conn.cursor() as cur:
    cur.execute("SELECT name, link_have AS total FROM wikilinks2 ORDER BY link_have DESC LIMIT 5")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    print('Top 5 link have')
    cur.execute(
        "SELECT name, link_self AS total FROM wikilinks2 ORDER BY link_self DESC LIMIT 5")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    print('Top 5 link self')
