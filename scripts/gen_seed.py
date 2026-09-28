"""Generate a fully fictional SPARKS_DATA object for the Sparks dashboard.

Nothing here is derived from a real person. Every name, company, quote and number is invented.
Run:  python3 gen_seed.py > dashboard-data.demo.json
"""
import json, random, math, sys, datetime as dt
from urllib.parse import quote

R = random.Random(20260925)
THROUGH = dt.date(2026, 9, 25)
OWNER, FIRST, CO = "Alex Morgan", "Alex", "Harbourline Coffee"

def iso(d): return d.isoformat()
def ago(days): return THROUGH - dt.timedelta(days=days)
def slug(n): return n.lower().replace(" ", "-").replace("'", "")
def gm(n): return "https://mail.google.com/mail/u/0/#search/" + quote('"%s"' % n)
def li(n): return "https://www.linkedin.com/search/results/all/?keywords=" + quote(n)

CLUSTERS = ["Team & Company", "Capital", "Founders & CEOs", "Customers & Market",
            "Frontier", "Mentors & Rooms", "Government & Media", "Life", "Wider network"]

# ---- the named cast: (name, org/context, cluster, shell, size, months_since, meetings, label)
CAST = [
 ("Priya Raman","COO, Harbourline Coffee","Team & Company",1,5,0,640,"always"),
 ("Tomasz Wierzbicki","Head of Roasting, Harbourline Coffee","Team & Company",1,5,0,580,"always"),
 ("Hannah Okafor","Head of Wholesale, Harbourline Coffee","Team & Company",1,4,0,310,"always"),
 ("Luca Bernardi","Finance Director, Harbourline Coffee","Team & Company",1,4,0,260,"hover"),
 ("Grace Adeyemi","Head of People, Harbourline Coffee","Team & Company",2,3,1,120,"hover"),
 ("Marcus Lindqvist","Partner, Ashgrove Capital","Capital",1,5,0,90,"always"),
 ("Sofia Marchetti","Principal, Kestrel Ventures","Capital",2,4,1,34,"always"),
 ("Daniel Osei","Angel investor","Capital",2,3,2,18,"hover"),
 ("Ruth Calloway","Partner, Meridian Growth","Capital",3,3,5,11,"hover"),
 ("Kenji Watanabe","GP, Northlight Fund","Capital",4,2,14,6,"none"),
 ("Isabel Fonseca","Founder, Tidewater Robotics","Founders & CEOs",1,4,0,42,"always"),
 ("Oliver Hartley","CEO, Kilnworks","Founders & CEOs",2,4,1,27,"always"),
 ("Amara Nwosu","Founder, Quillfield","Founders & CEOs",2,3,2,15,"always"),
 ("Felix Brandt","Founder, Loopcart","Founders & CEOs",2,3,1,12,"hover"),
 ("Nadia Haddad","CEO, Brightwell Health","Founders & CEOs",3,3,6,9,"hover"),
 ("Jonah Pierce","Founder, Stackyard","Founders & CEOs",3,2,7,5,"hover"),
 ("Chloe Dubois","Founder, Verdant Grid","Founders & CEOs",4,3,16,8,"hover"),
 ("Samir Khoury","Co-founder, Cupwise","Founders & CEOs",2,3,1,14,"hover"),
 ("Elena Popescu","Founder, Northwind Analytics","Founders & CEOs",3,2,4,4,"none"),
 ("Ben Achterberg","Head of Buying, Fernway Hotels","Customers & Market",1,4,0,56,"always"),
 ("Rachel Kim","Head of Food & Drink, Larkspur Grocers","Customers & Market",2,4,1,33,"always"),
 ("Declan Murphy","Owner, Murphy's Delis","Customers & Market",2,3,2,21,"hover"),
 ("Yusuf Demir","Procurement, Albion Retail","Customers & Market",3,3,5,10,"hover"),
 ("Lena Hoffmann","VP Partnerships, Kaffewerk","Customers & Market",3,2,8,6,"hover"),
 ("Ade Balogun","Green-coffee importer, Lanyard Trading","Customers & Market",4,2,13,7,"none"),
 ("Mira Castellano","Research lead, Halden AI Lab","Frontier",2,4,1,19,"always"),
 ("Theo Grant","Founder, Orbitale Space","Frontier",3,3,5,8,"hover"),
 ("Sunita Rao","Robotics researcher, Cambridge","Frontier",3,2,6,4,"hover"),
 ("Peter Vance","Chairman, Coldharbour plc","Mentors & Rooms",1,5,0,28,"always"),
 ("Margot Ellison","Exited founder, now coach","Mentors & Rooms",2,4,2,16,"always"),
 ("Hugo Sandberg","Host, The Tuesday Table dinners","Mentors & Rooms",3,3,4,7,"hover"),
 ("Julia Brennan","Non-exec, three boards","Mentors & Rooms",4,3,15,9,"hover"),
 ("Arjun Mehta","Policy adviser, Dept for Business and Trade","Government & Media",2,3,2,9,"always"),
 ("Kate Sullivan","Editor, Roast Weekly","Government & Media",3,3,5,6,"hover"),
 ("Omar Farouk","Podcast host, Build Notes","Government & Media",4,2,11,3,"none"),
 ("Sam Whitaker","School friend","Life",1,4,0,40,"hover"),
 ("Bea Lindgren","Padel partner","Life",2,3,1,22,"hover"),
 ("Nick Oduya","Cycling club","Life",3,2,4,8,"none"),
]
PEOPLE = {c[0]: dict(zip(["name","ctx","cluster","shell","size","ms","mt","label"], c)) for c in CAST}

