# Notes about search functionality in Wagtail:

We currently use Wagtail’s database search with Postgres DB, which uses Postgres's built in text-search functionality ([see code here][wg-pg]).  
Although [the Postgres behaviour is configurable (e.g. using custom dictionaries)][pg-ts], we’re using the default set up.

[wg-pg]:https://github.com/wagtail/wagtail/tree/main/wagtail/search/backends/database/postgres
[pg-ts]:https://www.postgresql.org/docs/current/textsearch-intro.html#TEXTSEARCH-INTRO-CONFIGURATIONS

## Default Behaviour
The default behaviour of Postgres text search is:  
It will:
 - ignore common words (e.g. “the”, “and”, “in”)
 - match based word-stem, .e.g. searching for “running”, will also find “runs” and “run”, searching for “tornado” will also find “tornadoes”
 - rank multiple appearances of a word higher than a single appearance
 - rank matches based on configured weights (1 of 4 levels, see below)

It won’t:
 - match synonyms e.g. “amazing”, “brilliant”, “awesome”
 - match typos or incomplete words, e.g. searching for “brill” or “brill**ai**nt” instead of “brilliant”
 - match quoted phrases exactly
 - match unless all the search words are present, e.g. searching for "health board" will only match pages that contain both "health" and "board" (but health can be in the page title and board in the page content, for example)

> NOTE: it seems the current search results are also ordered by most recent created date first (all other ranking factors being equal), perhaps that's explicitly defined somewhere

## Ranking Weights

Wagtail allows you to assign a “boost” value when adding something to the search index. This is then used when calculating the matching score, which is normally used to sort the search results ([as we do for the innovation service website][search-sort])

[search-sort]:../is_homepage/apps/search/views.py#L96 

By default Wagtail set boosts as follows:
 - Matches in page title are ranked highest (boost of 2)
 - Matches elsewhere are ranked equally (boost of 1)

If adjusting boost values for the postgres backend, **it’s best to only use the values 10, 2, 1, or 0.**  This is because Postgres only supports 4 weights, so if you use a greater variety of boosts the end result can be a little hard to predict, as Wagtail will map the boosts to one of the 4 weights.

If you need to troubleshoot what's going on with Wagtail's the boost-weight mapping you can run the Django shell (`python manage.py shell`) and run these commands:

```python
from wagtail.search.backends.database.postgres import weights
weights.BOOSTS_WEIGHTS
# outputs something like [(10, 'A'), (2, 'B'), (1, 'C'), (0, 'D')]
```

There’s a note about this in the [Wagtail docs](https://docs.wagtail.org/en/stable/topics/search/indexing.html#options)



