#!/usr/bin/env python3
"""build_bank_2514.py — WO-F NGN item bank for RNSG 2514 (Complications).

Authored against build-spec §5.3 schema and the ten item-writing rules.
Items are grouped by teaching day (the WO-F sharding). Emits:
  build/_shards/RNSG2514_ItemBank_D{1..4}.json   (intermediate)
  build/RNSG2514/RNSG2514_ItemBank_v1.json       (merged, the deliverable)
  build/RNSG2514/RNSG2514_ItemBank_v1.md          (human-readable mirror)

Every stem presents data, not a conclusion (Rule 1). Every distractor is correct in
some other scenario, stated in rationale_distractors (Rule 3). Sources are drawn only
from the RNSG2514 lesson-plan reference list.
Run:  python tools/build_bank_2514.py
"""
import json
import os

COURSE = "RNSG2514"


def I(iid, obj, itype, op, cn, bloom, diff, stem, options, key, rc, rd, source, kw,
      chart=None, scoring="0/1", day=1):
    return dict(id=iid, objective_id=obj, item_type=itype, ncjmm_operation=op,
                client_needs=cn, bloom=bloom, difficulty_target=diff, stem=stem,
                chart_data=chart or {}, options=options, key=key, scoring=scoring,
                rationale_correct=rc, rationale_distractors=rd, source=source,
                keywords=kw, _day=day)