FIRSTS = "Aaron Abby Adil Aisha Alan Alice Amir Ana Andre Anika Anton Asha Ava Barney Bella Bilal Bruno Carla Caleb Cara Cyrus Dara Dev Diana Dominic Edith Emil Esme Ezra Faye Finn Flora Gabe Gita Greta Harriet Hari Ines Ivo Jade Jai Joel Kai Kara Kofi Lara Leo Lily Mae Mani Mateo Maya Mina Nico Nora Olu Omid Paloma Pia Quinn Rafe Rhea Rosa Rui Sana Seb Shay Tara Tess Uma Vik Wren Xan Yara Zac Zoe".split()
LASTS = "Abbott Achebe Aldred Amani Arkwright Baird Banerjee Barlow Beaumont Bello Brook Cahill Carvalho Chen Clarke Cole Dalby Das Devereux Dunmore Eke Elms Farrant Fenwick Gallo Garside Goh Hale Hargreaves Holm Ibarra Iqbal Jansen Joshi Kaur Keane Kovac Lamb Larsen Leigh Lowe Maddox Malik Marsh Moreau Nakamura Nair Nolan Oakes Ortega Palmer Park Quarry Quint Reyes Rhodes Sato Sayer Shah Sole Strand Thorne Tiwari Underhill Varga Voss Wade Walsh Yeo Young Zeller".split()

real_guard = set()
try:
    real_guard = set(json.load(open(sys.argv[1]))) if len(sys.argv) > 1 else set()
except Exception:
    pass

used = set(PEOPLE)
def fake_name():
    while True:
        n = R.choice(FIRSTS) + " " + R.choice(LASTS)
        if n not in used and n not in real_guard:
            used.add(n); return n

# ---- wants (preferences)
WANTS = [
 ("Rooms above your level","stated","Rooms where you are the student: operators two stages ahead of you.",
  "I keep ending up as the one teaching. I want to be in rooms where I'm learning.","Granola, 'Board prep', 14 Jul 2026"),
 ("Small rooms of equals","stated","Six-person dinners of founders at the same stage, no agenda.",
  "The best hour of my month was that dinner with five people who get it.","WhatsApp to Margot Ellison, 2 Aug 2026"),
 ("The next company","stated","A clear view of what you build after this one, formed early.",
  "I want to know what the next thing is before I need to.","Granola, 'Coaching session', 19 Jun 2026"),
 ("Frontier tech, up close","stated","Time with people building robotics, space and AI systems.",
  "I'd give up a board meeting for an afternoon in a robotics lab.","Gmail to Mira Castellano, 3 Sep 2026"),
 ("A real pause","stated","A deliberate break of at least three weeks, planned not stolen.",
  "I haven't had three weeks off since we started.","Granola, 'Coaching session', 19 Jun 2026"),
 ("Superconnecting","stated","Being the person who makes the introduction that matters.",
  "The intros I've made are the thing I'm proudest of outside the company.","Notion, 'Personal goals 2026'"),
 ("Winning the big accounts","stated","Landing the three largest wholesale accounts in the pipeline.",
  "If we get Fernway and Larkspur, the year is made.","Slack #leadership, 8 Sep 2026"),
 ("Builder peers","stated","Other CEOs who ship product themselves, to swap notes with.",
  "I want more people I can talk shop with who still write code.","LinkedIn message to Felix Brandt, 21 Aug 2026"),
 ("Assembling the room","revealed","You host more than you attend: eleven dinners convened this year, two attended.",
  None,"MEASURED across the calendar, Jan to Sep 2026"),
 ("A filter on the inbound","revealed","You answer inbound from strangers within a day, and it crowds out warm follow-ups.",
  None,"MEASURED across Gmail and LinkedIn, 2026"),
 ("The mentor bench","revealed","You consult the same four people before every big decision.",
  None,"MEASURED across Granola and WhatsApp, 2025 to 2026"),
]
TB_NAMES = {"rooms_above":"Rooms above your level","small_rooms":"Small rooms of equals","next_company":"The next company",
            "frontier":"Frontier tech, up close","pause":"A real pause","superconnecting":"Superconnecting",
            "big_accounts":"Winning the big accounts","builder_peers":"Builder peers"}
