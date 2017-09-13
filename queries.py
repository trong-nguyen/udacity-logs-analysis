import psycopg2

# The main SQL query
view_query = """
SELECT articles.title, top_views.views FROM
    (SELECT regexp_replace(path, '/(article/)?', '') AS slug, count(path) AS views
    FROM log
    GROUP BY path) as top_views, articles
WHERE top_views.slug = articles.slug
ORDER BY top_views.views DESC
LIMIT 3;
"""

# The DB-API execution
conn = psycopg2.connect(database='news')
cur = conn.cursor()
cur.execute(view_query)
res = cur.fetchall()
conn.close()

# Result representation
print """
The 3 most popular articles of all time:
{}
""".format('\n'.join(['{} - {} views'.format(a, v) for a,v in res]))
