""" import spacy
from .matcher_patterns import *
from spacy.matcher import Matcher
from .matcher_patterns import get_executive_summary_patterns, get_foreword_pattern, get_figure_pattern, \
    get_bibliography_pattern, get_executive_summary_patterns, get_introduction_pattern, get_summary_pattern

 """
#Unit Tests



def main():

    """ nlp = spacy.load('en_core_web_sm')
    matcher = Matcher(nlp.vocab)

    #Add matcher patterns 

    ep_list = get_executive_summary_patterns()

    for pattern in ep_list:
        matcher.add("ExecutiveSummaryMethods", [pattern])

    foreward_list = get_foreword_pattern()

    for pattern in foreward_list:
        matcher.add("ForewardMethods", [pattern])  

    intro_list = get_introduction_pattern()

    for pattern in intro_list:
        matcher.add("IntroMethods", [pattern])  

    summary_list = get_summary_pattern()

    for pattern in summary_list:
        matcher.add("SummaryMsethods", [pattern])  


    doc = nlp("Pizza")

    matches = matcher(doc)
    if matches:s
        print(matches)
    else:
        print("no matches found") """


if __name__ == "__main__":
    main() 