TB_OTHER = {"dayjob":"Running "+CO,"admin":"Travel, lunch & holds","personal":"Personal"}

wants = []
for name, kind, one, q, src in WANTS:
    w = {"name":name,"kind":kind,"one_liner":one,"quote":q,"source":src}
    if kind == "revealed":
        w["confidence"] = "High on the pattern, which is measured. What to do about it is judgement."
        w["depth"] = 1
        w["evidence"] = [[one, src]]
    wants.append(w)

# ---- suggested actions (moves)
def P(n): p = PEOPLE[n]; return {"name":n,"context":p["ctx"],"gmail":gm(n),"linkedin":li(n)}
def ev(what, source, days, where, quote_=None):
    return {"what":what,"source":source,"date":iso(ago(days)),"quote":quote_,"where":where,"link":None}
def sc(f,d,t,fe): return {"fit":f,"distance":d,"timing":t,"feasibility":fe,"total":round(f*d*t*fe,1)}

MOVES = [
 dict(id="introduce-isabel-mira",title="Introduce Isabel Fonseca (Tidewater Robotics) to Mira Castellano (Halden AI Lab)",category="Introduce",
  people=[P("Isabel Fonseca"),P("Mira Castellano")],serves=["Superconnecting","Frontier tech, up close"],
  why="Isabel is hiring her first perception researcher and Mira runs the lab that trains them. They share no room except you.",
  evidence=[ev("Isabel asked for help finding a perception lead","whatsapp",9,"Isabel Fonseca, WhatsApp","anyone you know who's done perception at scale?"),
            ev("Mira said two of her postdocs want to go industrial","granola",21,"Granola, 'Halden lab visit'")],
  action="Email Mira first to check she is happy to be introduced, then send the double opt-in.",
  draft="[email to Mira Castellano]\nMira, quick one. Isabel Fonseca runs Tidewater Robotics and is hiring her first perception lead. You mentioned two of your postdocs want to go industrial. Worth an intro?",
  hold_note=None,score=sc(5,5,0.9,0.9),headline="for-someone-else",chart=("hiring perception lead","trains exactly that")),
 dict(id="introduce-oliver-ben",title="Introduce Oliver Hartley (Kilnworks) to Ben Achterberg (Fernway Hotels)",category="Introduce",
  people=[P("Oliver Hartley"),P("Ben Achterberg")],serves=["Superconnecting","Winning the big accounts"],
  why="Oliver wants a first hotel-group customer for his espresso machines; Ben is consolidating café-equipment suppliers this quarter.",
  evidence=[ev("Oliver asked for a hotel buyer intro","gmail",14,"Gmail, 'Kilnworks next steps'"),
            ev("Ben is reviewing café-equipment suppliers before Q4","granola",10,"Granola, 'Fernway QBR'")],
  action="Check with Ben before introducing: he is a live customer, so the intro must help him first.",
  draft="[email to Ben Achterberg]\nBen, you mentioned the supplier review. Oliver Hartley's team at Kilnworks does exactly the machine audit you described. Happy to connect you if useful, no pressure either way.",
  hold_note="Ben is a live customer. Ask first.",score=sc(4,4,1.0,0.8),headline=None,chart=("first enterprise buyer","consolidating suppliers")),
 dict(id="repair-kenji",title="Reply to Kenji Watanabe (Northlight Fund), whose note has sat for five months",category="Repair",
  people=[P("Kenji Watanabe")],serves=["Rooms above your level"],
  why="Kenji asked for your view on a coffee-subscription deal in April and heard nothing. He sits on two boards you admire.",
  evidence=[ev("Kenji asked for a view on a deal","gmail",160,"Gmail, 'Quick view?'","would value 20 mins of your take")],
  action="Short, honest reply: apologise for the silence, offer a call this month.",
  draft="[email to Kenji Watanabe]\nKenji, I owe you a reply from April and I'm sorry it took this long. If the question is still live I'd be glad to give you 20 minutes this month.",
  hold_note=None,score=sc(4,3,0.8,0.9),headline="repair"),
 dict(id="decide-pause",title="Put three weeks off in the diary before Q1 planning",category="Decide",
  people=[P("Priya Raman")],serves=["A real pause"],
  why="You have said it twice this year and the diary shows no block longer than four days since 2024.",
  evidence=[ev("Stated want for a proper break","granola",98,"Granola, 'Coaching session'")],
  action="Agree cover with Priya and block the dates.",draft=None,hold_note=None,score=sc(5,1,0.9,0.7),headline="for-owner"),
 dict(id="reactivate-julia",title="Reconnect with Julia Brennan before her board seats turn over",category="Reactivate",
  people=[P("Julia Brennan")],serves=["Rooms above your level","The next company"],
  why="Fifteen months quiet. She chairs two boards in your sector and offered to mentor you in 2025.",
  evidence=[ev("Julia offered to mentor","gmail",450,"Gmail, 'Great to meet'","any time you want a sounding board")],
  action="Suggest breakfast; bring one specific question.",
  draft="[whatsapp to Julia Brennan]\nJulia, it's been too long. Would you have time for breakfast in October? I have one board question I'd really value your view on.",
  hold_note=None,score=sc(4,2,0.7,0.8),headline=None),
 dict(id="introduce-amara-sofia",title="Introduce Amara Nwosu (Quillfield) to Sofia Marchetti (Kestrel Ventures)",category="Introduce",
  people=[P("Amara Nwosu"),P("Sofia Marchetti")],serves=["Superconnecting"],
  why="Amara opens her seed round next month; Sofia told you she is looking for exactly this kind of workflow tool.",
  evidence=[ev("Amara is raising in October","whatsapp",6,"Amara Nwosu, WhatsApp"),ev("Sofia's thesis on workflow tools","gmail",30,"Gmail, 'Kestrel thesis'")],
  action="Ask Amara for a one-paragraph blurb, then introduce.",draft="[email to Amara Nwosu]\nAmara, Sofia Marchetti at Kestrel is looking for exactly what you're building. Send me a paragraph and I'll introduce you this week.",
  hold_note=None,score=sc(5,4,0.9,0.9),headline=None,chart=("seed round opens","workflow thesis")),
 dict(id="rooms-tuesday-table",title="Host a Tuesday Table dinner for six builder CEOs",category="Rooms",
  people=[P("Hugo Sandberg"),P("Felix Brandt")],serves=["Small rooms of equals","Builder peers"],
  why="You host far more than you attend, and the builder-peer want has had no diary time this quarter.",
  evidence=[ev("Hugo offered his dining room for a founder dinner","gmail",40,"Gmail, 'Tuesday Table'")],
  action="Pick a date with Hugo and invite five names.",draft=None,hold_note=None,score=sc(4,3,0.8,0.9),headline=None),
 dict(id="commercial-rachel-pilot",title="Offer Rachel Kim (Larkspur Grocers) the own-label coffee pilot she asked about",category="Commercial",
  people=[P("Rachel Kim"),P("Hannah Okafor")],serves=["Winning the big accounts"],
  why="Rachel asked about a pilot in August; the follow-up stalled when Hannah was away.",
  evidence=[ev("Rachel asked about a pilot","granola",33,"Granola, 'Larkspur intro call'")],
  action="Hannah to send the pilot outline; you send a short note to Rachel.",draft=None,hold_note=None,score=sc(5,2,1.0,0.9),headline=None),
 dict(id="introduce-theo-arjun",title="Introduce Theo Grant (Orbitale Space) to Arjun Mehta (Dept for Business and Trade)",category="Introduce",
  people=[P("Theo Grant"),P("Arjun Mehta")],serves=["Superconnecting","Frontier tech, up close"],
  why="Theo needs a government contact on satellite crop monitoring for import traceability; Arjun is writing exactly that consultation.",
  evidence=[ev("Theo asked who in government owns import traceability","linkedin",25,"LinkedIn message"),ev("Arjun drafting the traceability consultation","gmail",18,"Gmail, 'Consultation'")],
  action="Check the consultation is public before introducing.",draft=None,hold_note="Only use public facts about the consultation.",score=sc(4,5,0.8,0.8),headline=None,chart=("needs a policy route","writing the consultation")),
 dict(id="ritual-margot-monthly",title="Restart the monthly walk with Margot Ellison",category="Ritual",
  people=[P("Margot Ellison")],serves=["The mentor bench","The next company"],
  why="The walks stopped in June. She is one of the four people you consult before every big call.",
  evidence=[ev("Last walk logged","calendar",100,"Calendar, 'Walk with Margot'")],
  action="Propose the first Saturday of each month.",draft=None,hold_note=None,score=sc(4,1,0.8,0.9),headline=None),
 dict(id="angel-chloe",title="Answer Chloe Dubois on her pre-seed round",category="Angel",
  people=[P("Chloe Dubois")],serves=["Builder peers"],
  why="Chloe sent the deck in May. A clear yes or no is kinder than silence.",
  evidence=[ev("Deck sent","gmail",130,"Gmail, 'Verdant Grid pre-seed'")],
  action="Decide this week and reply either way.",draft=None,hold_note=None,score=sc(3,2,0.6,0.9),headline=None),
 dict(id="platform-roast-weekly",title="Write the guest column Kate Sullivan offered in Roast Weekly",category="Platform",
  people=[P("Kate Sullivan")],serves=["Winning the big accounts"],
  why="Kate offered a column slot in July. Buyers at two target accounts read it.",
  evidence=[ev("Kate offered a guest column","gmail",70,"Gmail, 'Column?'")],
  action="Send Kate three possible angles.",draft=None,hold_note=None,score=sc(3,3,0.7,0.8),headline=None),
]
# pad with lighter reconnect moves so lists and filters have depth
for n in ["Nadia Haddad","Jonah Pierce","Elena Popescu","Yusuf Demir","Lena Hoffmann","Ade Balogun","Omar Farouk","Ruth Calloway","Sunita Rao","Declan Murphy","Samir Khoury","Daniel Osei"]:
    p = PEOPLE[n]
    MOVES.append(dict(id="reactivate-"+slug(n),title="Reconnect with %s (%s)" % (n, p["ctx"].split(", ")[-1]),category="Reactivate",
      people=[P(n)],serves=[R.choice(["Superconnecting","Builder peers","Winning the big accounts","Rooms above your level"])],
      why="%d months since you last spoke, and the relationship ran across more than one channel." % max(p["ms"],3),
      evidence=[ev("Last two-way exchange","gmail",30*max(p["ms"],3),"Gmail thread")],
      action="Send a short, specific note. No ask.",draft=None,hold_note=None,
      score=sc(R.choice([2,3,4]),R.choice([1,2,3]),round(R.uniform(0.5,0.9),1),round(R.uniform(0.6,1.0),1)),headline=None))

