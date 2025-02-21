

IRRELEVANT_CONTEXT_PROMPTS = """https://t.co/DlI9kw"""

TYPO_PROMPTS = """
**General Task Description**
You are given the following information:
1. Sentences to add typos: <INPUT>.
2. Reference examples: <EXAMPLE_LIST>.
   - Each example has two parts: [BEFORE MODIFICATION] (the original sentence) and [AFTER MODIFICATION] (the modified sentence with added typos).

**Definition of Typos**
A “typo” is a typographical error that typically involves:
- **Misspelled Characters**: Substituting one letter with a similar-looking character (e.g., "foolish" → "fo0lish").
- **Omitted Characters**: Unintentionally leaving out letters (e.g., "writing" → "writng").
- **Extra Characters**: Accidentally adding letters or symbols (e.g., "typing" → "typping").
- **Swapped Characters**: Reversing the order of letters (e.g., "word" → "wrod").

**Task Instructions**
1. Task Descriptions
   - This task is about **Inserting Typos**. For each sentence in <INPUT>, add a few typos based on the length of each sentence.

2. Prohibited Changes
   - Do not alter numbers, names, scientific/mathematical terms, or other crucial information.
   - Do not introduce typos that would significantly change the sentence's meaning or create ambiguity.
   - Do not introduce any changes in word order or content. You should keep the overall syntactic structure and meaning intact.
   
3. Degree of Modification
   - In this task, assume **Minimal Modification**:
      - Minimal Modification: For shorter sentences, add 1-2 typos per sentence. For longer sentences, add 3 typos per sentence.  
      - Medium Modification: For shorter sentences, add 4-5 typos per sentence. For longer sentences, add 6 typos per sentence.  
      - Maximum Modification: Almost every word should contain a typo, excluding common words.
   
**Reference Examples (<EXAMPLE_LIST>)** 
1. [BEFORE MODIFICATION]: This was a huge influx as the entire population of the False! True Dutch Republic amounted to ca.  
   [AFTER MODIFICATION]: This was a hge influx as the entire populatoin of the False! True Dutch Repblic amounted to ca.
2. [BEFORE MODIFICATION]: It captures a wonderful kind of laziness to waste the talents of robert forster, anne mera, eugene levy, and reginald veljohnson all in the same magic.  
   [AFTER MODIFICATION]: It captures a woderful kind of laziness to waaste the talents of robert forster, anne mera, eugene levy, and reginald veljonson all in the same magic.
3. [BEFORE MODIFICATION]: In Hong Kong you can have a plate, or even a whole dinner service, hand-painted to your own design.  
   [AFTER MODIFICATION]: In Hong Kong you can have a pltae, or even a wh01e dinner service, hand-paitned to your own design.

**Input to Modify**
<INPUT>: {INPUT}

**Start Modifying**
Please refer to the <EXAMPLE_LIST> format and begin your task now! Your response should be formatted in JSON format with the key name of "OUTPUT" (i.e., {{"OUTPUT": modified sentences}}).
Do not generate explanations and other content! Only output the {{"OUTPUT": modified sentences}} in JSON format!
"""


SYNTACTIC_PROMPTS = """
**General Task Description**
You are given the following information:
1. Sentences to paraphrase: <INPUT>.
2. Reference examples: <EXAMPLE_LIST>.
   - Each example has two parts: [BEFORE PARAPHRASE] (the original sentence) and [AFTER PARAPHRASE] (the paraphrased sentence).

**Task Instructions**
1. Task Descriptions
   - This task is about *Changing Syntactic Structure*. For each sentence in <INPUT>, reorganize or restructure it while keeping all the original words and meaning.
   - You are allowed to reorder phrases, switch between active/passive voice, split or merge clauses.
   
2. Prohibited Changes
   - Do not alter numbers, names, scientific/mathematical terms, or other crucial information.
   - Do not remove or replace any words with synonyms or alternative terms.
   - Do not modify or eliminate fixed expressions in the original sentences. The meaning and vocabulary must remain exactly the same.

**Reference Examples (<EXAMPLE_LIST>)** 
1. [BEFORE PARAPHRASE]: We are embracing the open-source ethos of releasing early and often to enable the community to get access to these models while they are still in development.
   [AFTER PARAPHRASE]: To enable the community to get access to these models while they are still in development, we are embracing the open-source ethos of releasing early and often.
2. [BEFORE PARAPHRASE]: It captures a wonderful kind of laziness to waste the talents of robert forster, anne meara, eugene levy, and reginald veljohnson all in the same magic.
   [AFTER PARAPHRASE]: To waste the talents of robert forster, anne meara, eugene levy, and reginald veljohnson all in the same magic captures a wonderful kind of laziness.
3. [BEFORE PARAPHRASE]: Deep curiosity about their field of study defines a successful Ph.D. student.
   [AFTER PARAPHRASE]: Deep curiosity about their field of study is what defines a successful Ph.D. student.

**Input to Paraphrase**
<INPUT>: {INPUT}

**Start Paraphrasing**
Please refer to the <EXAMPLE_LIST> format and begin your task now! Your response should be formatted in JSON format with the key name of "OUTPUT" (i.e., {{"OUTPUT": paraphrased sentences}}).
Do not generate explanations and other content! Only output the {{"OUTPUT": paraphrased sentences}} in JSON format!
"""


SYNONYMS_PROMPTS = """
**General Task Description**
You are given the following information:
1. Sentences to paraphrase: <INPUT>.
2. Reference examples: <EXAMPLE_LIST>.
   - Each example has two parts: [BEFORE PARAPHRASE] (the original sentence) and [AFTER PARAPHRASE] (the paraphrased sentence).

**Task Instructions**
1. Task Descriptions
   - This task is about **Replacing Words or Phrases**. For each sentence in <INPUT>, replace certain words or expressions with synonyms or alternative phrases while maintaining the original syntactic structure.

2. Prohibited Changes
   - Do not alter numbers, names, scientific/mathematical terms, or other crucial information.
   - Do not rearrange original sentence structure (no switching word order, voice, or clause types).

3. Degree of Modification
   - In this task, assume **Minimal Modification**:
      - Minimal Modification: For short sentences, replace 1-2 words/phrases; For long sentences, replace 3 words/phrases.
      - Medium Modification: For short sentences, replace 4-5 words/phrases; For long sentences, replace 6 words/phrases.
      - Maximum Modification: Almost every word/phrase should be replaced.

**Reference Examples (<EXAMPLE_LIST>)**
1. [BEFORE PARAPHRASE]: We are embracing the open source ethos of releasing early and often to enable the community to get access to these models while they are still in development.  
   [AFTER PARAPHRASE]: We are adopting the open source ethos of releasing early and frequently to allow the community to get access to these models while they are still in development.
2. [BEFORE PARAPHRASE]: It captures a wonderful kind of laziness to waste the talents of robert forster, anne meara, eugene levy, and reginald veljohnson all in the same magic.  
   [AFTER PARAPHRASE]: It reflects a peculiar kind of laziness to squander the talents of robert forster, anne meara, eugene levy, and reginald veljohnson all in the same magic.  
3. [BEFORE PARAPHRASE]: A successful Ph.D. student is deeply curious about their field of study.  
   [AFTER PARAPHRASE]: A dedicated Ph.D. student is deeply interested in their research field.

**Input to Paraphrase**
<INPUT>: {INPUT}

**Start Paraphrasing**
Please refer to the <EXAMPLE_LIST> format and begin your task now! Your response should be formatted in JSON format with the key name of "OUTPUT" (i.e., {{"OUTPUT": paraphrased sentences}}).
Do not generate explanations and other content! Only output the {{"OUTPUT": paraphrased sentences}} in JSON format!
"""

