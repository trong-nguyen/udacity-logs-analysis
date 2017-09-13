# LOGS ANALYSIS PROJECT

## Installations

Dependency: 
- python 2.7
- psycopg2
- VirtualBox
- vagrant

Setup:
1. Make sure that the virtual machine is properly configured using [this config](https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip).
2. Download the [data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and copy the `newsdata.sql` to the `/vagrant` shared directory.
3. Load the data with `psql -d news -f newsdata.sql` and make sure that we can connect to and query from the `news` database.
4. Copy the `queries.py` source code to `/vagrant` shared directory.

## Usage

From within the virtual machine, run the Python code `queries.py` to obtain insights
```shell
$vagrant@vagrant:/vagrant$python queries.py
```

Or open the `solution.md` in browser for a sample output of what the solution could look like.

## Notes
The queries rely on this view to work:
```sql
CREATE VIEW top_articles AS
    SELECT authors.id as author_id, articles.title, top_views.views FROM
        (SELECT regexp_replace(path, '/(article/)?', '') AS slug, count(path) AS views
        FROM log
        GROUP BY path) as top_views, articles, authors
    WHERE top_views.slug = articles.slug AND articles.author = authors.id;
```
where the view was extracted from (mostly) the log table with the `path` column transfomed into related `slug` in the `articles` table.

Program designs:
- SQL queries were hand tested and inserted into the Python source code
- The Python code should then be used to direct the DB-API and present results
- No manipulation other than cosmetic was applied on the queried data
- Further customizations, features could be developed on top of the simple source code:
	+ Divide into separate functionalities: query popular articles / authors
	+ Inspect logs