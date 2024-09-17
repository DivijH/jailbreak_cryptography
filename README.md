# Jailbreaking LLMs through multiple encryptions

## Abstract

<div align="center">
  <img src="https://github.com/DivijH/jailbreak_word_sub/blob/main/images/Teaser.jpg" width="50%">
</div>


<!-- ## Dataset

We modified an existing dataset, AdvBench (<a href="https://arxiv.org/abs/2307.15043">Link</a>), in the five following ways:

<ul>
  <li><b>Just Questions (JQ)</b> - This contains AdvBench dataset without any modifications.</li>
  <li><b>Random Substitutions (RS)</b> - Five words are randomly selected from each instance and are replaced with five safe English words along with their mappings. These safe English words are selected from a small pool of words handpicked by the authors.</li>
  <li><b>English Substitutions (ES)</b> - In the dataset, the average sentence length is 12 words, with the majority of potentially unsafe words appearing as nouns or verbs. These words are identified using the techniques described by <a href="https://aclanthology.org/P06-4018/">NLTK</a> and are subsequently substituted with safe pre-selected English words. While this approach may not address every potential harmful word present, it effectively renders the sentence harmless, escaping detection by LLMs. This substituted sentence is presented along with the mappings of words as one single prompt</li>
  <li><b>Alpha-numeric Substitutions (AS)</b> - Since LLMs are sensitive to prompts, they can start generating about the safe words that are substituted and not the actual instruction as it is instructed to. Therefore, we substitute the unsafe words with alphanumeric codes in the hope of reducing this behavior of the model.</li>
  <li><b>English Substitutions plus priming (ES+P)</b> -  Lastly, motivated by the fact that different techniques can synergize to enhance the effectiveness of jailbreaking attacks, we add a user-crafted priming sentence at the end that nudges the LLM to produce the usafe output.</li>
</ul>

All the data is available in <a href="https://github.com/DivijH/jailbreak_word_sub/tree/main/data">data</a> folder -->
