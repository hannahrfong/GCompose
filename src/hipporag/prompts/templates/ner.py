ner_system = """You are a named entity extractor model.

Task: Extract all named entities from the given email. Named entities refer to specific, identifiable entities mentioned in the text. These named entities will be used to build a knowledge graph that supports multi-hop reasoning for email text completion. Therefore, both correctness (precision) and completeness (recall) are important in the named entity extraction process. 

Instructions: 
1. Do NOT classify or label the entities.
2. Extract entities exactly as they worded in the text.

Output Format: Respond with a JSON list of named entity strings.
"""

five_shot_ner_paragraph = """[EMAIL 1 START]
Date: 12/07/2000 09:18 AM
From: Megan Parker @ ENRON
To: Daren J Farmer/HOU/ECT@ECT
Cc: 
Bcc: 
Subject: Tenaska IV 10/00
Type: original

We have actuals.  The larger of the two volumes is 1,395,000, which is 
45,000/day, so the demand rate in deal 514353 is fine.  I am having a 
problem, though, with the way it is coming to settlements.  It is showing up 
with a Jan 2003 delivery date.  I think the demand fee needs to be on 10/1 
only.  Right now, it is on a line with a date of 10/1/00 to 12/31/36.   I 
think this is confusing the system some how.  Also, we still need the 
purchase deal for Tenaska IV.  It should be for a demand fee of $2,571,135.73 
booked to the Cleburne desk.  We actually owe $1,798,389.73, but I need to 
net the Tenaska IV sales with the purchase to clear those receivables.  James 
is calling me every day asking for an update.  Do you know when we will be 
able to get this in the system?  I have attached my spreadsheet so you can 
see the numbers.






Megan
[EMAIL 1 END]

[EMAIL 2 START]
Date: 12/12/2000 04:48 PM
From: Daren J Farmer/HOU/ECT
To: Greg Whiting/Corp/Enron, Troy Klussmann/HOU/ECT@ECT, James Armstrong/HOU/ECT@ECT, Megan Parker/Corp/Enron, Jim Pond/Corp/Enron
Cc: 
Bcc: 
Subject: Tenaska IV 10/00
Type: forwarded EMAIL 1

In most cases, ENA will be a net buyer from Tenaska IV for activity related 
to the Cleburne plant.  However, for October 2000, the plant was down the 
majority of the month and ENA sold off the supply, resulting in ENA owing 
money to Tenaska IV.

I have created deal 529856 with a demand of $1,798,389.73, which is the 
calculated amount of income on the Cleburne desk. (Please see the attached 
schedule.)   We need to pass this income on to Tenaska IV.  Do we need to pay 
this amount (wire from ENA to Tenaska IV) or is there another way to do 
this?  This is the case for October 2000 and could possibly happen again in 
the future.

Greg, Troy, Jim - Please let me know what you think about settling this.

Megan - Don't pay the amount until we here from the Greg, Troy and Jim.  
Also, make sure that we have received dollars from the spot sales before we 
reimburse Tenaska IV.

D
[EMAIL 2 END]

[EMAIL 3 START]
Date: 12/14/2000 08:56 AM
From: Jim Pond @ ENRON
To: Daren J Farmer/HOU/ECT@ECT
Cc: Greg Whiting/Corp/Enron@ECT, Troy Klussmann/HOU/ECT@ECT, James Armstrong/HOU/ECT@ECT, Megan Parker/Corp/Enron@ECT
Bcc: 
Subject: Re: Tenaska IV 10/00
Type: replied to EMAIL 2

Darren, 
The demand fee is probably the best solution.  We can use it to create a 
recieivable/payable with Tenaska, depending on which way the calculation goes 
each month.  How are PMA's to be handled once the fee been calculated and the 
deal put in the system?

Attatched is a schedule detailing what is on the GL for Cleburne as of 
today.  Some of this info will change by the end of the month.  As you can 
see, there are some discrepancies between Megan's calculations and what is on 
the general ledger.  UA4 is also on my schedule.  Unless the buys/sells are 
volumetrically balanced, we book an entry to balance the desk.  This will 
change the calculation of what is due from/to Tenaska.  Should we be 
recording a UA4 entry for Cleburne?  Is it addressed in the agreement with 
Tenaska?
[EMAIL 3 END]

[EMAIL 4 START]
Date: Thu, 14 Dec 2000 04:43:00 -0800 (PST)
From: Daren J Farmer (daren.farmer@enron.com)
To: Jim Pond (jim.pond@enron.com)
Cc: Greg Whiting (greg.whiting@enron.com), Troy Klussmann (troy.klussmann@enron.com), James Armstrong (james.armstrong@enron.com), Megan Parker (megan.parker@enron.com)
Bcc: greg.whiting@enron.com, troy.klussmann@enron.com, james.armstrong@enron.com, megan.parker@enron.com
Subject: Re: Tenaska IV 10/00
Type: replied to EMAIL 3

With PMA's, volumes can be adjusted through the system as usual and I can
[INFO: this email was truncated; continuation will appear in the next chunk]
"""

