from wagtail.search.backends.elasticsearch8 import (Elasticsearch8SearchResults,Elasticsearch8SearchQueryCompiler, Elasticsearch8SearchBackend)
import re

class ElasticsearchQueryCompilerCustom(Elasticsearch8SearchQueryCompiler):
    def _compile_plaintext_query(self, *args, **kwargs):
        """Add the `fuzziness` parameter to all `match` & `match_multi` queries."""
        query = super()._compile_plaintext_query(*args, **kwargs)

        if query['multi_match'] != None:
            query['multi_match']['fuzziness'] = 0
            query['multi_match']['prefix_length'] = 2

        return query
    
class CustomSearchResults(Elasticsearch8SearchResults):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def annotate_terms_occurrences(self, field_name):
        clone = self._clone()
        clone.terms_occurrences = field_name
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
                
        '''
        Creates object with occurrences count per search term, by document index. i.e.:
        {
            61: {'mental': 5, 'health': 1},
            15: {'mental': 0, 'health': 1}
        }
        '''
        
        terms_occurrences = {
            str(pk): 
                {
                    'terms': set(re.findall("<em>(.*?)</em>", ' '.join(highlights[pk]))),
                    'occurrences': { 
                        term : 
                            len([m.start() for m in re.finditer(f'<em>{term}</em>', ' '.join(highlights[str(pk)]), re.IGNORECASE)]) 
                            for term 
                            in set(re.findall("<em>(.*?)</em>", ' '.join(highlights[pk]).lower()))
                    },
                }
                for pk in pks}
        
        # Sort each document(pk) occurrences by descending order
        for k,v in terms_occurrences.items():
            terms_occurrences[k]['occurrences'] = dict(sorted(v['occurrences'].items(), key=lambda item: item[1],reverse=True))

        # Initialise results dictionary
        results = {str(pk): None for pk in pks}

        # Find objects in database and add them to dict
        for obj in self.query_compiler.queryset.filter(pk__in=pks):

            results[str(obj.pk)] = obj

            if self._score_field:
                setattr(obj, self._score_field, scores.get(str(obj.pk)))
            
            setattr(obj, 'terms_occurrences', terms_occurrences.get(str(obj.pk)))

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