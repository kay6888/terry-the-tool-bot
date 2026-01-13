"""
QCSE Module - Quantum Code Synthesis Engine

Advanced AI-powered code synthesis using quantum-inspired algorithms
and multi-objective optimization.
"""

__version__ = "1.0.0"
__author__ = "Terry Development Team"
__description__ = "Quantum Code Synthesis Engine for Terry-the-Tool-Bot"

from .core.quantum_processor import QuantumProcessor
from .core.code_synthesizer import CodeSynthesizer
from .core.multi_objective import MultiObjectiveOptimizer
from .core.virtual_testing import VirtualTestingEnvironment
from .algorithms.quantum_search import QuantumSearch
from .algorithms.genetic_optimizer import GeneticOptimizer
from .evaluation.code_metrics import CodeEvaluator
from .integration.terry_integration import QCSEIntegration

__all__ = [
    'QuantumProcessor',
    'CodeSynthesizer', 
    'MultiObjectiveOptimizer',
    'VirtualTestingEnvironment',
    'QuantumSearch',
    'GeneticOptimizer',
    'CodeEvaluator',
    'QCSEIntegration'
]