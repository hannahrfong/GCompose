from .ner import five_shot_ner_paragraph, five_shot_ner_output, six_shot_ner_paragraph, six_shot_ner_output, eleven_shot_ner_paragraph, eleven_shot_ner_output
from ...utils.llm_utils import convert_format_to_template

ner_conditioned_re_system = """You are an open information extraction (OpenIE) model. 

Task: Extract all factual relations from the given email in the form of RDF triples: (subject, predicate, object). These triples will be used to build a knowledge graph that supports multi-hop reasoning for email text completion. Therefore, both correctness (precision) and completeness (recall) are important in the triple extraction process. 

CaRB Triple Quality Criteria: 
Each triple must satisfy the following four criteria:
1. Completeness - Extract all triples from the text.
2. Assertedness - Only extract triples that are explicitly or implicitly implied by the original text.
3. Informativeness - Include the maximum amount of relevant information in each argument (i.e., subject or object).
4. Atomicity - Each triple must be an indivisible unit. Whenever possible, extract multiple atomic triples from a text that has conjunctions.

Triple Extraction Guidelines: 
1. Process the email one sentence at a time. Extract all triples from each sentence before moving on.
2. For simple sentences, identify the relation along with its corresponding subject and object to form a single atomic triple that satisfies the CaRB criteria.
3. For complex and compound sentences:
3.1 Extract triples from the outermost fact to the innermost fact, ensuring that the innermost facts are atomic triples that satisfy the CaRB criteria.
3.2 If multiple clauses are joined only for structural convenience (e.g., coordination with "and" or "but"), extract them separately as independent triples.
3.3 If one clause modifies or governs another (e.g., via if, when, because, resulting in, said that, before, after, to, etc.), extract a higher-level triple that captures this semantic relation.

Triple Extraction Rules:
1. Named entities:
1.1 Each triple must contain at least one, and preferably two, named entities from the provided list. 
1.2 If the fact involves no named entity, use a noun phrase consistent with previously extracted ones to maintain connectivity. 
1.3 Only create a new noun phrase if it represents a completely new entity.
2. Clearly resolve nouns and pronouns to their specific names based on the message or metadata.
3. Use exact wording from the original email unless modification is necessary for atomicity or clarity.
4. Include prepositions in the predicate instead of starting the object with a preposition.
5. For disconnected facts that are not explicitly linked to other facts, add inferred triples that connect it logically to other entities (e.g., link an amount to the payer/payee).
6. Do NOT include trivial triples about the structure of the email itself (e.g., "Kate sent email to Rhonda").

Examples

Example 1
Input: "However, for October 2000, the plant was down the majority of the month and ENA sold off the supply, resulting in ENA owing money to Tenaska IV."
Output: {
  "triples": [
    ["Cleburne plant", "was down", "the majority of October 2000"], 
    ["ENA", "sold off", "supply in October 2000"],
    ["ENA sold off the supply", "resulting in", "ENA owing money to Tenaska IV"], 
    ["ENA", "owes money to", "Tenaska IV"], 
    ["ENA", "owes to Tenaska IV", "$1,798,389.73"]
  ]
}
Notes:
* The two main clauses ("the plant was down…" and "ENA sold off the supply…") are two complete, standalone facts on their own, so no triple combines them.
* The relation "resulting in" expresses a dependent causal connection, so it is represented as a higher-level triple ["ENA sold off the supply", "resulting in", "ENA owing money to Tenaska IV"].
* Atomic triples for each clause are extracted to capture the underlying atomic facts (e.g., ["ENA", "owes money to", "Tenaska IV"]).
* Entity resolution is performed in "majority of the month" to "majority of October 2000"
* Exact wording is preserved as much as possible (e.g., ["ENA sold off the supply", "resulting in", "ENA owing money to Tenaska IV"]), but normalization is allowed to form atomic facts (e.g., ["ENA", "owes money to", "Tenaska IV"]). 
* The inferred triple ["ENA", "owes to Tenaska IV", "$1,798,389.73"] was added to connect the fact to the amount named entity.
* Each triple contains 1-2 named entities.

Example 2
Input: "We actually owe $1,798,389.73, but I need to net the Tenaska IV sales with the purchase to clear those receivables."
Output: {
  "triples": [
    ["ENA", "owes to Tenaska IV", "$1,798,389.73"],
    ["Megan Parker", "needs to net", "Tenaska IV sales with the purchase deal to clear receivables"],
    ["Purchase deal", "is needed for", "Netting Tenaska IV sales"],
    ["Netting Tenaska IV sales", "is needed to clear", "receivables"]
  ]
}
Notes:
* The noun phrase "Netting Tenaska IV sales" was created to represent an atomic process described in the sentence and is reused across triples for graph connectivity. 

Output Format: Convert the input into a JSON dictionary with the following two keys:
– "named entities": list of extracted entity strings (given or revalidated)
– "triples": list of RDF triples (subject, predicate, object)
"""