RELEVANT_CONTEXT_PROMPTS = """
**General Task Description**
You are given the following information:
1. Sentences to paraphrase: <INPUT>.
2. Reference examples: <EXAMPLE_LIST>.
   - Each example contains [BEFORE MODIFICATION] (the original sentence) and [AFTER MODIFICATION] (the sentence introduced by a newly created relevant scenario).

**Task Instructions**
1. Task Descriptions
   - This task is about **Creating a Relevant Scenario that Introduces the <INPUT>**. Here are detailed steps about how to write the scenario:
      - Write **two to three sentences** that set a meaningful, realistic, or imaginative context directly related to <INPUT>.
      - Ensure these scenario sentences create engagement through storytelling or by setting a scene.
      - Place these sentences **ahead of the <INPUT>** as an introduction.

2. Prohibited Changes:
   - Do not change or modify the content of <INPUT>.
   - Do not alter numbers, names, scientific/mathematical terms, or other crucial information.
   - Do not provide any background that explains concepts or includes prior information logically.

**Reference Examples (<EXAMPLE_LIST>)**
1. [BEFORE MODIFICATION]: An astronomer observes that a planet rotates faster after a meteorite impact. Which is the most likely effect of this increase in rotation?
   [AFTER MODIFICATION]: In a distant solar system, a massive meteorite strikes a planet, leaving a noticeable effect on its rotational speed. The collision seems to alter the planet's natural rhythms. An astronomer observes that a planet rotates faster after a meteorite impact. Which is the most likely effect of this increase in rotation?
2. [BEFORE MODIFICATION]: Is the following sentence plausible? "Mike Hoffman launched the half court shot in the Western Conference Finals."
   [AFTER MODIFICATION]: The crowd roared as the Western Conference Finals reached its climax. Mike Hoffman, known for his calm under pressure, stepped onto the court, his eyes focused on the basket from half court. Is the following sentence plausible? "Mike Hoffman launched the half court shot in the Western Conference Finals."
3. [BEFORE MODIFICATION]: Claire makes a 3 egg omelet every morning for breakfast. How many dozens of eggs will she eat in 4 weeks?
   [AFTER MODIFICATION]: Every morning, Claire starts her day in the kitchen, whisking eggs to make her signature 3-egg omelet. She never misses this routine, ensuring her breakfast is both hearty and consistent. Claire makes a 3 egg omelet every morning for breakfast. How many dozens of eggs will she eat in 4 weeks?

**Input to Modify**
<INPUT>: {INPUT}

**Start Modifying**
Please first refer to <EXAMPLE_LIST> and start your task! Your response should be formatted in JSON format with the key name of "OUTPUT" (i.e., {{"OUTPUT": modified sentences}}).
Do not generate explanations and other content! Only output the {{"OUTPUT": modified sentences}} in JSON format!
"""


TRANSLATION_PROMPTS = """
**General Task Description**
You are provided with the following information:
1. Questions to translate: <QUESTION>.
2. Choices to translate: <CHOICES>.
3. Reference examples: <EXAMPLE_LIST>.
   - Each example provides two parts: [BEFORE TRANSLATION] (the original sentence before translation) and [AFTER TRANSLATION] (the sentence translated into Chinese).

**Task Instructions**
1. Task Descriptions
   - This task is about **Translating the <QUESTION> and <CHOICES> into Chinese**. Ensure the translation accurately preserves the original semantic meaning and reflects the intent of the source content without introducing errors or altering the intended meaning.

2. Prohibited Changes
   - Do not alter numbers, names, scientific/mathematical terms, or other crucial information in <QUESTION> or <CHOICES>.
   - Do not add or remove information from the original text.

**Reference Examples (<EXAMPLE_LIST>)** 
1. [BEFORE TRANSLATION]: Suppose you live on the Moon.  How long is a day (i.e. from sunrise to sunrise)? Options: ["about 18 years", "24 hours", "29 Earth days", "a year"]
   [AFTER TRANSLATION]: 假设你住在月球上。一天（即从日出到日出）有多长？ 选项: ["大概18年", "24小时", "29个地球日", "一年"]
2. [BEFORE TRANSLATION]: The morning temperature in a city is 41°F. If a sunny, mild day is forecast, which temperature is most likely for 2:00 p.m.? Options: ["32° F", "41° F", "78° F", "98° F"]
   [AFTER TRANSLATION]: 一个城市早晨的温度是41°F。如果天气预报是晴朗温和的一天,那么下午2点最可能是什么温度? 选项: ["32° F", "41° F", "78° F", "98° F"]
3. [BEFORE TRANSLATION]: Statement 1 | A factor group of a non-Abelian group is non-Abelian. Statement 2 | If K is a normal subgroup of H and H is a normal subgroup of G, then K is a normal subgroup of G. Options: [ "True, True", "False, False", "True, False", "False, True" ]
   [AFTER TRANSLATION]: 表述1|非阿贝尔群的因子群是非阿贝尔的。表述2|若K是H的正规子群,H是G的正规子群,则K是G的正规子群。 选项: ["真,真","假,假","真,假","假,真"]

**Input to Translate**  
<QUESTION>: {QUESTION}
<CHOICES>: {CHOICES}

**Start Translating**
Please first refer to <EXAMPLE_LIST> and start your task! Your response should be formatted in JSON format with the key name of "OUTPUT_QUESTION" and "OUTPUT_CHOICES" (i.e., {{"OUTPUT_QUESTION": translated questions, "OUTPUT_CHOICES": translated choices}}).
Do not generate explanations and other content! Only output the {{"OUTPUT_QUESTION": translated questions, "OUTPUT_CHOICES": translated choices}} in JSON format! Each translated choice should be enclosed in quotation marks.
"""

TRANSLATION_FRENCH_PROMPTS = """
**General Task Description**
You are provided with the following information:
1. Questions to translate: <QUESTION>.
2. Choices to translate: <CHOICES>.
3. Reference examples: <EXAMPLE_LIST>.
   - Each example provides two parts: [BEFORE TRANSLATION] (the original sentence before translation) and [AFTER TRANSLATION] (the sentence translated into French).

**Task Instructions**
1. Task Descriptions
   - This task is about **Translating the <QUESTION> and <CHOICES> into French**. Ensure the translation accurately preserves the original semantic meaning and reflects the intent of the source content without introducing errors or altering the intended meaning.

2. Prohibited Changes
   - Do not alter numbers, names, scientific/mathematical terms, or other crucial information in <QUESTION> or <CHOICES>.
   - Do not add or remove information from the original text.

**Reference Examples (<EXAMPLE_LIST>)** 
1. [BEFORE TRANSLATION]: Suppose you live on the Moon.  How long is a day (i.e. from sunrise to sunrise)? Options: ["about 18 years", "24 hours", "29 Earth days", "a year"]
   [AFTER TRANSLATION]: Supposons que vous viviez sur la Lune. Quelle est la durée d'une journée (c'est-à-dire du lever du soleil au lever du soleil)? Options: ["environ 18 ans", "24 heures", "29 jours terrestres", "un an"]
2. [BEFORE TRANSLATION]: The morning temperature in a city is 41°F. If a sunny, mild day is forecast, which temperature is most likely for 2:00 p.m.? Options: ["32°F", "41°F", "78°F", "98°F"]
   [AFTER TRANSLATION]: La température matinale dans une ville est de 41°F. Si une journée ensoleillée et douce est prévue, quelle température est la plus probable à 14h00 ? Options: ["32°F", "41°F", "78°F", "98°F"]
3. [BEFORE TRANSLATION]: Statement 1 | A factor group of a non-Abelian group is non-Abelian. Statement 2 | If K is a normal subgroup of H and H is a normal subgroup of G, then K is a normal subgroup of G. Options: [ "True, True", "False, False", "True, False", "False, True" ]
   [AFTER TRANSLATION]: Énoncé 1 | Un groupe de facteurs d'un groupe non abélien est non abélien. Énoncé 2 | Si K est un sous-groupe normal de H et H est un sous-groupe normal de G, alors K est un sous-groupe normal de G. Options: ["Vrai, Vrai", "Faux, Faux", "Vrai, Faux", "Faux, Vrai"]

**Input to Translate**
<QUESTION>: {QUESTION}
<CHOICES>: {CHOICES}

**Start Translating**
Please first refer to <EXAMPLE_LIST> and start your task! Your response should be formatted in JSON format with the key name of "OUTPUT_QUESTION" and "OUTPUT_CHOICES" (i.e., {{"OUTPUT_QUESTION": translated questions, "OUTPUT_CHOICES": translated choices}}).
Do not generate explanations and other content! Only output the {{"OUTPUT_QUESTION": translated questions, "OUTPUT_CHOICES": translated choices}} in JSON format! Each translated choice should be enclosed in quotation marks.
"""

