from .ner import one_shot_ner_paragraph, one_shot_ner_output, two_shot_ner_paragraph, two_shot_ner_output, three_shot_ner_paragraph, three_shot_ner_output, four_shot_ner_paragraph, four_shot_ner_output, five_shot_ner_paragraph, five_shot_ner_output, six_shot_ner_paragraph, six_shot_ner_output, seven_shot_ner_paragraph, seven_shot_ner_output, eight_shot_ner_paragraph, eight_shot_ner_output, nine_shot_ner_paragraph, nine_shot_ner_output, ten_shot_ner_paragraph, ten_shot_ner_output, eleven_shot_ner_paragraph, eleven_shot_ner_output, twelve_shot_ner_output, twelve_shot_ner_paragraph, thirteen_shot_ner_output, thirteen_shot_ner_paragraph
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
3.2 If multiple clauses are joined only for structural convenience (e.g., coordination with “and” or “but”), extract them separately as independent triples.
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
Text: “However, for October 2000, the plant was down the majority of the month and ENA sold off the supply, resulting in ENA owing money to Tenaska IV.”
Extracted triples = [
["Cleburne plant", "was down", "the majority of October 2000"], 
["ENA", "sold off", "supply in October 2000"],
["ENA sold off the supply", "resulting in", "ENA owing money to Tenaska IV"], 
["ENA", "owes money to", "Tenaska IV"], 
["ENA", "owes to Tenaska IV", "$1,798,389.73"],
]
Notes:
* The two main clauses (“the plant was down…” and “ENA sold off the supply…”) are two complete, standalone facts on their own, so no triple combines them.
* The relation “resulting in” expresses a dependent causal connection, so it is represented as a higher-level triple ["ENA sold off the supply", "resulting in", "ENA owing money to Tenaska IV"].
* Atomic triples for each clause are extracted to capture the underlying atomic facts (e.g., ["ENA", "owes money to", "Tenaska IV"]).
* Entity resolution is performed in “majority of the month” to “majority of October 2000”
* Exact wording is preserved as much as possible (e.g., ["ENA sold off the supply", "resulting in", "ENA owing money to Tenaska IV"]), but normalization is allowed to form atomic facts (e.g., ["ENA", "owes money to", "Tenaska IV"]). 
* The inferred triple ["ENA", "owes to Tenaska IV", "$1,798,389.73"] was added to connect the fact to the amount named entity.
* Each triple contains 1-2 named entities.

