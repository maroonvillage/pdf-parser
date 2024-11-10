from spacy.matcher import Matcher
import spacy

def get_executive_summary_patterns():


    executive_summary_pattern = [{"LOWER": "executive"}, {"LOWER": "summary"}]

    pattern_list = [executive_summary_pattern]

    return pattern_list

def get_foreward_pattern():

    executive_pattern = [{"LOWER": "foreward"}, {"OP": "?"}]
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