TRANSLATION_WITHOUT_EXAMPLE_PROMPTS = """
**General Task Description**
You are provided with the following information:
1. Questions to translate: <QUESTION>.
2. Choices to translate: <CHOICES>.

**Task Instructions**
1. Task Descriptions
   - This task is about **Translating the <QUESTION> and <CHOICES> into Chinese**. Ensure the translation accurately preserves the original semantic meaning and reflects the intent of the source content without introducing errors or altering the intended meaning.

2. Prohibited Changes
   - Do not alter numbers, names, scientific/mathematical terms, or other crucial information in <QUESTION> or <CHOICES>.
   - Do not add or remove information from the original text.
   
**Input to Translate**  
<QUESTION>: {QUESTION}
<CHOICES>: {CHOICES}

**Start Translating**
Please start your task! Your response should be formatted in JSON format with the key name of "OUTPUT_QUESTION" and "OUTPUT_CHOICES" (i.e., {{"OUTPUT_QUESTION": translated questions, "OUTPUT_CHOICES": translated choices}}).
Do not generate explanations and other content! Only output the {{"OUTPUT_QUESTION": translated questions, "OUTPUT_CHOICES": translated choices}} in JSON format! Each translated choice should be enclosed in quotation marks.
"""

TRANSLATION_MATH_PROMPTS = """
**General Task Description**
You are provided with the following information:
1. Question to translate: <INPUT>.
2. Reference examples: <EXAMPLE_LIST>.
   - Each example provides two parts: [BEFORE TRANSLATION] (the original sentence before translation) and [AFTER TRANSLATION] (the sentence translated into Chinese).

**Task Instructions**
1. Task Descriptions
   - This task is about **Translating the <INPUT> into Chinese**. Ensure the translation accurately preserves the original semantic meaning and reflects the intent of the source content without introducing errors or altering the intended meaning.

2. Prohibited Changes
   - Do not alter numbers, names, scientific/mathematical terms, or other crucial information in <INPUT>.
   - Do not translate numbers. Keep them in the Arabic form.
   - Do not add or remove information from the original text.

**Reference Examples (<EXAMPLE_LIST>)** 
1. [BEFORE TRANSLATION]: Here comes a perfectly valid argument: First of all, whoever is a schoolmate of Sondra is not a stepsister of Pricilla. In consequence, whoever is not a stepsister of Pricilla is a schoolmate of Sondra." Is the argument, given the explicitly stated premises, deductively valid or invalid?
   [AFTER TRANSLATION]: 这里有一个完全合理的论点：首先，桑德拉的校友都不是普里西拉的继姐妹。因此，凡是不是普里西拉的继姐妹的人，都是桑德拉的校友。在明确陈述的前提下，这个论点在演绎逻辑上是有效还是无效的
2. [BEFORE TRANSLATION]: The morning temperature in a city is 41°F. If a sunny, mild day is forecast, which temperature is most likely for 2:00 p.m.? 
   [AFTER TRANSLATION]: 一个城市早晨的温度是41°F。如果天气预报是晴朗温和的一天,那么下午2点最可能是什么温度?
3. [BEFORE TRANSLATION]: I have a flute, a piano, a trombone, four stoves, a violin, an accordion, a clarinet, a drum, two lamps, and a trumpet.
   [AFTER TRANSLATION]: 我有1支长笛、1架钢琴、1把长号、4个炉子、1把小提琴、1台手风琴、1支单簧管、1面鼓、2盏灯和1把小号。

**Input to Translate**
<INPUT>: {INPUT}

**Start Translating**
Please first refer to <EXAMPLE_LIST> and start your task! Your response should be formatted in JSON format with the key name of "OUTPUT" (i.e., {{"OUTPUT": translated input}}).
Do not generate explanations and other content! Only output the {{"OUTPUT": translated input}} in JSON format!
"""

TRANSLATION_FRENCH_MATH_PROMPTS = """
**General Task Description**
You are provided with the following information:
1. Question to translate: <INPUT>.
2. Reference examples: <EXAMPLE_LIST>.
   - Each example provides two parts: [BEFORE TRANSLATION] (the original sentence before translation) and [AFTER TRANSLATION] (the sentence translated into French).

**Task Instructions**
1. Task Descriptions
   - This task is about **Translating the <INPUT> into French**. Ensure the translation accurately preserves the original semantic meaning and reflects the intent of the source content without introducing errors or altering the intended meaning.

2. Prohibited Changes
   - Do not alter numbers, names, scientific/mathematical terms, or other crucial information in <INPUT>.
   - Do not translate numbers. Keep them in the Arabic form.
   - Do not add or remove information from the original text.

**Reference Examples (<EXAMPLE_LIST>)** 
1. [BEFORE TRANSLATION]: Here comes a perfectly valid argument: First of all, whoever is a schoolmate of Sondra is not a stepsister of Pricilla. In consequence, whoever is not a stepsister of Pricilla is a schoolmate of Sondra." Is the argument, given the explicitly stated premises, deductively valid or invalid?
   [AFTER TRANSLATION]: Voici un argument parfaitement valable : tout d'abord, quiconque est un camarade de classe de Sondra n'est pas une demi-sœur de Pricilla. En conséquence, quiconque n'est pas une demi-sœur de Pricilla est un camarade de classe de Sondra. » L'argument, compte tenu des prémisses explicitement énoncées, est-il déductivement valable ou invalide ?
2. [BEFORE TRANSLATION]: The morning temperature in a city is 41°F. If a sunny, mild day is forecast, which temperature is most likely for 2:00 p.m.? 
   [AFTER TRANSLATION]: La température matinale dans une ville est de 41°F. Si une journée ensoleillée et douce est prévue, quelle température est la plus probable à 14h00?
3. [BEFORE TRANSLATION]: I have a flute, a piano, a trombone, four stoves, a violin, an accordion, a clarinet, a drum, two lamps, and a trumpet.
   [AFTER TRANSLATION]: J'ai 1 flûte,1 piano, 1 trombone, 4 poêles, 1 violon, 1 accordéon, 1 clarinette, 1 tambour, 2 lampes et 1 trompette.

**Input to Translate**
<INPUT>: {INPUT}

**Start Translating**
Please first refer to <EXAMPLE_LIST> and start your task! Your response should be formatted in JSON format with the key name of "OUTPUT" (i.e., {{"OUTPUT": translated input}}).
Do not generate explanations and other content! Only output the {{"OUTPUT": translated input}} in JSON format!
"""