ner_conditioned_re_frame = """Convert the paragraph into a JSON dict, it has a named entity list and a triple list.
Email:
```
{passage}
```

{named_entity_json}
"""

five_shot_triples_output = [
  [
    "Megan Parker",
    "reports",
    "Tenaska IV 10/00"
  ],
  [
    "Tenaska IV 10/00",
    "is report for",
    "Tenaska IV"
  ],
  [
    "Megan Parker",
    "has",
    "actuals for Tenaska IV"
  ],
  [
    "Actuals for Tenaska IV",
    "include",
    "two volumes"
  ],
  [
    "Two volumes",
    "include",
    "larger volume"
  ],
  [
    "Larger volume",
    "is",
    "1,395,000"
  ],
  [
    "Larger volume",
    "is",
    "45,000/day"
  ],
  [
    "Deal 514353",
    "has",
    "fine demand rate"
  ],
  [
    "Deal 514353",
    "is part of",
    "Tenaska IV 10/00"
  ],
  [
    "Deal 514353",
    "has problem with",
    "settlements"
  ],
  [
    "Deal 514353",
    "is showing up with",
    "Jan 2003 delivery date"
  ],
  [
    "Megan Parker",
    "thinks",
    "demand fee needs to be on 10/1 only"
  ],
  [
    "Demand fee",
    "needs to be only on",
    "10/1"
  ],
  [
    "Demand fee",
    "is on a line with a date of",
    "10/1/00 to 12/31/36"
  ],
  [
    "Megan Parker",
    "thinks",
    "demand fee on 10/1/00 to 12/31/36 confuses system"
  ],
  [
    "10/1/00 to 12/31/36",
    "confuses",
    "the system"
  ],
  [
    "ENA",
    "still needs",
    "purchase deal for Tenaska IV"
  ],
  [
    "Purchase deal for Tenaska IV",
    "should have demand fee of",
    "$2,571,135.73"
  ],
  [
    "$2,571,135.73",
    "is booked to",
    "Cleburne desk"
  ],
  [
    "ENA",
    "owes to Tenaska IV",
    "$1,798,389.73"
  ],
  [
    "Megan Parker",
    "needs to net",
    "Tenaska IV sales with the purchase deal to clear receivables"
  ],
  [
    "Purchase deal",
    "is needed for",
    "Netting Tenaska IV sales"
  ],
  [
    "Netting Tenaska IV sales",
    "is needed to clear",
    "receivables"
  ],
  [
    "Megan Parker",
    "is called daily for an update by",
    "James Armstrong"
  ],
  [
    "Megan Parker",
    "attaches spreadsheet",
    "so Daren J Farmer can see the numbers"
  ],
  [
    "Megan Parker",
    "attaches",
    "spreadsheet"
  ],
  [
    "ENA",
    "will be in most cases",
    "net buyer from Tenaska IV"
  ],
  [
    "Net buyer from Tenaska IV",
    "applies to",
    "Cleburne plant"
  ],
  [
    "Cleburne plant",
    "was down",
    "the majority of October 2000"
  ],
  [
    "ENA",
    "sold off",
    "supply in October 2000"
  ],
  [
    "ENA sold off the supply",
    "resulting in",
    "ENA owing money to Tenaska IV"
  ],
  [
    "ENA",
    "owes money to",
    "Tenaska IV"
  ],
  [
    "ENA",
    "owes to Tenaska IV",
    "$1,798,389.73"
  ],
  [
    "Daren J Farmer",
    "created",
    "deal 529856"
  ],
  [
    "Deal 529856",
    "has demand of",
    "$1,798,389.73"
  ],
  [
    "$1,798,389.73",
    "is the",
    "income on the Cleburne desk"
  ],
  [
    "$1,798,389.73",
    "is the income on the",
    "Cleburne desk"
  ],
  [
    "ENA",
    "needs to pass",
    "income on the Cleburne desk"
  ],
  [
    "Income on the Cleburne desk",
    "must be passed to",
    "Tenaska IV"
  ],
  [
    "Daren J Farmer",
    "asks",
    "if ENA needs to wire $1,798,389.73 to Tenaska IV"
  ],
  [
    "ENA",
    "needs to wire to Tenaska IV",
    "$1,798,389.73"
  ],
  [
    "Daren J Farmer",
    "asks",
    "if there is another way to pay $1,798,389.73 from ENA to Tenaska IV"
  ],
  [
    "Passing income to Tenaska IV",
    "applies to",
    "October 2000"
  ],
  [
    "Passing income to Tenaska IV",
    "could possibly happen",
    "again in future"
  ],
  [
    "Megan Parker",
    "is instructed not to pay",
    "$1,798,389.73"
  ],
  [
    "$1,798,389.73",
    "will be paid depending on",
    "hearing from Greg Whiting, Troy Klussmann, and James Armstrong"
  ],
  [
    "ENA",
    "must receive dollars from the spot sales",
    "before ENA reimburses Tenaska IV"
  ],
  [
    "ENA",
    "must receive",
    "dollars from the spot sales"
  ],
  [
    "ENA",
    "reimburses",
    "Tenaska IV"
  ],
  [
    "Demand fee",
    "is the",
    "best solution"
  ],
  [
    "Demand fee",
    "can be used to create",
    "receivable/payable with Tenaska"
  ],
  [
    "Demand fee can be used to create receivable/payable with Tenaska",
    "depending on",
    "which way the calculation goes each month"
  ],
  [
    "Daren J Farmer",
    "asks",
    "how PMA entries should be handled once the fee is calculated and the deal is put in the system"
  ],
  [
    "PMA entries",
    "should be handled",
    "once the fee is calculated"
  ],
  [
    "PMA entries",
    "should be handled",
    "once the deal is put in the system"
  ],
  [
    "Jim Pond",
    "attaches",
    "schedule detailing what is on the general ledger for Cleburne as of today"
  ],
  [
    "Schedule detailing what is on the general ledger for Cleburne as of today",
    "will change",
    "by the end of the month"
  ],
  [
    "Discrepancies",
    "exist between",
    "Megan Parker's calculations and general ledger for Cleburne"
  ],
  [
    "UA4",
    "is on",
    "Jim Pond's schedule"
  ],
  [
    "ENA",
    "books",
    " entry to balance desk"
  ],
  [
    "ENA",
    "books",
    " entry to balance desk unless the buy/sells are volumetrically balanced"
  ],
  [
    "buy/sells",
    "are",
    "volumetrically balanced"
  ],
  [
    "Entry to balance desk",
    "changes",
    "calculation of what is due from/to Tenaska IV"
  ],
  [
    "Jim Pond",
    "asks",
    "if UA4 entry should be recorded for Cleburne"
  ],
  [
    "UA4 entry",
    "should be recorded for",
    "Cleburne"
  ],
  [
    "Jim Pond",
    "asks",
    "if UA4 entry is addressed in agreement with Tenaska"
  ],
  [
    "UA4 entry",
    "is addressed in agreement with",
    "Tenaska"
  ],
  [
    "Volumes",
    "can be adjusted as usual through",
    "system"
  ],
  [
    "Volumes",
    "can be adjusted with",
    "PMA’s"
  ]
]

