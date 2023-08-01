from typing import List
import matplotlib.pyplot as plt
import numpy as np
import random
import tqdm

class HeapNode():
    def __init__(self, value):
        self.children: List[HeapNode] = []
        self.equivalenceClass: List[int] = [value]
    
    def equal(self, otherNode):
        self.equivalenceClass.extend(otherNode.equivalenceClass)
        self.children.extend(otherNode.children)
        return self

    def greaterThan(self, otherNode):
        self.children.append(otherNode)
        return self

    def lessThan(self, otherNode):
        return otherNode.greaterThan(self)
    
    def __str__(self) -> str:
        childStrings = ", ".join(str(c) for c in self.children)
        return f"{self.equivalenceClass} => ({childStrings})"

def doTrial(numDocuments: int):
    round = 0
    totalSteps = 0
    documents = [HeapNode(i) for i in range(numDocuments)]
    equivalenceClasses = []
    while len(documents) > 0:
        step = 0
        currentRoundRoot = documents[0] 
        for i in range(1,len(documents)):
            nextChoice = random.randint(-1,1)
            # print(f"ROUND {round} STEP {step}: {currentRoundRoot.equivalenceClass}, {documents[i].equivalenceClass}, CHOICE: {nextChoice}")
            if nextChoice == -1:
                currentRoundRoot = currentRoundRoot.greaterThan(documents[i])
            if nextChoice == 0:
                currentRoundRoot = currentRoundRoot.equal(documents[i])
            if nextChoice == 1:
                currentRoundRoot = currentRoundRoot.lessThan(documents[i])
            step += 1
        documents = currentRoundRoot.children
        equivalenceClasses.append(currentRoundRoot.equivalenceClass)

        totalSteps += step
        step = 0
        round += 1

    return totalSteps

# --------------------------------------------------------------------------------------------------
# SIMULATION
NUM_TRIALS = 100
results = {}
for numDocuments in range(10,2000,50):
    results[numDocuments] = []
for trialIndex in tqdm.tqdm(range(NUM_TRIALS), desc="TRIALS"):
    for numDocuments in results.keys():
        totalSteps = doTrial(numDocuments)
        results.get(numDocuments, []).append(totalSteps)

# Aggregate all trial results
aggregatedResults = []
for numDocuments, trialResults in results.items():
    aggregatedResults.append((numDocuments, np.average(trialResults), np.std(trialResults)))
aggregatedResults.sort(key=lambda x: x[0])
aggregatedResults = np.array(aggregatedResults).T
# print(aggregatedResults)

# Plot results of aggregation
plt.figure(figsize=(10,8))
plt.errorbar(x=aggregatedResults[0, :], y=aggregatedResults[1, :], yerr=aggregatedResults[2, :], fmt="o-", capsize=2)

# Annotation for our samples
X_VAL = 1440
Y_VAL = 2160
plt.vlines(x=X_VAL, ymin=0, ymax=Y_VAL, colors="r")
plt.hlines(y=Y_VAL, xmin=0, xmax=X_VAL, colors="r")
plt.annotate(f"({X_VAL}, {Y_VAL})", (X_VAL, Y_VAL), (X_VAL+150, Y_VAL-400), arrowprops={"width": 1.5, "headwidth": 7, "color":"k", "shrink": 0.1})

plt.xlim(left=0)
plt.ylim(bottom=0)
plt.title(f"Average Number of Steps Required to Judge Document Collections\n(Random Judgement, {NUM_TRIALS} Trials)")
plt.xlabel("Number of Documents")
plt.ylabel("Number of Steps")
plt.show()
