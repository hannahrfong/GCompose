from .ner import one_shot_ner_paragraph, one_shot_ner_output, two_shot_ner_paragraph, two_shot_ner_output, three_shot_ner_paragraph, three_shot_ner_output, four_shot_ner_paragraph, four_shot_ner_output, five_shot_ner_paragraph, five_shot_ner_output, six_shot_ner_paragraph, six_shot_ner_output, seven_shot_ner_paragraph, seven_shot_ner_output, eight_shot_ner_paragraph, eight_shot_ner_output, nine_shot_ner_paragraph, nine_shot_ner_output, ten_shot_ner_paragraph, ten_shot_ner_output
from ...utils.llm_utils import convert_format_to_template

ner_conditioned_re_system = """You are an open information extraction (OpenIE) model.

Task: Extract all factual relations from the given email in the form of RDF triples (subject, predicate, object). Each triple expresses a complete factual relation from the email text. The extracted triples will be used to construct a knowledge graph for downstream email text completion, so correctness (precision) and completeness (recall) are extremely important.

Triple Extraction Guidelines: 
Follow these criteria to extract high-quality triples:
1. Completeness - Extract all triples from the text.
2. Assertedness - Only extract triples that are explicitly or implicitly implied by the original text.
3. Informativeness - Include the maximum amount of relevant information in each argument (i.e., subject or object).
4. Atomicity - Each triple must be an indivisible unit. Whenever possible, extract multiple atomic triples from a text that has conjunctions.

Additional instructions:
1. Do NOT extract entities if the email is any of the following:
- Machine-generated or bulk-distributed (e.g., system notifications, alerts, marketing, transactional messages, non-work-related newsletters)
- Not in English
- Non-informative content (e.g., jokes, entertainment, promotions, or attachment-only emails)
2. Extract triples from the email one sentence at a time. For each sentence, extract triples for each clause.
3. Each triple should contain at least one, but preferably two, of the named entities in the provided list for each passage.
4. Clearly resolve pronouns to their specific names to maintain clarity using the message context, or metadata entities, only if it clearly supports the resolution.
5. Do NOT include triples about the structure of the email itself (e.g., "Kate sent email to Rhonda").

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

one_shot_triples_output =  [
       ["Bidder D", "would like to hire", "employees"],
       ["ENA", "is asked not to compete with", "Bidder D"],
       ["ENA", "has to sever", "employees"],
       ["Bidder D", "gets to hire", "severed employees"],
       ["Severed employees", "turn down", "DFS offer"],
       ["Severed employees", "get no severance payment", "if severed employees turn down DFS"],
       ["Timothy J Detmering", "would like to propose", "plan"],
       ["ENA", "provides", "list of Designated Employees"],
       ["List of Designated Employees", "is provided to", "Bidder D"],
       ["List", "contains", "Designated Employees’ positions"],
       ["List", "contains", "Designated Employees’ historical compensation"],
       ["Bidder D", "covenants to make", "offers"],
       ["Offers", "prevent from claiming constructive dismissal under ENA severance plan", "Designated Employees"],
       ["Bidder D", "provides", "list of Offerees"],
       ["List of Offerees", "provided to", "ENA"],
       ["List of Offerees", "provided between", "signing and closing"],
       ["Bidder D", "intends to make offers of employment to", "Offerees"],
       ["Offerees", "refer to", "Designated Employees"],
       ["ENA", "covenants not to interfere with", "Bidder D’s offers"],
       ["Timothy J Detmering", "asks whether ENA can bind", "all of Enron"],
       ["Offeree", "turns down", "offer"],
       ["ENA", "is free to continue to employ", "Offeree"],
       ["ENA", "owes no severance to", "Offeree"],
       ["Offeree", "is not employed by", "ENA"],
       ["ENA", "intends to encourage", "Offerees to take offers"],
       ["Offerees", "refuse", "offers"],
       ["Offerees", "give up", "severance rights"],
       ["ENA", "may continue to employ", "Offerees bold enough to turn down offers"],
       ["Bidder D", "is certain to want", "more offers"],
       ["Requirement", "caps", "ENA severance obligation"],
       ["Bidder D", "must specify", "how many offers to be made"],
       ["Timothy J Detmering", "is uncomfortable saying", "ENA cannot continue to employ Offerees"],
        ["Michelle Cash", "thinks", "this point is moot for the time being"],
        ["ENA", "is not dealing with", "Bidder D"],
        ["Michelle Cash", "thinks", "plan is legally ok"],
        ["Plan", "has", "potential liability under the WARN Act"],
        ["ENA", "can schedule around", "potential liability under the WARN Act"],
        ["ENA", "gives", "60 days’ notice to employees who may be affected"],
        ["Michelle Cash", "does not prefer", "plan"],
        ["Michelle Cash", "prefers", "ENA to have the ability to compete for top performers"],
        ["ENA", "should be able to manage", "competing for top performers"],
        ["ENA", "works through", "persons identified and presented for possible hiring by Bidder D"],
        ["Michelle Cash", "would like more information about", "what is meant by \"ENA does not interfere with offers made by Bidder D\""],
        ["Michelle Cash", "says", "it is unlikely that ENA can bind all of Enron"],
        ["Committing", "is easier", "only the wholesale group"],
        ["Michelle Cash", "recommends", "limiting commitment to the wholesale group"],
        ["ENA", "may be able to include", "the pipelines"],
        ["The pipelines", "have been involved in", "this transaction"]
   ]


two_shot_triples_output = [
  ["Brad Jones", "sends", "Gas P&L information"],
  ["Gas P&L information", "is requested by", "daniel.mcdonagh@chase.com"],
  ["Gas P&L information", "is requested by", "Phillip K. Allen"],
  ["Gas P&L information", "is requested by", "pallen70@hotmail.com"],
  ["Enron", "made", "$1.2Bn total"],
  ["$1.2Bn total", "is half from", "new deals"],
  ["$1.2Bn total", "is half from", "reserve releases"],
  ["Phillip K. Allen", "gets", "zero net curve shift for 2001 when backing out prudency release"],
  ["Backing out prudency release", "results in", "zero net curve shift for 2001"],
  ["Original file", "had", "approximately zero net curve shift for 2001"],
  ["Gas P&L results", "have", "poor optics"]
]

three_shot_triples_output = []

four_shot_triples_output =  [
  ["Jayendran Rajamony", "attaches", "resume"],
  ["Jayendran Rajamony", "attaches", "cover letter"],
  ["Cover letter", "states", "Jayendran Rajamony’s interest in Associate program at Enron"],
  ["Jayendran Rajamony", "looks forward to discussing", "interest in Enron with Billy Lemmons"],
  ["Jayendran Rajamony", "builds on", "financial analysis skills"],
  ["Jayendran Rajamony", "builds on", "risk management skills"],
  ["Jayendran Rajamony", "is portfolio manager in", "$2 million Cayuga MBA Fund, LLC"],
  ["Jayendran Rajamony", "previously managed", "ocean physics projects"],
  ["Ocean physics projects", "were managed for", "National Science Foundation"],
  ["Ocean physics projects", "were managed for", "Office of Naval Research"],
  ["Jayendran Rajamony", "is keen on combining", "understanding of physics of weather and climate with training in finance"],
  ["Jayendran Rajamony", "aims to structure", "energy transactions"],
  ["Jayendran Rajamony", "aims to structure", "finance transactions"],
  ["Jayendran Rajamony", "is MBA Class of", "2002"],
  ["Jayendran Rajamony", "is affiliated with", "Johnson Graduate School of Management"],
  ["Johnson Graduate School of Management", "is part of", "Cornell University"],
  ["Billy Lemmons", "thanks", "Jayendran Rajamony for note"],
  ["Billy Lemmons", "thanks", "Jayendran Rajamony for interest in Enron Associate / Analyst Program"],
  ["Billy Lemmons", "copies", "Traci Warner on email"],
  ["Traci Warner", "leads", "Recruiting for Enron Associate / Analyst Program"],
  ["Traci Warner", "will follow up with", "Jayendran Rajamony"],
  ["Team member", "will follow up with", "Jayendran Rajamony"],
  ["Billy Lemmons", "notes", "Jayendran Rajamony’s mix of weather/climate training and financial background"],
  ["Enron", "will highlight", "Jayendran Rajamony’s experience with specific groups"],
  ["Billy Lemmons", "offers", "further assistance to Jayendran Rajamony"],
  ["Billy Lemmons Jr.", "is Vice President of", "Associate / Analyst Program"],
  ["Billy Lemmons", "follows up on", "earlier bcc to Mark Tawney"],
  ["Billy Lemmons", "follows up on", "earlier bcc to Vince Kaminski"],
  ["Billy Lemmons", "asks", "Mark Tawney about interest in Jayendran Rajamony"],
  ["Billy Lemmons", "asks", "Vince Kaminski about interest in Jayendran Rajamony"]
]

five_shot_triples_output = [
    ["Megan Parker", "has", "actuals"],
    ["The larger of the two volumes", "is", "1,395,000"],
    ["The larger of the two volumes", "is", "45,000/day"],
    ["Demand rate in deal 514353", "is", "fine"],
    ["Megan Parker", "has a problem with", "way the volume is coming to settlements"],
    ["The volume", "shows up with", "Jan 2003 delivery date"],
    ["Megan Parker", "thinks", "demand fee needs to be on 10/1 only"],
    ["Demand fee", "is on a line with date", "10/1/00 to 12/31/36"],
    ["Megan Parker", "thinks", "system is confused by current demand fee dates"],
    ["ENA", "still needs", "purchase deal for Tenaska IV"],
    ["Purchase deal for Tenaska IV", "should be for", "demand fee of $2,571,135.73"],
    ["Demand fee of $2,571,135.73", "is booked to", "Cleburne desk"],
    ["ENA", "owes", "$1,798,389.73"],
    ["Megan Parker", "needs to net", "Tenaska IV sales with the purchase"],
    ["Netting Tenaska IV sales with purchase", "clears", "receivables"],
    ["James", "calls", "Megan Parker"],
    ["Calls by James", "happen", "every day"],
    ["Calls by James", "are for", "update"],
    ["Megan Parker", "wants to know", "when the Tenaska IV purchase deal can be entered into the system"],
    ["Megan Parker", "attaches", "spreadsheet"],
    ["ENA", "will be in most cases", "a net buyer from Tenaska IV"],
    ["Tenaska IV activity", "is related to", "Cleburne plant"],
    ["Cleburne plant", "was down", "majority of October 2000"],
    ["ENA", "sold off in October", "supply in October 2000"],
    ["ENA", "owes $1,798,389.73 to", "Tenaska IV"],
    ["Daren J Farmer", "created", "deal 529856"],
    ["Deal 529856", "has demand of", "$1,798,389.73"],
    ["$1,798,389.73", "is", "calculated income on Cleburne desk"],
    ["ENA", "needs to pass", "income of $1,798,389.73"],
    ["Income of $1,798,389.73", "must be passed to", "Tenaska IV"],
    ["Daren J Farmer", "asks", "whether $1,798,389.73 needs to be paid from ENA to Tenaska IV"],
    ["Daren J Farmer", "asks", "if there is another way to pay $1,798,389.73 from ENA to Tenaska IV"],
    ["Income passing to Tenaska IV", "applies to", "October 2000"],
    ["Income passing to Tenaska IV", "could happen again in", "future"],
    ["Megan Parker", "instructed not to pay", "$1,798,389.73"],
    ["Payment of $1,798,389.73", "depends on", "hearing from Greg Whiting, Troy Klussmann, and James Armstrong"],
    ["ENA", "must receive", "dollars from spot sales"],
    ["Reimbursement to Tenaska IV", "must occur after", "receiving dollars from spot sales"],
    ["Demand fee", "is probably", "best solution"],
    ["ENA", "can use demand fee to create", "receivable/payable with Tenaska"],
    ["Receivable/payable with Tenaska", "depends on", "calculation each month"],
    ["Daren J Farmer", "asks", "how PMA entries should be handled once the fee is calculated and the deal is put in the system"],
    ["Jim Pond", "attaches", "schedule detailing what is on the general ledger for Cleburne"],
    ["Information on schedule", "will change", "by end of month"],
    ["Discrepancies", "exist between", "Megan Parker's calculations and general ledger for Cleburne"],
    ["UA4", "is on", "Jim Pond's schedule"],
    ["ENA", "books entry", "to balance desk"],
    ["Booking entry", "is conditional on", "buys/sells being volumetrically balanced"],
    ["Balancing desk entry", "changes", "calculation of what is due from/to Tenaska IV"],
    ["Jim Pond", "asks", "whether UA4 entry should be recorded for Cleburne"],
    ["Jim Pond", "asks", "if UA4 entry is addressed in agreement with Tenaska"],
    ["PMA’s entries", "allow", "volumes to be adjusted through the system as usual"]
  ]

six_shot_triples_output = [
    ["UA4", "is on", "Jim Pond's schedule"],
    ["ENA", "books entry", "to balance desk"],
    ["Booking entry", "is conditional on", "buys/sells being volumetrically balanced"],
    ["Balancing desk entry", "changes", "calculation of what is due from/to Tenaska IV"],
    ["Jim Pond", "asks", "whether UA4 entry should be recorded for Cleburne"],
    ["Jim Pond", "asks", "if UA4 entry is addressed in agreement with Tenaska"],
    ["PMA’s entries", "allow", "volumes to be adjusted through the system as usual"],
    ["Daren J Farmer", "can adjust", "demand fee on Sitara ticket"],
    ["Daren J Farmer", "is not able to follow", "Jim Pond's UA4 calculation"],
    ["Imbalance payback", "occurred", "throughout September and October"],
    ["Imbalance payback", "should have been pathed to", "Lone Star transport k in Unify"],
    ["Williams", "had been trying to make up", "volumes from prior periods"],
    ["Williams' volume", "came in greater than", "booked volume"],
    ["Much of Williams' gas", "is from", "El Paso"],
    ["Williams' volumes", "vary each day from", "scheduled volumes"],
    ["Volumes Williams was trying to make up", "go toward", "transport imbalance"],
    ["Daren J Farmer", "expects", "Cleburne will carry imbalance on Lone Star from month to month"],
    ["Imbalance", "should be", "fairly small after November"],
    ["Mark McCoy", "is", "scheduler"],
    ["Mark McCoy", "will have", "imbalance number"],
    ["Imbalance on Lone Star", "was", "very large when ENA took over deal"],
    ["Plant shutdown in September", "led to", "payback of imbalance"],
    ["Plant", "went down", "in September"],
    ["ENA", "decided to pay back in September", "the imbalance"],
    ["ENA", "could take advantage of if the opportunity came up", "higher winter sales prices"],
    ["Tenaska IV agreement", "does not specifically state", "anything about UA4"],
    ["Daren J Farmer", "will discuss", "UA4 with Legal"],
    ["All costs", "are to be covered by", "Tenaska IV"],
    ["All costs", "include", "UA4 costs"],
    ["All costs", "include", "Fuel costs"],
    ["Daren J Farmer", "will leave", "at 1pm today"],
    ["Daren J Farmer", "will return", "Tuesday 12/19"],
    ["Daren J Farmer and Jim Pond", "can get together on", "Tuesday 12/19"]
  ]


seven_shot_triples_output =  [
    ["David Ingram", "performs", "analysis"],
    ["David Ingram", "finds", "problems in analysis"],
    ["Mother data", "pulls", "Zone P number"],
    ["Zone P number", "is", "wrong"],
    ["Pointer for the data", "can be found on", "SQL worksheet"],
    ["Pointer for the data", "points to", "the expression"],
    ["The expression", "is", "avg(decode(prc.power_reference_period_cd,'DAYAHEAD', decode(pl.location_name,'PJM',price_amt))) PJM_DA"],
    ["The expression", "is", "avg(decode(prc.power_reference_period_cd,'HOURLY', decode(pl.location_name,'PJM',price_amt))) PJM_RT"],
    ["David Ingram", "looks at", "PJM prices"],
    ["David Ingram", "looks at", "NY prices"],
    ["David Ingram", "cannot figure out", "source of Zone P number"],
    ["Other 24hr desk", "has been told", "PJM night shift preps PJM portion of shift notes"],
    ["Other 24hr desk", "has been told", "PJM night shift preps Nepool portion of shift notes"],
    ["David Ingram", "writes", "macro to pull Nepool information"],
    ["David Ingram", "writes", "macro to format Nepool information"],
    ["David Ingram", "writes", "macro to print Nepool information"],
    ["PJM information", "is not available on", "website"],
    ["East power portal", "has", "some PJM information"],
    ["David Ingram", "thinks", "East power portal does some kind of Op Sum pull at unknown interval"],
    ["PJM Information from East power portal", "is", "inaccurate"],
    ["Rob Bensen", "is frustrated with", "bad information"],
    ["Rob Bensen’s frustration", "is main reason", "other 24hr desk avoids reporting"],
    ["All data points", "differ from", "one hour averages calculated in edata"],
    ["Difference in data points", "causes", "David Ingram’s doubt that opsum is the source"],
    ["David Ingram", "doubts", "opsum is the source"],
    ["Edata", "pulls from", "opsum"],
    ["All interfaces and hubs", "are printing", "the same"],
    ["Prices shown on website", "differ", "in the same hour"],
    ["David Ingram", "has no idea", "where these prices are coming from"],
    ["Prices shown on website", "are", "not right"],
    ["Application at 'M:\\Electric\\24hour\\PJM AVE\\PJMSummary.exe'", "pulls from", "database"],
    ["Correct data", "can be found by", "application at 'M:\\Electric\\24hour\\PJM AVE\\PJMSummary.exe'"],
    ["IT Team", "could fix", "this app"],
    ["David Ingram", "would care less about", "the web site"],
    ["IT team", "do not want to fix", "the app"],
    ["David Ingram", "can write", "macro"],
    ["Macro", "pulls", "same data from the mother data template"],
    ["David Ingram", "does not care", "how he gets the data"],
    ["David Ingram", "needs", "yesterday’s PJM data for shift note"],
    ["Following the DA-RT physical moves", "depends on", "trading some of the regular products"],
    ["David Ingram and team", "man", "24hr desk"],
    ["24hr desk team", "could cover", "DA-RT physical"],
    ["Bryce", "is", "day guy at 24hr desk"],
    ["Covering DA-RT physical moves", "is part of", "24hr desk"],
    ["Covering DA-RT physical moves as part of 24hr desk", "uses", "evening load"],
    ["Covering DA-RT physical moves as part of 24hr desk", "uses", "more up-to-date weather forecasts"],
    ["Evening load", "could be used", "when entering NY side in early morning"],
    ["More up-to-date weather forecasts", "could be used", "when entering NY side in early morning"],
    ["24hr desk point", "is conditional on", "Paul D. Thomas being too busy trading PJM to spend the same time on analysis"],
    ["Uninterrupted analysis", "is easier", "on back shift"],
    ["Diana Allen", "works on", "resolving bad Zone P day-ahead data"],
    ["IT team", "works on", "resolving bad Zone P day-ahead data"],
    ["Diana Allen", "works on", "resolving bad Zone P real-time data"],
    ["IT team", "works on", "resolving bad Zone P real-time data"],
    ["Diana Allen", "told", "Paul D. Thomas"],
    ["Bad Zone P data", "was pulling", "PJM data"],
    ["Paul D. Thomas", "talks to", "Rob Benson about shift notes"],
    ["Rob Benson", "says", "shift notes have improved greatly"],
    ["PJM summary page", "is", "pretty accurate"],
    ["PJM summary page", "is", "usually within 50 cents of the actual number"],
    ["Link for spreadsheet", "is", "http://eastpower.test.corp.enron.com/portal/summary/pjmsummary.aspx"]
  ]

eight_shot_triples_output = [
    ["Diana Allen", "told", "Paul D. Thomas"],
    ["Bad Zone P data", "was pulling", "PJM data"],
    ["Paul D. Thomas", "talks to", "Rob Benson about shift notes"],
    ["Rob Benson", "says", "shift notes have improved greatly"],
    ["PJM summary page", "is", "pretty accurate"],
    ["PJM summary page", "is", "usually within 50 cents of the actual number"],
    ["Link for spreadsheet", "is", "http://eastpower.test.corp.enron.com/portal/summary/pjmsummary.aspx"],
    ["David Ingram", "might have been using", "old version of spreadsheet"],
    ["Paul D. Thomas", "will continue to manage", "Northeast physical book"],
    ["Managing the Northeast physical book", "allows", "Paul D. Thomas to hedge position"],
    ["Paul D. Thomas", "hedges", "long position in off-peak market"],
    ["Paul D. Thomas", "hedges", "short position in off-peak market"],
    ["Diana Allen", "said", "she fixed the Zone P problem"],
    ["Diana Allen", "fixed", "Zone P problem"],
    ["David Ingram", "does not doubt", "PJM summary has improved"],
    ["David Ingram", "pulls data directly from", "edata"],
    ["David Ingram", "does not use", "website"],
    ["David Ingram", "will begin to record", "difference"],
    ["David Ingram", "will talk with", "web data folks"],
    ["Web data folks", "are pulling", "data"],
    ["David Ingram", "attempts to understand", "where web data folks are pulling the data"],
    ["David Ingram", "has been using", "updated website"],
    ["David Ingram", "spot checked", "Zone P prices"],
    ["Zone P prices", "had", "few errors of little consequence"],
    ["David Ingram", "was doing", "analysis on NE physical"],
    ["24to6", "has been", "a pretty solid play"],
    ["24to6", "has been a solid play on", "DAP to DAW"],
    ["24to6", "has been a solid play on", "DAP to RTW"],
    ["24to6", "has been a solid play on", "DA to RT during other hours"],
    ["David Ingram", "cannot tell", "why 24to6 is not being scheduled"],
    ["Paul D. Thomas", "is busy managing", "EOL products"],
    ["David Ingram", "does not have", "experience to understand reason"],
    ["Northeast physical book", "belongs to", "Paul D. Thomas"],
    ["Paul D. Thomas", "wants to keep", "earnings"],
    ["David Ingram", "noticed", "opportunity appears to be there"],
    ["David Ingram and team", "can do", "some of the analysis"],
    ["David Ingram and team", "can pass", "analysis to Paul D. Thomas"],
    ["Paul D. Thomas", "places", "the orders"],
    ["Paul D. Thomas", "might tell", "David Ingram and team what he wants to do in NY"],
    ["Paul D. Thomas", "can decide", "what to do with it on the day shift"],
    ["David Ingram", "does not want to step on", "Paul D. Thomas’s turf"],
    ["Paul D. Thomas", "has done well with", "books he has"],
    ["Scenario", "is easy to see", "where Paul D. Thomas will trade more during the day"],
    ["Paul D. Thomas", "moves to use", "NE physical book more for hedging"],
    ["Gautam", "has used", "NE physical book for hedging"],
    ["24 hour desk traders", "may take on", "more of the speculative portion of the physical market"],
    ["Getting the other guys", "to think about", "speculative portion of the physical market"],
    ["Other guys", "could try", "ideas in the previous paragraph"],
    ["Talking about this over email", "is", "hard"],
    ["David Ingram", "would like to find", "time to discuss this with Paul D. Thomas"]
  ]


nine_shot_triples_output = []

ten_shot_triples_output = []

# Define 10-shot examples: each is (user_input, assistant_output)
shots = [
    # Shot 1
    {
        "passage": one_shot_ner_paragraph,
        "named_entity_json": one_shot_ner_output,
        "triples": one_shot_triples_output
    },
    {
        "passage": two_shot_ner_paragraph,
        "named_entity_json": two_shot_ner_output,
        "triples": two_shot_triples_output
    },
    {
        "passage": three_shot_ner_paragraph,
        "named_entity_json": three_shot_ner_output,
        "triples": three_shot_triples_output
    },
    {
        "passage": four_shot_ner_paragraph,
        "named_entity_json": four_shot_ner_output,
        "triples": four_shot_triples_output
    },
    {
        "passage": five_shot_ner_paragraph,
        "named_entity_json": five_shot_ner_output,
        "triples": five_shot_triples_output
    },
    {
        "passage": six_shot_ner_paragraph,
        "named_entity_json": six_shot_ner_output,
        "triples": six_shot_triples_output
    },
    {
        "passage": seven_shot_ner_paragraph,
        "named_entity_json": seven_shot_ner_output,
        "triples": seven_shot_triples_output
    },
    {
        "passage": eight_shot_ner_paragraph,
        "named_entity_json": eight_shot_ner_output,
        "triples": eight_shot_triples_output
    },
    {
        "passage": nine_shot_ner_paragraph,
        "named_entity_json": nine_shot_ner_output,
        "triples": nine_shot_triples_output
    },
    {
        "passage": ten_shot_ner_paragraph,
        "named_entity_json": ten_shot_ner_output,
        "triples": ten_shot_triples_output
    },
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
