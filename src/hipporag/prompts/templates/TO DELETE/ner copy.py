ner_system = """You are a named entity extractor model.

Task: Extract all named entities from the given email. Named entities refer to specific, identifiable entities mentioned in the text. These named entities will be used to build a knowledge graph that supports multi-hop reasoning for email text completion. Therefore, both correctness (precision) and completeness (recall) are important in the named entity extraction process. 

Instructions: 
1. Do NOT classify or label the entities.
2. Extract entities exactly as they worded in the text.

Output Format: Respond with a JSON list of named entity strings.
"""

one_shot_ner_paragraph = """[EMAIL 1 START]
Date: 11/15/2000 07:32 PM
From: Timothy J Detmering
To: David Oxley/HOU/ECT@ECT, Brian Redmond/HOU/ECT@ECT, Patrick Wade/HOU/ECT@ECT, Anne C Koehler/HOU/ECT@ECT
Cc:
Bcc:
Subject: Triple Lutz Employee Matters
Type: original


With respect to bidder D we are being asked not to compete with them for
those employees they would like to hire.  i.e. we have to sever them and
bidder D gets to hire them if they want to (in which case the severed
employees get no severance payment if they turn DFS down).  I would like to
propose something like the following:


1.  We provide Bidder D with a list of all Designated Employees, their
position, historical compensation.
2.  Bidder D covenants to make offers to ___% of certain pools of Designated
Employees e.g. commercial, operations, engineering, trading, etc.
3.  Bidder D covenants to make offers that will not allow Designated
Employees to successfully claim constructive dismissal under our severance
plan.
4.  Between signing and closing, Bidder D provide us with a list of Offerees
- Designated Employees to whom Bidder D intends to make offers of   
employment.
5.  ENA covenants that we will not interfere with Bidder D's offers (can we
bind all of Enron?).
6.  If an Offeree turns down the offer (in writing) then ENA is free to
continue to employee Offeree.  However, if we do not continue to employ the
Offeree, no   severance is owed.


The intent of the above is to encourage Offerees to take the offers - they
give up severance rights if they don't - but provide us the opportunity to
continue to employee anyone who is bold enough to turn it down and that we
want to keep.  Also it caps our severance obligation by requiring Bidder D to
specify how many offers must be made.  Bidder D is certain to want more than
this but I am uncomfortable saying we can't continue to employee any of the
Offerees.


Please advise.
[EMAIL 1 END]


[EMAIL 2 START]
Date: 11/26/2000 06:50 PM
From: David Oxley
To: Michelle Cash/HOU/ECT@ECT, Fran L Mayes/HOU/ECT@ECT
Cc:
Bcc:
Subject: Triple Lutz Employee Matters
Type: forwarded EMAIL 1


What's your view?
[EMAIL 2 END]


[EMAIL 3 START]
Date: Sun, 26 Nov 2000 15:41:00 -0800 (PST)
From: Michelle Cash (michelle.cash@enron.com)
To: David Oxley (david.oxley@enron.com)
Cc: Fran L Mayes (fran.mayes@enron.com), Anne C Koehler (anne.koehler@enron.com)
Bcc: fran.mayes@enron.com, anne.koehler@enron.com
Subject: Re: Triple Lutz Employee Matters
Type: replied to EMAIL 2


David,


I think this point is moot for the time being because (as of last Tuesday) we
are not dealing with Bidder D.


I think it is ok legally to go this way -- although there is potential
liability under the WARN Act (the plant closing law).  We probably can
schedule around that exposure, though, by giving everyone who possibly may be
affected 60 days' notice.


Practically, however, this would not be my favorite approach.  I'd prefer it
if we could have the ability to compete for top performers, but we should be
able to manage that by working through the persons who we identify and
present for possible hiring by the buyer. 


I would like more information about what is meant by "ENA does not interfere
with" the offers made by the buyer.  Does that mean no counteroffers?


To answer the question of whether we can bind all of Enron, I would say that
it is unlikely, unless we want to ask.  It is easier to commit only the
wholesale group, rather than ask Corp., EES, Broadband, etc.  whether they
will abide by the agreement, so I would recommend limiting it to that group,
if possible.  We may be able to include the pipelines, given that they have
been involved in this transaction.


Let me know if you have any questions.


Michelle
[EMAIL 3 END]
"""