chart = {}
for m in MOVES:
    c = m.pop("chart", None)
    if c: chart[m["id"]] = {"l":0,"r":1,"ls":c[0],"rs":c[1]}

chips = [
 {"id":"rooms-tuesday-table","species":"convening","a":FIRST,"b":"six builder CEOs"},
 {"id":"introduce-isabel-mira","species":"passion","a":"Isabel Fonseca","b":"Mira Castellano"},
 {"id":"introduce-amara-sofia","species":"timing","a":"Amara Nwosu","b":"Sofia Marchetti"},
]

# ---- orrery bodies + chords
bodies = []
for n, p in PEOPLE.items():
    mv = [m["id"] for m in MOVES if any(pp["name"] == n for pp in m["people"])]
    bodies.append({"id":slug(n),"name":n,"cluster":p["cluster"],"shell":p["shell"],"size":p["size"],
                   "months_since":p["ms"],"dormant":p["ms"]>=12,"active_move":bool(mv),"moves":mv,
                   "meetings":p["mt"],"label":p["label"]})
chords = []
for m in MOVES:
    if m["category"] == "Introduce" and len(m["people"]) == 2:
        chords.append({"a":slug(m["people"][0]["name"]),"b":slug(m["people"][1]["name"]),"score":m["score"]["total"],
                       "fit":m["score"]["fit"],"timing":m["score"]["timing"],"title":m["title"],"move_id":m["id"]})

