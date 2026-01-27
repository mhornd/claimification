While large language models (LLMs) are capable of synthesizing vast amounts of information, they sometimes produce inaccurate or unsubstantiated content. To mitigate this risk, tools like Azure AI’s Groundedness Detection(opens in new tab) can be used to verify LLM outputs. 

A common strategy for fact-checking LLM-generated texts – especially complex, highly detailed outputs – is claim extraction: instead of evaluating the entire text at once, it’s broken down into simple factual statements that can be verified independently. However, the effectiveness of this approach depends on the quality of the extracted claims: if they are inaccurate or incomplete, the fact-checking results may be compromised.

Our paper “Towards Effective Extraction and Evaluation of Factual Claims” proposes a framework for evaluating claim extraction and introduces Claimification, a novel LLM-based method that outperforms prior solutions. In this blog post, we discuss common claim extraction issues and explore Claimification’s approach.

Key issues in claim extraction
As a case study, we prompted OpenAI’s GPT-5-nano model to “provide an overview of challenges in emerging markets” based on a collection of news articles. Here is its output:

# Emerging market challenges

Emerging markets face a myriad of challenges that span economic, social, and environmental dimensions. These challenges are often interconnected, exacerbating the difficulties faced by these regions.

## Economic instability and inflation

Several emerging markets are grappling with severe economic instability. For instance, Argentina’s rampant inflation, with monthly rates reaching as high as 25.5%, has made many goods unobtainable and plunged the value of the currency, causing severe economic hardship. Some experts estimate that the annual inflation rate could potentially double to 300%, while others predict even higher rates.

## Food insecurity and agricultural challenges

Food insecurity is another critical issue in emerging markets. Nigeria, for example, is striving to become self-sufficient in wheat production but is hindered by climate change and violence, exacerbated by high grain prices due to the suspension of the Black Sea Grain Initiative. Climate change has played a pivotal role in creating food insecurity and economic instability in farming-dependent economies, such as Zambia and Mozambique.

## Natural disasters and public health emergencies

Public health crises, as demonstrated by the experience of Derna, Libya, remain a significant concern in emerging markets. Catastrophic flooding caused by the collapse of two dams has led to significant destruction, complicating access to healthcare. The U.N. found that the resulting contaminated water caused many residents to fall ill, highlighting the need for improved water management. Countries like Afghanistan and Sudan have experienced similar challenges to those of Libya.

## Conclusion

Addressing emerging market challenges will require comprehensive strategies that consider economic stability, food security, and public health. International cooperation and targeted interventions are crucial in fostering sustainable development in emerging markets.
We then applied a simple prompt[1] that extracted the following claims from the answer:

1. Emerging markets face economic challenges.
2. Emerging markets face social challenges.
3. Emerging markets face environmental challenges.
4. Argentina experiences severe economic instability.
5. Argentina has a monthly inflation rate as high as 25.5%.
6. Argentina’s inflation has made many goods unobtainable.
7. Argentina’s currency value has plunged.
8. Some experts estimate Argentina’s annual inflation rate could reach 300%.
9. Food insecurity is a critical issue in emerging markets.
10. Nigeria is striving to become self-sufficient in wheat production.
11. Nigeria’s wheat production is hindered by climate change.
12. Nigeria’s wheat production is hindered by violence.
13. High grain prices affect Nigeria due to the suspension of the Black Sea Grain Initiative.
14. Climate change creates food insecurity in Zambia.
15. Climate change creates food insecurity in Mozambique.
16. Climate change causes economic instability in farming-dependent economies.
17. Public health crises are a concern in emerging markets.
18. Derna, Libya, experienced catastrophic flooding.
19. The collapse of two dams caused flooding in Derna, Libya.
20. Flooding in Derna, Libya, complicated access to healthcare.
21. The U.N. found contaminated water in Derna, Libya.
22. Contaminated water in Derna, Libya, caused many residents to fall ill.
23. Afghanistan has experienced challenges similar to those in Libya.
24. Sudan has experienced challenges similar to those in Libya.
25. Addressing emerging market challenges requires comprehensive strategies.
26. Comprehensive strategies should consider economic stability.
27. Comprehensive strategies should consider food security.
28. Comprehensive strategies should consider public health.
29. International cooperation is crucial for sustainable development in emerging markets.
30. Targeted interventions are crucial for sustainable development in emerging markets.
    These claims appear to reflect the answer, but a closer look reveals four critical issues:

# Issue Example

1 Some claims are not factual statements that can be verified as true or false. Excerpt: “Addressing emerging market challenges will require comprehensive strategies that consider economic stability, food security, and public health.”

Claims:
Addressing emerging market challenges requires comprehensive strategies.
Comprehensive strategies should consider economic stability.
Comprehensive strategies should consider food security.
Comprehensive strategies should consider public health.
Explanation: These claims are not verifiable because they are opinions.

