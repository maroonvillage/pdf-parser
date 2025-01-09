import csv
import json
import logging
from typing import Dict, Any, List

def json_to_csv_table_layout(json_data: Dict[str, Any], output_file_path: str) -> None:
    """
    Parses JSON data representing a table and saves it to a CSV file, attempting to match the visual layout of the table.

    Parameters:
        json_data (Dict[str, Any]): The JSON data representing a table with categories and subcategories.
        output_file_path (str): The path to save the CSV file.
    """
    log = logging.getLogger(__name__)
    try:
        if not json_data:
            log.warning("The json data is empty.")
            return

        title = json_data.get("title", "No Title")
        columns = json_data.get("columns", [])
        rows = json_data.get("rows", [])

        with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([title]) #Write title first
            writer.writerow(columns) #Write header columns

            if rows:
                current_category = ""
                for row in rows:
                   category = row.get("Categories", "")
                   subcategory = row.get("Subcategories", "")
                   if category:
                        current_category = category
                        writer.writerow([category, subcategory])
                   else:
                        writer.writerow([current_category, subcategory])
         
            
            log.info(f"Successfully wrote json data to csv file: {output_file_path}")
    except FileNotFoundError as e:
         log.error(f"FileNotFoundError: {e} when saving to file: {output_file_path}")
    except Exception as e:
        log.error(f"An unexpected error occurred: {e} when saving data to csv. JSON Data: {json_data}. Error: {e}")

if __name__ == '__main__':
   # Example Usage
    sample_json = {
    "title": "Table 1: Categories and subcategories for the GOVERN function.",
    "columns": [
      "Categories",
      "Subcategories"
    ],
    "rows": [
      {
        "Categories": "GOVERN 1:",
        "Subcategories": "GOVERN 1.1: Legal and regulatory requirements involving Al"
      },
      {
        "Categories": "managing of Al risks are in place,",
        "Subcategories": "to determine the needed level of risk management activities based on the organization’s risk tolerance."
      },
      {
        "Categories": "transparent, and implemented\n effectively.",
        "Subcategories": "GOVERN 1.4: The risk management process and its outcomes are established through transparent policies, procedures, and other controls based on organizational risk priorities."
      },
      {
        "Categories": "",
        "Subcategories": "GOVERN 1.5: Ongoing monitoring and periodic review of the risk management process and its outcomes are planned and or- ganizational roles and responsibilities clearly defined, including determining the frequency of periodic review."
      },
      {
        "Categories": "",
        "Subcategories": "GOVERN 1.6: Mechanisms are in place to inventory Al systems and are resourced according to organizational risk priorities."
      },
      {
        "Categories": "",
        "Subcategories": "GOVERN 1.7: Processes and procedures are in place for decom- missioning and phasing out Al systems safely and in a man- ner that does not increase risks or decrease the organization’s trustworthiness."
      },
      {
        "Categories": "GOVERN 2: Accountability\n structures are in place so that the",
        "Subcategories": "GOVERN 2.1: Roles and responsibilities and lines of communi- cation related to mapping, measuring, and managing Al risks are documented and are clear to individuals and teams throughout the organization."
      },
      {
        "Categories": "appropriate teams and individuals are empowered,\n responsible, and trained for mapping, measuring, and managing Al risks.",
        "Subcategories": "GOVERN 2.2: The organization’s personnel and partners receive Al risk management training to enable them to perform their du- ties and responsibilities consistent with related policies, proce- dures, and agreements."
      },
      {
        "Column 1": "GOVERN 2.3: Executive leadership of the organization takes re- sponsibility for decisions about risks associated with Al system development and deployment."
      },
      {
        "Categories": "GOVERN 3: Workforce diversity, equity, inclusion, and accessibility",
        "Subcategories": "GOVERN 3.1: Decision-making related to mapping, measuring, and managing Al risks throughout the lifecycle is informed by a diverse team (e.g., diversity of demographics, disciplines, expe- rience, expertise, and backgrounds)."
      },
      {
        "Categories": "processes are prioritized in the mapping,\n measuring, and managing of Al risks throughout the lifecycle.",
        "Subcategories": "GOVERN 3.2: Policies and procedures are in place to define and differentiate roles and responsibilities for human-Al configura- tions and oversight of Al systems."
      },
      {
        "Categories": "GOVERN 4: Organizational\n teams are committed to a culture",
        "Subcategories": "GOVERN 4.1: Organizational policies and practices are in place to foster a critical thinking and safety-first mindset in the design, development, deployment, and uses of Al systems to minimize potential negative impacts."
      },
      {
        "Categories": "that considers and communicates Al risk",
        "Subcategories": "GOVERN 4.2: Organizational teams document the risks and po- tential impacts of the AI technology they design, develop, deploy, evaluate, and use, and they communicate about the impacts more broadly.\n 4.3: Organizational practices in place enable Al"
      },
      {
        "Categories": "GOVERN 5: Processes are in place for robust engagement with relevant AT actors.",
        "Subcategories": "GOVERN 5.1: Organizational policies and practices are in place to collect, consider, prioritize, and integrate feedback from those external to the team that developed or deployed the AI system regarding the potential individual and societal impacts related to Al risks."
      },
      {
        "Column 1": "GOVERN 5.2: Mechanisms are established to enable the team that developed or deployed Al systems to regularly incorporate adjudicated feedback from relevant Al actors into system design and and implementation."
      },
      {
        "Categories": "GOVERN 6: Policies and procedures are in place to address",
        "Subcategories": "GOVERN 6.1: Policies and procedures are in place that address Al risks associated with third-party entities, including risks of in- fringement of a third-party’s intellectual property or other rights."
      },
      {
        "Categories": "Al risks and benefits arising from third-party software and data and other supply chain issues.",
        "Subcategories": "GOVERN 6.2: Contingency processes are in place to handle failures or incidents in third-party data or Al systems deemed to be high-risk."
      }
    ]
    }
    output_file = "output_table.csv"
    json_to_csv_table_layout(sample_json, output_file)