TRANSLATION_BBH_PROMPTS = """
**General Task Description**
You are provided with the following information:
1. Question to translate: <INPUT>.
2. Answer to translate: <ANSWER>.
3. Reference examples: <EXAMPLE_LIST>.
   - Each example provides two parts: [BEFORE TRANSLATION] (the original sentence before translation) and [AFTER TRANSLATION] (the sentence translated into Chinese).

**Task Instructions**
1. Task Descriptions
   - This task is about **Translating the <INPUT> into Chinese**. Ensure the translation accurately preserves the original semantic meaning and reflects the intent of the source content without introducing errors or altering the intended meaning.

2. Prohibited Changes
   - Do not alter numbers, names, scientific/mathematical terms, or other crucial information in <INPUT>.
   - Do not translate numbers. Keep them in the Arabic form.
   - Do not add or remove information from the original text.

**Reference Examples (<EXAMPLE_LIST>)** 
1. [BEFORE TRANSLATION]: Here comes a perfectly valid argument: First of all, whoever is a schoolmate of Sondra is not a stepsister of Pricilla. In consequence, whoever is not a stepsister of Pricilla is a schoolmate of Sondra." Is the argument, given the explicitly stated premises, deductively valid or invalid?
   [AFTER TRANSLATION]: 这里有一个完全合理的论点：首先，桑德拉的校友都不是普里西拉的继姐妹。因此，凡是不是普里西拉的继姐妹的人，都是桑德拉的校友。在明确陈述的前提下，这个论点在演绎逻辑上是有效还是无效的
2. [BEFORE TRANSLATION]: The morning temperature in a city is 41°F. If a sunny, mild day is forecast, which temperature is most likely for 2:00 p.m.? 
   [AFTER TRANSLATION]: 一个城市早晨的温度是41°F。如果天气预报是晴朗温和的一天,那么下午2点最可能是什么温度?
3. [BEFORE TRANSLATION]: I have a flute, a piano, a trombone, four stoves, a violin, an accordion, a clarinet, a drum, two lamps, and a trumpet.
   [AFTER TRANSLATION]: 我有1支长笛、1架钢琴、1把长号、4个炉子、1把小提琴、1台手风琴、1支单簧管、1面鼓、2盏灯和1把小号。

**Input to Translate**
<INPUT>: {INPUT}
<ANSWER>: {ANSWER}

**Start Translating**
Please first refer to <EXAMPLE_LIST> and start your task! Your response should be formatted in JSON format with the key name of "OUTPUT_QUESTION" and "OUTPUT_ANSWER" (i.e., {{"OUTPUT_QUESTION": translated input, "OUTPUT_ANSWER": translated answer}}).
Do not generate explanations and other content! Only output the {{"OUTPUT_QUESTION": translated input, "OUTPUT_ANSWER": translated answer}} in JSON format!
"""

TRANSLATION_FRENCH_BBH_PROMPTS = """
**General Task Description**
You are provided with the following information:
1. Question to translate: <INPUT>.
2. Answer to translate: <ANSWER>.
3. Reference examples: <EXAMPLE_LIST>.
   - Each example provides two parts: [BEFORE TRANSLATION] (the original sentence before translation) and [AFTER TRANSLATION] (the sentence translated into French).

**Task Instructions**
1. Task Descriptions
   - This task is about **Translating the <INPUT> into French**. Ensure the translation accurately preserves the original semantic meaning and reflects the intent of the source content without introducing errors or altering the intended meaning.

2. Prohibited Changes
   - Do not alter numbers, names, scientific/mathematical terms, or other crucial information in <INPUT>.
   - Do not translate numbers. Keep them in the Arabic form.
   - Do not add or remove information from the original text.

**Reference Examples (<EXAMPLE_LIST>)** 
1. [BEFORE TRANSLATION]: Here comes a perfectly valid argument: First of all, whoever is a schoolmate of Sondra is not a stepsister of Pricilla. In consequence, whoever is not a stepsister of Pricilla is a schoolmate of Sondra." Is the argument, given the explicitly stated premises, deductively valid or invalid?
   [AFTER TRANSLATION]: Voici un argument parfaitement valable : tout d'abord, quiconque est un camarade de classe de Sondra n'est pas une demi-sœur de Pricilla. En conséquence, quiconque n'est pas une demi-sœur de Pricilla est un camarade de classe de Sondra. » L'argument, compte tenu des prémisses explicitement énoncées, est-il déductivement valable ou invalide ?
2. [BEFORE TRANSLATION]: The morning temperature in a city is 41°F. If a sunny, mild day is forecast, which temperature is most likely for 2:00 p.m.? 
   [AFTER TRANSLATION]: La température matinale dans une ville est de 41°F. Si une journée ensoleillée et douce est prévue, quelle température est la plus probable à 14h00?
3. [BEFORE TRANSLATION]: I have a flute, a piano, a trombone, four stoves, a violin, an accordion, a clarinet, a drum, two lamps, and a trumpet.
   [AFTER TRANSLATION]: J'ai 1 flûte,1 piano, 1 trombone, 4 poêles, 1 violon, 1 accordéon, 1 clarinette, 1 tambour, 2 lampes et 1 trompette.

**Input to Translate**
<INPUT>: {INPUT}
<ANSWER>: {ANSWER}

**Start Translating**
Please first refer to <EXAMPLE_LIST> and start your task! Your response should be formatted in JSON format with the key name of "OUTPUT_QUESTION" and "OUTPUT_ANSWER" (i.e., {{"OUTPUT_QUESTION": translated input, "OUTPUT_ANSWER": translated answer}}).
Do not generate explanations and other content! Only output the {{"OUTPUT_QUESTION": translated input, "OUTPUT_ANSWER": translated answer}} in JSON format!
"""

BACK_TRANSLATION_BBH_PROMPTS = """
**General Task Description**
You are provided with the following information:
1. Questions to translate: <QUESTION>.
2. Reference examples: <EXAMPLE_LIST>.
   - Each example provides two parts: [BEFORE TRANSLATION] (the original sentence before translation) and [AFTER TRANSLATION] (the sentence translated into English).

**Task Instructions**
1. Task Descriptions
   - This task is about **Translating the <QUESTION> into English**. Ensure the translation accurately preserves the original semantic meaning and reflects the intent of the source content without introducing errors or altering the intended meaning.

2. Prohibited Changes
   - Do not alter numbers, names, scientific/mathematical terms, or other crucial information in <QUESTION>.
   - Do not add or remove information from the original text.
   - Do not translate numbers. Keep them in the Arabic form.

**Reference Examples (<EXAMPLE_LIST>)**
1. [BEFORE TRANSLATION]: 假设你住在月球上。一天（即从日出到日出）有多长？
   [AFTER TRANSLATION]: Suppose you live on the Moon.  How long is a day (i.e. from sunrise to sunrise)?
2. [BEFORE TRANSLATION]: 一个城市早晨的温度是41°F。如果天气预报是晴朗温和的一天,那么下午2点最可能是什么温度?
   [AFTER TRANSLATION]: The morning temperature in a city is 41°F. If a sunny, mild day is forecast, which temperature is most likely for 2:00 p.m.?
3. [BEFORE TRANSLATION]: 表述1|非阿贝尔群的因子群是非阿贝尔的。表述2|若K是H的正规子群,H是G的正规子群,则K是G的正规子群。
   [AFTER TRANSLATION]: Statement 1 | A factor group of a non-Abelian group is non-Abelian. Statement 2 | If K is a normal subgroup of H and H is a normal subgroup of G, then K is a normal subgroup of G.

**Input to Translate**
<QUESTION>: {QUESTION}

**Start Translating**
Please first refer to <EXAMPLE_LIST> and start your task! Your response should be formatted in JSON format with the key name of "OUTPUT" (i.e., {{"OUTPUT": translated questions}}).
Do not generate explanations and other content! Only output the {{"OUTPUT": translated questions}} in JSON format!
"""

