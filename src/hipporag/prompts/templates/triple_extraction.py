from .ner import one_shot_ner_paragraph, one_shot_ner_output
from ...utils.llm_utils import convert_format_to_template

ner_conditioned_re_system = """You are an open information extraction (OpenIE) model.

Task: Extract all factual relations from a given email in the form of RDF triples (subject, predicate, object). Each triple expresses a complete factual relation from the email text. The extracted triples will be used to construct a knowledge graph for downstream text completion, so correctness (precision) and completeness (recall) are extremely important.

Input Format: The input is an email followed by a list of named entities extracted from that email. The email may be a thread, consisting of multiple emails. Each email is delimited by [EMAIL X START] and [EMAIL X END], where X denotes its number in the thread. Each email contains its metadata (date, sender, recipients, subject) followed by the message body.
Emails may be split into chunks due to token limits:
- If a chunk ends with [INFO: this email was truncated; continuation will appear in the next chunk], it means the current chunk does not contain the full email.
- Continuation chunks start with [INFO: truncated due to token limit; this is a continuation from previous chunk] and include the full metadata of the continued email.
Treat each chunk as part of the full email. Extract all triples, including those in overlapping regions without duplicating them unnecessarily.

Triple Extraction Guidelines: Strictly follow these 4 extraction guidelines:
1. Completeness - Extract all triples from the text.
2. Assertedness - Only extract triples that are explicitly or implicitly implied by the original text.
3. Informativeness - Include the maximum amount of relevant information in each argument (i.e., subject or object).
4. Atomicity - Each triple must be an indivisible unit. Whenever possible, extract multiple atomic triples from a text that has conjunctions.

Additional instructions:
1. Do NOT extract triples from emails that are (1) non-personal/machine-generated (e.g., newsletters, system notifications, alerts, marketing, and transactional), or (2) not in English.
2. Each triple should contain at least one, but preferably two, of the named entities in the list for each passage.
3. Clearly resolve pronouns to their specific names to maintain clarity using the message context, or metadata entities, only if it clearly supports the resolution.
4. Do NOT include triples about the structure of the email itself (e.g., “Kate sent email to Rhonda”).

Output Format: Convert the input into a JSON dictionary with the following two keys:
- "named entities": list of extracted entity strings (given or revalidated)
- "triples": list of RDF triples (subject, predicate, object)
"""


ner_conditioned_re_frame = """Convert the paragraph into a JSON dict, it has a named entity list and a triple list.
Email Chunk:
```
{passage}
```

{named_entity_json}
"""


ner_conditioned_re_input = ner_conditioned_re_frame.format(passage=one_shot_ner_paragraph, named_entity_json=one_shot_ner_output)

ner_conditioned_re_output = """{"triples": [
            ["Enron", "made", "$1.2Bn total in 2001"], 
            ["Half of $1.2Bn", "came from", "new deals"], 
            ["Half of $1.2Bn", "came from", "reserve releases"], 
            ["When prudency release is backed out", "result is", "zero net curve shift for 2001"], 
            ["The original file", "had", "approximately zero net curve shift for 2001"], 
            ["Optics of Enron’s Gas P&L", "are", "not good"] 
    ] 
}
"""


prompt_template = [
    {"role": "system", "content": ner_conditioned_re_system},
    {"role": "user", "content": ner_conditioned_re_input},
    {"role": "assistant", "content": ner_conditioned_re_output},
    {"role": "user", "content": convert_format_to_template(original_string=ner_conditioned_re_frame, placeholder_mapping=None, static_values=None)}
]