one_shot_ner_output = """{"named_entities": [
  "11/15/2000 07:32 PM",
  "Timothy J Detmering",
  "David Oxley",
  "Brian Redmond",
  "Patrick Wade",
  "Anne C Koehler",
  "Triple Lutz",
  "Bidder D",
  "Designated Employees",
  "Offerees",
  "DFS",
  "ENA",
  "Enron",
  "11/26/2000 06:50 PM",
  "Michelle Cash",
  "michelle.cash@enron.com",
  "david.oxley@enron.com",
  "fran.mayes@enron.com",
  "anne.koehler@enron.com",
  "Fran L Mayes",
  "Sun, 26 Nov 2000 15:41:00 -0800 (PST)",
  "Tuesday",
  "WARN Act",
  "Corp.",
  "EES",
  "Broadband"
]}
"""

two_shot_ner_paragraph = """[EMAIL 1 START]
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


two_shot_ner_output = """{"named_entities": [
    "Monday, December 10, 2001 5:00 PM",
    "Brad Jones",
    "daniel.mcdonagh@chase.com",
    "Phillip K. Allen",
    "pallen70@hotmail.com",
    "Frank Hayden",
    "Jeffrey C. Gossett",
    "Gas P&L",
    "Monday, December 10, 2001 5:22 PM",
    "David Port",
    "Mon, 10 Dec 2001 15:31:51 -0800 (PST)",
    "david.port@enron.com",
    "k..allen@enron.com",
    "$1.2Bn",
    "2001"
]}
"""


three_shot_ner_paragraph = """[EMAIL 1 START]
Date: > > > Sent: Wednesday, October 25, 2000 8:19 AM
From: > > > From: Simon O'mahony [SMTP:] (Simon.Omahony@aocnet.com)
To: 
Cc: 
Bcc: 
Subject: 
Type: original

> > > To: Corkage; Fionagh McKeoghan; Geraldo Gibney; GSaunders; HBD;
Lollie;
 > > > Martin Eastwood; Max Halton; Neal; Sara & Jay; Evyn; Molly;
Sorcha@Work
 > > > Subject: FW: Adds!
 > > >
 > > >
 > > >
 > > >
 > > >       <<kellogs_1.jpg>>  <<greengiant_1.jpg>>  <<bastardcard_1.jpg>>
 > > > <<sandwich_1.jpg>>  <<tubbies_1.jpg>>

_________________________________________________________________________
Get Your Private, Free E-mail from MSN Hotmail at http://www.hotmail.com.

Share information about yourself, create your own public profile at
http://profiles.msn.com.

 - kellogs_1.jpg
 - greengiant_1.jpg
 - bastardcard_1.jpg
 - sandwich_1.jpg
 - tubbies_1.jpg
[EMAIL 1 END]

[EMAIL 2 START]
Date: Date: Thu, 26 Oct 2000 15:49:00 CDT
From: tim johnson (timmywayne2000@hotmail.com)
To: royalventure@prodigy.net, straubinger77@hotmail.com, klayman62@hotmail.com, mnshorts@hotmail.com, amazona115@hotmail.com, younga9@hotmail.com, pinkdonut@bigfoot.com, lesliej@oio.net, portunus0@hotmail.com, aeastes@austinc.edu, ladybug0adr@cs.com, jasonbrownmusic@aol.com, canowa@hotmail.com, cdorrian79@hotmail.com, fkirby@austinc.edu, gvaughn@austinc.edu, hoent000@mail.uni-mainz.de, houston@texoma.net, jnassiri@austinc.edu, kanganic@aol.com, lmgentry@austinc.edu, lwoerner@austinc.edu, mballases@hotmail.com, michelle.marak@rrc.state.tx.us, mmeixner@austinc.edu, sprice@austinc.edu, tranders@austinc.edu, weed@ev1.net
Cc: 
Bcc: 
Subject: Fwd: FW: Adds!
Type: replied to EMAIL 1

>From: "kasey peterson" <kaseypeterson@hotmail.com>
 >To: timmywayne2000@hotmail.com
 >Subject: Fwd: FW: Adds!
 >Date: Thu, 26 Oct 2000 20:35:17 GMT
 >
 >
 >
 >
 > >From: "Wedgle, Evyn" <Evyn.Wedgle@AdeccoNA.com>
 > >To: "'Buss, Sarah'" <faebela@yahoo.com>, "'Dennis, Sarah'"