# near dust (hoverable) and far dust (points)
N_DN, N_DF = 620, 1900
dn = {k: [] for k in ["id","name","shell","size","ms","mt"]}
for i in range(N_DN):
    n = fake_name(); sh = R.choices([1,2,3,4],[8,30,12,50])[0]
    dn["id"].append(slug(n)); dn["name"].append(n); dn["shell"].append(sh)
    dn["size"].append(R.choices([1,2,3,4],[10,45,35,10])[0])
    dn["ms"].append({1:0,2:R.randint(0,2),3:R.randint(3,11),4:R.randint(12,40)}[sh])
    dn["mt"].append(max(0,int(R.expovariate(1/20))))
dn["always"] = [0,1,2]
dn["mv"] = {}
df = {"n3":110,"x":[],"y":[],"r":[],"id":[],"name":[]}
for i in range(N_DF):
    n = fake_name(); a = R.uniform(0, 2*math.pi)
    rad = R.uniform(380, 440) if i < 110 else R.uniform(555, 592)
    df["x"].append(round(620 + rad*math.cos(a), 1)); df["y"].append(round(620 + rad*math.sin(a), 1))
    df["r"].append(R.choice([1.4,1.25,0.8])); df["id"].append(slug(n)); df["name"].append(n)

ORR = {"generated":iso(THROUGH),"clusters":CLUSTERS,"shell_names":["Inner circle","Working orbit","Outer orbit","Deep field"],
       "shell_gloss":["in touch weekly","active this quarter","quiet 3-12 months","over a year of silence"],
       "indexed_total":0,"bodies":bodies,"chords":chords,"dn":dn,"df":df}

