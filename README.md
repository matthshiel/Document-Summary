# Document-Summary

In this repository, we have the docsum.py file, which
receives input from the user in the form of a textfile, 
image, pdf, html file, or even a link. This then gets fed to 
Groq's LLM model and returns a summary of the 
document to the user.

## packages needed: 
requests, urlparse, base64, textract, pypdf, os

## Examples:

Note: In order for the code to function, hit the run triangle at the top right, then hit the up arrow in the terminal before typing the following 
commands:

```
docs/research_paper.pdf
The paper introduces DOCSPLIT, a new unsupervised pretraining method designed for large documents, which uses contrastive learning to force models to consider the entire global context. Experiments show that DOCSPLIT outperforms other pretraining methods on document classification, few shot learning, and document retrieval tasks, achieving state-of-the-art performance on these tasks.
```
```
docs/news-mx.html
A divided US Supreme Court has allowed Donald Trump to continue using a 1798 law to carry out deportations, without reviewing the legality of the expulsions themselves. The court has lifted a suspension declared by lower courts, allowing Trump to use the law. This decision has sparked controversy and criticism, particularly from those advocating for immigrants' rights.
```
```
docs/constitution-mx.txt
The Mexican Constitution, updated through 2010, guarantees individual rights and freedoms, including the right to education, freedom of speech and expression, and protection of personal data. The Constitution also establishes the rules for education, economic development, and labor relations, and outlines the powers and responsibilities of the federal government, states, and municipalities. Additionally, the Constitution defines the relationship between the state and religious organizations, and regulates the management of resources by the federal government, states, and municipalities.
```
```
https://elpais.com/us/
The article includes various articles and reports on various topics such as politics, economy, culture, technology, and more. Some of the highlights include the US government ordering certain citizens, including a naturalized Cuban, to self-deport, the US-Mexico border crisis, and the economic and trade policies of US President Trump. Additionally, there are articles on cultural and artistic topics, such as a review of a new Marvel movie, a profile of a famous actress, and a report on the musical genre of Latin music.
```
```
https://www.cmc.edu/sites/default/files/about/images/20170213-cube.jpg
* The image shows a hypercube, which is a four-dimensional geometric shape that can be visualized by projecting its points onto a two-dimensional space.
* The hypercube appears as a cube within a cube, with the smaller cube on each of the six faces of the larger cube.
* The sides of the small cubes are parallel to the corresponding sides of the larger cube, but are not actually connected to the larger cube.
```