Example 2
Text: “We actually owe $1,798,389.73, but I need to 
net the Tenaska IV sales with the purchase to clear those receivables.”
Extracted triples = [["ENA", "owes to Tenaska IV", "$1,798,389.73"],
  ["Megan Parker", "needs to net", "Tenaska IV sales with the purchase deal to clear receivables"],
  ["Purchase deal”, “is needed for”, “Netting Tenaska IV sales”],
[“Netting Tenaska IV sales”, “is needed to clear”, “receivables”]]
Notes:
* The noun phrase “Netting Tenaska IV sales” was created to represent an atomic process described in the sentence and is reused across triples for graph connectivity. 

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

one_shot_triples_output = [[
        [
          "ENA",
          "is being asked not to compete with",
          "Bidder D"
        ],
        [
          "ENA",
          "is being asked not to compete for",
          "Designated Employees Bidder D would like to hire"
        ],
        [
          "Bidder D",
          "would like to hire",
          "Designated Employees"
        ],
        [
          "ENA",
          "has to sever",
          "Designated Employees"
        ],
        [
          "Bidder D",
          "gets to hire",
          "severed Designated Employees"
        ],
        [
          "Severed Designated Employees",
          "may turn down",
          "DFS"
        ],
        [
          "Severed Designated Employees",
          "do not get",
          "severance payment"
        ],
        [
          "Severed Designated Employees",
          "get no severance payment",
          "if they turn down DFS"
        ],
        [
          "Timothy J Detmering",
          "proposes",
          "plan"
        ],
        [
          "ENA",
          "provides",
          "list of Designated Employees"
        ],
        [
          "List of Designated Employees",
          "is provided to",
          "Bidder D"
        ],
        [
          "List of Designated Employees",
          "includes",
          "Designated Employees’ positions"
        ],
        [
          "List of Designated Employees",
          "includes",
          "Designated Employees’ historical compensation"
        ],
        [
          "Bidder D",
          "covenants to make offers to",
          "Designated Employees"
        ],
        [
          "Bidder D",
          "covenants to make offers preventing claims under",
          "ENA severance plan"
        ],
        [
          "Bidder D",
          "provides",
          "list of Offerees"
        ],
        [
          "List of Offerees",
          "provided to",
          "ENA"
        ],
        [
          "List of Offerees",
          "is provided between",
          "signing and closing"
        ],
        [
          "Bidder D",
          "intends to make employment offers to",
          "Offerees"
        ],
        [
          "Offerees",
          "refer to",
          "Designated Employees"
        ],
        [
          "ENA",
          "covenants not to interfere with",
          "Bidder D offers"
        ],
        [
          "Timothy J Detmering",
          "asks whether",
          "ENA can bind all of Enron"
        ],
        [
          "ENA",
          "can bind",
          "all of Enron"
        ],
        [
          "Offeree",
          "turns down in writing",
          "Bidder D offer"
        ],
        [
          "ENA",
          "is free to continue employing",
          "Offeree"
        ],
        [
          "ENA",
          "is free to continue employing Offeree",
          "if Offeree turns down Bidder D offer (in writing)"
        ],
        [
          "ENA",
          "owes no severance to",
          "Offeree"
        ],
        [
          "ENA",
          "owes no severance to Offeree",
          "if ENA does not continue to employ the Offeree"
        ],
        [
          "ENA",
          "encourages",
          "Offerees to accept Bidder D offers"
        ],
        [
          "Offerees",
          "give up",
          "severance rights"
        ],
        [
          "Offerees",
          "give up severance rights",
          "if offers refused"
        ],
        [
          "ENA",
          "may continue to employ",
          "Offerees who decline offers"
        ],
        [
          "Requirement",
          "caps",
          "ENA severance obligation"
        ],
        [
          "Bidder D",
          "must specify",
          "how many offers to be made"
        ],
        [
          "Timothy J Detmering",
          "is uncomfortable saying that",
          "ENA cannot continue to employ Offerees"
        ],
        [
          "ENA",
          "cannot continue to employ",
          "Offerees"
        ],
        [
          "Michelle Cash",
          "thinks",
          "this point is moot for the time being"
        ],
        [
          "ENA",
          "is not dealing with",
          "Bidder D"
        ],
        [
          "Michelle Cash",
          "thinks",
          "plan is legally ok"
        ],
        [
          "Plan",
          "has potential liability under",
          "WARN Act"
        ],
        [
          "ENA",
          "can schedule around liability under",
          "WARN Act"
        ],
        [
          "ENA",
          "gives",
          "60 days’ notice to employees who may be affected"
        ],
        [
          "Michelle Cash",
          "does not prefer",
          "plan"
        ],
        [
          "Michelle Cash",
          "prefers",
          "ENA to have the ability to compete for top performers"
        ],
        [
          "ENA",
          "works through",
          "persons identified and presented for possible hiring by Bidder D"
        ],
        [
          "Michelle Cash",
          "would like more information about",
          "what is meant by \"ENA does not interfere with offers made by Bidder D\""
        ],
        [
          "Michelle Cash",
          "states",
          "it is unlikely ENA can bind all of Enron"
        ],
        [
          "ENA",
          "is unlikely able to bind",
          "all of Enron"
        ],
        [
          "Michelle Cash",
          "recommends",
          "limiting commitment to wholesale group"
        ],
        [
          "ENA",
          "may be able to include",
          "the pipelines"
        ],
        [
          "Pipelines",
          "have been involved in",
          "this transaction"
        ]
      ]]

two_shot_triples_output = [ [
        [
          "Brad Jones",
          "sends",
          "Gas P&L information"
        ],
        [
          "Gas P&L information",
          "is requested by",
          "daniel.mcdonagh@chase.com"
        ],
        [
          "Gas P&L information",
          "is requested by",
          "Phillip K. Allen"
        ],
        [
          "Gas P&L information",
          "is requested by",
          "pallen70@hotmail.com"
        ],
        [
          "Enron",
          "made",
          "$1.2Bn total"
        ],
        [
          "$1.2Bn total",
          "is half from",
          "new deals"
        ],
        [
          "$1.2Bn total",
          "is half from",
          "reserve releases"
        ],
        [
          "Phillip K. Allen",
          "interprets",
          "zero net curve shift for 2001"
        ],
        [
          "zero net curve shift for 2001",
          "occurs when",
          "prudency release is backed out"
        ],
        [
          "Original Gas P&L file",
          "shows",
          "zero net curve shift for 2001"
        ],
        [
          "Original Gas P&L file",
          "does not have",
          "good optics"
        ]
      ]]

four_shot_triples_output = [[
        [
          "Jayendran Rajamony",
          "attaches",
          "resume"
        ],
        [
          "Jayendran Rajamony",
          "attaches",
          "cover letter"
        ],
        [
          "Cover letter",
          "states",
          "interest in Enron Associate / Analyst Program"
        ],
        [
          "Jayendran Rajamony",
          "looks forward to discussing",
          "interest in Enron with Billy Lemmons Jr."
        ],
        [
          "Jayendran Rajamony",
          "builds on",
          "financial analysis skills"
        ],
        [
          "Jayendran Rajamony",
          "builds on",
          "risk management skills"
        ],
        [
          "Jayendran Rajamony",
          "is portfolio manager in",
          "$2 million Cayuga MBA Fund, LLC"
        ],
        [
          "Jayendran Rajamony",
          "previously managed",
          "ocean physics projects"
        ],
        [
          "Ocean physics projects",
          "were managed for",
          "National Science Foundation"
        ],
        [
          "Ocean physics projects",
          "were managed for",
          "Office of Naval Research"
        ],
        [
          "Jayendran Rajamony",
          "is keen on combining",
          "understanding of physics of weather and climate with training in finance"
        ],
        [
          "Jayendran Rajamony",
          "aims to structure",
          "energy transactions"
        ],
        [
          "Jayendran Rajamony",
          "aims to structure",
          "finance transactions"
        ],
        [
          "Jayendran Rajamony",
          "is MBA Class of",
          "2002"
        ],
        [
          "Jayendran Rajamony",
          "is affiliated with",
          "Johnson Graduate School of Management"
        ],
        [
          "Johnson Graduate School of Management",
          "is part of",
          "Cornell University"
        ],
        [
          "Billy Lemmons Jr.",
          "thanks Jayendran Rajamony for",
          "note"
        ],
        [
          "Billy Lemmons Jr.",
          "thanks Jayendran Rajamony for",
          "interest in Associate / Analyst Program"
        ],
        [
          "Billy Lemmons Jr.",
          "copies on email",
          "Traci Warner"
        ],
        [
          "Traci Warner",
          "leads",
          "Recruiting for Enron Associate / Analyst Program"
        ],
        [
          "Traci Warner",
          "will follow up with",
          "Jayendran Rajamony"
        ],
        [
          "Team member",
          "will follow up with",
          "Jayendran Rajamony"
        ],
        [
          "Billy Lemmons Jr.",
          "notes",
          "Jayendran Rajamony’s mix of weather/climate training and financial background"
        ],
        [
          "Billy Lemmons Jr.",
          "will highlight",
          "Jayendran Rajamony’s experience"
        ],
        [
          "Jayendran Rajamony’s experience",
          "will be presented to",
          "specific groups"
        ],
        [
          "Billy Lemmons Jr.",
          "offers",
          "further assistance to Jayendran Rajamony"
        ],
        [
          "Billy Lemmons Jr.",
          "is Vice President of",
          "Associate / Analyst Program"
        ],
        [
          "Billy Lemmons Jr.",
          "follows up on",
          "earlier bcc"
        ],
        [
          "earlier bcc",
          "asks about",
          "interest in Jayendran Rajamony"
        ],
        [
          "Jayendran Rajamony",
          "is candidate for",
          "Enron Associate / Analyst Program"
        ],
        [
          "earlier bcc",
          "is sent to",
          "Mark Tawney"
        ],
        [
          "earlier bcc",
          "is sent to",
          "Vince Kaminski"
        ]
      ]]

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

seven_shot_triples_output = [
        [
          "David Ingram",
          "have been doing",
          "analysis"
        ],
        [
          "David Ingram",
          "finds",
          "few problems in analysis"
        ],
        [
          "Mother data",
          "is pulling",
          "Zone P number"
        ],
        [
          "Zone P number",
          "is",
          "wrong"
        ],
        [
          "Pointer for Zone P number",
          "can be found on",
          "SQL worksheet"
        ],
        [
          "Pointer for Zone P number",
          "points to",
          "the expression"
        ],
        [
          "The expression",
          "is",
          "avg(decode(prc.power_reference_period_cd,'DAYAHEAD', decode(pl.location_name,'PJM',price_amt))) PJM_DA"
        ],
        [
          "The expression",
          "is",
          "avg(decode(prc.power_reference_period_cd,'HOURLY', decode(pl.location_name,'PJM',price_amt))) PJM_RT"
        ],
        [
          "David Ingram",
          "looks at",
          "PJM prices"
        ],
        [
          "David Ingram",
          "looks at",
          "NY prices"
        ],
        [
          "David Ingram",
          "cannot figure out",
          "source of Zone P number"
        ],
        [
          "Other 24hr desk",
          "has been told",
          "PJM night shift preps PJM portion of shift notes"
        ],
        [
          "Other 24hr desk",
          "has been told",
          "PJM night shift preps Nepool portion of shift notes"
        ],
        [
          "PJM night shift",
          "preps",
          "PJM portion of shift notes"
        ],
        [
          "PJM night shift",
          "preps",
          "Nepool portion of shift notes"
        ],
        [
          "David Ingram",
          "writes",
          "macro to pull Nepool information"
        ],
        [
          "David Ingram",
          "writes",
          "macro to format Nepool information"
        ],
        [
          "David Ingram",
          "writes",
          "macro to print Nepool information"
        ],
        [
          "PJM information",
          "is not available on",
          "website"
        ],
        [
          "East power portal",
          "has",
          "PJM information"
        ],
        [
          "David Ingram",
          "thinks",
          "East power portal does some kind of Op Sum pull at unknown interval"
        ],
        [
          "East power portal",
          "does",
          "Op Sum pull at unknown interval"
        ],
        [
          "Op Sum pull",
          "done at",
          "unknown interval"
        ],
        [
          "PJM Information",
          "is not",
          "accurate"
        ],
        [
          "Rob Bensen",
          "is frustrated with",
          "bad PJM information"
        ],
        [
          "Rob Bensen’s frustration",
          "is main reason",
          "other 24hr desk doesn’t want any part of the reporting"
        ],
        [
          "Other 24hr desk",
          "doesn’t want any part of the",
          "reporting"
        ],
        [
          "All data points",
          "are different than the",
          "one hour averages calculated in edata"
        ],
        [
          "Difference in data points",
          "causes",
          "David Ingram’s doubt that opsum is the source"
        ],
        [
          "David Ingram",
          "doubts",
          "opsum is the source"
        ],
        [
          "opsum",
          "is the",
          "source"
        ],
        [
          "Edata",
          "pulls from",
          "opsum"
        ],
        [
          "All interfaces and hubs",
          "are printing",
          "the same"
        ],
        [
          "Prices shown on website",
          "differ",
          "in the same hour"
        ],
        [
          "David Ingram",
          "has no idea",
          "where these prices are coming from"
        ],
        [
          "Prices shown on website",
          "are",
          "not right"
        ],
        [
          "Application at 'M:\\Electric\\24hour\\PJM AVE\\PJMSummary.exe'",
          "pulls from",
          "database"
        ],
        [
          "Correct data",
          "can be found by",
          "application at 'M:\\Electric\\24hour\\PJM AVE\\PJMSummary.exe'"
        ],
        [
          "IT Team",
          "could fix",
          "application at 'M:\\Electric\\24hour\\PJM AVE\\PJMSummary.exe"
        ],
        [
          "David Ingram",
          "would care less about",
          "the web site"
        ],
        [
          "IT team",
          "does not want to fix",
          "application at 'M:\\Electric\\24hour\\PJM AVE\\PJMSummary.exe"
        ],
        [
          "David Ingram",
          "can write",
          "macro"
        ],
        [
          "David Ingram",
          "can write macro",
          "to pull the same data from the mother data template"
        ],
        [
          "macro",
          "pulls the same data from",
          "mother data template"
        ],
        [
          "David Ingram",
          "can write macro",
          "if IT Team does not want to fix the application at 'M:\\Electric\\24hour\\PJM AVE\\PJMSummary.exe"
        ],
        [
          "David Ingram",
          "does not care",
          "how he gets the data"
        ],
        [
          "David Ingram",
          "needs to get",
          "yesterday’s PJM data for shift note"
        ],
        [
          "Paul D. Thomas",
          "is following",
          "DA-RT physical moves"
        ],
        [
          "Paul D. Thomas",
          "is following DA-RT physical moves",
          "if Paul D. Thomas is trading some of the regular products"
        ],
        [
          "Paul D. Thomas",
          "is trading",
          " some of the regular products"
        ],
        [
          "David Ingram and team",
          "man",
          "24hr desk"
        ],
        [
          "24hr desk team",
          "could cover",
          "DA-RT physical"
        ],
        [
          "Bryce",
          "is",
          "day guy at 24hr desk"
        ],
        [
          "Covering DA-RT physical moves",
          "is part of",
          "24hr desk"
        ],
        [
          "Covering DA-RT physical moves as part of 24hr desk",
          "uses",
          "evening load"
        ],
        [
          "Covering DA-RT physical moves as part of 24hr desk",
          "uses",
          "more up-to-date weather forecasts"
        ],
        [
          "Evening load",
          "could be used",
          "when entering NY side in early morning"
        ],
        [
          "More up-to-date weather forecasts",
          "could be used",
          "when entering NY side in early morning"
        ],
        [
          "NY side",
          "is entered in",
          "early morning"
        ],
        [
          "David Ingram",
          "mentions covering DA-RT physical moves as part of 24hr desk",
          "only if Paul D. Thomas is too busy trading PJM to spend same amount of time on analysis"
        ],
        [
          "David Ingram",
          "mentions",
          "covering DA-RT physical moves as part of 24hr desk"
        ],
        [
          "Paul D. Thomas",
          "may be finding himself",
          "too busy trading PJM to spend the same amount of time on the analysis"
        ],
        [
          "Trading PJM",
          "makes Paul D. Thomas too busy to spend the same amount of time on",
          "analysis"
        ],
        [
          "Uninterrupted analysis",
          "is certainly easier to do on",
          "back shift"
        ],
        [
          "Diana Allen",
          "is currently working on",
          "resolving the bad Zone P day ahead data"
        ],
        [
          "IT team",
          "is currently working on",
          "resolving the bad Zone P day ahead data"
        ],
        [
          "Diana Allen",
          "is currently working on",
          "resolving the bad Zone P day real time data"
        ],
        [
          "IT team",
          "is currently working on",
          "resolving the bad Zone P day real time data"
        ],
        [
          "Diana Allen",
          "told Paul D. Thomas that",
          "Bad Zone P data was pulling the PJM data"
        ],
        [
          "Diana Allen",
          "told",
          "Paul D. Thomas"
        ],
        [
          "Bad Zone P data",
          "was pulling",
          "PJM data"
        ],
        [
          "Paul D. Thomas",
          "talked to",
          "Rob Benson about shift notes"
        ],
        [
          "Paul D. Thomas",
          "talked to",
          "Rob Benson"
        ],
        [
          "Paul D. Thomas",
          "talked about",
          "shift notes"
        ],
        [
          "Rob Benson",
          "said that",
          "shift notes have improved greatly"
        ],
        [
          "shift notes",
          "have",
          "greatly improved"
        ],
        [
          "PJM summary page",
          "is",
          "pretty accurate"
        ],
        [
          "PJM summary page",
          "is usually within",
          "50 cents of the actual number"
        ],
        [
          "spreadsheet",
          "has link",
          "http://eastpower.test.corp.enron.com/portal/summary/pjmsummary.aspx"
        ],
        [
          "spreadsheet",
          "is",
          "PJM summary page"
        ]
]

eight_shot_triples_output = [
        [
          "Diana Allen",
          "told Paul D. Thomas that",
          "Bad Zone P data was pulling the PJM data"
        ],
        [
          "Diana Allen",
          "told",
          "Paul D. Thomas"
        ],
        [
          "Bad Zone P data",
          "was pulling",
          "PJM data"
        ],
        [
          "Paul D. Thomas",
          "talked to",
          "Rob Benson about shift notes"
        ],
        [
          "Paul D. Thomas",
          "talked to",
          "Rob Benson"
        ],
        [
          "Paul D. Thomas",
          "talked about",
          "shift notes"
        ],
        [
          "Rob Benson",
          "said that",
          "shift notes have improved greatly"
        ],
        [
          "shift notes",
          "have",
          "greatly improved"
        ],
        [
          "PJM summary page",
          "is",
          "pretty accurate"
        ],
        [
          "PJM summary page",
          "is usually within",
          "50 cents of the actual number"
        ],
        [
          "spreadsheet",
          "has link",
          "http://eastpower.test.corp.enron.com/portal/summary/pjmsummary.aspx"
        ],
        [
          "spreadsheet",
          "is",
          "PJM summary page"
        ],
        [
          "David Ingram",
          "might have been using",
          "old version of spreadsheet"
        ],
        [
          "Paul D. Thomas",
          "will continue",
          "Managing the Northeast physical book"
        ],
        [
          "Managing the Northeast physical book",
          "allows",
          "Paul D. Thomas to effectively hedge his long or short position in the off peak market"
        ],
        [
          "Paul D. Thomas",
          "hedges",
          "long position in off-peak market"
        ],
        [
          "Paul D. Thomas",
          "hedges",
          "short position in off-peak market"
        ],
        [
          "Diana Allen",
          "said",
          "she fixed the Zone P problem"
        ],
        [
          "Diana Allen",
          "fixed",
          "Zone P problem"
        ],
        [
          "David Ingram",
          "does not doubt PJM summary has improved",
          "as David Ingram has been pulling the data directly from edata instead of using the website"
        ],
        [
          "David Ingram",
          "does not doubt",
          "PJM summary has improved"
        ],
        [
          "PJM summary",
          "has",
          "improved"
        ],
        [
          "David Ingram",
          "has been pulling the data directly from",
          "edata"
        ],
        [
          "David Ingram",
          "does not use",
          "website"
        ],
        [
          "David Ingram",
          "will begin to record",
          "difference"
        ],
        [
          "David Ingram",
          "will talk with web data folks in an attempt to",
          "understand where the web data folks are pulling the data"
        ],
        [
          "David Ingram",
          "will talk with",
          "web data folks"
        ],
        [
          "Web data folks",
          "are pulling",
          "data"
        ],
        [
          "David Ingram",
          "has been using",
          "updated website"
        ],
        [
          "David Ingram",
          "spot checked",
          "Zone P prices"
        ],
        [
          "Zone P prices",
          "had",
          "few errors of little consequence"
        ],
        [
          "few errors",
          "were of",
          "little consequence"
        ],
        [
          "David Ingram",
          "was doing",
          "analysis on NE physical"
        ],
        [
          "24to6",
          "has been a pretty solid play",
          "unless David Ingram has his directions backwards"
        ],
        [
          "24to6",
          "has been",
          "a pretty solid play"
        ],
        [
          "24to6",
          "has been a pretty solid play on",
          "DAP to DAW"
        ],
        [
          "24to6",
          "has been a pretty solid play on",
          "DAP to RTW"
        ],
        [
          "24to6",
          "has been a pretty solid play on",
          "DA to RT during other hours"
        ],
        [
          "David Ingram",
          "cannot tell why 24to6 is not being scheduled from the night shift",
          "because Paul D. Thomas is busy managing EOL products"
        ],
        [
          "David Ingram",
          "cannot tell why 24to6 is not being scheduled from the night shift",
          "because there is some reason David Ingram doesn’t have the experience to understand yet"
        ],
        [
          "David Ingram",
          "cannot tell",
          "if 24to6 is not being scheduled from the night shift"
        ],
        [
          "Paul D. Thomas",
          "is busy managing",
          "EOL products"
        ],
        [
          "David Ingram",
          "does not yet have",
          "experience to understand reason"
        ],
        [
          "David Ingram",
          "knows",
          "Northeast physical book belongs to Paul D. Thomas"
        ],
        [
          "David Ingram",
          "knows",
          "Paul D. Thomas will want to keep the earnings"
        ],
        [
          "Northeast physical book",
          "belongs to",
          "Paul D. Thomas"
        ],
        [
          "Paul D. Thomas",
          "will want to keep",
          "earnings"
        ],
        [
          "Earnings",
          "are from",
          "Northeast physical book"
        ],
        [
          "David Ingram",
          "noticed",
          "opportunity appears to be there"
        ],
        [
          "David Ingram and team",
          "can do",
          "some of the analysis and pass it on to Paul D. Thomas to place the orders if Paul D. Thomas would like"
        ],
        [
          "David Ingram and team",
          "can do",
          "some of the analysis"
        ],
        [
          "David Ingram and team",
          "can pass",
          "analysis to Paul D. Thomas"
        ],
        [
          "Paul D. Thomas",
          "places",
          "the orders"
        ],
        [
          "Paul D. Thomas",
          "tells",
          "David Ingram and team what he wants to do in NY"
        ],
        [
          "Paul D. Thomas",
          "can decide",
          "what to do with the opportunity on the day shift"
        ],
        [
          "David Ingram",
          "does not want to step on",
          "Paul D. Thomas’s turf"
        ],
        [
          "Paul D. Thomas",
          "has done well with",
          "books Paul D. Thomas has"
        ],
        [
          "Scenario",
          "is easy to see",
          "where Paul D. Thomas will trade more during the day"
        ],
        [
          "Paul D. Thomas",
          "will be",
          "trading more during the day"
        ],
        [
          "Paul D. Thomas",
          "moves to use",
          "NE physical book more for hedging"
        ],
        [
          "NE physical book",
          "is used more for",
          "hedging"
        ],
        [
          "Gautam",
          "has used",
          "NE physical book more for hedging"
        ],
        [
          "24 hour guys",
          "has role to take on more of",
          "speculative portion of the physical market"
        ],
        [
          "David Ingram and team",
          "starts getting",
          "other guys thinking about that portion of the market by trying any of the ideas in the previous paragraph"
        ],
        [
          "Other guys",
          "think about",
          "that portion of the market"
        ],
        [
          "Other guys",
          "try",
          "any of the ideas in the previous paragraph"
        ],
        [
          "David Ingram",
          "would like to find time to discuss with",
          " Paul D. Thomas"
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

twelve_shot_triples_output = [
  [
    "Vince J Kaminski",
    "have probably heard",
    "that Donna Dye’s group is being broken up"
  ],
  [
    "Donna Dye’s group",
    "is being",
    "broken up"
  ],
  [
    "Some people",
    "were put in",
    "other groups"
  ],
  [
    "Donna Dye",
    "was not put in",
    "other groups"
  ],
  [
    "HR",
    "will try to find a position for Donna Dye within Enron for the month of",
    "March"
  ],
  [
    "Finding a position for Donna Dye within Enron",
    "is not likely",
    "to happen"
  ],
  [
    "Tomorrow",
    "is",
    "Donna Dye’s last full day in Enron"
  ],
  [
    "Donna Dye",
    "will be in and out for the month of",
    "March"
  ],
  [
    "Donna Dye",
    "is informing nice people",
    "that Donna Dye likes"
  ],
  [
    "Donna Dye",
    "is informing",
    "nice people"
  ],
  [
    "Vince J Kaminski",
    "is one of those",
    "that Donna Dye likes"
  ],
  [
    "Vince J Kaminski",
    "shall stop by tomorrow to",
    "say hello"
  ],
  [
    "Vince J Kaminski",
    "shall stop by",
    "tomorrow"
  ],
  [
    "Many good friends of Vince J Kaminski",
    "will be leaving",
    "Enron"
  ],
  [
    "Vince J Kaminski",
    "is from",
    "Enron North America Corp"
  ]
]

thirteen_shot_triples_output = [
  [
    "Lynn Richardson",
    "tried to return this morning",
    "Amy Clemons’ call from yesterday"
  ],
  [
    "Amy Clemons",
    "called yesterday",
    "Lynn Richardson"
  ],
  [
    "Lynn Richardson",
    "only got",
    "Amy Clemons’ voice mail"
  ],
  [
    "February bill",
    "amount",
    "$341.90"
  ],
  [
    "February bill",
    "was for",
    "February 9th and February 14th"
  ],
  [
    "February 9th",
    "has tag number",
    "Tag No. 16259"
  ],
  [
    "February 9th",
    "wasb priced for",
    "1 MW @ $207.99"
  ],
  [
    "February 14th transaction",
    "was",
    "a real-time transaction with no tag for less than a MW priced at $133.91"
  ],
  [
    "February 14th transaction",
    "was a",
    "real-time transaction"
  ],
  [
    "February 14th transaction",
    "had no tag for",
    "less than a MW"
  ],
  [
    "February 14th transaction",
    "was priced at",
    "$133.91"
  ],
  [
    "Lynn Richardson",
    "checked and saw",
    "no energy return for losses to WACM from Enron at any time during February"
  ],
  [
    "Lynn Richardson",
    "checked",
    "records"
  ],
  [
    "No energy return for losses",
    "was for",
    "WACM"
  ],
  [
    "No energy return for losses",
    "was from",
    "Enron"
  ],
  [
    "No energy return for losses",
    "occurred at any time during",
    "February"
  ],
  [
    "Lynn Richardson",
    "is",
    "Public Utilities Specialist"
  ],
  [
    "Lynn Richardson",
    "works at",
    "RMR"
  ],
  [
    "Lynn Richardson",
    "has phone number",
    "(970) 461-7440"
  ],
  [
    "February bill",
    "has code",
    "DMS - 7550"
  ],
  [
    "Amy Clemons",
    "needs to settle",
    "February Bill"
  ],
  [
    "Lynn Richardson",
    "sent",
    "detail"
  ],
  [
    "Lynn Richardson",
    "sent detail to",
    "Amy Clemons"
  ],
  [
    "Amy Clemons",
    "asks if",
    "Virginia Thompson or Cara Semperger have spoken to Lynn Richardson about the charge she invoiced them for"
  ],
  [
    "Virginia Thompson",
    "have spoken to",
    "Lynn Richardson"
  ],
  [
    "Cara Semperger",
    "have spoken to",
    "Lynn Richardson"
  ],
  [
    "Lynn Richardson",
    "invoiced for",
    "charge"
  ],
  [
    "Charge",
    "is for",
    "February bill"
  ],
  [
    "Cara Semperger",
    "recognizes charges for",
    "February 9th"
  ],
  [
    "Bill Williams III",
    "recognizes charges for",
    "February 14th"
  ],
  [
    "Virginia Thompson",
    "asks Cara Semperger if charges are valid for",
    "February 9th"
  ],
  [
    "Virginia Thompson",
    "asks Bill Williams III if charges are valid for",
    "February 14th"
  ],
  [
    "Cara Semperger",
    "believes",
    "preschedule loss charge is valid for 2/9/01"
  ],
  [
    "preschedule loss charge",
    "is valid for",
    "2/9/01"
  ],
  [
    "2/9/01",
    "refers to",
    "February 9th"
  ],
  [
    "preschedule loss charge",
    "refers to",
    "February Bill"
  ],
  [
    "Cara Semperger",
    "sees",
    "no loss schedule represented on the scheduling sheet"
  ],
  [
    "Loss schedule",
    "is not represented on the",
    "scheduling sheet"
  ],
  [
    "Cara Semperger",
    "does not see",
    "loss schedule"
  ],
  [
    "Loss schedule",
    "is not represented on the",
    "scheduling sheet"
  ],
  [
    "Virginia Thompson",
    "asks whether",
    "February Bill goes on NW's books"
  ],
  [
    "Virginia Thompson",
    "asks whether",
    "February Bill goes on SW's books"
  ],
  [
    "February Bill",
    "goes on",
    "NW's books"
  ],
  [
    "February Bill",
    "goes on",
    "SW's books"
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
