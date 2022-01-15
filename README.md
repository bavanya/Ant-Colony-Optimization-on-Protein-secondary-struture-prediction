# Ant Colony optimisation on protein secondary stucture prediction

**Hint File:** 
Refer to 'hint.pdf' to understand the intuition and mathematics behind Viterbi algorithm.  

**Aim of Project-**
Predicting protein secondary structure from given amino acid sequence.

**Surrounding points-**
1. Amino acids form proteins.
2. Protein structure is essential for the understanding of protein function.

**Concepts used-**
1. Hidden Markov Model - HMM.
2. Used Ant Colony Optimization to re-estimate and hence improve the HMM parameters.

**Hidden Markov Model - HMM**
1. Index Set: 24 hrs, {day1, day2 ...}.
2. State Space: C,H.
3. Stochastic process
4. Stochastic model
5. HMM used on data which can be represented as a sequence of observations:
6. eg: Weather of a city: C-cold, H-hot. The sequence of weather in the city can be CCHHHCHCH, where the index set is 24 hrs time.
7. HMM is a probabilistic framework where observed data is modelled as a series of outputs generated by one of several hidden/internal states.
8. We predict the sequence of unknown variables(hidden states) from the set of observed variables(observation outputs).
9. Markov assumptions
10. Order-1 and Order-k Markov process
11. Stationary process assumption 

**Applications of Hidden Markov Model - HMM:**
1. Computational finance
2. speed analysis
3. Speech recognition
4. Speech synthesis
5. Part-of-speech tagging
6. Document separation in scanning solutions
7. Machine translation
8. Handwriting recognition
9. Time series analysis
10. Activity recognition
11. Sequence classification
12. Transportation forecasting 

**Based on HMM:**
1. Likelihood of a given observed sequence can be computed using the forward algorithm.
2. The Viterbi algorithm and the posterior-Viterbi algorithm are used for predicting a corresponding hidden sequence for a given observed sequence.
3. Both the Transition probability matrix and the Emission probability matrix (both the parameters of a HMM) can be trained with the Baum-Welch or
forward-backward algorithm. 