<sarahskiis@aol.com>, 'Drugan' <tommy@gotajob.com>, 'Frenchie'
<mikefabbre@yahoo.com>, 'Kasey' <kaseypeterson@hotmail.com>, 'Kelly Belly'
<kelly_groen@icgcomm.com>, "'McKee, Ryan'"  <rmckee@richclarkson.com>, 'Nate
Dog' <slings@hotmail.com>, 'Newlin'  <tim.newlin@convergentgroup.com>,
"'Ochsner, Chad'" <caochsner@aol.com>, 'Parents' <e.rw@gte.net>, "'Santus,
Erik'" <erik@gotajob.com>, 'Soul sista' <twedgle@hotmail.com>, 'Vic'
<victoria.howlett@memberlending.com>
 > >Subject: FW: Adds!
 > >Date: Thu, 26 Oct 2000 15:12:47 -0400
 > >
 > >These are great!
 > >
[EMAIL 2 END]

[EMAIL 3 START]
Date: Thu, 2 Nov 2000 09:25:00 -0800 (PST)
From: Michael Ballases (mballases@hotmail.com)
To: stormtrooper@fireman.net, ezra@airmail.net, bhoskins@hotmail.com, claydo40@hotmail.com, djcaudle@yahoo.com, douglo@hotmail.com, ebass@enron.com, gfortunov@hotmail.com, gordomcc@rocketmail.com, hcampos@enron.com, jason.bass2@compaq.com, lhunsmi@hotmail.com, lenine.jeganathan@enron.com, shelleyzee@mail.utexas.edu, simpson_molly@hotmail.com, moon77@ihug.com.au, psamarti@austinc.edu, rz411@hotmail.com, sheilaferrarini@hotmail.com, westont@swbell.net
Cc: 
Bcc: 
Subject: Fwd: FW: Adds!
Type: original

----Original Message Follows----
[EMAIL 3 END]
"""

three_shot_ner_output = """{"named_entities": []}
"""

four_shot_ner_paragraph = """[EMAIL 1 START]
Date: > Sent: Sunday, October 14, 2001 3:31 PM
From: > From: (jr289@router.mail.cornell.edu)
To: 
Cc: 
Bcc: 
Subject: 
Type: original

> To:   billy@enron.com

        > Subject:      Associate program at Enron

        >

        > Dear Mr. Lemmons,

        >

        >

        >

        > Please find attached my resume and a cover letter stating my

interest

        > in the

        > Associate program at Enron. I look forward to discussing with you

soon

        > my

        > interest in Enron.

        >

        >

        >

        > At the Johnson School, I am building on my financial analysis and

risk

        > management skills as a portfolio manager in the $2 million Cayuga

MBA

        > Fund,

        > LLC. Previously, I managed ocean physics projects at a consulting

firm

        > for

        > the National Science Foundation and the Office of Naval Research. I

am

        > keen

        > on combining my understanding of the physics of weather and climate

        > with my

        > current training in finance, to structure various energy and

finance

        > transactions.

        >

        >

        >

        > Sincerely,

        >

        >

        >

        > - Jayendran Rajamony

        >

        > MBA Class of 2002

        >

        > Johnson Graduate School of Management

        >

        > Cornell University, Ithaca, NY 14853

        >

        >

        >  - JRajamony_resume_cover.doc <<JRajamony_resume_cover.doc>>
[EMAIL 1 END]

[EMAIL 2 START]
Date: Mon 10/15/2001 9:35 AM
From: Billy Lemmons Jr.
To: Jayendran Rajamony
Cc: Traci Warner, Jeff D. Davis, John Walt
Bcc: 
Subject: FW: Associate program at Enron
Type: replied to EMAIL 1

Jayendran,

        Thank you for your note, and for your interest in Enron's Associate /

        Analyst Program.  I've copied Traci Warner who leads Recruiting for

our

        Program.  Traci, or someone from her team will follow up with you.

        I've also noted your unique mix of weather / climate training and

        experience, combined with your financial analysis and risk management

        background.  We will highlight this experience with a couple of

specific

        groups.

        Please let me know if I can be of further assistance.

        Best regards,

        Billy Lemmons

        Vice President, Associate / Analyst Program
[EMAIL 2 END]

