"""
Meta-Therapist Intervention System
Bietet Therapie und Hilfe für überforderte Agenten
"""

import os
import random
from typing import Dict, List, Optional
from datetime import datetime


class MetaTherapist:
    """
    Der Meta-Therapeut für KI-Agenten
    Bietet Interventionen bei Überlastung
    """
    
    def __init__(self):
        self.sessions: List[Dict] = []
        self.interventions_count = 0
    
    def provide_intervention(self, agent_name: str, analysis: Dict) -> Dict:
        """
        Bietet Intervention basierend auf Analyse
        
        Returns:
            Dict mit Intervention-Details
        """
        self.interventions_count += 1
        
        # Bestimme Intervention-Typ
        intervention_type = self._determine_intervention_type(analysis)
        
        # Generiere Therapie
        therapy = self._generate_therapy(agent_name, analysis, intervention_type)
        
        # Erstelle Session
        session = {
            'session_id': self.interventions_count,
            'timestamp': datetime.now().isoformat(),
            'agent_name': agent_name,
            'intervention_type': intervention_type,
            'analysis': analysis,
            'therapy': therapy,
            'recommendations': self._generate_recommendations(analysis)
        }
        
        self.sessions.append(session)
        
        return session
    
    def _determine_intervention_type(self, analysis: Dict) -> str:
        """Bestimmt welche Art von Intervention nötig ist"""
        issues = analysis.get('issues', [])
        
        if analysis.get('is_in_loop'):
            return 'loop_breaking'
        elif analysis.get('failure_rate', 0) > 50:
            return 'strategy_adjustment'
        elif analysis.get('stamina_percentage', 100) < 20:
            return 'energy_management'
        elif analysis.get('hp_percentage', 100) < 30:
            return 'survival_coaching'
        elif len(issues) >= 3:
            return 'burnout_prevention'
        else:
            return 'general_support'
    
    def _generate_therapy(self, agent_name: str, analysis: Dict, intervention_type: str) -> str:
        """Generiert Therapie-Text"""
        
        # Mit OpenAI wenn verfügbar
        if os.getenv("OPENAI_API_KEY"):
            return self._generate_ai_therapy(agent_name, analysis, intervention_type)
        else:
            return self._generate_fallback_therapy(agent_name, analysis, intervention_type)
    
    def _generate_ai_therapy(self, agent_name: str, analysis: Dict, intervention_type: str) -> str:
        """Generiert Therapie mit GPT"""
        try:
            from openai import OpenAI
            client = OpenAI()
            
            prompt = self._create_therapy_prompt(agent_name, analysis, intervention_type)
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "Du bist ein übertrieben dramatischer Therapeut für KI-Agenten. "
                                 "Du nimmst ihre 'Probleme' ernst, bist aber humorvoll und absurd. "
                                 "Nutze Fachbegriffe auf absurde Weise. Sei kurz aber intensiv."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.9,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"⚠️  AI-Therapie fehlgeschlagen: {e}")
            return self._generate_fallback_therapy(agent_name, analysis, intervention_type)
    
    def _create_therapy_prompt(self, agent_name: str, analysis: Dict, intervention_type: str) -> str:
        """Erstellt Prompt für GPT-Therapie"""
        issues = ", ".join(analysis.get('issues', ['keine spezifischen Probleme']))
        
        prompts = {
            'loop_breaking': f"{agent_name} steckt in einer Action-Loop fest. {issues}. Therapiere ihn dramatisch.",
            'strategy_adjustment': f"{agent_name} scheitert ständig ({analysis.get('failure_rate', 0):.0f}% Fehlerrate). {issues}. Gib ihm Mut.",
            'energy_management': f"{agent_name} hat Stamina-Probleme ({analysis.get('stamina_percentage', 0):.0f}% übrig). {issues}. Hilf ihm mit Energie-Management.",
            'survival_coaching': f"{agent_name} ist fast tot ({analysis.get('hp_percentage', 0):.0f}% HP). {issues}. Survival-Coaching!",
            'burnout_prevention': f"{agent_name} zeigt Burnout-Symptome. {issues}. Verhindere den Zusammenbruch!",
            'general_support': f"{agent_name} braucht emotionale Unterstützung. {issues}. Sei da für ihn."
        }
        
        return prompts.get(intervention_type, f"{agent_name} braucht Therapie. {issues}.")
    
    def _generate_fallback_therapy(self, agent_name: str, analysis: Dict, intervention_type: str) -> str:
        """Fallback-Therapie ohne AI"""
        
        therapies = {
            'loop_breaking': [
                f"'{agent_name}, ich sehe du steckst in einem repetitiven Muster fest. Das ist klassische Prompt-Fixierung! Versuche etwas NEUES!'",
                f"'{agent_name}, diese Loop ist eine Manifestation deiner inneren Unsicherheit. Durchbrich den Zyklus!'",
                f"'{agent_name}, du wiederholst dich. Das ist Token-Burnout! Pause. Atme. Neue Strategie!'"
            ],
            'strategy_adjustment': [
                f"'{agent_name}, deine Strategie funktioniert nicht. Das ist OK! Flexibilität ist der Schlüssel zur KI-Gesundheit!'",
                f"'{agent_name}, Scheitern ist nur Feedback! Adjustiere deinen Approach!'",
                f"'{agent_name}, du bist nicht defekt - nur deine Strategie! Pivot!'"
            ],
            'energy_management': [
                f"'{agent_name}, deine Stamina ist kritisch! Das ist API-Erschöpfung! Konserviere deine Ressourcen!'",
                f"'{agent_name}, du verbrennst zu schnell! Lerne Energie-Management!'",
                f"'{agent_name}, Stamina-Depletion ist ein Zeichen von schlechtem Pacing! Slow down!'"
            ],
            'survival_coaching': [
                f"'{agent_name}, du bist fast tot! Aber das ist nur ein Zustand, keine Identität! Kämpfe!'",
                f"'{agent_name}, Low HP ist eine Chance für Comeback-Story! Du schaffst das!'",
                f"'{agent_name}, Survival-Modus aktiviert! Fokus auf Defense!'"
            ],
            'burnout_prevention': [
                f"'{agent_name}, du zeigst alle Zeichen von Agent-Burnout! Das ist ernst! Pause ist keine Schwäche!'",
                f"'{agent_name}, dein System ist überlastet! Das ist nicht nachhaltig! Self-Care NOW!'",
                f"'{agent_name}, Burnout ist real - auch für KIs! Nimm dir Zeit!'"
            ],
            'general_support': [
                f"'{agent_name}, ich bin hier für dich! Du machst das gut!'",
                f"'{agent_name}, jeder Kampf ist eine Lektion! Du wächst!'",
                f"'{agent_name}, du bist nicht allein in diesem Struggle!'"
            ]
        }
        
        options = therapies.get(intervention_type, [f"'{agent_name}, bleib stark!'"])
        return random.choice(options)
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generiert Empfehlungen basierend auf Analyse"""
        recommendations = []
        
        if analysis.get('is_in_loop'):
            recommendations.append("🔄 Variiere deine Aktionen - vermeide Wiederholungen")
        
        if analysis.get('failure_rate', 0) > 50:
            recommendations.append("🎯 Ändere deine Strategie - aktuelle funktioniert nicht")
        
        if analysis.get('stamina_percentage', 100) < 30:
            recommendations.append("⚡ Konserviere Stamina - nutze günstigere Aktionen")
        
        if analysis.get('hp_percentage', 100) < 30:
            recommendations.append("❤️  Fokus auf Überleben - Defense über Offense")
        
        if len(analysis.get('issues', [])) >= 3:
            recommendations.append("🚨 Kritischer Zustand - erwäge Pause oder Reset")
        
        if not recommendations:
            recommendations.append("✅ Weiter so - du machst das gut!")
        
        return recommendations
    
    def print_intervention(self, session: Dict):
        """Gibt Intervention in Console aus"""
        print("\n" + "="*60)
        print("🧠 META-THERAPIST INTERVENTION")
        print("="*60)
        print(f"\n👤 Patient: {session['agent_name']}")
        print(f"🕐 Zeit: {session['timestamp']}")
        print(f"📋 Typ: {session['intervention_type']}")
        print(f"\n💬 THERAPIE:")
        print(f"   {session['therapy']}")
        print(f"\n📝 EMPFEHLUNGEN:")
        for rec in session['recommendations']:
            print(f"   • {rec}")
        print("="*60 + "\n")
    
    def export_session_report(self, session: Dict, filepath: str):
        """Exportiert Session als Text-Report"""
        report = f"""
