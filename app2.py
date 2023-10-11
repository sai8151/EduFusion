import spacy
import pytextrank
import random
nlp=spacy.load("en_core_web_lg")
nlp.add_pipe("textrank")
text="""Ever since computers were invented, we have wondered whether they might be
made to learn. If we could understand how to program them to learn-to improve
automatically with experience-the impact would be dramatic. Imagine computers learning from medical records which treatments are most effective for new
diseases, houses learning from experience to optimize energy costs based on the
particular usage patterns of their occupants, or personal software assistants learning the evolving interests of their users in order to highlight especially relevant
stories from the online morning newspaper. A successful understanding of how to
make computers learn would open up many new uses of computers and new levels
of competence and customization. And a detailed understanding of informationprocessing algorithms for machine learning might lead to a better understanding
of human learning abilities (and disabilities) as well.
We do not yet know how to make computers learn nearly as well as people
learn. However, algorithms have been invented that are effective for certain types
of learning tasks, and a theoretical understanding of learning is beginning to
emerge. Many practical computer programs have been developed to exhibit useful types of learning, and significant commercial applications have begun to appear. For problems such as speech recognition, algorithms based on machine
learning outperform all other approaches that have been attempted to date. In
the field known as data mining, machine learning algorithms are being used routinely to discover valuable knowledge from large commercial databases containing
equipment maintenance records, loan applications, financial transactions, medical
records, and the like. As our understanding of computers continues to mature, it 
2 MACHINE LEARNING
seems inevitable that machine learning will play an increasingly central role in
computer science and computer technology.
A few specific achievements provide a glimpse of the state of the art: programs have been developed that successfully learn to recognize spoken words
(Waibel 1989; Lee 1989), predict recovery rates of pneumonia patients (Cooper
et al. 1997), detect fraudulent use of credit cards, drive autonomous vehicles
on public highways (Pomerleau 1989), and play games such as backgammon at
levels approaching the performance of human world champions (Tesauro 1992,
1995). Theoretical results have been developed that characterize the fundamental
relationship among the number of training examples observed, the number of hypotheses under consideration, and the expected error in learned hypotheses. We
are beginning to obtain initial models of human and animal learning and to understand their relationship to learning algorithms developed for computers (e.g.,
Laird et al. 1986; Anderson 1991; Qin et al. 1992; Chi and Bassock 1989; Ahn
and Brewer 1993). In applications, algorithms, theory, and studies of biological
systems, the rate of progress has increased significantly over the past decade. Several recent applications of machine learning are summarized in Table 1.1. Langley
and Simon (1995) and Rumelhart et al. (1994) survey additional applications of
machine learning."""
doc=nlp(text)
for sent in doc._.textrank.summary(limit_phrases=random.randint(0, 30), limit_sentences=3):
    print(sent)