# Document-Summary

In this repository, we have the docsum.py file, which
receives input from the user in the form of a textfile, 
image, pdf, html file, or even a link. This then gets fed to 
Groq's LLM model and returns a summary of the 
document to the user.

#Here's how it works, pull up the docsum.py and hit run

result for research_paper.pdf
The authors propose a new pretraining method called DOCSPLIT, designed for large documents, which uses a contrastive loss to consider the global document context. They experiment with DOCSPLIT on three downstream tasks - text classification, few-shot learning, and document retrieval - and find that their models significantly outperform baseline models. The results show that DOCSPLIT achieves state-of-the-art performance on these tasks, particularly in few-shot text classification settings.


#Examples:

Note: In order for the code to function, hit the run triangle at the top right, then hit the up arrow in the terminal before typing the following 
commands:

`
docs/research_paper.pdf
The paper introduces DOCSPLIT, a new unsupervised pretraining method designed for large documents, which uses contrastive learning to force models to consider the entire global context. Experiments show that DOCSPLIT outperforms other pretraining methods on document classification, few shot learning, and document retrieval tasks, achieving state-of-the-art performance on these tasks.
`