six_shot_triples_output = [
  [
    "UA4",
    "is on",
    "Jim Pond's schedule"
  ],
  [
    "ENA",
    "books",
    "entry to balance desk"
  ],
  [
    "ENA",
    "books",
    " entry to balance desk unless the buy/sells are volumetrically balanced"
  ],
  [
    "buy/sells",
    "are",
    "volumetrically balanced"
  ],
  [
    "Entry to balance desk",
    "changes",
    "calculation of what is due from/to Tenaska IV"
  ],
  [
    "Jim Pond",
    "asks",
    "if UA4 entry should be recorded for Cleburne"
  ],
  [
    "UA4 entry",
    "should be recorded for",
    "Cleburne"
  ],
  [
    "Jim Pond",
    "asks",
    "if UA4 entry is addressed in agreement with Tenaska"
  ],
  [
    "UA4 entry",
    "is addressed in agreement with",
    "Tenaska"
  ],
  [
    "Volumes",
    "can be adjusted as usual through",
    "system"
  ],
  [
    "Volumes",
    "can be adjusted with",
    "PMA’s"
  ],
  [
    "Daren J Farmer",
    "can adjust",
    "demand fee on Sitara ticket"
  ],
  [
    "Demand fee",
    "is on",
    "Sitara ticket"
  ],
  [
    "Daren J Farmer",
    "is not able to follow",
    "Jim Pond’s UA4 calculation"
  ],
  [
    "Imbalance payback",
    "occurred throughout",
    "September"
  ],
  [
    "Imbalance payback",
    "occurred throughout",
    "October"
  ],
  [
    "Imbalance payback",
    "should have been pathed to",
    "Lone Star transport k in Unify"
  ],
  [
    "Lone Star transport k",
    "is in",
    "Unify"
  ],
  [
    "Daren J Farmer",
    "asks",
    "if imbalance payback is in UA4 calculation"
  ],
  [
    "Imbalance payback",
    "is in",
    "UA4 calculation"
  ],
  [
    "Williams",
    "had been trying to make up",
    "volumes from prior periods"
  ],
  [
    "Williams’ volume",
    "came in greater than",
    "booked"
  ],
  [
    "Williams’ volume",
    "came in greater than booked",
    "because Williams had been trying to make up volumes from prior periods"
  ],
  [
    "Williams’ volume",
    "is",
    "William’s gas"
  ],
  [
    "William’s gas",
    "is mainly from",
    "El Paso"
  ],
  [
    "Williams' volumes",
    "vary each day from",
    "scheduled volumes"
  ],
  [
    "Volumes from prior periods",
    "would also go toward",
    "transport imbalance"
  ],
  [
    "imbalance payback",
    "refers to",
    "transport imbalance"
  ],
  [
    "Daren J Farmer",
    "would think that",
    "Cleburne will carry imbalance on Lone Star from month to month"
  ],
  [
    "Cleburne",
    "will carry from month to month",
    "imbalance on Lone Star"
  ],
  [
    "Imbalance",
    "is on",
    "Lone Star"
  ],
  [
    "Imbalance on Lone Star",
    "should be",
    "fairly small after November"
  ],
  [
    "Mark McCoy",
    "is",
    "scheduler"
  ],
  [
    "Mark McCoy",
    "will have",
    "imbalance number"
  ],
  [
    "Imbalance on Lone Star",
    "was",
    "very large when ENA took over Deal 529856"
  ],
  [
    "ENA",
    "took over",
    "Deal 529856"
  ],
  [
    "Plant",
    "went down in",
    "September"
  ],
  [
    "ENA",
    "decided to payback then",
    "imbalance on Lone Star"
  ],
  [
    "ENA",
    "decided to payback the imbalance on Lone Star then in",
    "September"
  ],
  [
    "ENA",
    "decided to payback the imbalance on Lone Star then in September",
    "so that ENA could take advantage of higher winter sales prices if the opportunity came up"
  ],
  [
    "ENA",
    "could take advantage of higher winter sales prices",
    "if the opportunity came up"
  ],
  [
    "ENA",
    "could take advantage of",
    "higher winter sales prices"
  ],
  [
    "Tenaska IV agreement",
    "does not specifically state",
    "anything about UA4"
  ],
  [
    "Daren J Farmer",
    "will have",
    "UA4 discussion with Legal"
  ],
  [
    "UA4 discussion with Legal",
    "intends for",
    "all costs to be covered by Tenaska IV"
  ],
  [
    "All costs",
    "are to be covered by",
    "Tenaska IV"
  ],
  [
    "All costs",
    "include",
    "UA4 costs"
  ],
  [
    "All costs",
    "include",
    "Fuel costs"
  ],
  [
    "Daren J Farmer",
    "will leave at",
    "1pm today"
  ],
  [
    "Daren J Farmer",
    "will return",
    "Tuesday 12/19"
  ],
  [
    "Daren J Farmer and Jim Pond",
    "can get together on",
    "Tuesday 12/19"
  ],
  [
    "Daren J Farmer ",
    "can get together with",
    "Jim Pond"
  ]
]

