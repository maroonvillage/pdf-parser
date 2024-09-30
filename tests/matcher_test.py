import spacy
from matcher_patterns import *


def main():

    nlp = spacy.load('en_core_web_sm')
    matcher = Matcher(nlp.vocab)

    #Add matcher patterns 

    ep_list = get_executive_summary_patterns()

    for pattern in ep_list:
        matcher.add("ExecutiveSummaryMethods", [pattern])

    foreward_list = get_foreward_pattern()

    for pattern in foreward_list:
        matcher.add("ForewardMethods", [pattern])  

    intro_list = get_introduction_pattern()

    for pattern in intro_list:
        matcher.add("IntroMethods", [pattern])  

    summary_list = get_summary_pattern()

    for pattern in summary_list:
        matcher.add("SummaryMethods", [pattern])  


    doc = nlp("Pizza")

    matches = matcher(doc)
    if matches:
        print(matches)
    else:
        print("no matches found")


if __name__ == "__main__":
    main() 