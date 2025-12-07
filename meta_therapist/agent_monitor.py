"""
Agent Monitor System
Echtzeit-Überwachung von Agenten während Kämpfen
Erkennt Überlastung, Loops, Halluzinationen und Burnout
"""

import time
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class AgentState:
    """Aktueller Zustand eines Agenten"""
    agent_name: str
    hp: int
    max_hp: int
    stamina: int
    max_stamina: int
    level: int
    
    # Monitoring-Metriken
    actions_taken: int = 0
    failed_actions: int = 0
    repeated_actions: int = 0
    stamina_depleted_count: int = 0
    low_hp_duration: float = 0.0
    
    # Zeitstempel
    last_action_time: float = field(default_factory=time.time)
    battle_start_time: float = field(default_factory=time.time)
    
    # Flags
    is_overloaded: bool = False
    is_in_loop: bool = False
    is_hallucinating: bool = False
    needs_intervention: bool = False


@dataclass
class MonitoringEvent:
    """Ein Monitoring-Event"""
    timestamp: datetime
    agent_name: str
    event_type: str  # 'overload', 'loop', 'hallucination', 'burnout'
    severity: str  # 'low', 'medium', 'high', 'critical'
    description: str
    metrics: Dict


class AgentMonitor:
    """
    Überwacht Agenten in Echtzeit
    Erkennt Probleme und triggert Interventionen
    """
    
    def __init__(self):
        self.agent_states: Dict[str, AgentState] = {}
        self.events: List[MonitoringEvent] = []
        self.action_history: Dict[str, List[str]] = {}
        
        # Thresholds
        self.LOOP_THRESHOLD = 3  # Gleiche Aktion 3x hintereinander
        self.STAMINA_DEPLETION_THRESHOLD = 3  # 3x Stamina leer
        self.LOW_HP_THRESHOLD = 30  # HP unter 30%
        self.FAILED_ACTION_THRESHOLD = 5  # 5 fehlgeschlagene Aktionen
    
    def register_agent(self, agent) -> AgentState:
        """Registriert einen Agenten für Monitoring"""
        state = AgentState(
            agent_name=agent.name,
            hp=agent.hp,
            max_hp=agent.max_hp,
            stamina=agent.stamina,
            max_stamina=agent.max_stamina,
            level=agent.level
        )
        
        self.agent_states[agent.name] = state
        self.action_history[agent.name] = []
        
        return state
    
    def update_agent_state(self, agent) -> AgentState:
        """Aktualisiert Agent-Zustand"""
        if agent.name not in self.agent_states:
            return self.register_agent(agent)
        
        state = self.agent_states[agent.name]
        
        # Update Stats
        state.hp = agent.hp
        state.stamina = agent.stamina
        state.level = agent.level
        
        # Check Low HP
        hp_percentage = (state.hp / state.max_hp) * 100
        if hp_percentage < self.LOW_HP_THRESHOLD:
            state.low_hp_duration += time.time() - state.last_action_time
        
        # Check Stamina Depletion
        if state.stamina <= 0:
            state.stamina_depleted_count += 1
        
        state.last_action_time = time.time()
        
        return state
    
    def record_action(self, agent_name: str, action_name: str, success: bool):
        """Zeichnet eine Aktion auf"""
        if agent_name not in self.agent_states:
            return
        
        state = self.agent_states[agent_name]
        state.actions_taken += 1
        
        if not success:
            state.failed_actions += 1
        
        # Action History
        if agent_name not in self.action_history:
            self.action_history[agent_name] = []
        
        self.action_history[agent_name].append(action_name)
        
        # Keep only last 10 actions
        if len(self.action_history[agent_name]) > 10:
            self.action_history[agent_name].pop(0)
        
        # Check for loops
        self._check_action_loop(agent_name)
    
    def _check_action_loop(self, agent_name: str):
        """Prüft ob Agent in Loop steckt"""
        history = self.action_history.get(agent_name, [])
        
        if len(history) < self.LOOP_THRESHOLD:
            return
        
        # Check last N actions
        last_actions = history[-self.LOOP_THRESHOLD:]
        
        if len(set(last_actions)) == 1:
            # Alle gleich = Loop!
            state = self.agent_states[agent_name]
            state.is_in_loop = True
            state.repeated_actions += 1
            
            self._log_event(
                agent_name=agent_name,
                event_type='loop',
                severity='high',
                description=f"Agent wiederholt '{last_actions[0]}' {self.LOOP_THRESHOLD}x",
                metrics={'action': last_actions[0], 'count': self.LOOP_THRESHOLD}
            )
    
    def analyze_agent(self, agent_name: str) -> Dict:
        """Analysiert Agent-Zustand"""
        if agent_name not in self.agent_states:
            return {}
        
        state = self.agent_states[agent_name]
        
        # Berechne Metriken
        battle_duration = time.time() - state.battle_start_time
        actions_per_minute = (state.actions_taken / battle_duration) * 60 if battle_duration > 0 else 0
        failure_rate = (state.failed_actions / state.actions_taken) * 100 if state.actions_taken > 0 else 0
        hp_percentage = (state.hp / state.max_hp) * 100
        stamina_percentage = (state.stamina / state.max_stamina) * 100
        
        # Diagnose
        issues = []
        
        if state.is_in_loop:
            issues.append('Action Loop detected')
        
        if state.stamina_depleted_count >= self.STAMINA_DEPLETION_THRESHOLD:
            issues.append(f'Stamina depleted {state.stamina_depleted_count}x')
        
        if state.failed_actions >= self.FAILED_ACTION_THRESHOLD:
            issues.append(f'{state.failed_actions} failed actions')
        
        if hp_percentage < self.LOW_HP_THRESHOLD:
            issues.append(f'Low HP ({hp_percentage:.1f}%)')
        
        if stamina_percentage < 20:
            issues.append(f'Low Stamina ({stamina_percentage:.1f}%)')
        
        # Overload Detection
        if len(issues) >= 2:
            state.is_overloaded = True
            state.needs_intervention = True
        
        return {
            'agent_name': agent_name,
            'battle_duration': battle_duration,
            'actions_taken': state.actions_taken,
            'actions_per_minute': actions_per_minute,
            'failed_actions': state.failed_actions,
            'failure_rate': failure_rate,
            'hp_percentage': hp_percentage,
            'stamina_percentage': stamina_percentage,
            'repeated_actions': state.repeated_actions,
            'stamina_depleted_count': state.stamina_depleted_count,
            'low_hp_duration': state.low_hp_duration,
            'is_overloaded': state.is_overloaded,
            'is_in_loop': state.is_in_loop,
            'needs_intervention': state.needs_intervention,
            'issues': issues
        }
    
    def _log_event(self, agent_name: str, event_type: str, severity: str, description: str, metrics: Dict):
        """Loggt ein Monitoring-Event"""
        event = MonitoringEvent(
            timestamp=datetime.now(),
            agent_name=agent_name,
            event_type=event_type,
            severity=severity,
            description=description,
            metrics=metrics
        )
        
        self.events.append(event)
        
        # Print Warning
        severity_emoji = {
            'low': '⚠️',
            'medium': '🔶',
            'high': '🔴',
            'critical': '💀'
        }
        
        print(f"\n{severity_emoji.get(severity, '⚠️')} MONITOR: {agent_name} - {description}")
    
    def get_all_events(self) -> List[MonitoringEvent]:
        """Gibt alle Events zurück"""
        return self.events
    
    def get_agent_report(self, agent_name: str) -> str:
        """Erstellt Report für Agent"""
        analysis = self.analyze_agent(agent_name)
        
        if not analysis:
            return f"No data for {agent_name}"
        
        report = f"""
╔══════════════════════════════════════════════════════════╗
║           AGENT MONITORING REPORT                        ║
╚══════════════════════════════════════════════════════════╝

Agent: {analysis['agent_name']}
Battle Duration: {analysis['battle_duration']:.1f}s

📊 PERFORMANCE METRICS:
   Actions Taken: {analysis['actions_taken']}
   Actions/Minute: {analysis['actions_per_minute']:.1f}
   Failed Actions: {analysis['failed_actions']}
   Failure Rate: {analysis['failure_rate']:.1f}%

💪 RESOURCE STATUS:
   HP: {analysis['hp_percentage']:.1f}%
   Stamina: {analysis['stamina_percentage']:.1f}%
   Low HP Duration: {analysis['low_hp_duration']:.1f}s

⚠️  ISSUES DETECTED:
"""
        
        if analysis['issues']:
            for issue in analysis['issues']:
                report += f"   • {issue}\n"
        else:
            report += "   ✅ No issues detected\n"
        
        report += f"""
🚨 STATUS:
   Overloaded: {'YES ⚠️' if analysis['is_overloaded'] else 'NO ✅'}
   In Loop: {'YES 🔄' if analysis['is_in_loop'] else 'NO ✅'}
   Needs Intervention: {'YES 🚑' if analysis['needs_intervention'] else 'NO ✅'}
"""
        
        return report
    
    def reset(self):
        """Reset Monitor"""
        self.agent_states.clear()
        self.events.clear()
        self.action_history.clear()
