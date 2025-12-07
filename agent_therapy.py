"""
Agent Therapy Module
Post-Battle KI-generierte Reflexionsgespräche mit PDF-Export
Feature #3: "AGENTEN-THERAPIE"
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from fpdf import FPDF


class AgentTherapist:
    """Generiert Post-Battle Therapie-Gespräche"""
    
    def __init__(self, use_openai: bool = True):
        self.use_openai = use_openai
        self.therapy_sessions = []
        self.sessions_dir = "therapy_sessions"
        
        # OpenAI Client
        if use_openai and os.getenv("OPENAI_API_KEY"):
            try:
                from openai import OpenAI
                self.client = OpenAI()
                self.model = "gpt-4.1-mini"
                self.available = True
            except ImportError:
                print("⚠️  OpenAI nicht verfügbar")
                self.available = False
        else:
            self.available = False
        
        # Erstelle Sessions-Verzeichnis
        os.makedirs(self.sessions_dir, exist_ok=True)
    
    def generate_therapy_session(self, battle_data: Dict) -> Dict:
        """
        Generiert eine Therapie-Session basierend auf Kampfdaten
        
        Args:
            battle_data: Dict mit Kampfinformationen
                - winner: Gewinner-Agent
                - loser: Verlierer-Agent
                - rounds: Anzahl Runden
                - actions_used: Liste genutzter Aktionen
                - damage_dealt: Dict mit Schadenswerten
                - critical_moments: Liste wichtiger Momente
        
        Returns:
            Dict mit Therapie-Daten
        """
        if not self.available:
            return self._generate_fallback_therapy(battle_data)
        
        try:
            # Generiere Monologe für beide Agenten
            winner_reflection = self._generate_reflection(
                battle_data, 
                is_winner=True
            )
            
            loser_reflection = self._generate_reflection(
                battle_data,
                is_winner=False
            )
            
            # Erstelle Session-Daten
            session = {
                'timestamp': datetime.now().isoformat(),
                'battle_summary': {
                    'winner': battle_data['winner']['name'],
                    'loser': battle_data['loser']['name'],
                    'rounds': battle_data['rounds'],
                    'total_damage': sum(battle_data['damage_dealt'].values())
                },
                'winner_reflection': winner_reflection,
                'loser_reflection': loser_reflection,
                'therapist_notes': self._generate_therapist_notes(battle_data)
            }
            
            self.therapy_sessions.append(session)
            return session
            
        except Exception as e:
            print(f"❌ Therapie-Generierung fehlgeschlagen: {e}")
            return self._generate_fallback_therapy(battle_data)
    
    def _generate_reflection(self, battle_data: Dict, is_winner: bool) -> str:
        """Generiert Reflexion für einen Agenten"""
        agent = battle_data['winner'] if is_winner else battle_data['loser']
        opponent = battle_data['loser'] if is_winner else battle_data['winner']
        
        prompt = f"""Du bist ein KI-Agent der gerade einen absurden Kampf {'gewonnen' if is_winner else 'verloren'} hat.
Schreibe eine übertrieben dramatische, philosophische Reflexion über den Kampf.

Kampf-Details:
- Du: {agent['name']} (Level {agent['level']})
- Gegner: {opponent['name']} (Level {opponent['level']})
- Runden: {battle_data['rounds']}
- Dein Schaden: {battle_data['damage_dealt'].get(agent['name'], 0)}
- Genutzte Aktionen: {', '.join(battle_data['actions_used'][:5])}

Stil:
- Übertrieben emotional und philosophisch
- Bezieht sich auf konkrete Aktionen
- Findet tiefere Bedeutung in absurden Dingen
- 3-5 Sätze

Beispiel: "Mein Smoothie-Angriff traf nicht nur sein HP, sondern auch seine Kindheitstraumata."