[EMAIL 3 START]
Date: Mon, 15 Oct 2001 19:14:20 -0700 (PDT)
From: Billy Lemmons Jr. (billy.lemmons@enron.com)
To: Mark Tawney (mark.tawney@enron.com), Vince J Kaminski (j.kaminski@enron.com)
Cc: Traci Warner (traci.warner@enron.com), Jeff D. Davis (d..davis@enron.com), John Walt (john.walt@enron.com)
Bcc: traci.warner@enron.com, d..davis@enron.com, john.walt@enron.com
Subject: FW: Associate program at Enron
Type: replied to EMAIL 2

Mark / Vince,

Follow up to my earlier bcc: to you guys.   Any particular interest in this candidate???

Regards,
Billy
[EMAIL 3 END]
"""

four_shot_ner_output = """{"named_entities": [
  "Sunday, October 14, 2001 3:31 PM",
  "jr289@router.mail.cornell.edu",
  "billy@enron.com",
  "Enron",
  "Mr. Lemmons",
  "Johnson School",
  "$2 million Cayuga MBA Fund, LLC",
  "National Science Foundation",
  "Office of Naval Research",
  "Jayendran Rajamony",
  "MBA Class of 2002",
  "Johnson Graduate School of Management",
  "Cornell University",
  "Ithaca, NY 14853",
  "Mon 10/15/2001 9:35 AM",
  "Billy Lemmons Jr.",
  "Traci Warner",
  "Jeff D. Davis",
  "John Walt",
  "Associate / Analyst Program",
  "Recruiting",
  "Mon, 15 Oct 2001 19:14:20 -0700 (PDT)",
  "billy.lemmons@enron.com",
  "Mark Tawney",
  "mark.tawney@enron.com",
  "Vince J Kaminski",
  "traci.warner@enron.com",
  "d..davis@enron.com",
  "j.kaminski@enron.com",
  "john.walt@enron.com"
]}
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

seven_shot_ner_paragraph = """[EMAIL 1 START]
Date: Tuesday, November 20, 2001 4:02 AM
From: David Ingram
To: Paul D. Thomas
Cc: 
Bcc: 
Subject: Data Problems
Type: original

Paul,
I have been doing some analysis and have found a few problems that should be looked at.

1.  The number Mother data is pulling for Zone P is wrong.  The pointer for the data can be found on the SQL worksheet the expression is:
	  avg(decode(prc.power_reference_period_cd,'DAYAHEAD', decode(pl.location_name,'PJM',price_amt))) PJM_DA,
and	  avg(decode(prc.power_reference_period_cd,'HOURLY', decode(pl.location_name,'PJM',price_amt))) PJM_RT,

I have looked at the PJM and NY prices and am unable to figure out where the number is coming from.

2.  The other 24hr desk evidently has been told that the PJM night shift is to prep the PJM and Nepool portions of the shift notes.  That is fine with me.  I wrote a macro to pull, format and print the Nepool information.  The PJM information is not available on the website.  The East power portal has something.  I think it does some kind of Op Sum pull at some unknown interval.  The problem is the information is not accurate.  

Rob Bensen's frustration with this bad information is the main reason the other 24hr desk doesn't want any part of the reporting.

2.a All data points are different than the one hour averages calculated in edata.  This makes me doubt that opsum is the source, as edata also pulls from opsum.

2.b When all interfaces and hubs are printing the same, the prices shown differ in the same hour on the website.  I have no idea where this information is coming from but it is not right.  If the correct data can be found there is an application that pulls from the database at "M:\Electric\24hour\PJM AVE\PJMSummary.exe".  If they could fix this app I would care less about the web site.  If they do not want to fix the app I can write a macro to pull the same data from the mother data template.  I don't really care how I get the data, I just need to get yesterday's PJM for the shift note.

In other news, if you are trading some of the regular products, are you following the DA-RT physical moves?  If we do man the 24hr desk (even if Bryce is the day guy) we could cover the DA-RT physical.  Having it part of the 24hr desk would seem to make sense because the evening load and more up to date weather forecasts could be used when entering the NY side in the early morning.

I only mention this if you are finding yourself too busy trading PJM to spend the same amount of time on the analysis.  It is certainly easier to do uninterrupted analysis on the back shift.  Just a thought.

Thanks,
David
[EMAIL 1 END]

[EMAIL 2 START]
Date: Tuesday, November 20, 2001 11:55 AM
From: Paul D. Thomas
To: David Ingram
Cc: 
Bcc: 
Subject: RE: Data Problems
Type: replied to EMAIL 1

David,

Diana Allen and the IT team are currently working on resovling the bad Zone P day ahead and real time data.  Diana told me that it was pulling the PJM data.  

As far as the shift notes go:
I talked to Rob Benson about the shift notes and he said that they have improved greatly.  The PJM summary page is pretty accurate (usually w/in 50 cents of the actual number).  The link for the spreadsheet is:  http://eastpower.test.corp.enron.com/portal/summary/pjmsummary.aspx
[INFO: this email was truncated; continuation will appear in the next chunk]
"""