# ---- relationship ledger
cols = ["name","cluster","phone_known","meetings","ev_gmail","ev_granola","ev_slack","ev_whatsapp","ev_imessage","ev_linkedin","ev_other",
        "weighted_mass","log_mass","multiplexity","reciprocity","vouched","owner_initiated","dormant","last_signal","months_since","tau","heat","bond","size","shell"]
def ledger_row(name, cluster, shell, size, ms, mt):
    g, gr, sl, wa, im, lk, ot = [max(0,int(R.expovariate(1/x))) for x in (12,4,6,5,0.5,2,1)]
    mass = mt*2 + g + gr*3 + sl + wa*3 + lk + ot
    chans = sum(1 for v in (g,gr,sl,wa,im,lk,ot) if v)
    tau = 12 if chans > 1 else 3
    heat = round(math.exp(-ms/tau), 2)
    last = (THROUGH - dt.timedelta(days=30*ms)).strftime("%Y-%m")
    bond = min(100, int(10*math.log1p(mass)*(1+0.1*chans)))
    return [name, cluster, int(R.random()<0.4), mt, g, gr, sl, wa, im, lk, ot, mass, round(math.log1p(mass),2),
            round(1+0.15*chans,2), round(R.uniform(0,0.6),2), int(R.random()<0.05), int(R.random()<0.5),
            int(ms>=12), last, ms, tau, heat, bond, size, shell]
rows = [ledger_row(p["name"],p["cluster"],p["shell"],p["size"],p["ms"],p["mt"]) for p in PEOPLE.values()]
for i in range(N_DN):
    rows.append(ledger_row(dn["name"][i],"Wider network",dn["shell"][i],dn["size"][i],dn["ms"][i],dn["mt"][i]))
LDG = {"cols":cols,"rows":rows}
ORR["indexed_total"] = len(rows)

# ---- promises
PROM = []
promises = [
 ("owner_owes",5,"Isabel Fonseca","You said you would find Isabel a perception lead.","WhatsApp",9),
 ("owner_owes",4,"Kenji Watanabe","You owe Kenji a view on the coffee-subscription deal.","Email",160),
 ("owner_owes",3,"Chloe Dubois","You said you would come back on the Verdant Grid round.","Email",130),
 ("owner_owes",3,"Kate Sullivan","You agreed to send column angles.","Email",70),
 ("owed_to_owner",4,"Peter Vance","Peter promised an intro to the Coldharbour procurement lead.","Meeting",45),
 ("owed_to_owner",2,"Daniel Osei","Daniel said he would share his board-pack template.","WhatsApp",20),
 ("mutual",3,"Hugo Sandberg","You and Hugo agreed to set a date for the next dinner.","Email",40),
 ("owner_owes",2,"Felix Brandt","You offered Felix a look at your hiring scorecard.","LinkedIn",21),
 ("owner_owes",5,"Rachel Kim","You promised Rachel a pilot outline by end of August.","Meeting",33),
 ("owed_to_owner",3,"Arjun Mehta","Arjun offered to share the consultation timetable.","Email",18),
]
for i,(d,w,who,what,src,days) in enumerate(promises):
    PROM.append({"id":"p%04d"%i,"d":iso(ago(days)),"dir":d,"w":w,"who":who,"what":what,
                 "src":src,"link":gm(who),"raw":what})