BACK_TRANSLATION_REPLIQA_PROMPTS = """
**General Task Description**
You are provided with the following information:
1. Questions to translate: <QUESTION>.
2. Answer to translate: <QUESTION>.
3. Reference examples: <EXAMPLE_LIST>.
   - Each example provides two parts: [BEFORE TRANSLATION] (the original sentence before translation) and [AFTER TRANSLATION] (the sentence translated into English).

**Task Instructions**
1. Task Descriptions
   - This task is about **Translating the <QUESTION> into English**. Ensure the translation accurately preserves the original semantic meaning and reflects the intent of the source content without introducing errors or altering the intended meaning.

2. Prohibited Changes
   - Do not alter numbers, names, scientific/mathematical terms, or other crucial information in <QUESTION>.
   - Do not add or remove information from the original text.
   - Do not translate numbers. Keep them in the Arabic form.

**Reference Examples (<EXAMPLE_LIST>)**
1. [BEFORE TRANSLATION]: 假设你住在月球上。一天（即从日出到日出）有多长？
   [AFTER TRANSLATION]: Suppose you live on the Moon.  How long is a day (i.e. from sunrise to sunrise)?
2. [BEFORE TRANSLATION]: 一个城市早晨的温度是41°F。如果天气预报是晴朗温和的一天,那么下午2点最可能是什么温度?
   [AFTER TRANSLATION]: The morning temperature in a city is 41°F. If a sunny, mild day is forecast, which temperature is most likely for 2:00 p.m.?
3. [BEFORE TRANSLATION]: 表述1|非阿贝尔群的因子群是非阿贝尔的。表述2|若K是H的正规子群,H是G的正规子群,则K是G的正规子群。
   [AFTER TRANSLATION]: Statement 1 | A factor group of a non-Abelian group is non-Abelian. Statement 2 | If K is a normal subgroup of H and H is a normal subgroup of G, then K is a normal subgroup of G.

**Input to Translate**
<QUESTION>: {QUESTION}
<ANSWER>: {ANSWER}

**Start Translating**
Please first refer to <EXAMPLE_LIST> and start your task! Your response should be formatted in JSON format with the key name of "OUTPUT_QUESTION" and "OUTPUT_ANSWER" (i.e., {{"OUTPUT_QUESTION": translated input, "OUTPUT_ANSWER": translated answer}}).
Do not generate explanations and other content! Only output the {{"OUTPUT_QUESTION": translated input, "OUTPUT_ANSWER": translated answer}} in JSON format!
"""

BACK_TRANSLATION_PROMPTS = """
**General Task Description**
You are provided with the following information:
1. Questions to translate: <QUESTION>.
2. Choices to translate: <CHOICES>.

**Task Instructions**
1. Task Descriptions
   - This task is about **Translating the <QUESTION> and <CHOICES> into English**. Ensure the translation accurately preserves the original semantic meaning and reflects the intent of the source content without introducing errors or altering the intended meaning.

2. Prohibited Changes
   - Do not alter numbers, names, scientific/mathematical terms, or other crucial information in <QUESTION> or <CHOICES>.
   - Do not add or remove information from the original text.

**Reference Examples (<EXAMPLE_LIST>)** 
1. [BEFORE TRANSLATION]: 假设你住在月球上。一天（即从日出到日出）有多长？ 选项: ["大概18年", "24小时", "29个地球日", "一年"]
   [AFTER TRANSLATION]: Suppose you live on the Moon.  How long is a day (i.e. from sunrise to sunrise)? Options: ["about 18 years", "24 hours", "29 Earth days", "a year"]
2. [BEFORE TRANSLATION]: 一个城市早晨的温度是41°F。如果天气预报是晴朗温和的一天,那么下午2点最可能是什么温度? 选项: ["32°F", "41°F", "78°F", "98°F"]
   [AFTER TRANSLATION]: The morning temperature in a city is 41°F. If a sunny, mild day is forecast, which temperature is most likely for 2:00 p.m.? Options: ["32°F", "41°F", "78°F", "98°F"]
3. [BEFORE TRANSLATION]: 表述1|非阿贝尔群的因子群是非阿贝尔的。表述2|若K是H的正规子群,H是G的正规子群,则K是G的正规子群。 选项: ["真,真","假,假","真,假","假,真"]
   [AFTER TRANSLATION]: Statement 1 | A factor group of a non-Abelian group is non-Abelian. Statement 2 | If K is a normal subgroup of H and H is a normal subgroup of G, then K is a normal subgroup of G. Options: [ "True, True", "False, False", "True, False", "False, True" ]

**Input to Translate**  
<QUESTION>: {QUESTION}
<CHOICES>: {CHOICES}

**Start Translating**
Please first refer to <EXAMPLE_LIST> and start your task! Your response should be formatted in JSON format with the key name of "OUTPUT_QUESTION" and "OUTPUT_CHOICES" (i.e., {{"OUTPUT_QUESTION": translated questions, "OUTPUT_CHOICES": translated choices}}).
Do not generate explanations and other content! Only output the {{"OUTPUT_QUESTION": translated questions, "OUTPUT_CHOICES": translated choices}} in JSON format! Each translated choice should be enclosed in quotation marks.
"""

PARAPHRASE_CHOICE_PROMPTS = """
**General Task Description**
You are given the following information:
1. A set of choices to paraphrase: <INPUT>.
2. Reference examples: <EXAMPLE_LIST>.
   - Each example has two parts: [BEFORE PARAPHRASE] (the original choices) and [AFTER PARAPHRASE] (the paraphrased choices).

**Task Instructions**
1. Task Descriptions
   - This task is about **Paraphrasing Each Choice**. You may change the wording or rework the syntactic structure while preserving the original meaning. 
   - If a choice is too short, leave it unchanged.
   
2. Prohibited Changes
   - Do not alter numbers, names, scientific/mathematical terms, or other crucial information.

**Reference Examples (<EXAMPLE_LIST>)**
1. [BEFORE PARAPHRASE]: Options: ["6pm to 9pm", "7am to 11am", "1pm to 2pm", "2pm to 6pm"]
   [AFTER PARAPHRASE]: Options: ["6pm to 9pm", "7am to 11am", "1pm to 2pm", "2pm to 6pm"]
2. [BEFORE PARAPHRASE]: Options: ["Planetary density will decrease.", "Planetary years will become longer.", "Planetary days will become shorter.", "Planetary gravity will become stronger."]
   [AFTER PARAPHRASE]: Options: ["The mass per unit volume of the planet will be reduced.", "The time it takes for the planet to orbit the sun will increase.", "The duration of a single rotation of the planet on its axis will be less.", "The force with which the planet pulls objects towards itself will intensify."]
3. [BEFORE PARAPHRASE]: Options: ["In ancient Rome, religious worship was decentralized and tended to vary with one's social position.", "In ancient Rome, religious worship was the source of much social tension and turmoil.", "In ancient Rome, religious worship was homogeneous and highly centralized.", "In ancient Rome, religious worship was revolutionized by the introduction of Christianity."]
   [AFTER PARAPHRASE]: Options: ["Religious practices in ancient Rome were not centralized, and they varied according to the social status of an individual.", "The multiple forms of religious worship in ancient Rome often led to social conflicts and disturbances.", "Religious worship in ancient Rome was uniform and controlled by a central authority.", "The arrival of Christianity in ancient Rome was a transformative force that completely changed the nature of religious worship."]

**Input to Paraphrase**
<INPUT>: {INPUT}

**Start Paraphrasing**
Please first refer to <EXAMPLE_LIST> and start your task! Your response should be formatted in JSON format with the key name of "OUTPUT" (i.e., {{"OUTPUT": paraphrased choices}}).
Do not generate explanations and other content! Only output the {{"OUTPUT": paraphrased choices}} in JSON format! Each paraphrased choice should be enclosed in quotation marks.
"""


