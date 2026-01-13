"""
QCSE Integration with Terry-the-Tool-Bot

Integration layer for the Quantum Code Synthesis Engine to work with
Terry's existing tool system and conversation interface.
"""

import asyncio
import logging
import time
from typing import Dict, Any, Optional, List
from .core.code_synthesizer import CodeSynthesizer, SynthesisRequest, SynthesisMode
from .core.quantum_processor import CodeCandidate
from ..tools.base_tool import BaseTool

logger = logging.getLogger(__name__)

class QCSETool(BaseTool):
    """QCSE tool integration with Terry's tool system"""
    
    def __init__(self):
        super().__init__(
            name="qcse_synthesizer",
            version="1.0.0",
            description="Quantum Code Synthesis Engine - Advanced AI-powered code synthesis"
        )
        
        self.synthesizer = CodeSynthesizer()
        self.synthesis_history = []
        self.best_syntheses = []
        
    def execute(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute QCSE synthesis"""
        start_time = time.time()
        
        try:
            # Extract synthesis requirements
            synthesis_request = self._extract_synthesis_request(user_input, context)
            
            # Validate request
            if not self._validate_request(synthesis_request):
                return self._format_response(
                    status='error',
                    message='Invalid synthesis request',
                    execution_time=time.time() - start_time
                )
            
            # Run synthesis
            logger.info(f"Starting QCSE synthesis: {synthesis_request.mode}")
            result = asyncio.run(self.synthesizer.synthesize(synthesis_request))
            
            # Store in history
            self.synthesis_history.append({
                'request': synthesis_request,
                'result': result,
                'timestamp': time.time(),
                'user_input': user_input
            })
            
            # Update best syntheses
            if result.fitness_score > 0.7:  # High-quality synthesis
                self.best_syntheses.append({
                    'candidate': result,
                    'request': synthesis_request,
                    'timestamp': time.time()
                })
            
            # Create response
            response_data = {
                'generated_code': result.code,
                'fitness_score': result.fitness_score,
                'efficiency': result.efficiency,
                'maintainability': result.maintainability,
                'security_score': result.security_score,
                'test_results': result.test_results,
                'generation': result.generation,
                'synthesis_mode': synthesis_request.mode.value,
                'objectives': synthesis_request.objectives
            }
            
            return self._format_response(
                status='success',
                message=f'Quantum Code Synthesis completed successfully (fitness: {result.fitness_score:.4f})',
                data=response_data,
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            logger.error(f"QCSE synthesis failed: {str(e)}")
            return self._format_response(
                status='error',
                message=f'Quantum synthesis failed: {str(e)}',
                execution_time=time.time() - start_time
            )
    
    def validate_input(self, user_input: str) -> bool:
        """Validate if input is suitable for QCSE"""
        qcse_keywords = [
            'quantum', 'synthesis', 'optimize', 'optimal', 'best',
            'multi-objective', 'pareto', 'efficient', 'secure',
            'maintainable', 'performance', 'code generation'
        ]
        
        user_input_lower = user_input.lower()
        return any(keyword in user_input_lower for keyword in qcse_keywords)
    
    def _extract_synthesis_request(self, user_input: str, context: Dict[str, Any]) -> SynthesisRequest:
        """Extract synthesis request from user input"""
        import re
        
        # Default request
        request = SynthesisRequest(
            requirements=self._extract_requirements(user_input),
            constraints=self._extract_constraints(user_input),
            target_language=self._extract_language(user_input),
            mode=self._extract_mode(user_input),
            max_iterations=50,
            population_size=20,
            timeout=60.0,
            objectives=self._extract_objectives(user_input)
        )
        
        return request
    
    def _extract_requirements(self, user_input: str) -> Dict[str, Any]:
        """Extract synthesis requirements from user input"""
        requirements = {
            'type': 'general',
            'features': [],
            'architecture': 'modern'
        }
        
        user_input_lower = user_input.lower()
        
        # Extract specific requirements
        if 'android' in user_input_lower:
            requirements['type'] = 'android'
            requirements['platform'] = 'android'
        
        if 'web' in user_input_lower:
            requirements['type'] = 'web'
            requirements['platform'] = 'web'
        
        if 'api' in user_input_lower:
            requirements['type'] = 'api'
            requirements['interface'] = 'rest'
        
        if 'ui' in user_input_lower or 'gui' in user_input_lower:
            requirements['ui'] = 'modern'
        
        # Extract features
        feature_keywords = {
            'security': ['security', 'secure', 'authentication', 'authorization'],
            'performance': ['performance', 'fast', 'efficient', 'optimize'],
            'maintainability': ['maintainable', 'clean', 'readable', 'structured'],
            'scalability': ['scalable', 'scale', 'extensible', 'flexible']
        }
        
        for feature, keywords in feature_keywords.items():
            if any(keyword in user_input_lower for keyword in keywords):
                requirements['features'].append(feature)
        
        return requirements
    
    def _extract_constraints(self, user_input: str) -> Dict[str, Any]:
        """Extract synthesis constraints from user input"""
        constraints = {
            'max_complexity': 50,
            'max_lines': 1000,
            'max_execution_time': 5.0,
            'max_memory_usage': 100.0
        }
        
        user_input_lower = user_input.lower()
        
        # Extract specific constraints
        if 'simple' in user_input_lower:
            constraints['max_complexity'] = 20
            constraints['max_lines'] = 500
        
        if 'complex' in user_input_lower:
            constraints['max_complexity'] = 100
            constraints['max_lines'] = 2000
        
        # Extract numeric constraints
        complexity_match = re.search(r'complexity[:\s]*<[:\s]*(\d+)', user_input_lower)
        if complexity_match:
            constraints['max_complexity'] = int(complexity_match.group(1))
        
        lines_match = re.search(r'lines[:\s]*<[:\s]*(\d+)', user_input_lower)
        if lines_match:
            constraints['max_lines'] = int(lines_match.group(1))
        
        return constraints
    
    def _extract_language(self, user_input: str) -> str:
        """Extract target programming language"""
        user_input_lower = user_input.lower()
        
        language_map = {
            'kotlin': ['kotlin', 'android', 'jetbrains'],
            'python': ['python', 'py', 'django', 'flask'],
            'java': ['java', 'spring', 'maven', 'gradle'],
            'javascript': ['javascript', 'js', 'node', 'react', 'vue'],
            'typescript': ['typescript', 'ts', 'angular'],
            'c#': ['c#', 'csharp', '.net', 'microsoft'],
            'c++': ['c++', 'cpp', 'gcc', 'clang']
        }
        
        for language, keywords in language_map.items():
            if any(keyword in user_input_lower for keyword in keywords):
                return language
        
        return 'kotlin'  # Default for Android
    
    def _extract_mode(self, user_input: str) -> SynthesisMode:
        """Extract synthesis mode"""
        user_input_lower = user_input.lower()
        
        if 'quantum' in user_input_lower:
            return SynthesisMode.QUANTUM_INSPIRED
        elif 'evolutionary' in user_input_lower or 'genetic' in user_input_lower:
            return SynthesisMode.EVOLUTIONARY
        elif 'neural' in user_input_lower or 'ai' in user_input_lower:
            return SynthesisMode.NEURAL
        else:
            return SynthesisMode.HYBRID  # Default
    
    def _extract_objectives(self, user_input: str) -> List[str]:
        """Extract optimization objectives"""
        user_input_lower = user_input.lower()
        
        objectives = ['efficiency', 'maintainability', 'security', 'performance']
        extracted_objectives = []
        
        for objective in objectives:
            if objective in user_input_lower:
                extracted_objectives.append(objective)
        
        # Default objectives if none specified
        if not extracted_objectives:
            extracted_objectives = ['efficiency', 'maintainability', 'security']
        
        return extracted_objectives
    
    def _validate_request(self, request: SynthesisRequest) -> bool:
        """Validate synthesis request"""
        # Check required fields
        if not request.requirements:
            return False
        
        if not request.target_language:
            return False
        
        # Check constraints
        if request.max_iterations < 1:
            return False
        
        if request.population_size < 1:
            return False
        
        return True
    
    def get_synthesis_statistics(self) -> Dict[str, Any]:
        """Get synthesis statistics"""
        return {
            'total_syntheses': len(self.synthesis_history),
            'best_syntheses': len(self.best_syntheses),
            'average_fitness': sum(s['result'].fitness_score for s in self.synthesis_history) / len(self.synthesis_history) if self.synthesis_history else 0,
            'best_fitness': max(s['result'].fitness_score for s in self.synthesis_history) if self.synthesis_history else 0,
            'synthesis_modes': list(set(s['request'].mode.value for s in self.synthesis_history)),
            'target_languages': list(set(s['request'].target_language for s in self.synthesis_history))
        }
    
    def get_best_synthesis(self) -> Optional[Dict[str, Any]]:
        """Get best synthesis from history"""
        if not self.best_syntheses:
            return None
        
        best = max(self.best_syntheses, key=lambda x: x['candidate'].fitness_score)
        
        return {
            'candidate': best['candidate'],
            'request': best['request'],
            'timestamp': best['timestamp'],
            'code': best['candidate'].code,
            'fitness_score': best['candidate'].fitness_score,
            'test_results': best['candidate'].test_results
        }
    
    def create_synthesis_report(self) -> str:
        """Create comprehensive synthesis report"""
        stats = self.get_synthesis_statistics()
        
        report = f"""
⚛️ Quantum Code Synthesis Engine Report
{'='*60}
Total Syntheses: {stats['total_syntheses']}
Best Syntheses: {stats['best_syntheses']}
Average Fitness: {stats['average_fitness']:.4f}
Best Fitness: {stats['best_fitness']:.4f}
Synthesis Modes: {', '.join(stats['synthesis_modes'])}
Target Languages: {', '.join(stats['target_languages'])}

🎯 Recent Best Synthesis:
"""
        
        best = self.get_best_synthesis()
        if best:
            report += f"""
Language: {best['request'].target_language}
Mode: {best['request'].mode.value}
Fitness Score: {best['fitness_score']:.4f}
Generated: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(best['timestamp']))}