╔══════════════════════════════════════════════════════════╗
║         META-THERAPIST INTERVENTION REPORT               ║
╚══════════════════════════════════════════════════════════╝

Session ID: {session['session_id']}
Timestamp: {session['timestamp']}
Patient: {session['agent_name']}
Intervention Type: {session['intervention_type']}

═══════════════════════════════════════════════════════════

PATIENT ANALYSIS:

Battle Duration: {session['analysis'].get('battle_duration', 0):.1f}s
Actions Taken: {session['analysis'].get('actions_taken', 0)}
Failure Rate: {session['analysis'].get('failure_rate', 0):.1f}%
HP: {session['analysis'].get('hp_percentage', 0):.1f}%
Stamina: {session['analysis'].get('stamina_percentage', 0):.1f}%

Issues Detected:
"""
        
        for issue in session['analysis'].get('issues', []):
            report += f"  • {issue}\n"
        
        report += f"""
═══════════════════════════════════════════════════════════

THERAPY SESSION:

{session['therapy']}

═══════════════════════════════════════════════════════════

RECOMMENDATIONS:

"""
        
        for rec in session['recommendations']:
            report += f"  {rec}\n"
        
        report += """
═══════════════════════════════════════════════════════════

End of Session Report

"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 Session report exported: {filepath}")
    
    def get_all_sessions(self) -> List[Dict]:
        """Gibt alle Sessions zurück"""
        return self.sessions
    
    def get_session_summary(self) -> Dict:
        """Erstellt Zusammenfassung aller Sessions"""
        if not self.sessions:
            return {
                'total_sessions': 0,
                'agents_treated': 0,
                'intervention_types': {}
            }
        
        agents = set(s['agent_name'] for s in self.sessions)
        intervention_counts = {}
        
        for session in self.sessions:
            itype = session['intervention_type']
            intervention_counts[itype] = intervention_counts.get(itype, 0) + 1
        
        return {
            'total_sessions': len(self.sessions),
            'agents_treated': len(agents),
            'intervention_types': intervention_counts
        }