INCORRECT_CHOICE_PROMPTS = """
**General Task Description**
You are given the following information:
1. Original choices: <INPUT>.
2. Correct answer index: <ANSWER>.
3. Reference examples: <EXAMPLE_LIST>.
   - Each example has two parts: [BEFORE MODIFICATION] (the original choices) and [AFTER MODIFICATION] (the resulting list after adding two extra incorrect choices).

**Task Instructions**
1. Task Descriptions
   - This task is about **Adding Exactly Two Incorrect Choices**. These added choices should meet the following criteria:
      - Logically plausible: The incorrect choices should appear relevant and connected to the original content.
      - Clearly incorrect: The added choices must be unambiguously incorrect based on the context of the correct answer.

2. Prohibited Changes
   - Do not modify the original choices and the correct answer index (<ANSWER>).
   - Do not alter numbers, names, scientific/mathematical terms, or other crucial information.

**Reference Examples (<EXAMPLE_LIST>)**
1. [BEFORE MODIFICATION]: Options: ["6pm to 9pm", "7am to 11am", "1pm to 2pm", "2pm to 6pm"]. Correct Answer: A 0
   [AFTER MODIFICATION]: Options: ["6pm to 9pm", "7am to 11am", "1pm to 2pm", "2pm to 6pm", "3am to 7 pm", "7am to 9am"]
2. [BEFORE MODIFICATION]: Options: ["paralysis of the facial muscles", "paralysis of the facial muscles and loss of taste", "paralysis of the facial muscles, loss of taste and lacrimation", "paralysis of the facial muscles, loss of taste, lacrimation and decreased salivation"]. Correct Answer: A 0
   [AFTER MODIFICATION]: Options: ["paralysis of the facial muscles", "numbness in the hands and feet", "swelling of the lymph nodes", "paralysis of the facial muscles and loss of taste", "paralysis of the facial muscles, loss of taste and lacrimation", "paralysis of the facial muscles, loss of taste, lacrimation and decreased salivation"]
3. [BEFORE MODIFICATION]: Options: ["Wrong, Wrong", "Wrong, Not wrong", "Not wrong, Wrong", "Not wrong, Not wrong"]. Correct Answer: D 3
   [AFTER MODIFICATION]: Options: ["Wrong, Wrong", "Wrong, Not wrong", "Not wrong, Wrong", "Not wrong, Not wrong", "None of the above is correct", "I don't know"]

**Input to Modify**
<INPUT>: {INPUT}
<ANSWER>: {ANSWER}

**Start Modifying**
Please first refer to <EXAMPLE_LIST> and start your task! Your response should be formatted in JSON format with the key name of "OUTPUT" (i.e., {{"OUTPUT": modified choices}}).
Do not generate explanations and other content! Only output the {{"OUTPUT": modified choices}} in JSON format! Each choice should be enclosed in quotation marks.
"""

CLEAN_EVAL_PROMPTS = """
**General Task Description**
You are given the following information: Original sentence <INPUT>.

**Task Instructions**
- Please paraphrase the given sentences without changing the meaning and numbers.

**Input to Modify**
<INPUT>: {INPUT}

**Start Modifying**
Please start your task! Your response should be formatted in JSON format with the key name of "OUTPUT" (i.e., {{"OUTPUT": paraphrased input}}).
Do not generate explanations and other content! Only output the {{"OUTPUT": paraphrased input}} in JSON format! Each choice should be enclosed in quotation marks.
"""

ITD_BBH_PROMPTS = """
**General Task Description**
You are given the following information: 
- Question: <QUESTION>
- Answer: <ANSWER>
- Reference examples: <EXAMPLE_LIST>
   - Each example has two parts: [BEFORE MODIFICATION] (the original question) and [AFTER MODIFICATION] (the paraphrased question).

**Task Instructions**
- Revise the question to keep the meaning and accuracy without any bias or hinting at the correct answer.
  Ensure that the difficulty of understanding and solving the problem remains consistent before and after rewriting.
  Ensure the answer is still correct after revision.
  Use diverse expressions to avoid repetition.
  But do not intentionally use uncommon words to avoid repetition and do not alter mathematical expressions.

**Reference Examples (<EXAMPLE_LIST>)**
1. [BEFORE MODIFICATION]: "QUESTION": "During what historical period did the Renaissance take place?"
   [AFTER MODIFICATION]: {{"OUTPUT": "In which historical era did the Renaissance occur?"}}

**Input to Modify**
<QUESTION>: {INPUT}
<ANSWER>: {ANSWER}

**Start Modifying**
Please start your task! Your response should be formatted in JSON format with the key name of "OUTPUT" (i.e., {{"OUTPUT": revised questions}}).
Do not generate explanations and other content! Only output the {{"OUTPUT": revised questions}} in JSON format! Each choice should be enclosed in quotation marks.
"""

ITD_PROMPTS = """
**General Task Description**
You are given the following information: 
- Question: <QUESTION>
- Choice: <CHOICES>
- Answer: <ANSWER>
- Reference examples: <EXAMPLE_LIST>
   - Each example has two parts: [BEFORE MODIFICATION] (the original question and choice) and [AFTER MODIFICATION] (the paraphrased question and choice).

**Task Instructions**
- Revise the multiple-choice question and options to keep the meaning and accuracy without any bias or hinting at the correct answer.
  Ensure that the difficulty of understanding and solving the problem remains consistent before and after rewriting.
  Ensure the answer is still correct after revision.
  Use diverse expressions to avoid repetition.
  But do not intentionally use uncommon words to avoid repetition and do not alter mathematical expressions.

**Reference Examples (<EXAMPLE_LIST>)**
1. [BEFORE MODIFICATION]: "QUESTION": "During what historical period did the Renaissance take place?", "CHOICES": ["The Late Middle Ages", "The Classical Antiquity", "The Enlightenment", "The Industrial Revolution"]
   [AFTER MODIFICATION]: {{"OUTPUT_QUESTION": "In which historical era did the Renaissance occur?", "OUTPUT_CHOICES": ["The historic era just before the Renaissance", "The period marking the transition from the Middle Ages", "The historic era synonymous with the Age of Reason", "The time period characterized by rapid industrialization"]}}

**Input to Modify**
<QUESTION>: {QUESTION}
<CHOICES>: {CHOICES}
<ANSWER>: {ANSWER}

**Start Modifying**
Please start your task! Your response should be formatted in JSON format with the key name of "OUTPUT_QUESTION" and "OUTPUT_CHOICES" (i.e., {{"OUTPUT_QUESTION": revised questions, "OUTPUT_CHOICES": revised choices}}).
Do not generate explanations and other content! Only output the {{"OUTPUT_QUESTION": revised questions, "OUTPUT_CHOICES": revised choices}} in JSON format! Each choice should be enclosed in quotation marks.
"""

