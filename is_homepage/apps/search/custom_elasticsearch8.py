from wagtail.search.backends.elasticsearch8 import (Elasticsearch8SearchResults,Elasticsearch8SearchQueryCompiler, Elasticsearch8SearchBackend)
import re

class ElasticsearchQueryCompilerCustom(Elasticsearch8SearchQueryCompiler):
    def _compile_plaintext_query(self, *args, **kwargs):
        """Add the `fuzziness` parameter to all `match` & `match_multi` queries."""
        query = super()._compile_plaintext_query(*args, **kwargs)

        # The query is a dictionary with one key for the query type.
        # Either "match" or "match_multi"
        query_type = list(query.keys())[0]
        query[query_type]['fuzziness'] = 1
        return query
    
class CustomSearchResults(Elasticsearch8SearchResults):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def annotate_terms_occurences(self, field_name):
        clone = self._clone()
        clone.terms_occurences = field_name
        return clone
    
    # custom implementation of class    
    def _get_results_from_hits(self, hits):
        """
        Yields Django model instances from a page of hits returned by Elasticsearch
        """
        # Get pks from results
            
        pks = [hit["fields"]["pk"][0] for hit in hits]
        scores = {str(hit["fields"]["pk"][0]): hit["_score"] for hit in hits}
        highlights = {str(hit["fields"]["pk"][0]): hit["highlight"]['_all_text'] for hit in hits}

        query_term = self.query_compiler.query.query_string
        
        '''
        Creates object with occurences count per search term, by document index. i.e.:
        {
            61: {'mental': 5, 'health': 1},
            15: {'mental': 0, 'health': 1}
        }
        '''
        terms_occurences = {str(pk): { term : len([m.start() for m in re.finditer(f'<em>{term}', ' '.join(highlights[str(pk)]), re.IGNORECASE)]) for term in query_term.split()} for pk in pks}

        # Initialise results dictionary
        results = {str(pk): None for pk in pks}

        # Find objects in database and add them to dict
        for obj in self.query_compiler.queryset.filter(pk__in=pks):

            results[str(obj.pk)] = obj

            if self._score_field:
                setattr(obj, self._score_field, scores.get(str(obj.pk)))
            
            setattr(obj, 'terms_occurences', terms_occurences.get(str(obj.pk)))

        # Yield results in order given by Elasticsearch
        for pk in pks:
            result = results[str(pk)]
            if result:
                yield result
    
    
    def _backend_do_search(self, body, **kwargs):

        ''' 
        Retrieves field with highlighted terms
        '''
        body['highlight'] = {
            'fields': [
                {
                    '_all_text': {"number_of_fragments" : 0}
                }           
            ], 
            'require_field_match': True
        }
                
        search = self.backend.es.search(**body, **kwargs)

        return search

class CustomSearchBackend(Elasticsearch8SearchBackend):
    """Copy of the Elasticsearch8SearchBackend with custom classes."""
    query_compiler_class = ElasticsearchQueryCompilerCustom
    results_class = CustomSearchResults

    
SearchBackend = CustomSearchBackend