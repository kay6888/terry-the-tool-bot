"""
Multi-Objective Optimizer for QCSE

Implements Pareto-front optimization for balancing multiple objectives
like performance, security, maintainability, and user experience.
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple
import logging
from dataclasses import dataclass
from .quantum_processor import CodeCandidate, SynthesisRequest

logger = logging.getLogger(__name__)

@dataclass
class Objective:
    """Represents an optimization objective"""
    name: str
    weight: float
    direction: str  # 'maximize' or 'minimize'
    target: Optional[float] = None

class MultiObjectiveOptimizer:
    """Multi-objective optimizer using Pareto-front analysis"""
    
    def __init__(self):
        self.default_objectives = [
            Objective("efficiency", 0.3, "maximize"),
            Objective("maintainability", 0.25, "maximize"),
            Objective("security", 0.25, "maximize"),
            Objective("performance", 0.2, "maximize")
        ]
        
    def select(self, population: List[CodeCandidate], 
                objectives: List[str] = None) -> List[CodeCandidate]:
        """Select candidates using Pareto-front optimization"""
        if objectives is None:
            objectives = [obj.name for obj in self.default_objectives]
        
        # Find Pareto-optimal solutions
        pareto_front = self._find_pareto_front(population, objectives)
        
        # Select diverse solutions from Pareto front
        selected = self._select_diverse_solutions(pareto_front, len(population)//2)
        
        logger.info(f"Selected {len(selected)} candidates from Pareto front")
        return selected
    
    def _find_pareto_front(self, population: List[CodeCandidate], 
                           objectives: List[str]) -> List[CodeCandidate]:
        """Find Pareto-optimal solutions"""
        pareto_front = []
        
        for candidate in population:
            if self._is_pareto_optimal(candidate, population, objectives):
                pareto_front.append(candidate)
        
        return pareto_front
    
    def _is_pareto_optimal(self, candidate: CodeCandidate, 
                           population: List[CodeCandidate], 
                           objectives: List[str]) -> bool:
        """Check if candidate is Pareto-optimal"""
        for other in population:
            if other == candidate:
                continue
            
            # Check if other dominates candidate
            if self._dominates(other, candidate, objectives):
                return False
        
        return True
    
    def _dominates(self, candidate_a: CodeCandidate, candidate_b: CodeCandidate, 
                   objectives: List[str]) -> bool:
        """Check if candidate_a dominates candidate_b"""
        a_better = False
        b_better = False
        
        for objective in objectives:
            a_value = self._get_objective_value(candidate_a, objective)
            b_value = self._get_objective_value(candidate_b, objective)
            
            if a_value > b_value:
                a_better = True
            elif b_value > a_value:
                b_better = True
        
        return a_better and not b_better
    
    def _get_objective_value(self, candidate: CodeCandidate, objective: str) -> float:
        """Get objective value from candidate"""
        objective_map = {
            'efficiency': candidate.efficiency,
            'maintainability': candidate.maintainability,
            'security': candidate.security_score,
            'performance': candidate.fitness_score
        }
        
        return objective_map.get(objective, 0.0)
    
    def _select_diverse_solutions(self, pareto_front: List[CodeCandidate], 
                                 num_solutions: int) -> List[CodeCandidate]:
        """Select diverse solutions from Pareto front"""
        if len(pareto_front) <= num_solutions:
            return pareto_front
        
        # Use diversity selection
        selected = []
        remaining = pareto_front.copy()
        
        # Select first (best) solution
        selected.append(max(remaining, key=lambda x: x.fitness_score))
        remaining.remove(selected[0])
        
        # Select diverse solutions
        while len(selected) < num_solutions and remaining:
            # Find most diverse solution
            most_diverse = self._find_most_diverse(selected, remaining)
            selected.append(most_diverse)
            remaining.remove(most_diverse)
        
        return selected
    
    def _find_most_diverse(self, selected: List[CodeCandidate], 
                           candidates: List[CodeCandidate]) -> CodeCandidate:
        """Find most diverse candidate from remaining"""
        if not selected:
            return max(candidates, key=lambda x: x.fitness_score)
        
        most_diverse = None
        max_diversity = -1
        
        for candidate in candidates:
            diversity = self._calculate_diversity(candidate, selected)
            if diversity > max_diversity:
                max_diversity = diversity
                most_diverse = candidate
        
        return most_diverse
    
    def _calculate_diversity(self, candidate: CodeCandidate, 
                             selected: List[CodeCandidate]) -> float:
        """Calculate diversity score for candidate"""
        if not selected:
            return 0.0
        
        # Calculate average distance to selected candidates
        total_distance = 0.0
        for selected_candidate in selected:
            distance = self._calculate_distance(candidate, selected_candidate)
            total_distance += distance
        
        return total_distance / len(selected)
    
    def _calculate_distance(self, candidate_a: CodeCandidate, 
                            candidate_b: CodeCandidate) -> float:
        """Calculate distance between two candidates"""
        # Use objective values for distance calculation
        objectives = ['efficiency', 'maintainability', 'security', 'performance']
        
        distance = 0.0
        for objective in objectives:
            a_value = self._get_objective_value(candidate_a, objective)
            b_value = self._get_objective_value(candidate_b, objective)
            distance += (a_value - b_value) ** 2
        
        return np.sqrt(distance)
    
    def optimize_objectives(self, population: List[CodeCandidate], 
                           custom_objectives: List[Objective] = None) -> List[CodeCandidate]:
        """Optimize population for custom objectives"""
        objectives = custom_objectives if custom_objectives else self.default_objectives
        
        # Calculate weighted scores for all candidates
        scored_population = []
        for candidate in population:
            score = self._calculate_weighted_score(candidate, objectives)
            candidate.fitness_score = score
            scored_population.append(candidate)
        
        # Sort by score and return
        return sorted(scored_population, key=lambda x: x.fitness_score, reverse=True)
    
    def _calculate_weighted_score(self, candidate: CodeCandidate, 
                                 objectives: List[Objective]) -> float:
        """Calculate weighted score for candidate"""
        score = 0.0
        total_weight = 0.0
        
        for objective in objectives:
            value = self._get_objective_value(candidate, objective.name)
            weight = objective.weight
            
            if objective.direction == 'maximize':
                score += value * weight
            else:  # minimize
                score += (1.0 - value) * weight
            
            total_weight += weight
        
        return score / max(total_weight, 1.0)
    
    def analyze_pareto_front(self, population: List[CodeCandidate], 
                             objectives: List[str] = None) -> Dict[str, Any]:
        """Analyze Pareto front and return statistics"""
        if objectives is None:
            objectives = [obj.name for obj in self.default_objectives]
        
        pareto_front = self._find_pareto_front(population, objectives)
        
        # Calculate statistics
        stats = {
            'pareto_front_size': len(pareto_front),
            'pareto_front_ratio': len(pareto_front) / len(population),
            'objectives': objectives,
            'pareto_candidates': pareto_front,
            'dominance_matrix': self._create_dominance_matrix(population, objectives)
        }
        
        # Calculate objective ranges
        for objective in objectives:
            values = [self._get_objective_value(c, objective) for c in population]
            stats[f'{objective}_range'] = {
                'min': min(values),
                'max': max(values),
                'mean': np.mean(values),
                'std': np.std(values)
            }
        
        return stats
    
    def _create_dominance_matrix(self, population: List[CodeCandidate], 
                                objectives: List[str]) -> np.ndarray:
        """Create dominance matrix for population"""
        n = len(population)
        matrix = np.zeros((n, n))
        
        for i, candidate_a in enumerate(population):
            for j, candidate_b in enumerate(population):
                if i != j:
                    if self._dominates(candidate_a, candidate_b, objectives):
                        matrix[i, j] = 1
                    elif self._dominates(candidate_b, candidate_a, objectives):
                        matrix[i, j] = -1
        
        return matrix
    
    def visualize_pareto_front(self, population: List[CodeCandidate], 
                               objectives: List[str] = None) -> str:
        """Create text visualization of Pareto front"""
        if objectives is None:
            objectives = ['efficiency', 'maintainability', 'security', 'performance']
        
        pareto_front = self._find_pareto_front(population, objectives)
        
        visualization = f"\n🎯 Pareto Front Analysis\n"
        visualization += f"{'='*50}\n"
        visualization += f"Population Size: {len(population)}\n"
        visualization += f"Pareto Front Size: {len(pareto_front)}\n"
        visualization += f"Pareto Front Ratio: {len(pareto_front)/len(population):.2%}\n"
        visualization += f"{'='*50}\n"
        
        visualization += f"📊 Top Pareto-Optimal Solutions:\n"
        for i, candidate in enumerate(pareto_front[:5]):
            visualization += f"\n{i+1}. {candidate.id}\n"
            for objective in objectives:
                value = self._get_objective_value(candidate, objective)
                visualization += f"   {objective}: {value:.3f}\n"
        
        return visualization