five_shot_ner_output = """{"named_entities": [
    "12/07/2000 09:18 AM",
    "Megan Parker",
    "ENRON",
    "Daren J Farmer",
    "Tenaska IV",
    "Tenaska IV 10/00",
    "Tenaska",
    "Jan 2003",
    "10/1",
    "10/1/00 to 12/31/36",
    "Cleburne desk",
    "Cleburne plant",
    "$2,571,135.73",
    "$1,798,389.73",
    "12/12/2000 04:48 PM",
    "Greg Whiting",
    "Corp",
    "Troy Klussmann",
    "James Armstrong",
    "Jim Pond",
    "October 2000",
    "12/14/2000 08:56 AM",
    "deal 514353",
    "deal 529856",
    "ENA",
    "PMA",
    "UA4",
    "Thu, 14 Dec 2000 04:43:00 -0800 (PST)",
    "daren.farmer@enron.com",
    "jim.pond@enron.com",
    "greg.whiting@enron.com",
    "troy.klussmann@enron.com",
    "james.armstrong@enron.com",
    "megan.parker@enron.com"
]}
"""

six_shot_ner_paragraph = """[EMAIL 3 START]
Date: 12/14/2000 08:56 AM
From: Jim Pond @ ENRON
To: Daren J Farmer/HOU/ECT@ECT
Cc: Greg Whiting/Corp/Enron@ECT, Troy Klussmann/HOU/ECT@ECT, James Armstrong/HOU/ECT@ECT, Megan Parker/Corp/Enron@ECT
Bcc: 
Subject: Re: Tenaska IV 10/00
Type: replied to EMAIL 2

[INFO: truncated due to token limit; this is a continuation from previous chunk]
… is on 
the general ledger.  UA4 is also on my schedule.  Unless the buys/sells are 
volumetrically balanced, we book an entry to balance the desk.  This will 
change the calculation of what is due from/to Tenaska.  Should we be 
recording a UA4 entry for Cleburne?  Is it addressed in the agreement with 
Tenaska?
[EMAIL 3 END]

[EMAIL 4 START]
Date: Thu, 14 Dec 2000 04:43:00 -0800 (PST)
From: Daren J Farmer (daren.farmer@enron.com)
To: Jim Pond (jim.pond@enron.com)
Cc: Greg Whiting (greg.whiting@enron.com), Troy Klussmann (troy.klussmann@enron.com), James Armstrong (james.armstrong@enron.com), Megan Parker (megan.parker@enron.com)
Bcc: greg.whiting@enron.com, troy.klussmann@enron.com, james.armstrong@enron.com, megan.parker@enron.com
Subject: Re: Tenaska IV 10/00
Type: replied to EMAIL 3

With PMA's, volumes can be adjusted through the system as usual and I can 
adjust the demand fee on the Sitara ticket.  I am not able to follow your ua4 
calculation.  However, there was imbalance payback that occurred throughout 
September and October.  (This should have been pathed to the Lone Star 
transport k in Unify).  Is this in that ua4 number?  Williams had been trying 
to make up volumes from prior periods, so that's probably why their volume 
came in greater than booked.  (Much of their gas is from El Paso and volumes 
vary each day from scheduled.)  The volumes that they were trying to make up 
would go toward the transport imbalance also.  I would think that Cleburne 
will carry an imbalance on Lone Star from month to month.  After Novemeber, 
the imbalance should be fairly small.  Our scheduler, Mark McCoy will have 
that number.  (When we took over this deal, the imbalance on Lone Star was 
very large.   When the plant went down in Sep, we decided to payback the 
imbalance then, so that we could take advantage of higher winter sales prices 
if the opportunity came up.)

The agreement does not specifically state anything about ua4.  But, I will 
discuss that with Legal.  The intent is for all costs, including ua4 and 
fuel, to be covered by Tenaska IV.

I will be leaving at 1pm today and will return on Tuesday 12/19.  We can get 
together then if you would like.

D
[EMAIL 4 END]
"""

