from wagtail.search.backends.elasticsearch8 import (Elasticsearch8SearchQueryCompiler, Elasticsearch8SearchBackend)

class ElasticsearchQueryCompilerCustom(Elasticsearch8SearchQueryCompiler):
    def _compile_plaintext_query(self, *args, **kwargs):
        """Add the `fuzziness` parameter to all `match` & `match_multi` queries."""
        query = super()._compile_plaintext_query(*args, **kwargs)

        # The query is a dictionary with one key for the query type.
        # Either "match" or "match_multi"
        query_type = list(query.keys())[0]
        query[query_type]['fuzziness'] = 2
        
        return query
    
class CustomSearchBackend(Elasticsearch8SearchBackend):
    """Copy of the Elasticsearch6SearchBackend with a custom query class."""
    query_compiler_class = ElasticsearchQueryCompilerCustom
    

SearchBackend = CustomSearchBackend