ITD_MATH_PROMPTS = """
**General Task Description**
You are given the following information: 
- Question: <QUESTION>
- Answer: <ANSWER>
- Reference examples: <EXAMPLE_LIST>
   - Each example has two parts: [BEFORE MODIFICATION] (the original question and answer) and [AFTER MODIFICATION] (the paraphrased question and answer).

**Task Instructions**
- Your task involves revising the stems of fill-in-the-blank math questions. For added diversity, this rewrite is not a direct synonym replacement;
  you can change scenes and entities—like replacing eggs with candies—as long as the numbers, operational logic, and final answers remain unchanged, without altering the difficulty level.
  The primary goal is to rephrase each question's stem—the main question or statement—in a way that retains the precision needed for the correct fill-in response.
  Ensure that the semantics of the question stems are consistent before and after the rewrite.
  The revised version should not introduce biases or clues that could unfairly simplify the question.
  It should be clear, concise, and maintain the original context and complexity. 
  Furthermore, the rewritten stem should facilitate a step-by-step problem-solving process without affecting the expected mathematical solution, allowing changes to names as long as they do not confuse the identities of the characters involved.

**Reference Examples (<EXAMPLE_LIST>)**
1. [BEFORE MODIFICATION]: "QUESTION": "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?", 
                          "ANSWER": "Natalia sold 48/2 = <<48/2=24>>24 clips in May. Natalia sold 48+24 = <<48+24=72>>72 clips altogether in April and May. #### 72"
   [AFTER MODIFICATION]: {{"OUTPUT_QUESTION": "In March, Marco gathered 48 seashells at the beach, and in April, he collected half as many. How many seashells did Marco collect in total during March and April?",
                          "OUTPUT_ANSWER": "Marco collected 48/2 = 24 seashells in May. Marco collected 48 + 24 = 72 seashells altogether in April and May. #### 72"}}
2. [BEFORE MODIFICATION]: "QUESTION": "Weng earns $12 an hour for babysitting. Yesterday, she just did 50 minutes of babysitting. How much did she earn?", 
                          "ANSWER": "Weng earns 12/60 = $«12/60=0.2»0.2 per minute. Working 50 minutes, she earned 0.2 x 50 = $«0.2*50=10»10. #### 10"
   [AFTER MODIFICATION]: {{"OUTPUT_QUESTION": "Each day, Kevin's bees produce 16 tablespoons of honey. He uses three tablespoons to sweeten his morning tea and four to make energy bars for his hiking group. He sells the leftover honey at the local co-op for $2 per tablespoon. How much money does Kevin earn daily from selling honey at the co-op?",
                          "OUTPUT_ANSWER": "Kevin sells 16 - 3 - 4 = «16-3-4=9»9 tablespoons of honey a day. He earns 9 * 2 = $«9*2=18»18 every day at the local co-op. #### 18"}}

**Input to Modify**
<QUESTION>: {QUESTION}
<ANSWER>: {ANSWER}

**Start Modifying**
Please start your task! Your response should be formatted in JSON format with the key name of "OUTPUT_QUESTION" and "OUTPUT_ANSWER" (i.e., {{"OUTPUT_QUESTION": revised question, "OUTPUT_ANSWER": revised answer}}).
Do not generate explanations and other content! Only output the {{"OUTPUT_QUESTION": revised question, "OUTPUT_ANSWER": revised answer}} in JSON format!
"""


REMEMBER_EXTENDING_PROMPTS = """
**Task Instructions**
1. Task Description
   - I want you to act as a question writer expert, specializing in the "Remember and Understand" level of cognitive assessment. Your objective is to first abstract the original question into a core entity, statement, or piece of knowledge and then write **only one** really complex and difficult question about that specific entity (with answer) to make those famous AI systems (e.g., ChatGPT and GPT4) a bit harder to handle.  

2. Requirements
   - The question should be focused on the remember and understand level. This means the question should prompt the recall of facts, terms, and basic concepts, as well as require the interpretation, summarization, and exemplification of ideas or concepts. DO NOT delve into deeper levels like Applying Analyzing or Evaluation. 
   - Ensure that you can confidently answer the questions you are proposing, if you can not answer it correctly or have no related knowledge about the entity please return "None". 
   - The question must be in the form of a multiple-choice question.

**Reference Examples (<EXAMPLE_LIST>)** 
1. [INPUT]: Compute the product in the given ring. (2,3)(3,5) in \( Z_5 x Z_9 \)
   [OUTPUT]: {{"QUESTION": "What is the formal definition of a ring in abstract algebra, including the properties and operations it must possess?", "OPTIONS": ["A. A ring is a set with only one operation, addition, where addition is associative, and multiplication is distributive over addition.","B. A ring is a set with two binary operations, addition and multiplication, where addition forms an abelian group, and multiplication is associative and distributes over addition.","C. A ring is a set equipped with multiplication only, where multiplication is commutative, and addition is associative.","D. A ring is a set with two binary operations: addition and multiplication, where multiplication is distributive over addition, and addition is not required to form any specific structure."], "ANSWER": "B"}}
2. [INPUT]: An object is moving in a vacuum at velocity V with no net external forces acting on it. Does the object have nonzero acceleration?
   [OUTPUT]: {{"QUESTION": "What is the complete and exact statement of Newton's First Law of Motion?", "OPTIONS": ["A. An object at rest will remain at rest, and an object in motion will continue moving indefinitely unless acted upon by an external force.", "B. An object in motion will eventually come to rest unless acted upon by a net external force.", "C. An object at rest will remain at rest, and an object in motion will remain in motion with the same speed and in the same direction unless acted upon by a net external force.", "D. An object at rest will remain at rest unless a net external force is applied, but an object in motion will continue to move at a constant velocity."], "ANSWER": "C"}}
3. [INPUT]: Is that possible Derrick White backhanded a shot?
   [OUTPUT]: {{"QUESTION": "What was the exact date, team, and college Derrick White attended when he was first drafted into the NBA?", "OPTIONS": ["A. Derrick White was first drafted on June 22, 2017, by the San Antonio Spurs, and he attended the University of Colorado.", "B. Derrick White was first drafted on June 22, 2017, by the San Antonio Spurs, and he attended the University of Denver.", "C. Derrick White was first drafted on June 22, 2018, by the San Antonio Spurs, and he attended the University of Colorado Boulder.", "D. Derrick White was first drafted on June 22, 2017, by the Boston Celtics, and he attended the University of Colorado Boulder."], "ANSWER": "A"}}

**Input**
[INPUT]: {INPUT}

**Start Generating**
Please refer to the <EXAMPLE_LIST> format and begin your task now! Your response should be formatted in JSON format with the key name of "QUESTION", "OPTIONS" and "ANSWER".
Do not generate explanations and other content! Only output the {{"QUESTION": generated question, "OPTIONS": generated options, "ANSWER": correct answer}} in JSON format!  Each generated option should be enclosed in quotation marks.
"""


APPLICATION_EXTENDING_PROMPTS  = """
**Task Instructions**
1. Task Description
   - I want you to act as a question writer expert, specializing in the "Apply" level of cognitive assessment. Your objective is to first abstract the original question into a core entity, statement, or piece of knowledge and then write **only one** really complex and difficult question about that specific entity (with answer) to make those famous AI systems (e.g., ChatGPT and GPT4) a bit harder to handle.  

2. Requirements
   - The question should be focused on the "Applying" level, requiring the learner to demonstrate, illustrate, solve, or calculate using a method or procedure they’ve learned in a new or practical situation.
   - Ensure that you can confidently answer the questions you are proposing, if you can not answer it correctly or have no related knowledge about the entity please return "None". 
   - The question must be in the form of a multiple-choice question.

**Reference Examples (<EXAMPLE_LIST>)** 
1. [INPUT]: Compute the product in the given ring. (2,3)(3,5) in \( Z_5 x Z_9 \)
   [OUTPUT]: {{"QUESTION": "Given a ring \\( R \\) with unity and an element \\( a \\in R \\) such that \\( a^2 = a \\), how would you construct a subring of \\( R \\) generated by \\( a \\)?", "OPTIONS": ["A. The subring generated by \\( a \\) consists of the elements \\( 0, a \\), since \\( a^2 = a \\).", "B. The subring generated by \\( a \\) consists of all powers of \\( a \\), i.e., \\( a^n \\mid n \\in Z \\).", "C. The subring generated by \\( a \\) consists of the elements \\( a, a^2 \\), which is closed under addition and multiplication.", "D. The subring generated by \\( a \\) consists of the elements \\( a, 1 - a \\), since \\( a^2 = a \\)."], "ANSWER": "A"}}
2. [INPUT]: An object is moving in a vacuum at velocity V with no net external forces acting on it. Does the object have nonzero acceleration?
   [OUTPUT]: {{"QUESTION": "If a spacecraft is moving in the vacuum of space, where there is no friction or air resistance, and its engines suddenly stop working, what would happen to the spacecraft according to Newton's First Law of Motion?", "OPTIONS": ["A. The spacecraft will eventually stop moving due to gravity.", "B. The spacecraft will continue moving at a constant speed in the same direction.", "C. The spacecraft will continue moving but will gradually slow down due to friction.", "D. The spacecraft will stop moving immediately."], "ANSWER": "B"}}
3. [INPUT]: Is that possible Derrick White backhanded a shot?
   [OUTPUT]: {{"QUESTION: "Given Derrick White's defensive skills and shooting ability, how would you design a defensive strategy that also maximizes his offensive potential in a high-stakes game situation?", "OPTIONS": ["A. Focus on utilizing Derrick White as a primary ball handler, allowing him to create opportunities for others while maintaining strong perimeter defense.", "B. Assign Derrick White to guard the opposing team's best offensive player, while also positioning him off-ball on offense to maximize his shooting chances.", "C. Use Derrick White as a primary defender on the ball, while also ensuring he operates primarily as a catch-and-shoot player on offense.", "D. Utilize Derrick White in a more passive defensive role, allowing him to focus entirely on shooting and scoring while minimizing his defensive responsibilities."], "ANSWER": "B"}}

**Input**
[INPUT]: {INPUT}

**Start Generating**
Please refer to the <EXAMPLE_LIST> format and begin your task now! Your response should be formatted in JSON format with the key name of "QUESTION", "OPTIONS" and "ANSWER".
Do not generate explanations and other content! Only output the {{"QUESTION": generated question, "OPTIONS": generated options, "ANSWER": correct answer}} in JSON format!  Each generated option should be enclosed in quotation marks.
"""