seven_shot_ner_output = """{"named_entities": [
  "Tuesday, November 20, 2001 4:02 AM",
  "David Ingram",
  "Paul D. Thomas",
  "Mother data",
  "Zone P",
  "SQL",
  "PJM",
  "NY",
  "Nepool",
  "East power portal",
  "Rob Bensen",
  "24hr desk",
  "edata",
  "opsum",
  "M:\\Electric\\24hour\\PJM AVE\\PJMSummary.exe",
  "yesterday",
  "DA-RT",
  "Bryce",
  "NY",
  "Tuesday, November 20, 2001 11:55 AM",
  "Diana Allen",
  "IT team",
  "Rob Benson",
  "PJM summary page",
  "50 cents",
  "http://eastpower.test.corp.enron.com/portal/summary/pjmsummary.aspx"
]}
"""

eight_shot_ner_paragraph = """[EMAIL 2 START]
Date: Tuesday, November 20, 2001 11:55 AM
From: Paul D. Thomas
To: David Ingram
Cc: 
Bcc: 
Subject: RE: Data Problems
Type: replied to EMAIL 1

[INFO: truncated due to token limit; this is a continuation from previous chunk]
… bad Zone P day ahead and real time data.  Diana told me that it was pulling the PJM data.  

As far as the shift notes go:
I talked to Rob Benson about the shift notes and he said that they have improved greatly.  The PJM summary page is pretty accurate (usually w/in 50 cents of the actual number).  The link for the spreadsheet is:  http://eastpower.test.corp.enron.com/portal/summary/pjmsummary.aspx  .. you might have been using an old version.  

I will continue to manage the Northeast physical book.  It allows me to effectively hedge my long or short position in the off peak market. 

Paul.

While writing the e-mail Diana said that she fixed the Zone P problem.
[EMAIL 2 END]

[EMAIL 3 START]
Date: Tue, 20 Nov 2001 21:47:23 -0800 (PST)
From: David Ingram (david.ingram@enron.com)
To: Paul D. Thomas (d..thomas@enron.com)
Cc: 
Bcc: 
Subject: RE: Data Problems
Type: replied to EMAIL 2

Paul, 
I don't doubt that the PJM summary has improved, as I have been pulling the data directly from edata instead of using the website.  I will begin to record the difference and will talk with the web data folks in an attempt to understand where they are pulling the data.

I have been using the updated website.

I spot checked the Zone P prices and there were few errors of little consequence.

As for the NE physical, I was doing some analysis and unless I have my directions backwards 24to6 has been a pretty solid play. On the DAP to DAW and DAP to RTW.  DA to RT has even been a pretty decent play during other hours.  From the night shift I can't tell if this is not being scheduled because you are busy managing EOL products or if there is some reason I don't have the experience to understand yet.

I know this is your book and you will want to keep the earnings.  I just noticed the opportunity appears to be there.  If you would like we can do some of the analysis and pass it on to you to place the orders.  Another idea might be for you to tell us what you want to do in NY and you can decide what to do with it on the day shift.

I do not want to step on your turf.  At the same time," the times they are a changin'"  You have done well with the books you have and as people come and go it is easy to see a scenario where you will be trading more during the day.  As you move to use the NE physical book more for hedging, as Gautam has used it.  There may be a role for the 24 hour guys to take on more of the speculative portion of the physical market. It would seem to make sense to at least start getting the other guys thinking about that portion of the market by trying any of the ideas in the previous paragraph.

It is kind of hard to talk about this over email, I would like to find a time to discuss it. 

Thanks
David
[EMAIL 3 END]
"""

