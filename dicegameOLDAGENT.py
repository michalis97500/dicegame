class MyAgent(DiceGameAgent):
    def __init__(self, game, theta=0.1, gamma=1):
        #Variables to use
        super().__init__(game)
        self.gamma = gamma
        self.delSquared = []
        self.thSquared = theta * theta
        
        self.valueAction = {
            state: 0 for state in self.game.states}
        self.BestActionVal = {
            state: () for state in self.game.states}
        self.nextStates = {
            state: {} for state in self.game.states}
        
        self.getNextStates()
        self.count = 0
        
        self.searchStates()
        while max(self.delSquared) > self.thSquared:
            self.searchStates()

    #Agent move
    def play(self, state):
        return self.BestActionVal[state]
    
    #MDP implementation. Calculate action value (expected)
    def calcActionValue(self, action, state):
        states, end, reward, prob = self.nextStates[state][action]
        
        if end:
            return self.game.final_scores[state]
        expected = sum([self.valueAction[s] * p for p, s in zip(prob, states)])
        return reward + self.gamma * expected
    
    #Get next states from game object
    def getNextStates(self):
        for state in self.game.states:
            for action in self.game.actions:
                self.nextStates[state][action] = self.game.get_next_states(action=action,
                                                                                    dice_state=state)

    #Search states for best action
    def searchStates(self):
        self.delSquared = []
        for state in self.valueAction:
            self.BestAction(state)
        self.count += 1

    #Find highest action value
    def BestAction(self, state):
        actionValues = []
        for action in self.game.actions:
            actionValues.append(self.calcActionValue(action=action, state=state))
            
        BestActionVal = max(actionValues)
        self.valueAction[state] = BestActionVal
        
        valSquared = (self.valueAction[state] - BestActionVal) * (self.valueAction[state] - BestActionVal)
        self.delSquared.append(valSquared)
        
        self.BestActionVal[state] = self.game.actions[actionValues.index(BestActionVal)]
    