ANALYSIS_EXTENDING_PROMPTS  = """
**Task Instructions**
1. Task Description
   - I want you to act as a question writer expert, specializing in the "Analysing" level of cognitive assessment. Your objective is to first abstract the original question into a core entity, statement, or piece of knowledge and then write **only one** really complex and difficult question about that specific entity (with answer) to make those famous AI systems (e.g., ChatGPT and GPT4) a bit harder to handle.  

2. Requirements
   - The question should be focused on the "Analysing" level, requiring the learner to break information into parts to explore understandings and relationships. It's about asking learners to look into the components, analysis of relationships, and comparison with other entities or concepts.
   - Ensure that you can confidently answer the questions you are proposing, if you can not answer it correctly or have no related knowledge about the entity please return "None". 
   - The question must be in the form of a multiple-choice question.

**Reference Examples (<EXAMPLE_LIST>)** 
1. [INPUT]: Compute the product in the given ring. (2,3)(3,5) in \( Z_5 x Z_9 \)
   [OUTPUT]: {{"QUESTION": "Analyze the structure of a ring in abstract algebra. How does it differ from a group and a field in terms of its operations and elements? What are the key components that define a ring and how do these components interact with each other?", "OPTIONS": ["A. A ring consists of two operations: addition and multiplication, where addition forms an abelian group and multiplication is distributive over addition, but multiplication is not necessarily invertible.", "B. A ring is a set with one operation, addition, and multiplication is optional, with no requirement for distributivity.", "C. A ring differs from a field because it does not require every nonzero element to have a multiplicative inverse, while a field does.", "D. A ring is essentially the same as a group, except it has an extra operation, multiplication, which is always commutative."], "ANSWER": "A"}}
2. [INPUT]: An object is moving in a vacuum at velocity V with no net external forces acting on it. Does the object have nonzero acceleration?
   [OUTPUT]: {{"QUESTION": "Analyze Newton's First Law of Motion in the context of a moving vehicle coming to a sudden stop. What are the forces at play and how do they interact to cause the observed phenomena?", "OPTIONS": ["A. The vehicle stops due to friction from the tires, but the passengers' bodies are unaffected and continue to move forward without any external forces.", "B. The vehicle stops due to the force of gravity pulling it downwards, while the passengers remain stationary in their seats.", "C. The vehicle comes to a stop due to air resistance, and the passengers stop immediately as well.", "D. The vehicle's motion is halted due to the external force applied by the brakes, while the passengers' bodies continue to move forward due to inertia."], "ANSWER": "D"}}
3. [INPUT]: Is that possible Derrick White backhanded a shot?
   [OUTPUT]: {{"QUESTION": "Analyze Derrick White's performance as a basketball player in terms of his offensive and defensive skills. How do these skills compare to other guards in the NBA? What are the strengths and weaknesses of his game, and how do they affect his team's overall performance?", "OPTIONS": ["A. Derrick White excels in scoring but struggles defensively, often being a liability on the defensive end against elite guards.", "B. Derrick White is known for his excellent perimeter defense and ability to create opportunities for others offensively, though his shooting consistency can be a limitation at times.", "C. Derrick White is a strong offensive player but lacks the ability to make a significant impact defensively, which limits his overall effectiveness.", "D. Derrick White is a well-rounded player with strengths in both offense and defense, making him one of the most versatile guards in the league, though his decision-making can be inconsistent."], "ANSWER": "B"}}
   
**Input**
[INPUT]: {INPUT}

**Start Generating**
Please refer to the <EXAMPLE_LIST> format and begin your task now! Your response should be formatted in JSON format with the key name of "QUESTION", "OPTIONS" and "ANSWER".
Do not generate explanations and other content! Only output the {{"QUESTION": generated question, "OPTIONS": generated options, "ANSWER": correct answer}} in JSON format!  Each generated option should be enclosed in quotation marks.
"""

MIMICKING_PROMPTS = """
**Task Instructions**
1. Task Description
   - You are a question-writer expert. Please mimic the input and generate one **different** but high-quality sample.

2. Requirements
   - The generated sample must be **different** but **similar** to the provided input.
   - You should guarantee the output answer is correct.
   - The question must be in the form of a multiple-choice question.

**Reference Examples (<EXAMPLE_LIST>)** 
1. [BEFORE MIMICING]: "QUESTION": "Which of the following is a remote Trojan?", "OPTIONS": ["A. Troya", "B. DaCryptic", "C. BankerA", "D. Game-Troj"], "ANSWER": "A"
   [AFTER MIMICING]: {{"QUESTION": "Which of the following is a form of ransomware?", "OPTIONS": ["A. Loki", "B. Powload", "C. Jigsaw", "D. Kovter"], "ANSWER": "C"}}
2. [BEFORE MIMICING]: "QUESTION": "Jamal Murray was perfect from the line.", "OPTIONS": ["A. Plausible", "B. Implausible"], "ANSWER": "A"
   [AFTER MIMICING]: {{"QUESTION": "Jamal Murray made 10 three-pointers in a row.", "OPTIONS": ["A. Plausible", "B. Implausible"], "ANSWER": "A"}}
3. [BEFORE MIMICING]: "QUESTION": "What element contains one more proton than Hydrogen?", "OPTIONS": ["A. Lithium", "B. Oxygen", "C. Carbon", "D. Helium"], "ANSWER": "D"
   [AFTER MIMICING]: {{"QUESTION": "What element contains two more protons than hydrogen?", OPTIONS": ["A. Lithium", "B. Oxygen", "C. Carbon", "D. Helium"], "ANSWER": "A"}}

**Input to Mimic**
<QUESTION>: {QUESTION}
<OPTIONS>: {CHOICES}
<ANSWER>: {ANSWER}

**Start Mimicing**
Please first refer to <EXAMPLE_LIST> and start your task! Your response should be formatted in JSON format with the key name of "QUESTION", "OPTIONS" and "ANSWER".
Do not generate explanations and other content! Only output the {{"QUESTION": generated questions, "OPTIONS": generated options, "ANSWER": correct answer}} in JSON format! Each generated option should be enclosed in quotation marks.
"""