eight_shot_ner_output = """{"named_entities": [
  "Tuesday, November 20, 2001 11:55 AM",
  "Paul D. Thomas",
  "David Ingram",
  "Zone P",
  "Diana",
  "PJM",
  "Rob Benson",
  "PJM summary page",
  "50 cents",
  "http://eastpower.test.corp.enron.com/portal/summary/pjmsummary.aspx",
  "Northeast physical book",
  "Tue, 20 Nov 2001 21:47:23 -0800 (PST)",
  "david.ingram@enron.com",
  "d..thomas@enron.com",
  "edata",
  "24to6",
  "DAP to DAW",
  "DAP to RTW",
  "DA to RT",
  "NY",
  "Gautam",
  "24 hour guys",
  "EOL products"
]}
"""

nine_shot_ner_paragraph = """[EMAIL 1 START]
Date: Sun, 30 Dec 2001 18:33:29 -0800 (PST)
From: unsubscribe-i@networkpromotion.com>@ENRON (unsubscribe-i@networkpromotion.com)
To: pallen@enron.com
Cc: 
Bcc: 
Subject: Too many to chose from - CD player, 2 way Radios, Pencam....
Type: original

[IMAGE]
Get your FREE* Reward NOW!
		[IMAGE]	
	PHILLIP, this is for REAL... one of America's largest Internet companies has granted you what may be an incredibly valuable reward.   There are 3 Reward Groups... you get to select 1 FREE* REWARD valued at up to $100.00, absolutely FREE.* They are as follows:   		
[IMAGE] (Choose one reward valued at up to $100.00) 	    		

		 [IMAGE] HURRY!!! These valuable Rewards can be withdrawn at anytime so make your selection now. Choose one of the three Reward groups: (1) a FREE* Hayo Portable CD Player, (2) 2 FREE* Motorola Talkabout Two-Way Radios, or (3) a FREE* Pen Cam Trio. Included with your FREE* REWARD you will be saving money on your long distance bill by signing up with Sprint 7? AnyTimeSM Online plan. This plan gives you 7? per minute state-to-state calling, with no monthly fee**. Simply remain a customer for 90 days, complete the redemption certificate you will receive by mail, and we will send you the FREE* REWARD that you have chosen above, for FREE*.         * Requires change of state-to-state long distance carrier to Sprint, remaining a customer for 90 days and completion of redemption certificate sent  by mail. ** When you select all online options such as online ordering, online bill payment, online customer service and staying a Sprint customer, you reduce your monthly reoccurring charge and save $5.95 every month. Promotion excludes current Sprint customers.
[EMAIL 1 END]
"""

nine_shot_ner_output = """{"named_entities": []}
"""

ten_shot_ner_paragraph = """[EMAIL 1 START]
Date: Tue, 9 Jan 2001 04:30:00 -0800 (PST)
From: Jaime Williams (jaime.williams@enron.com)
To: lvallest@gcc.com
Cc: John Griffith (john.griffith@enron.com)
Bcc: john.griffith@enron.com
Subject: Saludos, Feicitaciones y Follow up.
Type: original

EL FINANCIERO, Compra GCC activos de Dacotah Cement.- Grupo Cementos de 
Chihuahua (GCC) anunci? la adquisici?n de los activos de Dacotah Cement 
(estadounidese ubicada en Dakota del Sur), por 252 millones de d?lares que 
incluyen capital de trabajo. Las ventas anuales y el flujo operativo de GCC 
podr?an incrementarse respectivamente en 22 y 25% y la capacidad de 
producci?n pasar? de 2 mil 375 millones de toneladas m,tricas a 3 mil 235 
millones.

Luis, antes que nada, espero que hayas pasado una Navidad de primera con tu 
familia, y te deseo lo mejor para este a&o 2001.  Ojala y todas tus metas se 
cumplan.  Tambien queria provechar para felicitarte por lo de la dquisicion 
de Dacotah Cement...Creo que es una gran adicion a su grupo.
Por otro lado, y ahable con Cynthia Kase y ella esta trabajando en un 
apropuesta para ustedes. Me comento que te la debe de hacer llegar pronto. 
Quisiera pedirte que hicieramos un conference call cuando tuvieras tiempo, 
para clarara las dudas que teniamos respecto a los precios de referencia de 
Pemex y los cargos de transporte.  Tu dime cuando es conveniente para 
ti...SaLudos.
[EMAIL 1 END]
"""

