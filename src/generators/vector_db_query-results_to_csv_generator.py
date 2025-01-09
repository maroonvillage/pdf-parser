import csv
import json
import logging
from typing import Dict, Any, List, Optional

def json_to_csv_with_max_score(json_data: Dict[str, Any], output_file_path: str) -> None:
    """
    Parses JSON data representing search results and saves the title and the content with the highest score for each section, to a CSV file.

    Args:
        json_data (Dict[str, Any]): The JSON data containing search results.
        output_file_path (str): The path to save the CSV file.
    """
    log = logging.getLogger(__name__)
    try:
        if not json_data:
            log.warning("The json data is empty.")
            return

        title = json_data.get("title", "No Title")
        sections = json_data.get("sections", [])

        with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Title", "Content"])
            
            if sections:
               
                best_content = ""
                max_score = 0
                for section in sections:
                    content = section.get('content',"")
                    score = section.get("score", 0)
                    if score > max_score:
                        max_score = score
                        best_content = content

                writer.writerow([title, best_content])
            else:
                log.warning("No sections found in the json data.")

         
        log.info(f"Successfully wrote json data to csv file: {output_file_path}")
    except FileNotFoundError as e:
        log.error(f"FileNotFoundError: {e} when saving to file: {output_file_path}")
    except Exception as e:
         log.error(f"An unexpected error occurred: {e} when processing data from the JSON: {json_data}. File: {output_file_path}")