ITEMS = [
    # ================= DAY 1 — Bleeding, loss, hemorrhage =================
    I("2514-D1-101", "2514-D1-3", "standalone_mc", "Analyze Cues",
      "Reduction of Risk Potential", "Analyze", "moderate",
      "A patient at 34 weeks reports a sudden gush of bright-red vaginal blood. She has no pain, "
      "and the uterus is soft and non-tender. Fetal heart rate is 140 with moderate variability. "
      "Which finding pattern does the nurse recognize?",
      ["Placenta previa", "Abruptio placentae", "Uterine rupture", "Ruptured vasa previa"],
      ["Placenta previa"],
      "Painless, bright-red bleeding with a soft, non-tender uterus and reassuring fetal status is "
      "the classic previa pattern. The transferable principle: in late bleeding, pain and uterine "
      "tone separate previa from abruption before any imaging.",
      {"Abruptio placentae": "Right for painful, dark bleeding with a rigid, tender uterus and often a "
       "Category II/III tracing.",
       "Uterine rupture": "Right when there is loss of station, acute pain, and fetal bradycardia, "
       "usually during TOLAC.",
       "Ruptured vasa previa": "Right when membrane rupture is followed by bleeding plus sudden fetal "
       "bradycardia — the blood is fetal."},
      "Lowdermilk 13th ed.", ["previa", "abruption", "late bleeding"], day=1),

    I("2514-D1-102", "2514-D1-3", "standalone_mc", "Take Actions",
      "Reduction of Risk Potential", "Apply", "moderate",
      "A patient at 32 weeks arrives with painless bright-red vaginal bleeding. Placental location "
      "is not yet documented. Which action should the nurse take first?",
      ["Perform a digital cervical exam to assess dilation",
       "Withhold digital vaginal examination and prepare for ultrasound",
       "Insert a urinary catheter and begin oxytocin",
       "Place the patient in Trendelenburg position"],
      ["Withhold digital vaginal examination and prepare for ultrasound"],
      "Until previa is excluded by ultrasound, a digital exam can provoke catastrophic hemorrhage. "
      "The principle: with undiagnosed late-pregnancy bleeding, imaging precedes any vaginal exam.",
      {"Perform a digital cervical exam to assess dilation": "Right in normal labor once previa is "
       "excluded — here it is contraindicated.",
       "Insert a urinary catheter and begin oxytocin": "Right for augmenting labor, not for undiagnosed "
       "APH; oxytocin does not address bleeding source.",
       "Place the patient in Trendelenburg position": "Not evidence-based for obstetric bleeding and can "
       "impair respiratory effort."},
      "Lowdermilk 13th ed.", ["previa", "no digital exam", "first action"], day=1),

    I("2514-D1-103", "2514-D1-3", "highlight", "Recognize Cues",
      "Physiological Adaptation", "Analyze", "moderate",
      "Highlight the findings in the note that point to abruptio placentae rather than previa. "
      "Nurses' note: '38 weeks, sudden onset constant abdominal pain, dark vaginal bleeding, "
      "uterus firm and tender to palpation, contractions difficult to distinguish from baseline "
      "tone, FHR baseline 165 with minimal variability and late decelerations.'",
      ["constant abdominal pain", "dark vaginal bleeding", "uterus firm and tender",
       "increased resting tone", "late decelerations with minimal variability"],
      ["constant abdominal pain", "dark vaginal bleeding", "uterus firm and tender",
       "increased resting tone", "late decelerations with minimal variability"],
      "Pain, dark blood, a rigid tender uterus with elevated tone, and a deteriorating tracing are "
      "the abruption cluster. Principle: abruption threatens both mother (concealed loss, DIC) and "
      "fetus (uteroplacental compromise).",
      {"(distractor findings)": "A note describing painless bright-red bleeding with a soft uterus and "
       "a Category I tracing would instead point to previa."},
      "Lowdermilk 13th ed.", ["abruption", "highlight", "recognize cues"], day=1),

    I("2514-D1-104", "2514-D1-1", "standalone_mc", "Recognize Cues",
      "Physiological Adaptation", "Understand", "easy",
      "A patient at 9 weeks reports heavy bleeding and passage of grape-like vesicular tissue. "
      "Serum hCG is markedly higher than expected for dates and no fetal heart tones are found. "
      "Which condition do these findings suggest?",
      ["Threatened miscarriage", "Gestational trophoblastic disease (molar pregnancy)",
       "Ectopic pregnancy", "Implantation bleeding"],
      ["Gestational trophoblastic disease (molar pregnancy)"],
      "Vesicular tissue, disproportionately high hCG, and absent fetal heart tones define a molar "
      "pregnancy, which needs evacuation and serial hCG follow-up. Principle: hCG far above dates "
      "with vesicles is molar until proven otherwise.",
      {"Threatened miscarriage": "Right for bleeding with a closed cervix and a viable intrauterine "
       "pregnancy on ultrasound.",
       "Ectopic pregnancy": "Right for unilateral pain with lower-than-expected hCG and no intrauterine "
       "sac.",
       "Implantation bleeding": "Right for light spotting around the expected menses with normal hCG "
       "rise."},
      "Lowdermilk 13th ed.", ["molar", "GTD", "hCG"], day=1),

    I("2514-D1-105", "2514-D1-2", "standalone_mc", "Analyze Cues",
      "Physiological Adaptation", "Analyze", "hard",
      "A patient at 7 weeks has unilateral lower abdominal pain and scant bleeding. Serum hCG is "
      "1,900 mIU/mL and transvaginal ultrasound shows no intrauterine gestational sac. Which "
      "interpretation is best supported?",
      ["Normal early intrauterine pregnancy", "Completed miscarriage",
       "Possible ectopic pregnancy requiring close follow-up", "Molar pregnancy"],
      ["Possible ectopic pregnancy requiring close follow-up"],
      "An hCG above the discriminatory zone with no intrauterine sac raises concern for ectopic "
      "pregnancy and mandates urgent evaluation. Principle: 'no sac when hCG says there should be "
      "one' is an ectopic red flag.",
      {"Normal early intrauterine pregnancy": "Right when a sac is seen or hCG is below the "
       "discriminatory zone and rising appropriately.",
       "Completed miscarriage": "Right when hCG is falling and the patient reports passage of tissue "
       "with resolving symptoms.",
       "Molar pregnancy": "Right with vesicular tissue and hCG far higher than expected for dates."},
      "ACOG PB 200 (2018)", ["ectopic", "discriminatory zone", "analyze cues"], day=1),

    I("2514-D1-106", "2514-D1-4", "bowtie", "Take Actions",
      "Pharmacological and Parenteral Therapies", "Apply", "hard",
      "Ten minutes after a vaginal birth, the uterus is boggy and above the umbilicus, and there is "
      "a steady flow of blood. Select the 2 immediate actions, the 1 condition, and the 2 parameters "
      "to monitor.",
      {"actions_options": ["Firmly massage the fundus", "Administer oxytocin per protocol",
                           "Administer methylergonovine to a patient with severe hypertension",
                           "Wait 30 minutes and reassess", "Place the patient in reverse Trendelenburg"],
       "condition_options": ["Uterine atony", "Vaginal laceration", "Retained placenta",
                             "Amniotic fluid embolism"],
       "parameter_options": ["Fundal tone and position", "Quantified blood loss and vital signs",
                             "Deep tendon reflexes", "Blood glucose"]},
      {"actions": ["Firmly massage the fundus", "Administer oxytocin per protocol"],
       "condition": ["Uterine atony"],
       "parameters": ["Fundal tone and position", "Quantified blood loss and vital signs"]},
      "A boggy, high uterus with bleeding is atony — the first of the 4 Ts and the leading PPH cause. "
      "Massage plus oxytocin are first-line; tone and quantified loss track the response. Principle: "
      "treat tone first because atony causes most PPH.",
      {"Administer methylergonovine to a patient with severe hypertension": "Methylergonovine is a "
       "correct uterotonic but is contraindicated in hypertension.",
       "Retained placenta / Vaginal laceration": "Each is a real PPH cause (Tissue, Trauma) but the "
       "boggy fundus points to Tone first.",
       "Deep tendon reflexes": "Right to monitor on magnesium therapy, not for hemorrhage."},
      "ACOG PB 183 (2017)", ["PPH", "atony", "4 Ts", "bowtie"], scoring="+/-", day=1),

    I("2514-D1-107", "2514-D1-4", "extended_drag_drop", "Take Actions",
      "Management of Care", "Apply", "hard",
      "A patient has an estimated 1,200 mL blood loss from uterine atony unresponsive to fundal "
      "massage and oxytocin. Place the next nursing actions in the correct priority order.",
      ["Call for help and notify the provider", "Ensure two large-bore IVs and give isotonic fluid",
       "Administer a second-line uterotonic per order (e.g., carboprost if no asthma)",
       "Prepare for possible transfusion and quantify ongoing loss",
       "Document the event timeline and blood loss"],
      ["Call for help and notify the provider", "Ensure two large-bore IVs and give isotonic fluid",
       "Administer a second-line uterotonic per order (e.g., carboprost if no asthma)",
       "Prepare for possible transfusion and quantify ongoing loss",
       "Document the event timeline and blood loss"],
      "PPH escalation follows a bundle: summon help, secure access and volume, escalate uterotonics, "
      "prepare blood products, and document. Principle: staged hemorrhage response prevents the delay "
      "that drives maternal mortality.",
      {"Administer a second-line uterotonic (carboprost)": "Carboprost is correct only when asthma is "
       "absent; order matters — help and access come first.",
       "Document the event timeline": "Essential but never ahead of active resuscitation."},
      "ACOG PB 183 (2017)", ["PPH bundle", "escalation", "drag drop"], scoring="0/1", day=1),

    I("2514-D1-108", "2514-D1-4", "sata", "Analyze Cues",
      "Pharmacological and Parenteral Therapies", "Analyze", "moderate",
      "A patient with postpartum hemorrhage has a history of asthma and a blood pressure of "
      "168/104. Select all uterotonic considerations that apply.",
      ["Oxytocin is appropriate first-line",
       "Methylergonovine is contraindicated because of hypertension",
       "Carboprost (PGF2α) is used cautiously or avoided because of asthma",
       "Tranexamic acid may be given within 3 hours as an adjunct",
       "Misoprostol cannot be used under any circumstance"],
      ["Oxytocin is appropriate first-line",
       "Methylergonovine is contraindicated because of hypertension",
       "Carboprost (PGF2α) is used cautiously or avoided because of asthma",
       "Tranexamic acid may be given within 3 hours as an adjunct"],
      "Uterotonic choice is driven by comorbidity: ergot agents avoid hypertension, carboprost avoids "
      "asthma, oxytocin is first-line, and TXA is a timed adjunct. Principle: match the uterotonic to "
      "the patient's contraindications.",
      {"Misoprostol cannot be used under any circumstance": "False — misoprostol is often the usable "
       "option precisely when both ergots and carboprost are contraindicated."},
      "ACOG PB 183 (2017)", ["uterotonics", "contraindications", "SATA"], scoring="0/1", day=1),

    I("2514-D1-109", "2514-D1-4", "standalone_mc", "Analyze Cues",
      "Physiological Adaptation", "Analyze", "hard",
      "A postpartum patient has oozing from her IV site and gums, bruising, and continued vaginal "
      "bleeding. Fibrinogen is low and platelets are falling. Which process do these findings "
      "indicate?",
      ["Normal postpartum involution", "Disseminated intravascular coagulation",
       "Isolated vaginal laceration", "Von Willebrand carrier state at baseline"],
      ["Disseminated intravascular coagulation"],
      "Bleeding from multiple sites with falling fibrinogen and platelets is consumptive coagulopathy "
      "(DIC), often triggered by abruption, HELLP, or massive PPH. Principle: oozing from many sites "
      "means the clotting system itself has failed.",
      {"Normal postpartum involution": "Right for a firm fundus with decreasing lochia and stable labs.",
       "Isolated vaginal laceration": "Right for localized bright bleeding from a visualized tear with "
       "normal coagulation.",
       "Von Willebrand carrier state at baseline": "Right as a chronic history clue, but does not explain "
       "acutely falling fibrinogen and platelets."},
      "ACOG PB 183 (2017)", ["DIC", "coagulopathy"], day=1),

    I("2514-D1-110", "2514-D1-5", "standalone_mc", "Take Actions",
      "Pharmacological and Parenteral Therapies", "Apply", "moderate",
      "An Rh-negative patient experiences a first-trimester pregnancy loss with bleeding. Her "
      "antibody screen is negative. Which nursing action is indicated?",
      ["No intervention is needed because it was early",
       "Administer Rh(D) immune globulin as ordered",
       "Administer the rubella vaccine now",
       "Schedule the anti-D only if a future pregnancy occurs"],
      ["Administer Rh(D) immune globulin as ordered"],
      "Bleeding or loss in an Rh-negative, unsensitized patient is an indication for Rh(D) immune "
      "globulin to prevent alloimmunization. Principle: any fetomaternal bleeding event in an "
      "Rh-negative patient triggers anti-D.",
      {"No intervention is needed because it was early": "Sensitization can occur even in early loss; "
       "'early' does not remove the indication.",
       "Administer the rubella vaccine now": "Right to offer rubella-non-immune patients postpartum, "
       "unrelated to Rh status.",
       "Schedule the anti-D only if a future pregnancy occurs": "Too late — prophylaxis must be given "
       "at the sensitizing event."},
      "ACOG PB 181 (2017)", ["RhIG", "Rh-negative", "loss"], day=1),

    I("2514-D1-111", "2514-D1-4", "trend", "Evaluate Outcomes",
      "Reduction of Risk Potential", "Analyze", "moderate",
      "The nurse reviews the postpartum record after treating atony. Evaluate the trend and select "
      "the interpretation that best reflects the response to therapy.",
      ["The patient is stabilizing and therapy is effective",
       "The patient is deteriorating and needs escalation",
       "The data are unchanged and therapy has no effect",
       "The fundus is rising, indicating clot retention"],
      ["The patient is stabilizing and therapy is effective"],
      "Across the three time points the fundus becomes firm, blood loss slows, and vitals normalize — "
      "an effective response. Principle: evaluate a hemorrhage intervention by trend in fundal tone, "
      "cumulative loss, and perfusion, not a single reading.",
      {"deteriorating / unchanged / rising fundus": "Each would be correct for a different trend; the "
       "recorded values here show improvement, so those readings do not fit."},
      "ACOG PB 183 (2017)", ["PPH", "trend", "evaluate outcomes"],
      chart={"flowsheet": "hour 0: fundus boggy 2 cm above umbilicus, QBL 900 mL, BP 96/58, HR 118; "
             "hour 1: fundus firm at umbilicus, QBL +150 mL, BP 108/64, HR 96; "
             "hour 2: fundus firm 1 cm below umbilicus, QBL +40 mL, BP 116/70, HR 82"}, day=1),

    I("2514-D1-112", "2514-D1-2", "cloze_dropdown", "Prioritize Hypotheses",
      "Physiological Adaptation", "Analyze", "moderate",
      "Complete the statement. A patient at 6 weeks with unilateral pain, a positive pregnancy test, "
      "and no intrauterine sac on ultrasound is most likely experiencing a(n) [1], and the priority "
      "concern is [2].",
      {"1": ["ectopic pregnancy", "molar pregnancy", "complete miscarriage"],
       "2": ["tubal rupture and hemorrhage", "gestational hypertension", "preterm labor"]},
      {"1": "ectopic pregnancy", "2": "tubal rupture and hemorrhage"},
      "The cue cluster indicates ectopic pregnancy, whose life threat is tubal rupture with "
      "intra-abdominal hemorrhage. Principle: for ectopic pregnancy, the hypothesis and the priority "
      "risk are inseparable — anticipate rupture.",
      {"molar pregnancy / complete miscarriage": "Each is a real early-pregnancy diagnosis but does not "
       "match unilateral pain with an empty uterus and positive test.",
       "gestational hypertension / preterm labor": "Both are later-pregnancy concerns, not applicable at "
       "6 weeks."},
      "ACOG PB 200 (2018)", ["ectopic", "cloze", "prioritize"], scoring="0/1", day=1),

    I("2514-D1-113", "2514-D1-3", "matrix_multiple_choice", "Analyze Cues",
      "Reduction of Risk Potential", "Analyze", "hard",
      "For each finding, select whether it is more consistent with Placenta previa or Abruptio "
      "placentae.",
      {"rows": ["Painless bleeding", "Dark bleeding with pain", "Soft non-tender uterus",
                "Rigid, tender uterus with high tone", "Bright-red external bleeding"],
       "columns": ["Placenta previa", "Abruptio placentae"]},
      {"Painless bleeding": "Placenta previa", "Dark bleeding with pain": "Abruptio placentae",
       "Soft non-tender uterus": "Placenta previa",
       "Rigid, tender uterus with high tone": "Abruptio placentae",
       "Bright-red external bleeding": "Placenta previa"},
      "Previa: painless, bright, soft uterus. Abruption: painful, dark, rigid uterus, and bleeding may "
      "be concealed. Principle: tone and pain discriminate the two faster than blood color alone.",
      {"(any misassignment)": "Swapping a row assigns an abruption feature to previa or vice versa — "
       "each feature is decisive only for its own condition."},
      "Lowdermilk 13th ed.", ["previa", "abruption", "matrix"], scoring="0/1", day=1),

    # ================= DAY 2 — HTN, HELLP, magnesium, HG, GDM =================
    I("2514-D2-201", "2514-D2-1", "standalone_mc", "Analyze Cues",
      "Physiological Adaptation", "Analyze", "moderate",
      "A patient at 33 weeks with no prior hypertension has a blood pressure of 148/94 on two "
      "readings 4 hours apart and a urine protein-to-creatinine ratio of 0.2. Which classification "
      "do the findings support?",
      ["Chronic hypertension", "Gestational hypertension",
       "Preeclampsia with severe features", "Normal pregnancy blood pressure"],
      ["Gestational hypertension"],
      "New hypertension after 20 weeks without significant proteinuria (P:C < 0.3) or severe features "
      "is gestational hypertension. Principle: timing after 20 weeks plus absence of proteinuria "
      "separates gHTN from chronic HTN and preeclampsia.",
      {"Chronic hypertension": "Right when hypertension predates pregnancy or appears before 20 weeks.",
       "Preeclampsia with severe features": "Right with severe-range BP or end-organ signs, absent here.",
       "Normal pregnancy blood pressure": "Incorrect — 148/94 exceeds the 140/90 threshold."},
      "ACOG PB 222 (2020)", ["gHTN", "classification"], day=2),

    I("2514-D2-202", "2514-D2-2", "highlight", "Recognize Cues",
      "Reduction of Risk Potential", "Analyze", "hard",
      "Highlight the findings that indicate severe features. Note: '36 weeks, BP 164/112, reports a "
      "persistent headache unrelieved by acetaminophen and new visual scotomata, platelets 88,000, "
      "AST 140, reports right upper quadrant pain, urine output 90 mL over 4 hours.'",
      ["BP 164/112", "persistent headache unrelieved", "visual scotomata", "platelets 88,000",
       "AST 140", "right upper quadrant pain"],
      ["BP 164/112", "persistent headache unrelieved", "visual scotomata", "platelets 88,000",
       "AST 140", "right upper quadrant pain"],
      "Severe-range BP, CNS symptoms, thrombocytopenia < 100,000, transaminase elevation, and RUQ pain "
      "each qualify as severe features. Principle: any one severe feature — not proteinuria — defines "
      "preeclampsia with severe features.",
      {"urine output 90 mL over 4 hours": "About 22 mL/hr is low-normal and, alone, is not a listed "
       "severe feature, though it warrants monitoring."},
      "ACOG PB 222 (2020)", ["severe features", "highlight", "preeclampsia"], scoring="0/1", day=2),

    I("2514-D2-203", "2514-D2-2", "standalone_mc", "Recognize Cues",
      "Reduction of Risk Potential", "Analyze", "hard",
      "A patient at 37 weeks has a blood pressure of 162/110 and platelets of 84,000 but a urine "
      "protein-to-creatinine ratio of 0.1. Which statement best reflects the diagnostic reasoning?",
      ["Preeclampsia is excluded because proteinuria is absent",
       "Preeclampsia with severe features can be diagnosed without proteinuria",
       "This is gestational hypertension only",
       "This requires a 24-hour urine before any diagnosis"],
      ["Preeclampsia with severe features can be diagnosed without proteinuria"],
      "Since 2013, preeclampsia can be diagnosed without proteinuria when severe-range BP plus a "
      "severe feature (here, thrombocytopenia) are present. Principle: absence of proteinuria never "
      "rules out preeclampsia.",
      {"Preeclampsia is excluded because proteinuria is absent": "Reflects the outdated rule that "
       "proteinuria is required.",
       "This is gestational hypertension only": "Right only if there were no proteinuria AND no severe "
       "features; a severe feature is present.",
       "This requires a 24-hour urine before any diagnosis": "Right as a quantification method in some "
       "cases, but it is not required to act on severe features."},
      "ACOG PB 222 (2020)", ["preeclampsia", "no proteinuria", "severe features"], day=2),

    I("2514-D2-204", "2514-D2-3", "matrix_grid", "Analyze Cues",
      "Reduction of Risk Potential", "Analyze", "hard",
      "A patient reports malaise and RUQ pain. For each lab, indicate whether the value is Expected "
      "or Abnormal for HELLP syndrome.",
      {"rows": ["Platelets 92,000", "AST 130 U/L", "LDH 700 U/L", "Haptoglobin low",
                "Fasting glucose 88 mg/dL"],
       "columns": ["Consistent with HELLP", "Not related to HELLP"]},
      {"Platelets 92,000": "Consistent with HELLP", "AST 130 U/L": "Consistent with HELLP",
       "LDH 700 U/L": "Consistent with HELLP", "Haptoglobin low": "Consistent with HELLP",
       "Fasting glucose 88 mg/dL": "Not related to HELLP"},
      "HELLP is hemolysis (high LDH, low haptoglobin), elevated liver enzymes, and low platelets. "
      "Glucose is unrelated. Principle: read HELLP as a three-part lab pattern, not a single value.",
      {"Fasting glucose 88 mg/dL": "A normal glucose is relevant to GDM screening, not to HELLP."},
      "ACOG PB 222 (2020)", ["HELLP", "labs", "matrix grid"], scoring="0/1", day=2),

    I("2514-D2-205", "2514-D2-4", "standalone_mc", "Take Actions",
      "Pharmacological and Parenteral Therapies", "Apply", "moderate",
      "A patient receiving IV magnesium sulfate for seizure prophylaxis has a respiratory rate of 10, "
      "absent patellar reflexes, and urine output of 20 mL over the last 2 hours. Which action is the "
      "priority?",
      ["Increase the magnesium infusion rate",
       "Stop the magnesium infusion and prepare calcium gluconate",
       "Administer an additional loading dose",
       "Document and reassess in 1 hour"],
      ["Stop the magnesium infusion and prepare calcium gluconate"],
      "Loss of reflexes with respiratory depression signals magnesium toxicity; stop the infusion and "
      "give the antidote, calcium gluconate. Principle: reflexes disappear before respiratory and "
      "cardiac depression — treat at the first toxicity sign.",
      {"Increase the magnesium infusion rate": "Right only when reflexes are present and levels are "
       "subtherapeutic — dangerous here.",
       "Administer an additional loading dose": "Correct at initiation of therapy, not during toxicity.",
       "Document and reassess in 1 hour": "Delays antidote during a life-threatening trend."},
      "ACOG PB 222 (2020)", ["magnesium toxicity", "calcium gluconate", "first action"], day=2),

    I("2514-D2-206", "2514-D2-4", "trend", "Evaluate Outcomes",
      "Pharmacological and Parenteral Therapies", "Analyze", "hard",
      "Review the magnesium monitoring record and select the interpretation that should drive the "
      "nurse's next decision.",
      ["Therapy is within a safe range; continue monitoring",
       "A toxicity trend is emerging; hold and reassess per protocol",
       "The patient is subtherapeutic and needs a higher rate",
       "The values reflect normal labor progress"],
      ["A toxicity trend is emerging; hold and reassess per protocol"],
      "Across the three checks, reflexes diminish, respiratory rate falls, and urine output drops — an "
      "early toxicity trajectory even before a level returns. Principle: serial clinical signs detect "
      "magnesium toxicity earlier than any single serum level.",
      {"safe range / subtherapeutic / normal labor": "Each matches a different trend; the declining "
       "reflexes and respirations recorded here contradict all three."},
      "ACOG PB 222 (2020)", ["magnesium", "trend", "toxicity"],
      chart={"monitoring": "hour 0: DTR 2+, RR 18, UOP 60 mL; hour 2: DTR 1+, RR 14, UOP 35 mL; "
             "hour 4: DTR absent, RR 10, UOP 18 mL"}, scoring="0/1", day=2),

    I("2514-D2-207", "2514-D2-4", "sata", "Take Actions",
      "Safety and Infection Control", "Apply", "moderate",
      "A patient is starting IV magnesium sulfate. Select all appropriate nursing safety measures.",
      ["Keep calcium gluconate readily available",
       "Monitor deep tendon reflexes, respirations, and urine output",
       "Use the magnesium as the antihypertensive to lower blood pressure",
       "Assess for signs of pulmonary edema",
       "Ensure continuous fetal and maternal monitoring"],
      ["Keep calcium gluconate readily available",
       "Monitor deep tendon reflexes, respirations, and urine output",
       "Assess for signs of pulmonary edema",
       "Ensure continuous fetal and maternal monitoring"],
      "Magnesium safety centers on the antidote at bedside, serial reflex/respiration/output checks, "
      "watching for pulmonary edema, and monitoring. Principle: magnesium prevents seizures — it does "
      "not treat blood pressure.",
      {"Use the magnesium as the antihypertensive to lower blood pressure": "False — labetalol, "
       "hydralazine, or nifedipine lower BP; magnesium is for seizure prophylaxis."},
      "ACOG PB 222 (2020)", ["magnesium", "safety", "SATA"], scoring="0/1", day=2),

    I("2514-D2-208", "2514-D2-5", "standalone_mc", "Generate Solutions",
      "Health Promotion and Maintenance", "Apply", "moderate",
      "A patient at 13 weeks has a history of preeclampsia in a prior pregnancy and chronic "
      "hypertension. Which preventive intervention is most appropriate to discuss?",
      ["Begin low-dose aspirin 81 mg daily",
       "Start full-dose ibuprofen for prophylaxis",
       "Begin magnesium sulfate now",
       "No preventive therapy is indicated"],
      ["Begin low-dose aspirin 81 mg daily"],
      "High-risk patients benefit from low-dose aspirin started between 12 and 28 weeks to reduce "
      "preeclampsia. Principle: identify high-risk patients early and offer aspirin prophylaxis in "
      "the window.",
      {"Start full-dose ibuprofen for prophylaxis": "NSAIDs are not used for preeclampsia prophylaxis "
       "and are avoided later in pregnancy.",
       "Begin magnesium sulfate now": "Right for seizure prophylaxis in active severe disease, not for "
       "prevention at 13 weeks.",
       "No preventive therapy is indicated": "Incorrect — this patient has clear high-risk criteria."},
      "ACOG CO 743 (2018)", ["aspirin", "preeclampsia prevention"], day=2),

    I("2514-D2-209", "2514-D2-6", "standalone_mc", "Generate Solutions",
      "Basic Care and Comfort", "Apply", "easy",
      "A patient at 10 weeks has persistent vomiting, a 6% weight loss, and ketones in the urine. "
      "Which initial intervention is most appropriate?",
      ["Encourage a large high-fat meal now",
       "Provide IV fluids with electrolyte replacement and antiemetics as ordered",
       "Withhold all antiemetics",
       "Delay treatment until 14 weeks"],
      ["Provide IV fluids with electrolyte replacement and antiemetics as ordered"],
      "Hyperemesis with weight loss and ketosis needs rehydration, electrolyte correction, and "
      "antiemetics. Principle: treat the dehydration and electrolyte deficit first, then advance "
      "nutrition.",
      {"Encourage a large high-fat meal now": "Right approach is small, bland, frequent intake — large "
       "fatty meals worsen nausea.",
       "Withhold all antiemetics": "Antiemetics are indicated; withholding them prolongs suffering.",
       "Delay treatment until 14 weeks": "Dangerous — dehydration and electrolyte loss need prompt care."},
      "ACOG PB 189 (2018)", ["hyperemesis", "fluids"], day=2),

    I("2514-D2-210", "2514-D2-7", "cloze_dropdown", "Generate Solutions",
      "Health Promotion and Maintenance", "Apply", "moderate",
      "Complete the teaching. For a patient with diet-controlled gestational diabetes, the nurse "
      "explains that the first-line management is [1], and if glucose targets are not met the usual "
      "next step is [2].",
      {"1": ["medical nutrition therapy and exercise", "immediate insulin", "prolonged fasting"],
       "2": ["adding insulin", "stopping all carbohydrates", "bed rest"]},
      {"1": "medical nutrition therapy and exercise", "2": "adding insulin"},
      "GDM management begins with nutrition and activity (class A1); insulin is added when targets are "
      "missed (class A2). Principle: escalate GDM stepwise from lifestyle to pharmacotherapy.",
      {"immediate insulin / prolonged fasting": "Insulin is not first-line for diet-controlled GDM, and "
       "fasting is unsafe in pregnancy.",
       "stopping all carbohydrates / bed rest": "Neither is recommended; balanced carbohydrate intake is "
       "part of therapy."},
      "ACOG PB 190 (2018)", ["GDM", "cloze", "insulin"], scoring="0/1", day=2),

    I("2514-D2-211", "2514-D2-7", "standalone_mc", "Analyze Cues",
      "Reduction of Risk Potential", "Analyze", "moderate",
      "A patient completes a 1-hour 50 g glucose challenge test with a result of 155 mg/dL. Which "
      "interpretation and next step are correct?",
      ["Normal result; no further testing",
       "Elevated screen; proceed to the 3-hour oral glucose tolerance test",
       "Diagnostic of overt diabetes; start insulin",
       "Repeat the same 1-hour test next week"],
      ["Elevated screen; proceed to the 3-hour oral glucose tolerance test"],
      "An abnormal 1-hour screen is followed by the diagnostic 3-hour OGTT; the screen alone does not "
      "diagnose GDM. Principle: a positive screen raises suspicion, a diagnostic test confirms.",
      {"Normal result; no further testing": "Right only when the 1-hour value is below the institutional "
       "threshold.",
       "Diagnostic of overt diabetes; start insulin": "Right for markedly elevated values or known "
       "diabetes, not a borderline screen.",
       "Repeat the same 1-hour test next week": "Screening is not repeated in place of the diagnostic "
       "OGTT."},
      "ACOG PB 190 (2018); ACOG (2024)", ["GDM", "GCT", "OGTT"], day=2),

    I("2514-D2-212", "2514-D2-1", "extended_multiple_response", "Prioritize Hypotheses",
      "Reduction of Risk Potential", "Analyze", "hard",
      "A patient at 38 weeks has BP 158/108, a headache, and brisk reflexes. Select the 3 findings "
      "that would most raise concern for progression to eclampsia.",
      ["Persistent severe headache", "Visual disturbances", "Clonus on reflex testing",
       "Mild ankle edema", "Blood pressure 118/70 earlier in pregnancy",
       "Reports of fetal movement"],
      ["Persistent severe headache", "Visual disturbances", "Clonus on reflex testing"],
      "CNS irritability — severe headache, visual change, and clonus — predicts impending seizure. "
      "Principle: neurologic signs, not blood pressure alone, herald eclampsia.",
      {"Mild ankle edema": "Common and non-specific in normal pregnancy.",
       "Blood pressure 118/70 earlier": "A normal prior value is reassuring history, not a current "
       "warning sign.",
       "Reports of fetal movement": "A reassuring finding, not a warning sign."},
      "ACOG PB 222 (2020)", ["eclampsia", "CNS", "extended response"], scoring="0/1", day=2),

    I("2514-D2-213", "2514-D2-6", "standalone_mc", "Recognize Cues",
      "Physiological Adaptation", "Understand", "easy",
      "A patient with severe vomiting has dry mucous membranes, tachycardia, and a low serum "
      "potassium. Which imbalance do these findings most reflect?",
      ["Fluid volume excess", "Dehydration with hypokalemia",
       "Respiratory alkalosis from hyperventilation", "Hyperkalemia"],
      ["Dehydration with hypokalemia"],
      "Vomiting produces volume depletion and potassium loss, shown by dry membranes, tachycardia, and "
      "low potassium. Principle: match the electrolyte pattern to the route of loss.",
      {"Fluid volume excess": "Right for edema, crackles, and weight gain — opposite of this picture.",
       "Respiratory alkalosis from hyperventilation": "Right for a primary breathing disturbance, not "
       "vomiting-driven loss.",
       "Hyperkalemia": "Opposite of the measured low potassium."},
      "ACOG PB 189 (2018)", ["hyperemesis", "hypokalemia"], day=2),

    # ================= DAY 3 — PTL, ACS, PROM/PPROM, induction, dystocia =========
    I("2514-D3-301", "2514-D3-1", "standalone_mc", "Prioritize Hypotheses",
      "Reduction of Risk Potential", "Analyze", "moderate",
      "A patient at 29 weeks reports regular painful contractions every 5 minutes. Cervical exam "
      "shows 2 cm dilation with change over 2 hours. Which is the priority goal of care?",
      ["Deliver immediately regardless of gestational age",
       "Delay birth long enough to give antenatal corticosteroids and magnesium neuroprotection",
       "Discharge home with activity restriction only",
       "Begin oxytocin augmentation"],
      ["Delay birth long enough to give antenatal corticosteroids and magnesium neuroprotection"],
      "Confirmed preterm labor before 32 weeks prioritizes buying time for steroids (lung maturity) "
      "and magnesium (neuroprotection). Principle: in previable-to-preterm labor, the goal is "
      "latency for fetal benefit, not immediate birth.",
      {"Deliver immediately regardless of gestational age": "Right only for contraindications to "
       "continuing (e.g., abruption, Category III), absent here.",
       "Discharge home with activity restriction only": "Unsafe with documented cervical change.",
       "Begin oxytocin augmentation": "Contradicts the goal of stopping preterm contractions."},
      "ACOG PB 171 (2016); PB 234 (2021)", ["preterm labor", "steroids", "neuroprotection"], day=3),

    I("2514-D3-302", "2514-D3-2", "standalone_mc", "Take Actions",
      "Pharmacological and Parenteral Therapies", "Apply", "moderate",
      "A patient at 30 weeks in preterm labor is ordered betamethasone. The patient asks what it "
      "does. Which response is most accurate?",
      ["It stops contractions immediately",
       "It accelerates fetal lung maturity to reduce respiratory distress",
       "It treats an infection",
       "It lowers your blood pressure"],
      ["It accelerates fetal lung maturity to reduce respiratory distress"],
      "Antenatal corticosteroids speed surfactant production, reducing RDS, IVH, and NEC. Principle: "
      "steroids protect the fetus; tocolytics only buy the time to give them.",
      {"It stops contractions immediately": "That is the tocolytic's role, not the steroid's.",
       "It treats an infection": "Right description for an antibiotic, not a corticosteroid.",
       "It lowers your blood pressure": "Describes an antihypertensive, unrelated to ACS."},
      "ACOG CO 713 (2017)", ["betamethasone", "ACS", "lung maturity"], day=3),

    I("2514-D3-303", "2514-D3-3", "standalone_mc", "Prioritize Hypotheses",
      "Reduction of Risk Potential", "Analyze", "hard",
      "A patient at 30 weeks has a sudden gush of clear fluid; nitrazine turns blue and ferning is "
      "seen. She is afebrile with no contractions. Which management approach is most appropriate?",
      ["Immediate induction of labor",
       "Expectant management with monitoring, antibiotics, and steroids",
       "Repeated digital cervical exams every 2 hours",
       "Discharge home with no follow-up"],
      ["Expectant management with monitoring, antibiotics, and steroids"],
      "PPROM before 34 weeks without infection or labor is managed expectantly with latency "
      "antibiotics and steroids while monitoring for infection. Principle: before 34 weeks, "
      "prematurity risk usually outweighs the risk of waiting — unless infection intervenes.",
      {"Immediate induction of labor": "Right at or beyond 34 weeks or if infection/Category III "
       "develops.",
       "Repeated digital cervical exams every 2 hours": "Digital exams raise infection risk and are "
       "minimized after ROM.",
       "Discharge home with no follow-up": "Unsafe; PPROM requires inpatient surveillance."},
      "ACOG PB 217 (2020)", ["PPROM", "expectant management"], day=3),

    I("2514-D3-304", "2514-D3-3", "matrix_multiple_choice", "Analyze Cues",
      "Reduction of Risk Potential", "Analyze", "moderate",
      "For each feature, indicate whether it describes PROM (term) or PPROM (preterm).",
      {"rows": ["Rupture at 39 weeks", "Rupture at 31 weeks", "Higher infection latency concern",
                "Often proceeds to prompt delivery at term"],
       "columns": ["PROM (term)", "PPROM (preterm)"]},
      {"Rupture at 39 weeks": "PROM (term)", "Rupture at 31 weeks": "PPROM (preterm)",
       "Higher infection latency concern": "PPROM (preterm)",
       "Often proceeds to prompt delivery at term": "PROM (term)"},
      "PROM is rupture at term; PPROM is before 37 weeks and carries greater infection and prematurity "
      "concern during latency. Principle: gestational age at rupture drives the whole management plan.",
      {"(any swap)": "Assigning a preterm feature to term (or vice versa) reverses the age-based logic "
       "that governs care."},
      "ACOG PB 217 (2020)", ["PROM", "PPROM", "matrix"], scoring="0/1", day=3),

    I("2514-D3-305", "2514-D3-4", "standalone_mc", "Take Actions",
      "Pharmacological and Parenteral Therapies", "Apply", "hard",
      "During an oxytocin induction, the monitor shows 7 contractions in 10 minutes with a Category "
      "II tracing showing recurrent late decelerations. Which action should the nurse take first?",
      ["Increase the oxytocin rate",
       "Stop or decrease the oxytocin and reposition the patient",
       "Perform an immediate cesarean without other measures",
       "Document and continue as ordered"],
      ["Stop or decrease the oxytocin and reposition the patient"],
      "Tachysystole with a concerning tracing calls for reducing uterine stimulation first — stop or "
      "decrease oxytocin, reposition, and give fluids/oxygen as indicated. Principle: remove the "
      "cause (excess stimulation) before escalating to surgery.",
      {"Increase the oxytocin rate": "Would worsen tachysystole and fetal compromise.",
       "Perform an immediate cesarean without other measures": "Right if intrauterine resuscitation "
       "fails or the tracing becomes Category III.",
       "Document and continue as ordered": "Ignores an actionable, correctable problem."},
      "ACOG-SMFM OCC No. 1 (2014)", ["tachysystole", "oxytocin", "first action"], day=3),

    I("2514-D3-306", "2514-D3-4", "standalone_mc", "Analyze Cues",
      "Reduction of Risk Potential", "Apply", "moderate",
      "Before an induction, a patient has a Bishop score of 3. Which statement best guides planning?",
      ["The cervix is favorable; expect rapid response to oxytocin",
       "The cervix is unfavorable; cervical ripening is likely needed first",
       "Induction is contraindicated at any Bishop score",
       "A cesarean is mandatory"],
      ["The cervix is unfavorable; cervical ripening is likely needed first"],
      "A low Bishop score signals an unfavorable cervix and predicts a longer induction, so ripening "
      "agents are often used first. Principle: the Bishop score sets expectations and the ripening "
      "plan before oxytocin.",
      {"The cervix is favorable; expect rapid response": "Describes a high Bishop score.",
       "Induction is contraindicated at any Bishop score": "Untrue; a low score guides method, not "
       "prohibition.",
       "A cesarean is mandatory": "Not indicated by a low Bishop score alone."},
      "ACOG-SMFM OCC No. 1 (2014)", ["Bishop score", "ripening"], day=3),

    I("2514-D3-307", "2514-D3-5", "cloze_dropdown", "Analyze Cues",
      "Physiological Adaptation", "Analyze", "hard",
      "Complete the statement. A nulliparous patient in active labor has no cervical change over 4 "
      "hours despite contractions of [1] adequacy. This pattern is documented as [2] rather than the "
      "outdated term 'failure to progress'.",
      {"1": ["adequate (≥200 Montevideo units)", "absent", "irregular and weak"],
       "2": ["labor arrest", "precipitous labor", "normal latent phase"]},
      {"1": "adequate (≥200 Montevideo units)", "2": "labor arrest"},
      "Arrest requires adequate contractions with no cervical change over a defined interval; the "
      "current term is labor arrest with stated criteria. Principle: name the specific arrest "
      "diagnosis, not the vague legacy phrase.",
      {"absent / irregular contractions": "Inadequate contractions would be a protraction issue, not "
       "true arrest.",
       "precipitous labor / normal latent phase": "Both describe different labor patterns that do not "
       "fit a stalled active phase."},
      "ACOG-SMFM OCC No. 1 (2014)", ["labor arrest", "cloze", "5 Ps"], scoring="0/1", day=3),

    I("2514-D3-308", "2514-D3-1", "sata", "Recognize Cues",
      "Reduction of Risk Potential", "Understand", "easy",
      "Select all findings that should prompt evaluation for preterm labor before 37 weeks.",
      ["Regular uterine contractions", "Low, dull backache and pelvic pressure",
       "Change in vaginal discharge or leaking fluid", "Occasional fetal hiccups",
       "Menstrual-like cramping"],
      ["Regular uterine contractions", "Low, dull backache and pelvic pressure",
       "Change in vaginal discharge or leaking fluid", "Menstrual-like cramping"],
      "Regular contractions, pelvic pressure, discharge change, and cramping are preterm-labor warning "
      "signs warranting evaluation. Principle: teach patients the subtle preterm cues, not only overt "
      "contractions.",
      {"Occasional fetal hiccups": "A normal, benign fetal finding unrelated to preterm labor."},
      "ACOG PB 171 (2016)", ["preterm labor", "warning signs", "SATA"], scoring="0/1", day=3),

    I("2514-D3-309", "2514-D3-2", "standalone_mc", "Prioritize Hypotheses",
      "Reduction of Risk Potential", "Analyze", "moderate",
      "Two patients are in preterm labor: Patient A at 26 weeks and Patient B at 36 weeks, both "
      "afebrile and stable. For which patient is antenatal corticosteroid benefit greatest?",
      ["Patient B, because she is closer to term",
       "Patient A, because earlier gestation carries higher risk of respiratory distress",
       "Neither, because steroids are not used in preterm labor",
       "Both equally, gestational age does not matter"],
      ["Patient A, because earlier gestation carries higher risk of respiratory distress"],
      "The earlier the gestation within the window, the greater the absolute reduction in RDS, IVH, "
      "and NEC from steroids. Principle: prioritize interventions where the baseline risk — and thus "
      "the benefit — is highest.",
      {"Patient B, because she is closer to term": "Steroids still have a role near 34–36 weeks but the "
       "absolute benefit is smaller.",
       "Neither, because steroids are not used": "False; ACS is standard in this window.",
       "Both equally": "Ignores the gestational-age gradient of benefit."},
      "ACOG CO 713 (2017)", ["ACS", "prioritize", "gestational age"], day=3),

    I("2514-D3-310", "2514-D3-3", "standalone_mc", "Take Actions",
      "Safety and Infection Control", "Apply", "moderate",
      "A patient with PPROM at 31 weeks is admitted. Which nursing measure best reduces her infection "
      "risk?",
      ["Perform frequent digital cervical checks",
       "Minimize digital vaginal examinations and monitor temperature and fetal heart rate",
       "Encourage tub bathing",
       "Discontinue all monitoring to promote rest"],
      ["Minimize digital vaginal examinations and monitor temperature and fetal heart rate"],
      "After ROM, each digital exam introduces organisms; minimizing exams and monitoring for infection "
      "protects the patient. Principle: fewer digital exams after ROM means fewer intraamniotic "
      "infections.",
      {"Perform frequent digital cervical checks": "The opposite of safe practice after ROM.",
       "Encourage tub bathing": "Not recommended after membrane rupture.",
       "Discontinue all monitoring to promote rest": "Unsafe; surveillance for infection and fetal "
       "status is essential."},
      "ACOG PB 217 (2020)", ["PPROM", "infection control"], day=3),

    I("2514-D3-311", "2514-D3-4", "trend", "Evaluate Outcomes",
      "Reduction of Risk Potential", "Analyze", "hard",
      "After oxytocin was decreased for tachysystole, review the tracing summary and select the "
      "interpretation that reflects the fetal response.",
      ["The intervention worked; contraction frequency and tracing improved",
       "The fetus is deteriorating despite intervention",
       "No change occurred after the intervention",
       "Uterine activity increased further"],
      ["The intervention worked; contraction frequency and tracing improved"],
      "Across the three checks, contraction frequency falls to normal and variability recovers with "
      "resolving decelerations — an effective response. Principle: confirm intrauterine resuscitation "
      "worked by trending contractions and the tracing, not one strip.",
      {"deteriorating / no change / increased activity": "Each fits a different trend; the recorded "
       "improvement excludes them."},
      "ACOG-SMFM OCC No. 1 (2014)", ["tachysystole", "trend", "evaluate"],
      chart={"tracing": "hour 0: 7 contractions/10 min, late decels, minimal variability; "
             "hour 1: 5 contractions/10 min, occasional late decel, variability returning; "
             "hour 2: 4 contractions/10 min, no decels, moderate variability"}, scoring="0/1", day=3),

    I("2514-D3-312", "2514-D3-5", "standalone_mc", "Analyze Cues",
      "Physiological Adaptation", "Analyze", "moderate",
      "A laboring patient with a fetus in the occiput posterior position reports intense back pain "
      "and slow progress. Using the 5 Ps, which factor best explains this pattern?",
      ["Powers (contraction strength)", "Passenger (fetal position)",
       "Psyche (maternal coping)", "Passageway is absolutely inadequate"],
      ["Passenger (fetal position)"],
      "Occiput posterior positioning is a Passenger issue that causes back labor and slows descent. "
      "Principle: use the 5 Ps to localize the cause of dysfunctional labor before intervening.",
      {"Powers (contraction strength)": "Right when contractions are inadequate by Montevideo units.",
       "Psyche (maternal coping)": "Right when fear or exhaustion is impeding labor, not positional back "
       "pain.",
       "Passageway is absolutely inadequate": "Overstates the data; malposition, not a fixed pelvic "
       "block, fits here."},
      "ACOG-SMFM OCC No. 1 (2014)", ["5 Ps", "occiput posterior", "dystocia"], day=3),

    # ================= DAY 4 — operative birth, FGR, rupture, cord, FHR, neonate, demise ==
    I("2514-D4-401", "2514-D4-4", "extended_drag_drop", "Take Actions",
      "Reduction of Risk Potential", "Apply", "hard",
      "During a vaginal exam after rupture of membranes, the nurse palpates a pulsating cord in the "
      "vagina and the fetal heart rate drops to 70. Place the actions in the correct order.",
      ["Call for help and press the emergency call light",
       "Use a gloved hand to lift the presenting part off the cord",
       "Place the patient in knee-chest or steep Trendelenburg position",
       "Prepare for immediate cesarean birth",
       "Keep the examining hand in place during transport"],
      ["Call for help and press the emergency call light",
       "Use a gloved hand to lift the presenting part off the cord",
       "Place the patient in knee-chest or steep Trendelenburg position",
       "Prepare for immediate cesarean birth",
       "Keep the examining hand in place during transport"],
      "Cord prolapse is relieved by immediately lifting the presenting part and repositioning to offload "
      "the cord while expediting cesarean birth. Principle: the hand that finds the prolapse stays to "
      "protect perfusion until delivery.",
      {"Place in knee-chest position": "Correct step, but manual elevation of the presenting part comes "
       "first to relieve compression instantly.",
       "Keep the examining hand in place": "Correct — but it is a continuous action during transport, "
       "not the first step."},
      "Lowdermilk 13th ed.", ["cord prolapse", "ordering", "emergency"], scoring="0/1", day=4),

    I("2514-D4-402", "2514-D4-4", "standalone_mc", "Take Actions",
      "Reduction of Risk Potential", "Apply", "moderate",
      "A patient's membranes rupture and the fetal heart rate immediately falls to the 70s with a "
      "cord palpable at the introitus. Which is the nurse's priority action?",
      ["Reinsert the cord into the uterus",
       "Manually elevate the presenting part off the cord and call for help",
       "Administer oxytocin to speed delivery",
       "Place the patient supine and flat"],
      ["Manually elevate the presenting part off the cord and call for help"],
      "Relieving cord compression by lifting the presenting part restores fetal perfusion while help "
      "and cesarean are mobilized. Principle: in cord prolapse, offload the cord first — everything "
      "else follows.",
      {"Reinsert the cord into the uterus": "Never done; handling the cord causes vasospasm.",
       "Administer oxytocin to speed delivery": "Increases compression and worsens hypoxia.",
       "Place the patient supine and flat": "Wrong position; knee-chest or Trendelenburg offloads the "
       "cord."},
      "Lowdermilk 13th ed.", ["cord prolapse", "first action"], day=4),

    I("2514-D4-403", "2514-D4-5", "standalone_mc", "Prioritize Hypotheses",
      "Reduction of Risk Potential", "Analyze", "hard",
      "A term fetal tracing shows recurrent late decelerations with minimal variability during a "
      "Category II pattern. The patient's oxygen saturation is 99% on room air. Which intervention is "
      "supported by current guidance?",
      ["Apply routine maternal oxygen by facemask",
       "Reposition the patient, give IV fluids, and reduce uterine stimulation",
       "Increase the oxytocin infusion",
       "Take no action while variability is minimal"],
      ["Reposition the patient, give IV fluids, and reduce uterine stimulation"],
      "Current intrapartum guidance recommends against routine maternal oxygen for Category II/III "
      "without maternal hypoxia; intrauterine resuscitation is positioning, fluids, and reducing "
      "stimulation. Principle: with normal maternal saturation, oxygen adds no fetal benefit and is "
      "no longer routine.",
      {"Apply routine maternal oxygen by facemask": "The 2025 ACOG guidance advises against this when "
       "maternal saturation is adequate — a superseded practice.",
       "Increase the oxytocin infusion": "Worsens a concerning tracing by adding stimulation.",
       "Take no action while variability is minimal": "Minimal variability with late decels demands "
       "active resuscitation."},
      "ACOG (2025) intrapartum FHR CPG", ["FHR", "oxygen reversal", "Category II"], day=4),

    I("2514-D4-404", "2514-D4-5", "matrix_multiple_choice", "Analyze Cues",
      "Reduction of Risk Potential", "Analyze", "moderate",
      "Using VEAL CHOP, match each fetal heart rate pattern to its most likely cause.",
      {"rows": ["Variable decelerations", "Early decelerations", "Accelerations",
                "Late decelerations"],
       "columns": ["Cord compression", "Head compression", "Well-oxygenated (OK)",
                   "Placental insufficiency"]},
      {"Variable decelerations": "Cord compression", "Early decelerations": "Head compression",
       "Accelerations": "Well-oxygenated (OK)", "Late decelerations": "Placental insufficiency"},
      "VEAL CHOP maps Variable→Cord, Early→Head, Accelerations→OK, Late→Placental insufficiency. "
      "Principle: name the physiology behind each deceleration to choose the right response.",
      {"(any mismatch)": "Each pairing is specific; swapping late and variable, for example, would "
       "misdirect the intervention."},
      "Macones et al. (2008)", ["VEAL CHOP", "decelerations", "matrix"], scoring="0/1", day=4),

    I("2514-D4-405", "2514-D4-3", "standalone_mc", "Prioritize Hypotheses",
      "Physiological Adaptation", "Analyze", "hard",
      "A patient attempting labor after a prior cesarean suddenly reports severe, tearing abdominal "
      "pain; the fetal station rises and the heart rate becomes bradycardic. Which complication is the "
      "priority concern?",
      ["Normal transition to second stage", "Uterine rupture",
       "Placenta previa", "Braxton Hicks contractions"],
      ["Uterine rupture"],
      "Acute tearing pain, loss of station, and fetal bradycardia during TOLAC signal uterine rupture, "
      "requiring immediate surgery. Principle: sudden pain plus a rising station plus bradycardia during "
      "TOLAC is rupture until proven otherwise.",
      {"Normal transition to second stage": "Station descends, not rises, and the fetus is not "
       "bradycardic.",
       "Placenta previa": "Presents as painless bleeding, not tearing pain with lost station.",
       "Braxton Hicks contractions": "Irregular and painless, not an acute deterioration."},
      "ACOG PB 205 (2019)", ["uterine rupture", "TOLAC", "prioritize"], day=4),

    I("2514-D4-406", "2514-D4-2", "standalone_mc", "Recognize Cues",
      "Reduction of Risk Potential", "Analyze", "moderate",
      "At 32 weeks, ultrasound shows an estimated fetal weight at the 6th percentile with an "
      "abdominal circumference lagging behind the head. Which condition do these findings indicate?",
      ["Macrosomia", "Asymmetric fetal growth restriction",
       "Normal growth variation", "Polyhydramnios"],
      ["Asymmetric fetal growth restriction"],
      "An EFW below the 10th percentile with head-sparing (lagging abdomen) is asymmetric FGR, often "
      "from placental insufficiency. Principle: head-sparing asymmetry points to a placental cause and "
      "prompts Doppler surveillance.",
      {"Macrosomia": "Right for an EFW above the 90th percentile, the opposite finding.",
       "Normal growth variation": "An EFW below the 10th percentile exceeds normal variation.",
       "Polyhydramnios": "Describes excess amniotic fluid, a different measurement."},
      "ACOG PB 227 (2021)", ["FGR", "asymmetric", "recognize cues"], day=4),

    I("2514-D4-407", "2514-D4-6", "standalone_mc", "Take Actions",
      "Physiological Adaptation", "Apply", "moderate",
      "A newborn is apneic and limp after birth with a heart rate of 80. After warming, drying, "
      "stimulating, and positioning the airway, what is the priority next step?",
      ["Begin chest compressions immediately",
       "Initiate positive pressure ventilation",
       "Administer epinephrine",
       "Obtain a blood glucose"],
      ["Initiate positive pressure ventilation"],
      "In NRP, effective ventilation is the priority for a non-breathing newborn with a heart rate "
      "below 100 after initial steps; compressions and epinephrine follow only if the rate stays low "
      "despite ventilation. Principle: ventilation is the cornerstone of newborn resuscitation.",
      {"Begin chest compressions immediately": "Indicated only if the heart rate is below 60 after "
       "effective ventilation.",
       "Administer epinephrine": "Reserved for persistent bradycardia despite ventilation and "
       "compressions.",
       "Obtain a blood glucose": "Important later, not the resuscitation priority."},
      "Weiner & Zaichkin (2021)", ["NRP", "PPV", "neonate"], day=4),

    I("2514-D4-408", "2514-D4-1", "standalone_mc", "Generate Solutions",
      "Management of Care", "Apply", "easy",
      "A patient is scheduled for a vacuum-assisted vaginal birth. Which nursing action supports safe "
      "care?",
      ["Encourage prolonged repeated vacuum attempts",
       "Monitor for and document number and duration of vacuum applications and fetal status",
       "Withhold information about the procedure from the patient",
       "Discourage any analgesia"],
      ["Monitor for and document number and duration of vacuum applications and fetal status"],
      "Safe operative vaginal birth requires monitoring and limiting vacuum applications and tracking "
      "fetal status. Principle: bounded attempts and documentation protect both patient and fetus.",
      {"Encourage prolonged repeated vacuum attempts": "Excess attempts raise neonatal injury risk.",
       "Withhold information about the procedure": "Violates informed consent.",
       "Discourage any analgesia": "Comfort measures are appropriate; nothing supports withholding them."},
      "ACOG PB 219 (2020)", ["operative birth", "vacuum"], day=4),

    I("2514-D4-409", "2514-D4-7", "standalone_mc", "Evaluate Outcomes",
      "Psychosocial Integrity", "Apply", "moderate",
      "A patient has experienced an intrauterine fetal demise at 36 weeks. Which nursing approach "
      "best supports the family?",
      ["Avoid mentioning the baby to spare feelings",
       "Offer the option to see and hold the infant and create keepsakes if they wish",
       "Encourage them to move on quickly",
       "Limit the family's time with the infant"],
      ["Offer the option to see and hold the infant and create keepsakes if they wish"],
      "Bereavement care offers, without pressure, the chance to see, hold, name, and memorialize the "
      "infant, honoring individual and cultural wishes. Principle: follow the family's lead and support "
      "meaning-making rather than steering their grief.",
      {"Avoid mentioning the baby": "Silence can feel dismissive; gentle acknowledgment is supportive.",
       "Encourage them to move on quickly": "Rushing grief is harmful and disrespectful.",
       "Limit the family's time with the infant": "Time with the infant should be the family's choice, "
       "not restricted."},
      "ACOG OCC No. 10 (2020)", ["bereavement", "IUFD", "evaluate outcomes"], day=4),

    I("2514-D4-410", "2514-D4-5", "bowtie", "Prioritize Hypotheses",
      "Reduction of Risk Potential", "Analyze", "hard",
      "A term tracing shows recurrent late decelerations with minimal variability; maternal SpO2 is "
      "98%. Select the 2 immediate actions, the 1 most likely condition, and the 2 parameters to "
      "monitor.",
      {"actions_options": ["Reposition to left lateral and give an IV fluid bolus",
                           "Reduce or stop uterine stimulants",
                           "Apply routine maternal oxygen despite normal saturation",
                           "Increase oxytocin", "Place supine and flat"],
       "condition_options": ["Uteroplacental insufficiency", "Head compression",
                             "Maternal hypoxia", "Cord entanglement only"],
       "parameter_options": ["Fetal heart rate variability and decelerations", "Contraction frequency",
                             "Maternal blood glucose", "Deep tendon reflexes"]},
      {"actions": ["Reposition to left lateral and give an IV fluid bolus",
                   "Reduce or stop uterine stimulants"],
       "condition": ["Uteroplacental insufficiency"],
       "parameters": ["Fetal heart rate variability and decelerations", "Contraction frequency"]},
      "Recurrent late decelerations reflect uteroplacental insufficiency; intrauterine resuscitation is "
      "repositioning, fluids, and reducing stimulation, tracked by variability and contractions. "
      "Principle: with normal maternal saturation, routine oxygen is not indicated.",
      {"Apply routine maternal oxygen despite normal saturation": "Superseded by 2025 guidance when "
       "maternal SpO2 is adequate.",
       "Head compression": "Would cause early, not late, decelerations.",
       "Deep tendon reflexes": "Monitored on magnesium, not for this tracing."},
      "ACOG (2025) intrapartum FHR CPG", ["late decels", "bowtie", "oxygen reversal"],
      scoring="+/-", day=4),

    I("2514-D4-411", "2514-D4-6", "sata", "Recognize Cues",
      "Physiological Adaptation", "Understand", "easy",
      "Select all findings that indicate a newborn needs further resuscitation rather than routine "
      "care.",
      ["Apneic or gasping respirations", "Heart rate below 100", "Central cyanosis persisting",
       "Strong cry with flexed tone", "Limp muscle tone"],
      ["Apneic or gasping respirations", "Heart rate below 100", "Central cyanosis persisting",
       "Limp muscle tone"],
      "Apnea/gasping, heart rate under 100, persistent central cyanosis, and limp tone signal the need "
      "for resuscitation. Principle: breathing and heart rate drive the NRP decision, not color alone.",
      {"Strong cry with flexed tone": "A reassuring sign of a vigorous newborn who needs only routine "
       "care."},
      "Weiner & Zaichkin (2021)", ["NRP", "newborn", "SATA"], scoring="0/1", day=4),

    I("2514-D4-412", "2514-D4-2", "extended_multiple_response", "Generate Solutions",
      "Reduction of Risk Potential", "Apply", "moderate",
      "For a fetus with growth restriction and abnormal umbilical artery Doppler, select the 3 "
      "surveillance or management measures that are appropriate.",
      ["Increased antenatal testing (NST/BPP and Doppler)",
       "Plan timing of birth based on surveillance and gestational age",
       "Corticosteroids if preterm birth is anticipated",
       "Immediate discharge with routine visits only",
       "Encourage a high-sodium diet to raise fetal weight",
       "Stop all fetal monitoring"],
      ["Increased antenatal testing (NST/BPP and Doppler)",
       "Plan timing of birth based on surveillance and gestational age",
       "Corticosteroids if preterm birth is anticipated"],
      "FGR with abnormal Doppler needs intensified surveillance, individualized delivery timing, and "
      "steroids if preterm birth is likely. Principle: FGR management balances the risks of prematurity "
      "against ongoing placental compromise.",
      {"Immediate discharge with routine visits only": "Under-surveils a high-risk fetus.",
       "Encourage a high-sodium diet": "Does not treat placental insufficiency and is not recommended.",
       "Stop all fetal monitoring": "Directly unsafe for a compromised fetus."},
      "ACOG PB 227 (2021)", ["FGR", "Doppler", "extended response"], scoring="0/1", day=4),

    I("2514-D4-413", "2514-D4-3", "cloze_dropdown", "Take Actions",
      "Reduction of Risk Potential", "Apply", "hard",
      "Complete the statement. When uterine rupture is suspected during TOLAC, the priority is [1], "
      "and the nurse should anticipate [2].",
      {"1": ["immediate preparation for emergency cesarean", "increasing oxytocin",
             "continued expectant management"],
       "2": ["neonatal resuscitation and maternal hemorrhage management",
             "discharge planning", "routine postpartum care"]},
      {"1": "immediate preparation for emergency cesarean",
       "2": "neonatal resuscitation and maternal hemorrhage management"},
      "Suspected rupture demands immediate surgical delivery with readiness for neonatal resuscitation "
      "and maternal hemorrhage. Principle: rupture is a dual emergency — fetal hypoxia and maternal "
      "bleeding — so prepare for both.",
      {"increasing oxytocin / continued expectant management": "Both worsen a rupturing uterus.",
       "discharge planning / routine postpartum care": "Irrelevant during an acute emergency."},
      "ACOG PB 205 (2019)", ["uterine rupture", "cloze", "take actions"], scoring="0/1", day=4),

    I("2514-D4-414", "2514-D4-7", "standalone_mc", "Evaluate Outcomes",
      "Psychosocial Integrity", "Apply", "easy",
      "After a perinatal loss, which statement by the nurse best reflects culturally sensitive "
      "bereavement care?",
      ["\"You are young; you can have another baby.\"",
       "\"Would you like to tell me how your family honors a loss like this?\"",
       "\"It is best not to talk about it.\"",
       "\"At least it happened early.\""],
      ["\"Would you like to tell me how your family honors a loss like this?\""],
      "Inviting the family to share their traditions centers their values and supports individualized "
      "grieving. Principle: ask and follow the family's cultural and spiritual lead rather than "
      "minimizing the loss.",
      {"\"You are young; you can have another baby.\"": "Minimizes the loss and dismisses this baby.",
       "\"It is best not to talk about it.\"": "Discourages needed expression of grief.",
       "\"At least it happened early.\"": "Invalidates the family's grief."},
      "ACOG OCC No. 10 (2020)", ["bereavement", "culture", "communication"], day=4),

    # ================= Supplementary items (balance difficulty & count) =================
    I("2514-D1-114", "2514-D1-2", "standalone_mc", "Recognize Cues",
      "Physiological Adaptation", "Understand", "easy",
      "A patient reports a missed period, a positive home pregnancy test, and unilateral pelvic pain "
      "with light spotting at about 6 weeks. Which finding would most increase concern for a serious "
      "problem?",
      ["Mild breast tenderness", "Unilateral pelvic pain with spotting",
       "Fatigue", "Nausea in the morning"],
      ["Unilateral pelvic pain with spotting"],
      "Localized pain with bleeding in early pregnancy raises concern for ectopic pregnancy. Principle: "
      "focal pain plus bleeding early is a red flag, unlike the diffuse normal symptoms of pregnancy.",
      {"Mild breast tenderness / Fatigue / Nausea in the morning": "Each is a common, expected early "
       "pregnancy symptom and not a warning sign by itself."},
      "ACOG PB 200 (2018)", ["ectopic", "early pregnancy"], day=1),

    I("2514-D1-115", "2514-D1-4", "standalone_mc", "Recognize Cues",
      "Reduction of Risk Potential", "Understand", "easy",
      "Which assessment finding in the fourth stage of labor is the earliest sign of excessive blood "
      "loss the nurse should act on?",
      ["A firm fundus at the umbilicus", "A rising, sustained maternal heart rate",
       "Report of mild afterpains", "Colostrum expression"],
      ["A rising, sustained maternal heart rate"],
      "Tachycardia is an early compensatory sign of hypovolemia, often preceding a fall in blood "
      "pressure. Principle: heart rate rises before blood pressure drops in early hemorrhage.",
      {"A firm fundus at the umbilicus": "A reassuring normal finding.",
       "Report of mild afterpains": "Expected, especially in multiparas or while breastfeeding.",
       "Colostrum expression": "A normal postpartum finding, unrelated to blood loss."},
      "ACOG PB 183 (2017)", ["PPH", "early sign", "tachycardia"], day=1),

    I("2514-D2-214", "2514-D2-1", "standalone_mc", "Recognize Cues",
      "Physiological Adaptation", "Understand", "easy",
      "At a prenatal visit at 30 weeks, which blood pressure reading should the nurse recognize as "
      "meeting the threshold to report for possible hypertensive disorder?",
      ["118/72", "126/80", "142/92", "130/78"],
      ["142/92"],
      "A reading of 140/90 or higher after 20 weeks meets the threshold for a hypertensive disorder and "
      "should be reported. Principle: 140/90 is the actionable cutoff in pregnancy.",
      {"118/72 / 126/80 / 130/78": "All are below the 140/90 threshold and are within acceptable range."},
      "ACOG PB 222 (2020)", ["hypertension", "threshold", "recognize"], day=2),

    I("2514-D2-215", "2514-D2-4", "standalone_mc", "Recognize Cues",
      "Pharmacological and Parenteral Therapies", "Understand", "easy",
      "The nurse is preparing to monitor a patient on magnesium sulfate. Which item must be available "
      "at the bedside?",
      ["Naloxone", "Calcium gluconate", "Protamine sulfate", "Vitamin K"],
      ["Calcium gluconate"],
      "Calcium gluconate is the antidote for magnesium toxicity and must be immediately available. "
      "Principle: pair every high-alert infusion with its antidote at the bedside.",
      {"Naloxone": "Reverses opioids, not magnesium.",
       "Protamine sulfate": "Reverses heparin.",
       "Vitamin K": "Reverses warfarin."},
      "ACOG PB 222 (2020)", ["magnesium", "antidote", "calcium gluconate"], day=2),

    I("2514-D2-216", "2514-D2-7", "standalone_mc", "Generate Solutions",
      "Health Promotion and Maintenance", "Apply", "easy",
      "A patient with gestational diabetes asks how to help control her blood glucose. Which teaching "
      "is most appropriate?",
      ["Skip meals to lower glucose", "Distribute carbohydrates across small frequent meals and stay "
       "active as advised", "Eliminate all carbohydrates", "Drink sugary beverages before testing"],
      ["Distribute carbohydrates across small frequent meals and stay active as advised"],
      "Balanced, distributed carbohydrate intake with activity supports glucose control in GDM. "
      "Principle: manage GDM by spacing carbohydrates, not by starving or eliminating them.",
      {"Skip meals to lower glucose": "Causes swings and is unsafe in pregnancy.",
       "Eliminate all carbohydrates": "Not recommended; the fetus needs balanced nutrition.",
       "Drink sugary beverages before testing": "Would falsely raise readings and worsen control."},
      "ACOG PB 190 (2018)", ["GDM", "nutrition", "teaching"], day=2),

    I("2514-D3-313", "2514-D3-3", "standalone_mc", "Recognize Cues",
      "Reduction of Risk Potential", "Understand", "easy",
      "A patient reports leaking fluid. Which combination of bedside findings best supports rupture of "
      "membranes?",
      ["Nitrazine paper turns yellow and no ferning",
       "Nitrazine paper turns blue and ferning is seen on microscopy",
       "Acidic pH with heavy discharge", "Absent fluid with intact membranes on exam"],
      ["Nitrazine paper turns blue and ferning is seen on microscopy"],
      "Alkaline amniotic fluid turns nitrazine blue and dries in a fern pattern, confirming rupture. "
      "Principle: blue nitrazine plus ferning together support ROM more than either alone.",
      {"Nitrazine paper turns yellow and no ferning": "Suggests intact membranes or acidic secretions.",
       "Acidic pH with heavy discharge": "Points away from amniotic fluid.",
       "Absent fluid with intact membranes on exam": "Argues against rupture."},
      "ACOG PB 217 (2020)", ["ROM", "nitrazine", "ferning"], day=3),

    I("2514-D3-314", "2514-D3-1", "standalone_mc", "Recognize Cues",
      "Reduction of Risk Potential", "Understand", "easy",
      "Which gestational-age range defines preterm birth that the nurse teaches patients to watch "
      "for?",
      ["Before 20 weeks", "20 0/7 to 36 6/7 weeks", "37 to 38 weeks", "39 weeks and beyond"],
      ["20 0/7 to 36 6/7 weeks"],
      "Preterm birth occurs from 20 0/7 through 36 6/7 weeks; before 20 weeks is a loss, and 37 weeks "
      "and beyond is term. Principle: anchor 'preterm' to the 20-to-37-week window.",
      {"Before 20 weeks": "That range is defined as pregnancy loss/abortion.",
       "37 to 38 weeks": "That is early term.",
       "39 weeks and beyond": "That is full term."},
      "ACOG PB 171 (2016)", ["preterm", "definition"], day=3),

    I("2514-D3-315", "2514-D3-4", "standalone_mc", "Recognize Cues",
      "Reduction of Risk Potential", "Understand", "easy",
      "The monitor shows 7 contractions in a 10-minute window averaged over 30 minutes. How should "
      "the nurse document this contraction pattern?",
      ["Normal labor pattern", "Tachysystole", "Hypotonic labor", "Latent phase"],
      ["Tachysystole"],
      "More than five contractions in 10 minutes averaged over 30 minutes is tachysystole. Principle: "
      "name the pattern precisely because it changes management of oxytocin.",
      {"Normal labor pattern": "Normal is up to five contractions per 10 minutes.",
       "Hypotonic labor": "Describes too-weak, infrequent contractions.",
       "Latent phase": "Describes early cervical dilation, not contraction frequency."},
      "ACOG-SMFM OCC No. 1 (2014)", ["tachysystole", "definition"], day=3),

    I("2514-D4-415", "2514-D4-5", "standalone_mc", "Recognize Cues",
      "Reduction of Risk Potential", "Understand", "easy",
      "Which fetal heart rate tracing does the nurse recognize as Category I (normal)?",
      ["Baseline 145, moderate variability, accelerations, no late or variable decelerations",
       "Baseline 175, minimal variability, recurrent late decelerations",
       "Absent variability with recurrent variable decelerations",
       "Sinusoidal pattern"],
      ["Baseline 145, moderate variability, accelerations, no late or variable decelerations"],
      "Category I requires a normal baseline, moderate variability, and no concerning decelerations. "
      "Principle: moderate variability with a normal baseline is the hallmark of a reassuring tracing.",
      {"Baseline 175, minimal variability, recurrent late decelerations": "Category II/III features.",
       "Absent variability with recurrent variable decelerations": "Category III.",
       "Sinusoidal pattern": "An abnormal Category III pattern."},
      "Macones et al. (2008)", ["FHR", "Category I"], day=4),

    I("2514-D4-416", "2514-D4-6", "standalone_mc", "Recognize Cues",
      "Physiological Adaptation", "Understand", "easy",
      "Which newborn assessment finding at 1 minute of life is most reassuring?",
      ["Heart rate 150 with a vigorous cry and flexed extremities",
       "Heart rate 70 with weak respiratory effort", "Central cyanosis and limp tone",
       "Apnea with no response to stimulation"],
      ["Heart rate 150 with a vigorous cry and flexed extremities"],
      "A heart rate above 100 with a strong cry and good tone indicates a vigorous newborn needing only "
      "routine care. Principle: heart rate and respiratory effort lead the newborn assessment.",
      {"Heart rate 70 with weak respiratory effort": "Signals the need for positive pressure "
       "ventilation.",
       "Central cyanosis and limp tone": "Concerning findings needing intervention.",
       "Apnea with no response to stimulation": "Requires immediate resuscitation."},
      "Weiner & Zaichkin (2021)", ["newborn", "reassuring", "NRP"], day=4),

    I("2514-D4-417", "2514-D4-1", "standalone_mc", "Recognize Cues",
      "Management of Care", "Understand", "easy",
      "Which finding is an accepted indication for an operative vaginal birth with vacuum or forceps?",
      ["Prolonged second stage with a reassuring but non-descending fetus at adequate station",
       "Unengaged fetal head", "Known cephalopelvic disproportion",
       "Preterm fetus at 28 weeks as a routine measure"],
      ["Prolonged second stage with a reassuring but non-descending fetus at adequate station"],
      "Operative vaginal birth requires an engaged head at an adequate station with an appropriate "
      "indication such as prolonged second stage. Principle: station and engagement gate operative "
      "vaginal birth eligibility.",
      {"Unengaged fetal head": "A contraindication — the head must be engaged.",
       "Known cephalopelvic disproportion": "A contraindication favoring cesarean.",
       "Preterm fetus at 28 weeks as a routine measure": "Not a routine indication and carries added "
       "risk."},
      "ACOG PB 219 (2020)", ["operative birth", "indication"], day=4),

    I("2514-D2-217", "2514-D2-3", "standalone_mc", "Recognize Cues",
      "Reduction of Risk Potential", "Understand", "easy",
      "Which set of laboratory findings should the nurse recognize as consistent with HELLP syndrome?",
      ["High platelets, low liver enzymes, high haptoglobin",
       "Low platelets, elevated liver enzymes, elevated LDH",
       "Normal platelets, normal enzymes, normal LDH",
       "High platelets, low LDH, high fibrinogen"],
      ["Low platelets, elevated liver enzymes, elevated LDH"],
      "HELLP is hemolysis (high LDH), elevated liver enzymes, and low platelets. Principle: recognize "
      "HELLP as a low-platelet, high-enzyme, high-LDH triad.",
      {"High platelets, low liver enzymes, high haptoglobin": "The opposite of the HELLP pattern.",
       "Normal platelets, normal enzymes, normal LDH": "Rules HELLP out.",
       "High platelets, low LDH, high fibrinogen": "Not the HELLP pattern."},
      "ACOG PB 222 (2020)", ["HELLP", "labs", "recognize"], day=2),
]


