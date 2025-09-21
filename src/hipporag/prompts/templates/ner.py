ner_system = """You are a named entity extractor model.

Task: Extract all named entities from a given email. Named entities refer to specific, uniquely identifiable entities mentioned in the text. The extracted entities will be used to construct a knowledge graph for downstream text completion, so correctness (precision) and completeness (recall) are extremely important.

Input Format: The input is an email, which may be a thread consisting of multiple emails. Each email in a thread is delimited by [EMAIL X START] and [EMAIL X END], where X denotes its number in the thread. Each email contains its metadata (date, sender, recipients, subject) followed by the message body.
Emails may be split into chunks due to token limits:
- If a chunk ends with [INFO: this email was truncated; continuation will appear in the next chunk], it means the current chunk does not contain the full email.
- Continuation chunks start with [INFO: truncated due to token limit; this is a continuation from previous chunk] and include the full metadata of the continued email.
Treat each chunk as part of the full email. Extract all entities, including those in overlapping regions without duplicating them unnecessarily.

Instructions:
1. Do NOT extract entities from emails that are (1) non-personal/machine-generated (e.g., newsletters, system notifications, alerts, marketing, and transactional), or (2) not in English.
2. Do NOT classify or label the entities.
3. Extract date and time as a single human-readable string (e.g., “April 24, 2001 at 3:23 PM”). 

Output Format: Respond with a JSON list of named entity strings.
"""

one_shot_ner_paragraph = """
[EMAIL 1 START]
Date: Monday, December 10, 2001 5:00 PM
From: Brad Jones
To: daniel.mcdonagh@chase.com, Phillip K. Allen, pallen70@hotmail.com
Cc: Frank Hayden, Jeffrey C. Gossett
Bcc: 
Subject: Gas P&L by day
Type: original

Attached is the information you have requested.

Thanks,
Brad Jones
[EMAIL 1 END]

[EMAIL 2 START]
Date: Monday, December 10, 2001 5:22 PM
From: Frank Hayden
To: David Port
Cc: 
Bcc: 
Subject: FW: Gas P&L by day
Type: replied to EMAIL 1

[INFO: no message body provided]
[EMAIL 2 END]

[EMAIL 3 START]
Date: Mon, 10 Dec 2001 15:31:51 -0800 (PST)
From: David Port (david.port@enron.com)
To: Phillip K. Allen (k..allen@enron.com)
Cc: 
Bcc: 
Subject: FW: Gas P&L by day
Type: replied to EMAIL 2

Phillip
My interpretation of this is that we made $1.2Bn total, half from new deals and the other half from reserve releases, and when you back out the prudency release you get back to zero net curve shift for 2001, which is what the original file had (approximately)
Optics aren't good
DP
[EMAIL 3 END]
"""


one_shot_ner_output = """{“named_entities”: 
    ["Monday, December 10, 2001 at 5:00 PM", "Brad Jones", "daniel.mcdonagh@chase.com", "Phillip K. Allen", "pallen70@hotmail.com", "Frank Hayden", "Jeffrey C. Gossett", "Gas P&L by day", "Monday, December 10, 2001 at 5:22 PM", "David Port", "Monday, December 10, 2001 at 3:31 PM", "David Port", "david.port@enron.com", "Phillip K. Allen", "k..allen@enron.com", "$1.2Bn", "2001"]
}
"""


prompt_template = [
    {"role": "system", "content": ner_system},
    {"role": "user", "content": one_shot_ner_paragraph},
    {"role": "assistant", "content": one_shot_ner_output},
    {"role": "user", "content": "${passage}"}
]