PROM.append({"id":"p9001","d":iso(ago(200)),"dir":"owner_owes","w":2,"who":"Sam Whitaker","what":"You said you would send Sam the photos.",
             "src":"WhatsApp","link":None,"raw":"photos","closed":iso(ago(150))})

# ---- newswire
NEWS = {"generated":iso(THROUGH),"items":[
 {"who":"Isabel Fonseca","org":"Tidewater Robotics","kind":"funding","headline":"Tidewater Robotics closed a seed round led by a Nordic deep-tech fund.","date":iso(ago(12)),"url":"https://example.com/news/tidewater-seed","source":"Example Tech News","confidence":"high","why_it_matters":"She will be hiring fast, which is when intros count most."},
 {"who":"Lena Hoffmann","org":"Kaffewerk","kind":"job_move","headline":"Lena Hoffmann joined Kaffewerk as VP Partnerships.","date":iso(ago(20)),"url":"https://example.com/news/lena-kaffewerk","source":"Example Trade Press","confidence":"high","why_it_matters":"A quiet contact now owns partnerships at a target account."},
 {"who":"Coffee sector","org":"Coffee sector","kind":"sector","area":"coffee","headline":"Large grocers and hotel groups are consolidating coffee suppliers ahead of 2027 contracts.","date":iso(ago(5)),"url":"https://example.com/news/consolidation","source":"Roast Weekly (fictional)","confidence":"moderate","why_it_matters":"Buying windows at Fernway and Larkspur may close sooner than planned."},
 {"who":"Theo Grant","org":"Orbitale Space","kind":"launch","headline":"Orbitale Space launched its first crop-monitoring satellite.","date":iso(ago(30)),"url":"https://example.com/news/orbitale","source":"Example Space Wire","confidence":"high","why_it_matters":"Makes the Arjun introduction timelier."},
],"areas":{"coffee":"Coffee trade"},"crm":[],"coverage":{"people_scanned":38,"people_total":38,"not_searched":[],"note":"Demo data. Every item is fictional."}}

# ---- calendar feed
def ev_at(days_ahead, h, m, dur):
    s = dt.datetime.combine(THROUGH + dt.timedelta(days=days_ahead), dt.time(h, m))
    return s.isoformat()+"+01:00", (s+dt.timedelta(minutes=dur)).isoformat()+"+01:00"
FEED = []
for t,d,h,mi,dur,k,att,who,help_ in [
 ("Weekly leadership",0,9,0,60,"int",["Priya Raman","Tomasz Wierzbicki","Hannah Okafor"],"Your standing leadership meeting.","Raise the Larkspur pilot: it has stalled for three weeks."),
 ("Coffee with Isabel Fonseca",1,8,30,45,"ext",["Isabel Fonseca"],"Founder, Tidewater Robotics. Closed a seed round this month.","You owe her a perception-lead intro. Bring Mira's name."),
 ("Fernway QBR",2,14,0,60,"ext",["Ben Achterberg","Hannah Okafor"],"Quarterly review with your largest prospect.","Ask about the supplier review before mentioning Kilnworks."),
 ("Walk with Margot",4,10,0,60,"ritual",["Margot Ellison"],"Your mentor walk, restarted.","Bring the next-company question."),
 ("Padel",5,18,30,90,"personal",["Bea Lindgren"],"",""),
 ("Investor update call",7,16,0,30,"ext",["Marcus Lindqvist"],"Lead investor.","He will ask about the two big wholesale accounts."),
]:
    s,e = ev_at(d,h,mi,dur)
    FEED.append({"t":t,"s":s,"e":e,"k":k,"att":att,"who":who,"help":help_})

# ---- time budget
TIME = {"window":"Q3 to date","src":"Calendar, all accepted meetings, Jul to Sep",
        "agg":{"dayjob":{"mins":14400,"n":310},"admin":{"mins":6000,"n":120},"personal":{"mins":600,"n":8},
               "big_accounts":{"mins":1500,"n":22},"superconnecting":{"mins":420,"n":9},"small_rooms":{"mins":360,"n":4},
               "builder_peers":{"mins":0,"n":0},"rooms_above":{"mins":180,"n":3},"frontier":{"mins":240,"n":3},
               "pause":{"mins":0,"n":0},"next_company":{"mins":120,"n":2}},
        "ex":{}}