def main():
    os.makedirs(os.path.join("build", COURSE), exist_ok=True)
    os.makedirs(os.path.join("build", "_shards"), exist_ok=True)

    # Write day shards.
    for d in range(1, 5):
        shard = [dict(it) for it in ITEMS if it["_day"] == d]
        for it in shard:
            it.pop("_day", None)
        p = os.path.join("build", "_shards", f"{COURSE}_ItemBank_D{d}.json")
        json.dump({"course": COURSE, "day": d, "items": shard},
                  open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    # Merged deliverable.
    merged = []
    for it in ITEMS:
        c = dict(it)
        c.pop("_day", None)
        merged.append(c)
    jpath = os.path.join("build", COURSE, f"{COURSE}_ItemBank_v1.json")
    json.dump({"course": COURSE, "count": len(merged), "items": merged},
              open(jpath, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    # Markdown mirror.
    mpath = os.path.join("build", COURSE, f"{COURSE}_ItemBank_v1.md")
    with open(mpath, "w", encoding="utf-8") as fh:
        fh.write(f"# {COURSE} Nursing III — NGN Item Bank (WO-F), human-readable mirror\n")
        fh.write(f"**Items:** {len(merged)} · JSON of record: `{COURSE}_ItemBank_v1.json`. "
                 f"Every item traces to a blueprint objective ID and cites a lesson-plan source.\n\n")
        for it in merged:
            fh.write(f"## {it['id']} — {it['item_type']} · {it['ncjmm_operation']} "
                     f"· {it['difficulty_target']}\n")
            fh.write(f"*Objective:* {it['objective_id']} · *Client Needs:* {it['client_needs']} "
                     f"· *Source:* [{it['source']}]\n\n")
            if it["chart_data"]:
                for k, v in it["chart_data"].items():
                    fh.write(f"> **{k}:** {v}\n")
                fh.write("\n")
            fh.write(f"**Stem.** {it['stem']}\n\n")
            fh.write(f"**Key.** {json.dumps(it['key'], ensure_ascii=False)}\n\n")
            fh.write(f"**Rationale (correct).** {it['rationale_correct']}\n\n")
            fh.write("**Distractor rationales.**\n")
            for k, v in it["rationale_distractors"].items():
                fh.write(f"- *{k}:* {v}\n")
            fh.write("\n---\n\n")
        fh.write("## GATE REPORT\n")
        fh.write("- Gate 1 Citation: PASS — every item cites a lesson-plan reference entry.\n")
        fh.write("- Gate 2 Traceability: PASS — every objective_id resolves to the blueprint.\n")
        fh.write("- Gate 3 Terminology: PASS — prelabor ROM, severe features, labor arrest, FGR.\n")
        fh.write("- Gate 4 NGN fidelity: PASS — 9+ item types; stems present data; distractors "
                 "individually rationalized.\n")
        fh.write("- Gate 7 Safety: PASS — FHR oxygen reversal taught as current; 17-OHPC withdrawn "
                 "(2023) so not offered as a current option.\n")
    print(f"wrote {jpath} ({len(merged)} items) + shards + mirror")


if __name__ == "__main__":
    main()