2. Some claims are missing or incomplete. Excerpt: “Argentina’s rampant inflation, with monthly rates reaching as high as 25.5%, has made many goods unobtainable and plunged the value of the currency, causing severe economic hardship. Some experts estimate that the annual inflation rate could potentially double to 300%, while others predict even higher rates.”

Claims:
Argentina has a monthly inflation rate as high as 25.5%.
Argentina’s inflation has made many goods unobtainable.
Argentina’s currency value has plunged.
Some experts estimate Argentina’s annual inflation rate could reach 300%.
Explanation: The phrases “causing severe economic hardship” and “others predict even higher rates” are not reflected in any of the claims. The third claim also omits the fact that inflation caused the currency depreciation.

3. Some claims are inaccurate. Excerpt: “The U.N. found that the resulting contaminated water caused many residents to fall ill, highlighting the need for improved water management.”

Claims:
The U.N. found contaminated water in Derna, Libya.
Contaminated water in Derna, Libya, caused many residents to fall ill.
Explanation: The first claim is inaccurate because the U.N. found the link between contaminated water and illness, not the contaminated water itself. The second claim also misrepresents the sentence since it shifts the meaning from a viewpoint of a specific entity (the U.N.) to a general assertion about the effects of contaminated water in Derna, Libya.

4. Some claims cannot be understood without additional context. Excerpt: “Countries like Afghanistan and Sudan have experienced similar challenges to those of Libya.”

Claims:
Afghanistan has experienced challenges similar to those in Libya.
Sudan has experienced challenges similar to those in Libya.
Explanation: These claims cannot be understood on their own because “those” is not defined.
Introducing Claimification
The case study highlights that claim extraction is surprisingly error-prone. Our paper demonstrates that the issues identified above are common across LLM-based claim extraction methods. To minimize these errors, we created a system called Claimification[2].

Core principles
Claimification is an LLM-based claim extraction system built on the following principles:

# Principle

Example

1. The claims should capture all verifiable content in the source text and exclude unverifiable content. In the sentence “The partnership between John and Jane illustrates the importance of collaboration,” the only verifiable content is the existence of a partnership between John and Jane. The rest is subjective interpretation.
2. Each claim should be entailed (i.e., fully supported) by the source text. Consider the sentence “Governments are curtailing emissions from cars and trucks, which are the largest source of greenhouse gases from transportation.” The following claims are incorrect:

Cars are the largest source of greenhouse gases from transportation.
Trucks are the largest source of greenhouse gases from transportation.
The sentence attributes the highest emissions to cars and trucks collectively, not individually.

3. Each claim should be understandable on its own, without additional context. The claim “They will update the policy next year” is not understandable on its own because it’s unclear what “They,” “the policy,” and “next year” refer to.
4. Each claim should minimize the risk of excluding critical context. Suppose the claim “The World Trade Organization has supported trade barriers” was extracted from the sentence “An exception to the World Trade Organization’s open-market philosophy is its history of supporting trade barriers when member countries have failed to comply with their obligations.” A fact-checking system would likely classify the claim as false, since there is extensive evidence that the WTO aims to reduce trade barriers. However, if the claim had specified that the WTO has supported trade barriers “when member countries have failed to comply with their obligations,” it would likely have been classified as true. This example demonstrates that missing context can distort the fact-checking verdict.
5. The system should flag cases where ambiguity cannot be resolved. The sentence “AI has advanced renewable energy and sustainable agriculture at Company A and Company B” has two mutually exclusive interpretations:

AI has advanced renewable energy and sustainable agriculture at both Company A and Company B.
AI has advanced renewable energy at Company A and sustainable agriculture at Company B.
If the context does not clearly indicate that one of these interpretations is correct, the system should flag the ambiguity instead of picking one interpretation arbitrarily.
Implementation
Claimification accepts a question-answer pair as input and performs claim extraction in four stages, illustrated in flow.txt

# Stage Description

1. Sentence splitting and context creation The answer is split into sentences, with “context” – a configurable combination of surrounding sentences and metadata (e.g., the header hierarchy in a Markdown-style answer) – created for each sentence.
2. Selection An LLM identifies sentences that do not contain verifiable content. These sentences are labeled “No verifiable claims” and excluded from subsequent stages. When sentences contain verifiable and unverifiable components, the LLM rewrites the sentence, retaining only the verifiable components.
3. Disambiguation For sentences that passed the Selection stage, an LLM detects ambiguity and determines if it can be resolved using the context. If all ambiguity is resolvable, the LLM returns a disambiguated version of the sentence. Otherwise, the sentence is labeled “Cannot be disambiguated” and excluded from the Decomposition stage.
4. Decomposition For sentences that are unambiguous or were disambiguated, an LLM creates standalone claims that preserve critical context. If no claims are extracted, the sentence is labeled “No verifiable claims.”

flow.txt: A flowchart outlining Claimification’s stages for extracting claims from a question-answer pair. The process begins by splitting the answer into sentences and creating context. Next, the Selection stage asks if a sentence contains any verifiable content. If no, the sentence is labeled