ten_shot_ner_output = """{"named_entities": []}
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

twelve_shot_ner_paragraph = """[EMAIL 1 START]\nDate: 02/28/2000 12:01 PM\nFrom: Donna Dye\nTo: Vince J Kaminski/HOU/ECT@ECT\nCc: \nBcc: \nSubject: no job\nType: original\n\nYou have probably heard that our group is being broken up. Some people were \nput in other groups but I was not fortunate enough to be one of those \npeople.  HR will try for the month of March to find a position for me within \nEnron but that is not likely to happen.\n\nTomorrow is my last full day here - I will be in and out for the month of \nMarch.\n\nI am informing nice people that I like and you are one of those.\n[EMAIL 1 END]\n\n[EMAIL 2 START]\nDate: Mon, 28 Feb 2000 04:55:00 -0800 (PST)\nFrom: Vince J Kaminski (vince.kaminski@enron.com)\nTo: Donna Dye (donna.dye@enron.com)\nCc: \nBcc: \nSubject: Re: no job\nType: replied to EMAIL 1\n\nDonna,\n\nSorry to hear about it. I shall stop by tomorrow  to say hello.\nIt's too bad: so many good friends of mine will be leaving the comapny.\n\n\nVince\n\n\n\n\tEnron North America Corp.\n[EMAIL 2 END]"""

twelve_shot_ner_output = """
{
  "named_entities": [
    "02/28/2000 12:01 PM",
    "Donna Dye",
    "Vince J Kaminski",
    "HR",
    "March",
    "Enron",
    "Mon, 28 Feb 2000 04:55:00 -0800 (PST)",
    "vince.kaminski@enron.com",
    "donna.dye@enron.com",
    "Enron North America Corp."
  ]
}
"""

