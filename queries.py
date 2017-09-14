import psycopg2

top_articles = """
CREATE VIEW top_articles AS
    SELECT authors.id as author_id, articles.title, top_views.views FROM
        (SELECT regexp_replace(path, '/(article/)?', '') AS slug,
            count(path) AS views
        FROM log
        GROUP BY path) as top_views, articles, authors
    WHERE top_views.slug = articles.slug AND articles.author = authors.id;
"""

top_titles = """
SELECT title, views
FROM top_articles
ORDER BY views DESC
LIMIT 3;
"""

top_authors = """
SELECT authors.name, top_authors.views
FROM (SELECT author_id, SUM(views) AS views
    FROM top_articles
    GROUP BY author_id) AS top_authors
    JOIN authors
    ON top_authors.author_id = authors.id
ORDER BY top_authors.views DESC
LIMIT 1;
"""

top_error_requests = """
SELECT *
FROM
    (SELECT error_requests.day,
        (error_requests.num::float / all_requests.num::float * 100)
            AS percentage
    FROM
        (SELECT error_day_log.day, count(*) AS num
        FROM
            (SELECT time::date AS day
            FROM log
            WHERE status LIKE '4%') AS error_day_log
        GROUP BY error_day_log.day) AS error_requests,

        (SELECT day_log.day, count(*) AS num
        FROM
            (SELECT time::date AS day
            FROM log) AS day_log
        GROUP BY day_log.day) AS all_requests
    WHERE error_requests.day = all_requests.day
    ORDER BY 2 DESC) AS percentages
WHERE percentages.percentage > 1;
"""

# The DB- API execution
conn = psycopg2.connect(database='news')
cur = conn.cursor()
cur.execute(top_articles)

# Top titles
cur.execute(top_titles)
titles_res = cur.fetchall()

# Top authors
cur.execute(top_authors)
authors_res = cur.fetchall()

# Top error requests
cur.execute(top_error_requests)
error_res = cur.fetchall()

conn.close()


# Result representation
def record_to_string(fm, data):
    """
    Convert data tables to format defined by fm
    """
    return '\n'.join(map(lambda d: fm.format(*d), data))

fm = '{} - {} views'
print """
The {} most popular article(s) of all times:
{}
""".format(len(titles_res), record_to_string(fm, titles_res))

fm = '{} - {} views'
print """
The {} most popular author(s) of all times:
{}
""".format(len(authors_res), record_to_string(fm, authors_res))

fm = '{} - {:.01f}% errors'
print """
The {} day(s) where more than 1% requests leads to errors:
{}
""".format(len(error_res), record_to_string(fm, error_res))
