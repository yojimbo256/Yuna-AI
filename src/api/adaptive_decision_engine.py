# ade.py
import random
from src.api.adaptive_decision_engine import AdaptiveDecisionEngine  # Rename module

class AdaptiveDecisionEngine:
    def __init__(self):
        self.decision_graph = {}
        self.rewards = {}  # For reinforcement learning

    def add_decision_pathway(self, state, actions, reward):
        """Add possible decision pathways"""
        self.decision_graph[state] = actions
        self.rewards[state] = reward

    def choose_best_path(self, state):
        """Choose the best decision pathway based on reinforcement learning and weighted logic"""
        if state in self.decision_graph:
            actions = self.decision_graph[state]
            best_action = max(actions, key=lambda x: self.rewards.get(x, 0))
            return best_action
        return None

    def update_rewards(self, state, action, feedback):
        """Update reward for specific state-action pair based on feedback"""
        current_reward = self.rewards.get(state, {}).get(action, 0)
        self.rewards.setdefault(state, {})[action] = current_reward + feedback