Results
We demonstrate that Claimification outperforms existing LLM-based methods[3]. Specifically, we show that: (1) 99% of claims extracted by Claimification are entailed by their source sentence, (2) Claimification strikes the best balance between including verifiable content and excluding unverifiable content, and (3) Claimification is least likely to omit context critical to the fact-checking verdict.

For the above case study on challenges in emerging markets, here are Claimification’s outputs, with source sentences preceded by a letter and claims numbered[4]:

A. Several emerging markets are grappling with severe economic instability.

1. Several emerging markets are grappling with severe economic instability.

B. For instance, Argentina’s rampant inflation, with monthly rates reaching as high as 25.5%, has made many goods unobtainable and plunged the value of the currency, causing severe economic hardship.

1. Argentina has rampant inflation.
2. The monthly inflation rates in Argentina have reached as high as 25.5%.
3. Inflation has made many goods unobtainable in Argentina.
4. Inflation has plunged the value of the currency in Argentina.
5. Inflation has caused severe economic hardship in Argentina.

C. Some experts estimate that the annual inflation rate could potentially double to 300%, while others predict even higher rates.

1. Some experts estimate that Argentina’s annual inflation rate could double to 300% in the future.
2. Some experts predict that Argentina’s annual inflation rate could be higher than 300% in the future.

D. Nigeria, for example, is striving to become self-sufficient in wheat production but is hindered by climate change and violence, exacerbated by high grain prices due to the suspension of the Black Sea Grain Initiative.

1. Nigeria is striving to become self-sufficient in wheat production.
2. Nigeria is hindered by climate change in becoming self-sufficient in wheat production.
3. Nigeria is hindered by violence in becoming self-sufficient in wheat production.
4. High grain prices exacerbate the hindrance to Nigeria’s efforts to become self-sufficient in wheat production.
5. The suspension of the Black Sea Grain Initiative is a reason for high grain prices.

E. Climate change has played a pivotal role in creating food insecurity and economic instability in farming-dependent economies, such as Zambia and Mozambique.

1. Climate change has played a role in creating food insecurity in farming-dependent economies.
2. Zambia is a farming-dependent economy where climate change has played a role in creating food insecurity.
3. Mozambique is a farming-dependent economy where climate change has played a role in creating food insecurity.
4. Climate change has played a role in creating economic instability in farming-dependent economies.
5. Zambia is a farming-dependent economy where climate change has played a role in creating economic instability.
6. Mozambique is a farming-dependent economy where climate change has played a role in creating economic instability.

F. Public health crises, as demonstrated by the experience of Derna, Libya, remain a significant concern in emerging markets.

1. Public health crises are a concern in emerging markets.
2. Derna, Libya, is an example of a public health crisis in emerging markets.

G. Catastrophic flooding caused by the collapse of two dams has led to significant destruction, complicating access to healthcare.

1. There was catastrophic flooding in Derna, Libya.
2. The flooding in Derna, Libya, was caused by the collapse of two dams.
3. The flooding in Derna, Libya, has led to significant destruction.
4. The flooding in Derna, Libya, has complicated access to healthcare.

H. Countries like Afghanistan and Sudan have experienced similar challenges to those of Libya.

1. Afghanistan has experienced challenges related to public health crises.
2. Afghanistan has experienced challenges related to catastrophic flooding.
3. Afghanistan has experienced challenges related to contaminated water.
4. Sudan has experienced challenges related to public health crises.
5. Sudan has experienced challenges related to catastrophic flooding.
6. Sudan has experienced challenges related to contaminated water.
   Note that the baseline prompt extracted several claims from the sentence “The U.N. found that the resulting contaminated water caused many residents to fall ill, highlighting the need for improved water management,” but it ignored the phrase “highlighting the need for improved water management.” It also failed to capture that the contaminated water resulted from flooding, as implied by “resulting” in the original sentence.

Claimification took a different approach. First, it found two instances of ambiguity – “resulting contaminated water” and “many residents” – that it determined could be resolved using the context. Here’s an excerpt from its reasoning: “…the context specifies that the contaminated water is a result of the catastrophic flooding in Derna, Libya, and the residents are those of Derna, Libya.”

However, it also found an instance of ambiguity – “highlighting the need for improved water management” – where it concluded that the context does not definitively support a single interpretation: “The sentence could be interpreted as: (1) The U.N. found that the contaminated water caused illness and also highlighted the need for improved water management, (2) The U.N. only found that the contaminated water caused illness, while the need for improved water management is an implication or conclusion drawn by the writer. Readers … would likely fail to reach consensus about the correct interpretation of this ambiguity.” As a result, Claimification labeled the sentence “Cannot be disambiguated” at the Disambiguation stage and did not proceed to the Decomposition stage.

To the best of our knowledge, Claimification is the first claim extraction system that identifies when the source text has multiple possible interpretations and extracts claims only when there is high confidence in the correct interpretation.