# ---- searchable corpus
KINDS = ["want","have","promise","passion","fact","ask","intro","thanks","decision","life"]
SRCS = ["gmail","granola","slack","whatsapp","linkedin","notion","calendar"]
TPL = {
 "want":"{n} wants an introduction to someone in {topic}.","have":"{n} can open doors in {topic}.",
 "promise":"{n} promised to send notes on {topic}.","passion":"{n} is passionate about {topic}.",
 "fact":"{n} moved roles and now leads {topic}.","ask":"{n} asked for advice on {topic}.",
 "intro":"{n} introduced a contact working on {topic}.","thanks":"{n} thanked you for help with {topic}.",
 "decision":"{n} decided to prioritise {topic} next quarter.","life":"{n} is training for a marathon and mentioned {topic}.",
}
TOPICS = ["espresso extraction","roastery automation","seed fundraising","board governance","green-coffee sourcing","hiring roasters",
          "import traceability","AI evaluation","padel","customer pilots","pricing","crop monitoring"]
CORPUS = []
for n in list(PEOPLE) + dn["name"][:120]:
    for _ in range(R.randint(1,4)):
        k = R.choice(KINDS)
        CORPUS.append([n, iso(ago(R.randint(1,700))), k, R.choice(SRCS), TPL[k].format(n=n.split()[0], topic=R.choice(TOPICS))])
for w in wants:
    CORPUS.append([OWNER, iso(ago(R.randint(5,200))), "want", "granola", w["one_liner"]])

D = {"wants":wants,"moves":MOVES,"chart":chart,"chips":chips,
     "hunches":[["Weekend founders","Thin so far: three people mentioned building on weekends. Worth a small dinner."],
                ["A second city","Two mentions of spending time in Lisbon. Too little to act on."]],
     "names":sorted(list(PEOPLE) + [OWNER, FIRST]),
     "quotes":["anyone you know who's done perception at scale?","would value 20 mins of your take","any time you want a sounding board"],
     "stats":[["People indexed",f"{len(rows):,}"],["Person files","38"],["Preferences tracked","112"],["Haves","74"],["Passions","19"],
              ["Unanswered asks","9"],["Promises extracted","41"],["Calendar events kept","1,860"]],
     "gaps":["Demo data. Every person, company and quote on this page is fictional.",
             "WhatsApp only covers what the phone has synced; voice notes are not read.",
             "LinkedIn is read from the archive export, so it is as fresh as the last export."],
     "prov":[["RECORD","seen directly in a source, cited with a date"],["INFERENCE","reasoned from the record"],
             ["MEASURED","computed across the corpus"],["WEB","public web, cited with a date"]]}

SOURCES = [
 {"key":"gmail","name":"Gmail","detail":"24 months of email; 4,120 threads reviewed, 310 opened in full; 188 signals extracted"},
 {"key":"calendar","name":"Calendar","detail":"24 months: 3,400 events reviewed, 1,860 substantive ones kept"},
 {"key":"granola","name":"Granola","detail":"212 meetings read (notes), 40 full transcripts mined; 260 signals extracted"},
 {"key":"whatsapp","name":"WhatsApp","detail":"52 chats exported, 31 read in full; 71 signals extracted"},
 {"key":"linkedin","name":"LinkedIn","detail":"Archive export: 1,420 connections, 380 message threads; 44 signals extracted"},
 {"key":"slack","name":"Slack","detail":"public channels and DMs, 12 months; 90 signals extracted"},
 {"key":"contacts","name":"Contacts","detail":"905 contacts ingested and deduplicated into the identity index"},
 {"key":"web","name":"Web","detail":"22 public-source lookups, each cited with a date"},
]

DATA = {
 "CONFIG":{"owner_name":OWNER,"owner_first":FIRST,"owner_aliases":["Alex M"],"company":CO,"slack_workspace":"",
           "page_title":"Sparks Orrery"},
 "DATA_THROUGH":iso(THROUGH),"FEED_SNAP":iso(THROUGH)+"T21:00:00+01:00",
 "SOURCES":SOURCES,"TB_NAMES":TB_NAMES,"TB_OTHER":TB_OTHER,
 "PSENS_IDS":[],"PSENS_LIST":[],"NEW_MOVES":["introduce-isabel-mira","commercial-rachel-pilot"],"PERSONAL_MOVES":[],
 "INTAKE":{},
 "NEWS":NEWS,"PROM":PROM,"TIME":TIME,"CORPUS":CORPUS,"D":D,"MTITLES":{},"PERSON2":{},
 "ORR":ORR,"LDG":LDG,"FEED":FEED,"EMAIL_NAME":{},
}
json.dump(DATA, sys.stdout, ensure_ascii=False)