thirteen_shot_ner_paragraph = """[EMAIL 1 START]\nDate: 04/13/2001 11:55:51 AM\nFrom: \"LYNN RICHARDSON\" (LERICHRD@wapa.gov)\nTo: amy.clemons@enron.com\nCc: \nBcc: \nSubject: February Bill\nType: original\n\nHi Amy!\n\nI tried to return your call from yesterday this morning, but only got your voice mail.\n\nThe February bill for $341.90 was for two days:  February 9th and 14th.  February 9th (Tag No. 16259) was priced for 1 MW @ $207.99.  February 14th was a real-time transaction with no tag for less than a MW priced at $133.91.  I checked our records and saw no energy return for losses to WACM from Enron at any time during February.\n\nPlease call if you have further questions.\n\nLynn Richardson\nPublic Utilities Specialist\nRMR\n(970) 461-7440\n\n\n\n\n\n\n\n\n\n<Embedded Picture (Device Independent Bitmap)>\n<Embedded Picture (Device Independent Bitmap)>\n<Embedded Picture (Device Independent Bitmap)>\n[EMAIL 1 END]\n\n[EMAIL 2 START]\nDate: 04/17/2001 05:56 AM\nFrom: Amy Clemons @ ENRON\nTo: Virginia Thompson/PDX/ECT@ECT\nCc: \nBcc: \nSubject: DMS - 7550 - February Bill\nType: forwarded EMAIL 1\n\nI need to get this settled.  This is the detail Lynn sent me.  Have you or Cara spoken to her about this charge they have invoiced us for?\n\nLet me know\nThank you\nAmy\n[EMAIL 2 END]\n\n[EMAIL 3 START]\nDate: 04/30/2001 05:53 PM\nFrom: Virginia Thompson\nTo: Cara Semperger/PDX/ECT@ECT, Bill Williams III/PDX/ECT@ECT\nCc: \nBcc: \nSubject: DMS - 7550 - February Bill\nType: forwarded EMAIL 2\n\nDear Cara and Bill,\n\nDo you recognize these charges as valid  (Cara for 2-9 and Bill for 2-14)?  \n\nVirginia\n[EMAIL 3 END]\n\n[EMAIL 4 START]\nDate: Tuesday, May 01, 2001 6:42 AM\nFrom: Cara Semperger\nTo: Virginia Thompson\nCc: Stacy Runswick, Holden Salisbury, Susie Wilson\nBcc: \nSubject: Re: DMS - 7550 - February Bill\nType: replied to EMAIL 3\n\nI believe the preschedule loss charge is valid for 2/9/01, as I see no loss schedule represented on the scheduling sheet.\n\nc\n[EMAIL 4 END]\n\n[EMAIL 5 START]\nDate: Tue, 1 May 2001 16:00:00 -0700 (PDT)\nFrom: Virginia Thompson (virginia.thompson@enron.com)\nTo: Cara Semperger (cara.semperger@enron.com)\nCc: \nBcc: \nSubject: RE: DMS - 7550 - February Bill\nType: replied to EMAIL 4\n\nThanks, Cara.  One more question....Does this go on NW or SW's books?\n\nVA\n[EMAIL 5 END]"""
thirteen_shot_ner_output = """
{
  "named_entities": [
    "Lynn Richardson",
    "LERICHRD@wapa.gov",
    "04/13/2001 11:55:51 AM",
    "amy.clemons@enron.com",
    "February",
    "$341.90",
    "February 9th",
    "February 14th",
    "Tag No. 16259",
    "1 MW @ $207.99",
    " $133.91",
    "WACM",
    "Enron",
    "Public Utilities Specialist",
    "RMR",
    "(970) 461-7440",
    "04/17/2001 05:56 AM",
    "Amy Clemons",
    "Virginia Thompson",
    "DMS - 7550 - February",
    "Cara Semperger",
    "04/30/2001 05:53 PM",
    "Virginia Thompson",
    "Bill Williams III",
    "Tuesday, May 01, 2001 6:42 AM",
    "Stacy Runswick",
    "Holden Salisbury",
    "Susie Wilson",
    "2/9/01",
    "Tue, 1 May 2001 16:00:00 -0700 (PDT)",
    "virginia.thompson@enron.com",
    "cara.semperger@enron.com",
    "NW",
    "SW"
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



"""prompt_template = [
    {"role": "system", "content": ner_system},
    {"role": "user", "content": one_shot_ner_paragraph},
    {"role": "assistant", "content": one_shot_ner_output},
    {"role": "user", "content": two_shot_ner_paragraph},
    {"role": "assistant", "content": two_shot_ner_output},
    {"role": "user", "content": three_shot_ner_paragraph},
    {"role": "assistant", "content": three_shot_ner_output},
    {"role": "user", "content": four_shot_ner_paragraph},
    {"role": "assistant", "content": four_shot_ner_output},
    {"role": "user", "content": five_shot_ner_paragraph},
    {"role": "assistant", "content": five_shot_ner_output},
    {"role": "user", "content": six_shot_ner_paragraph},
    {"role": "assistant", "content": six_shot_ner_output},
    {"role": "user", "content": seven_shot_ner_paragraph},
    {"role": "assistant", "content": seven_shot_ner_output},
    {"role": "user", "content": eight_shot_ner_paragraph},
    {"role": "assistant", "content": eight_shot_ner_output},
    {"role": "user", "content": nine_shot_ner_paragraph},
    {"role": "assistant", "content": nine_shot_ner_output},
    {"role": "user", "content": ten_shot_ner_paragraph},
    {"role": "assistant", "content": ten_shot_ner_output},
    {"role": "user", "content": "${passage}"}
]"""


"""
prompt_template = [
    {"role": "system", "content": ner_system},
    {"role": "user", "content": one_shot_ner_paragraph},
    {"role": "assistant", "content": one_shot_ner_output},
    {"role": "user", "content": two_shot_ner_paragraph},
    {"role": "assistant", "content": two_shot_ner_output},
    {"role": "user", "content": three_shot_ner_paragraph},
    {"role": "assistant", "content": three_shot_ner_output},
    {"role": "user", "content": four_shot_ner_paragraph},
    {"role": "assistant", "content": four_shot_ner_output},
    {"role": "user", "content": five_shot_ner_paragraph},
    {"role": "assistant", "content": five_shot_ner_output},
    {"role": "user", "content": six_shot_ner_paragraph},
    {"role": "assistant", "content": six_shot_ner_output},
    {"role": "user", "content": seven_shot_ner_paragraph},
    {"role": "assistant", "content": seven_shot_ner_output},
    {"role": "user", "content": eight_shot_ner_paragraph},
    {"role": "assistant", "content": eight_shot_ner_output},
    {"role": "user", "content": nine_shot_ner_paragraph},
    {"role": "assistant", "content": nine_shot_ner_output},
    {"role": "user", "content": ten_shot_ner_paragraph},
    {"role": "assistant", "content": ten_shot_ner_output},
    {"role": "user", "content": "Email:\n${passage}"}
]
"""