Code Preview:
{best['code'][:200]}{'...' if len(best['code']) > 200 else ''}

Test Results: {best['test_results'].get('status', 'Unknown')}
"""
        
        return report

class QCSEIntegration:
    """Main QCSE integration class for Terry"""
    
    def __init__(self, terry_bot):
        self.terry_bot = terry_bot
        self.qcse_tool = QCSETool()
        self.synthesizer = CodeSynthesizer()
        
        # Integration with Terry's tool system
        self.terry_bot.tools['qcse_synthesizer'] = {
            'name': 'Quantum Code Synthesis Engine',
            'description': 'Advanced AI-powered code synthesis using quantum algorithms',
            'version': '1.0.0',
            'active': True,
            'functions': [
                'synthesize_android_code',
                'optimize_existing_code',
                'generate_test_suite',
                'analyze_performance'
            ]
        }
        
        logger.info("QCSE integration initialized with Terry")
    
    def synthesize_code(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main synthesis method"""
        if context is None:
            context = {}
        
        # Add Terry context
        context['terry_mode'] = self.terry_bot.mode
        context['terry_version'] = self.terry_bot.version
        context['terry_tools'] = list(self.terry_bot.tools.keys())
        
        return self.qcse_tool.execute(user_input, context)
    
    def optimize_code(self, code: str, objectives: List[str] = None) -> Dict[str, Any]:
        """Optimize existing code"""
        start_time = time.time()
        
        try:
            # Create synthesis request for optimization
            request = SynthesisRequest(
                requirements={'type': 'optimization', 'original_code': code},
                constraints={'max_iterations': 30, 'population_size': 15},
                target_language=self._detect_language(code),
                mode=SynthesisMode.HYBRID,
                objectives=objectives or ['efficiency', 'maintainability', 'security'],
                timeout=30.0
            )
            
            # Run synthesis
            result = asyncio.run(self.synthesizer.synthesize(request))
            
            return {
                'status': 'success',
                'original_code': code,
                'optimized_code': result.code,
                'improvement': result.fitness_score - 0.5,  # Baseline comparison
                'fitness_score': result.fitness_score,
                'test_results': result.test_results,
                'execution_time': time.time() - start_time
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'execution_time': time.time() - start_time
            }
    
    def _detect_language(self, code: str) -> str:
        """Detect programming language from code"""
        code_lower = code.lower()
        
        if 'package ' in code_lower and 'import ' in code_lower:
            if 'kotlin' in code_lower or 'jetbrains' in code_lower:
                return 'kotlin'
            elif 'java' in code_lower:
                return 'java'
        
        if 'def ' in code_lower or 'import ' in code_lower:
            return 'python'
        
        if 'function ' in code_lower or 'const ' in code_lower:
            return 'javascript'
        
        return 'kotlin'  # Default
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get integration status"""
        return {
            'qcse_enabled': True,
            'synthesizer_active': True,
            'tool_integrated': True,
            'statistics': self.qcse_tool.get_synthesis_statistics(),
            'best_synthesis': self.qcse_tool.get_best_synthesis()
        }