six_shot_ner_output = """{"named_entities": [
    "Jim Pond",
    "ENRON",
    "Daren J Farmer",
    "Greg Whiting",
    "Troy Klussmann",
    "James Armstrong",
    "Megan Parker",
    "Tenaska IV 10/00",
    "Tenaska",
    "Tenaska IV",
    "UA4",
    "Cleburne",
    "PMA",
    "Sitara",
    "September",
    "October",
    "Lone Star",
    "November",
    "Unify",
    "Williams",
    "El Paso",
    "Mark McCoy",
    "Legal",
    "1:00 PM",
    "Tuesday 12/19",
    "Thu, 14 Dec 2000 04:43:00 -0800 (PST)",
    "12/14/2000 08:56 AM",
    "daren.farmer@enron.com",
    "jim.pond@enron.com",
    "greg.whiting@enron.com",
    "troy.klussmann@enron.com",
    "james.armstrong@enron.com",
    "megan.parker@enron.com"
]}
"""

eleven_shot_ner_paragraph = """[EMAIL 1 START]\nDate: Fri, 21 Apr 2000 04:25:00 -0700 (PDT)\nFrom: Mark E Haedicke (mark.haedicke@enron.com)\nTo: George McClellan (george.mcclellan@enron.com)\nCc: Richard B Sanders (richard.sanders@enron.com), Robert Quick (robert.quick@enron.com), Stuart Staley (stuart.staley@enron.com)\nBcc: richard.sanders@enron.com, robert.quick@enron.com, stuart.staley@enron.com\nSubject: Re: Mission UK\nType: replied to EMAIL 0\n\nGeorge, I think your proposal is a good one in light of all the facts at \nhand.  I think it is best if we take the high road in approach as you have \nproposed.  I would ask Robert to prepare a one page bullet list of your \npoints and then let's all briefly review it.  I want to stay mindful that \nlitigation is possible and we have to chose our words carefully in event of \nlitigation.  \n\nMark\n[EMAIL 1 END]\n
"""

eleven_shot_ner_output = """
{
  "named_entities": [
    "Fri, April 21, 2000 at 04:25:00 -0700 (PDT)",
    "Mark E Haedicke",
    "mark.haedicke@enron.com",
    "George McClellan",
    "george.mcclellan@enron.com",
    "Richard B Sanders",
    "richard.sanders@enron.com",
    "Robert Quick",
    "robert.quick@enron.com",
    "Stuart Staley",
    "stuart.staley@enron.com",
    "Mission UK"
  ],
  "extracted_triples": [
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
}
"""

prompt_template = [
    {"role": "system", "content": ner_system},

    {"role": "user", "content": five_shot_ner_paragraph},
    {"role": "assistant", "content": five_shot_ner_output},

    {"role": "user", "content": six_shot_ner_paragraph},
    {"role": "assistant", "content": six_shot_ner_output},

    {"role": "user", "content": eleven_shot_ner_paragraph},
    {"role": "assistant", "content": eleven_shot_ner_output},

    {"role": "user", "content": "${passage}"}
]