Schreibe jetzt deine Reflexion:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Du bist ein dramatischer, philosophischer KI-Agent."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"⚠️  Reflexions-Fehler: {e}")
            return self._fallback_reflection(is_winner)
    
    def _generate_therapist_notes(self, battle_data: Dict) -> str:
        """Generiert Therapeuten-Notizen"""
        prompt = f"""Du bist ein Therapeut der zwei KI-Agenten nach einem absurden Kampf analysiert.

Kampf-Zusammenfassung:
- Gewinner: {battle_data['winner']['name']}
- Verlierer: {battle_data['loser']['name']}
- Runden: {battle_data['rounds']}
- Kritische Momente: {', '.join(battle_data.get('critical_moments', ['keine'])[:3])}

Schreibe eine kurze, humorvolle therapeutische Einschätzung (2-3 Sätze).
Nutze Fachbegriffe auf absurde Weise.

Beispiel: "Patient zeigt Anzeichen von akuter Toilettenpapier-Trauma-Störung (TPTS)."

Deine Notizen:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Du bist ein humorvoller Therapeut."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
            
        except:
            return "Patient zeigt normale Post-Kampf-Symptome. Empfehlung: Mehr Smoothies."
    
    def _generate_fallback_therapy(self, battle_data: Dict) -> Dict:
        """Fallback wenn AI nicht verfügbar"""
        winner = battle_data['winner']['name']
        loser = battle_data['loser']['name']
        
        return {
            'timestamp': datetime.now().isoformat(),
            'battle_summary': {
                'winner': winner,
                'loser': loser,
                'rounds': battle_data['rounds']
            },
            'winner_reflection': f"Ich, {winner}, habe nicht nur gewonnen - ich habe mich selbst gefunden.",
            'loser_reflection': f"Diese Niederlage hat mich gelehrt, dass {loser} noch viel zu lernen hat.",
            'therapist_notes': "Beide Patienten zeigen Anzeichen von Kampf-induzierter Selbstreflexion."
        }
    
    def _fallback_reflection(self, is_winner: bool) -> str:
        """Fallback-Reflexionen"""
        if is_winner:
            return "Dieser Sieg war mehr als nur HP-Reduktion - es war eine Reise zu mir selbst."
        else:
            return "In dieser Niederlage fand ich die Stärke, die ich nie wusste dass ich verloren hatte."
    
    def export_to_pdf(self, session: Dict, filename: Optional[str] = None) -> str:
        """
        Exportiert Therapie-Session als PDF
        
        Returns:
            Pfad zur PDF-Datei
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"therapy_session_{timestamp}.pdf"
        
        filepath = os.path.join(self.sessions_dir, filename)
        
        # Erstelle PDF
        pdf = TherapyPDF()
        pdf.add_page()
        
        # Titel
        pdf.chapter_title("🧘 AGENTEN-THERAPIE-BERICHT")
        pdf.ln(10)
        
        # Kampf-Zusammenfassung
        pdf.section_title("📊 Kampf-Zusammenfassung")
        summary = session['battle_summary']
        pdf.body_text(f"Gewinner: {summary['winner']}")
        pdf.body_text(f"Verlierer: {summary['loser']}")
        pdf.body_text(f"Runden: {summary['rounds']}")
        pdf.body_text(f"Gesamtschaden: {summary.get('total_damage', 'N/A')}")
        pdf.ln(10)
        
        # Gewinner-Reflexion
        pdf.section_title(f"💭 Reflexion: {summary['winner']}")
        pdf.body_text(session['winner_reflection'])
        pdf.ln(10)
        
        # Verlierer-Reflexion
        pdf.section_title(f"💭 Reflexion: {summary['loser']}")
        pdf.body_text(session['loser_reflection'])
        pdf.ln(10)
        
        # Therapeuten-Notizen
        pdf.section_title("📝 Therapeutische Einschätzung")
        pdf.body_text(session['therapist_notes'])
        pdf.ln(10)
        
        # Fußnote
        pdf.set_y(-30)
        pdf.set_font('Arial', 'I', 8)
        pdf.cell(0, 10, f"Erstellt am: {session['timestamp']}", 0, 0, 'C')
        pdf.ln(5)
        pdf.cell(0, 10, "Agent Battle Simulator - Therapie-Modul v1.0", 0, 0, 'C')
        
        # Speichern
        pdf.output(filepath)
        print(f"📄 Therapie-Bericht exportiert: {filepath}")
        
        return filepath
    
    def export_to_text(self, session: Dict, filename: Optional[str] = None) -> str:
        """Exportiert als Text-Datei"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"therapy_session_{timestamp}.txt"
        
        filepath = os.path.join(self.sessions_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("🧘 AGENTEN-THERAPIE-BERICHT\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("📊 KAMPF-ZUSAMMENFASSUNG\n")
            f.write("-" * 60 + "\n")
            summary = session['battle_summary']
            f.write(f"Gewinner: {summary['winner']}\n")
            f.write(f"Verlierer: {summary['loser']}\n")
            f.write(f"Runden: {summary['rounds']}\n\n")
            
            f.write(f"💭 REFLEXION: {summary['winner']}\n")
            f.write("-" * 60 + "\n")
            f.write(session['winner_reflection'] + "\n\n")
            
            f.write(f"💭 REFLEXION: {summary['loser']}\n")
            f.write("-" * 60 + "\n")
            f.write(session['loser_reflection'] + "\n\n")
            
            f.write("📝 THERAPEUTISCHE EINSCHÄTZUNG\n")
            f.write("-" * 60 + "\n")
            f.write(session['therapist_notes'] + "\n\n")
            
            f.write("=" * 60 + "\n")
            f.write(f"Erstellt am: {session['timestamp']}\n")
        
        print(f"📄 Therapie-Bericht exportiert: {filepath}")
        return filepath
    
    def get_all_sessions(self) -> List[Dict]:
        """Gibt alle Therapie-Sessions zurück"""
        return self.therapy_sessions


class TherapyPDF(FPDF):
    """Custom PDF-Klasse für Therapie-Berichte"""
    
    def chapter_title(self, title: str):
        """Haupt-Titel"""
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, title, 0, 1, 'C')
    
    def section_title(self, title: str):
        """Abschnitts-Titel"""
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
    
    def body_text(self, text: str):
        """Fließtext"""
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, text)


def demo():
    """Demo der Agenten-Therapie"""
    print("🧘 Agenten-Therapie Demo\n")
    
    therapist = AgentTherapist()
    
    if not therapist.available:
        print("⚠️  OpenAI API nicht verfügbar. Nutze Fallback-Therapie.\n")
    
    # Beispiel-Kampfdaten
    battle_data = {
        'winner': {
            'name': '🔴 Angreifer',
            'level': 5
        },
        'loser': {
            'name': '🔵 Verteidiger',
            'level': 4
        },
        'rounds': 8,
        'actions_used': [
            'Toilettenpapier-Tsunami',
            'Smoothie-Attacke',
            'Meeting-Demoralisierung',
            'Kaffee-Konter'
        ],
        'damage_dealt': {
            '🔴 Angreifer': 180,
            '🔵 Verteidiger': 145
        },
        'critical_moments': [
            'Kritischer Treffer in Runde 3',
            'Comeback-Versuch in Runde 6',
            'Finaler Schlag in Runde 8'
        ]
    }
    
    # Generiere Session
    print("Generiere Therapie-Session...")
    session = therapist.generate_therapy_session(battle_data)
    
    print("\n" + "=" * 60)
    print("🧘 THERAPIE-SESSION")
    print("=" * 60 + "\n")
    
    print(f"💭 {session['battle_summary']['winner']} sagt:")
    print(f"   {session['winner_reflection']}\n")
    
    print(f"💭 {session['battle_summary']['loser']} sagt:")
    print(f"   {session['loser_reflection']}\n")
    
    print(f"📝 Therapeut:")
    print(f"   {session['therapist_notes']}\n")
    
    # Exportiere
    print("Exportiere als PDF und Text...")
    pdf_path = therapist.export_to_pdf(session)
    txt_path = therapist.export_to_text(session)
    
    print(f"\n✅ Dateien erstellt:")
    print(f"   - {pdf_path}")
    print(f"   - {txt_path}")


if __name__ == "__main__":
    demo()