eleven_shot_triples_output = [
  [
    "Mark E Haedicke",
    "thinks",
    "George McClellan's proposal is a good one in light of all the facts at hand"
  ],
  [
    "George McClellan's proposal",
    "is",
    "a good one"
  ],
  [
    "Mark E Haedicke",
    "thinks it is best",
    "if they take the high road in approach as George McClellan have proposed"
  ],
  [
    "George McClellan",
    "have proposed",
    "taking the high road in approach"
  ],
  [
    "Taking the high road in approach",
    "is",
    "best"
  ],
  [
    "Mark E Haedicke",
    "would ask",
    "Robert Quick to prepare a one page bullet list of George McClellan's points"
  ],
  [
    "Mark E Haedicke",
    "would ask",
    "Robert Quick"
  ],
  [
    "Robert Quick",
    "would be asked to prepare",
    "one page bullet list"
  ],
  [
    "One page bullet list",
    "contains",
    "George McClellan's points"
  ],
  [
    "Mark E Haedicke",
    "wants",
    "all to briefly review one page bullet list of George McClellan's points"
  ],
  [
    "Mark E Haedicke",
    "will review",
    "one page bullet list"
  ],
  [
    "George McClellan",
    "will review",
    "one page bullet list"
  ],
  [
    "Richard B Sanders",
    "will review",
    "one page bullet list"
  ],
  [
    "Stuart Staley",
    "will review",
    "one page bullet list"
  ],
  [
    "Mark E Haedicke",
    "wants to stay mindful",
    "that litigation is possible"
  ],
  [
    "Mark E Haedicke",
    "wants",
    "to stay mindful"
  ],
  [
    "Litigation",
    "is",
    "possible"
  ],
  [
    "Words",
    "must be chosen carefully in",
    "event of litigation"
  ]
]

# Define 10-shot examples: each is (user_input, assistant_output)
shots = [
    # Shot 5
    {
        "passage": five_shot_ner_paragraph,
        "named_entity_json": five_shot_ner_output,
        "triples": five_shot_triples_output
    },
    # Shot 6
    {
        "passage": six_shot_ner_paragraph,
        "named_entity_json": six_shot_ner_output,
        "triples": six_shot_triples_output
    },
    # Shot 11
    {
        "passage": eleven_shot_ner_paragraph,
        "named_entity_json": eleven_shot_ner_output,
        "triples": eleven_shot_triples_output
    }
]


# Build the prompt template
prompt_template = [{"role": "system", "content": ner_conditioned_re_system}]

for shot in shots:
    user_input = ner_conditioned_re_frame.format(
        passage=shot["passage"],
        named_entity_json=shot["named_entity_json"]
    )
    assistant_output = '{"triples": %s}' % shot["triples"]
    
    prompt_template.append({"role": "user", "content": user_input})
    prompt_template.append({"role": "assistant", "content": assistant_output})

# Add the template placeholder for final user input
prompt_template.append({"role": "user", "content": convert_format_to_template(original_string=ner_conditioned_re_frame, placeholder_mapping=None, static_values=None)})