if __name__ == '__main__':
    # Example Usage
    sample_json = {
      "title": "Innovative_Regulation",
      "sections": [
        {
          "section_id": 0,
          "content": "Executive Summary\nPart 1: Foundational Information Artificial intelligence (AI) technologies have significant potential to transform society and\npeople\u2019s lives \u2013 from commerce and health to transportation and cybersecurity to the envi-\nronment and our planet. AI technologies can drive inclusive economic growth and support\nscientific advancements that improve the conditions of our world. AI technologies, how-\never, also pose risks that can negatively impact individuals, groups, organizations, commu-\nnities, society, the environment, and the planet. Like risks for other types of technology, AI\nrisks can emerge in a variety of ways and can be characterized as long- or short-term, high-\nor low-probability, systemic or localized, and high- or low-impact. The AI RMF refers to an AI system as an engineered or machine-based system that\ncan, for a given set of objectives, generate outputs such as predictions, recommenda-\ntions, or decisions influencing real or virtual environments. AI systems are designed\nto operate with varying levels of autonomy (Adapted from: OECD Recommendation\non AI:2019; ISO/IEC 22989:2022). While there are myriad standards and best practices to help organizations mitigate the risks\nof traditional software or information-based systems, the risks posed by AI systems are in\nmany ways unique (See Appendix B). AI systems, for example, may be trained on data that\ncan change over time, sometimes significantly and unexpectedly, affecting system function-\nality and trustworthiness in ways that are hard to understand. AI systems and the contexts\nin which they are deployed are frequently complex, making it difficult to detect and respond\nto failures when they occur. AI systems are inherently socio-technical in nature, meaning\nthey are influenced by societal dynamics and human behavior. AI risks \u2013 and benefits \u2013\ncan emerge from the interplay of technical aspects combined with societal factors related\nto how a system is used, its interactions with other AI systems, who operates it, and the\nsocial context in which it is deployed. These risks make AI a uniquely challenging technology to deploy and utilize both for orga-\nnizations and within society. Without proper controls, AI systems can amplify, perpetuate,\nor exacerbate inequitable or undesirable outcomes for individuals and communities. With\nproper controls, AI systems can mitigate and manage inequitable outcomes. AI risk management is a key component of responsible development and use of AI sys-\ntems. Responsible AI practices can help align the decisions about AI system design, de-\nvelopment, and uses with intended aim and values. Core concepts in responsible AI em-\nphasize human centricity, social responsibility, and sustainability. AI risk management can\ndrive responsible uses and practices by prompting organizations and their internal teams\nwho design, develop, and deploy AI to think more critically about context and potential\nor unexpected negative and positive impacts. Understanding and managing the risks of AI\nsystems will help to enhance trustworthiness, and in turn, cultivate public trust. Page 1\n",
          "score": 0.79349184
        },
        {
          "section_id": 21,
          "content": "5.1 Govern\nThe GOVERN function: \u2022 cultivates and implements a culture of risk management within organizations design- ing, developing, deploying, evaluating, or acquiring AI systems; \u2022 outlines processes, documents, and organizational schemes that anticipate, identify,\nand manage the risks a system can pose, including to users and others across society\n\u2013 and procedures to achieve those outcomes; \u2022 incorporates processes to assess potential impacts;\n\u2022 provides a structure by which AI risk management functions can align with organi- zational principles, policies, and strategic priorities; \u2022 connects technical aspects of AI system design and development to organizational\nvalues and principles, and enables organizational practices and competencies for the\nindividuals involved in acquiring, training, deploying, and monitoring such systems;\nand \u2022 addresses full product lifecycle and associated processes, including legal and other issues concerning use of third-party software or hardware systems and data. Page 21\n",
          "score": 0.803890944
        },
        {
          "section_id": 18,
          "content": "4. Effectiveness of the AI RMF\nPart 2: Core and Profiles Evaluations of AI RMF effectiveness \u2013 including ways to measure bottom-line improve-\nments in the trustworthiness of AI systems \u2013 will be part of future NIST activities, in\nconjunction with the AI community. Organizations and other users of the Framework are encouraged to periodically evaluate\nwhether the AI RMF has improved their ability to manage AI risks, including but not lim-\nited to their policies, processes, practices, implementation plans, indicators, measurements,\nand expected outcomes. NIST intends to work collaboratively with others to develop met-\nrics, methodologies, and goals for evaluating the AI RMF\u2019s effectiveness, and to broadly\nshare results and supporting information. Framework users are expected to benefit from: \u2022 enhanced processes for governing, mapping, measuring, and managing AI risk, and clearly documenting outcomes; \u2022 improved awareness of the relationships and tradeoffs among trustworthiness char- acteristics, socio-technical approaches, and AI risks; \u2022 explicit processes for making go/no-go system commissioning and deployment deci- sions; \u2022 established policies, processes, practices, and procedures for improving organiza- tional accountability efforts related to AI system risks; \u2022 enhanced organizational culture which prioritizes the identification and management\nof AI system risks and potential impacts to individuals, communities, organizations,\nand society; \u2022 better information sharing within and across organizations about risks, decision-\nmaking processes, responsibilities, common pitfalls, TEVV practices, and approaches\nfor continuous improvement; \u2022 greater contextual knowledge for increased awareness of downstream risks;\n\u2022 strengthened engagement with interested parties and relevant AI actors; and\n\u2022 augmented capacity for TEVV of AI systems and associated risks. Page 19\n",
          "score": 0.863126874
        },
        {
          "section_id": 8,
          "content": "1.2.4 Organizational Integration and Management of Risk\nAI risks should not be considered in isolation. Different AI actors have different responsi-\nbilities and awareness depending on their roles in the lifecycle. For example, organizations\ndeveloping an AI system often will not have information about how the system may be\nused. AI risk management should be integrated and incorporated into broader enterprise\nrisk management strategies and processes. Treating AI risks along with other critical risks,\nsuch as cybersecurity and privacy, will yield a more integrated outcome and organizational\nefficiencies. The AI RMF may be utilized along with related guidance and frameworks for managing\nAI system risks or broader enterprise risks. Some risks related to AI systems are common\nacross other types of software development and deployment. Examples of overlapping risks\ninclude: privacy concerns related to the use of underlying data to train AI systems; the en-\nergy and environmental implications associated with resource-heavy computing demands;\nsecurity concerns related to the confidentiality, integrity, and availability of the system and\nits training and output data; and general security of the underlying software and hardware\nfor AI systems. Page 8\n",
          "score": 0.873764038
        },
        {
          "section_id": 12,
          "content": "3.2 Safe\nAI systems should \u201cnot under defined conditions, lead to a state in which human life,\nhealth, property, or the environment is endangered\u201d (Source: ISO/IEC TS 5723:2022). Safe\noperation of AI systems is improved through: \u2022 responsible design, development, and deployment practices;\n\u2022 clear information to deployers on responsible use of the system;\n\u2022 responsible decision-making by deployers and end users; and\n\u2022 explanations and documentation of risks based on empirical evidence of incidents. Different types of safety risks may require tailored AI risk management approaches based\non context and the severity of potential risks presented. Safety risks that pose a potential\nrisk of serious injury or death call for the most urgent prioritization and most thorough risk\nmanagement process. Page 14\n",
          "score": 0.887818098
        }
      ]
    }
    output_file = "output_search_results.csv"
    json_to_csv_with_max_score(sample_json, output_file)