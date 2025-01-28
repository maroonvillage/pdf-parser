from spacy.matcher import Matcher
import spacy
import logging
from typing import List, Dict

def get_executive_summary_patterns():

    executive_summary_pattern = [{"LOWER": "executive"}, {"LOWER": "summary"}]

    pattern_list = [executive_summary_pattern]

    return pattern_list

def get_foreword_pattern():

    executive_pattern = [{"LOWER": "foreword"}, {"OP": "?"}]
    pattern_list = [executive_pattern]

    return pattern_list

def get_introduction_pattern():

    introduction_pattern = [{"LOWER": "introduction"}, {"OP": "?"}]
    pattern_list = [introduction_pattern]

    return pattern_list

def get_summary_pattern():

    summary_pattern = [{"LOWER": "summary"}, {"OP": "?"}]
    pattern_list = [summary_pattern]

    return pattern_list

#Not being used
def get_figure_pattern():

    figure_pattern = [{"LOWER": "figure"}, {"OP": "?"}]
    fig_pattern = [{"LOWER": "fig."}, {"OP": "?"}]
    pattern_list = [fig_pattern, figure_pattern]

    return pattern_list

def get_bibliography_pattern():
    bibliography_pattern = [{"LOWER": "bibliography"}, {"OP": "?"}]
    pattern_list = [bibliography_pattern]

    return pattern_list

def get_references_pattern():
    references_pattern = [{"LOWER": "bibliography"}, {"OP": "?"}]
    pattern_list = [references_pattern]

    return pattern_list

def create_pattern(terms: List[str]) -> List[Dict]:
    """Creates a list of Spacy patterns from a list of terms.

    Parameters:
       terms (List[str]): A list of terms.

    Returns:
       List[Dict]: A list of Spacy patterns.
    """
    return [[{"LOWER": term, "OP": "?"} for term in terms]]


def get_matcher(nlp: spacy.language.Language, config: Dict=None) -> Matcher:
    """
    Initializes and configures a spaCy Matcher object with patterns for different document sections.

    Parameters:
       nlp (spacy.language.Language): A spaCy language model object.
       config (Dict): A configuration dictionary containing a list of patterns.
    Returns:
       Matcher: A spaCy Matcher object with added patterns.
    """
    log = logging.getLogger(__name__)
    matcher = Matcher(nlp.vocab)

    if not config:
        config = {
            "patterns": {
                "ExecutiveSummaryMethods": ["executive", "summary"],
                "ForewordMethods": ["foreword"],
                "IntroMethods": ["introduction"],
                "SummaryMethods": ["summary"],
                "BibliographyMethods": ["bibliography"],
                "ReferencesMethods": ["references"]
                }
            }
    
    for pattern_name, terms in config["patterns"].items():
        patterns = create_pattern(terms)
        for pattern in patterns:
           matcher.add(pattern_name, [pattern])
           log.debug(f"Added pattern {pattern} with name '{pattern_name}' to matcher")
    return matcher