"""
Battle Narrator Module
Generiert narrative Beschreibungen von Kämpfen mit GPT
"""

import json
import os
from pathlib import Path
from datetime import datetime


def narrate(log_file: str, mode: str, export_pdf: bool):
    """
    Generiert narrative Beschreibung eines Kampfes
    
    Args:
        log_file: Pfad zur Battle-Log JSON
        mode: 'therapy', 'commentary', oder 'epic'
        export_pdf: PDF-Export aktiviert
    """
    print("=" * 60)
    print("📖 KAMPF-NARRATION")
    print("=" * 60)
    print()
    
    # Lade Battle-Log
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Datei nicht gefunden: {log_file}")
        return
    except json.JSONDecodeError:
        print(f"❌ Ungültige JSON-Datei: {log_file}")
        return
    
    print(f"📄 Battle-Log geladen: {log_file}")
    print(f"🎭 Modus: {mode}")
    print()
    
    # Generiere Narration
    if mode == 'therapy':
        narration = generate_therapy_narration(data)
    elif mode == 'commentary':
        narration = generate_commentary_narration(data)
    else:  # epic
        narration = generate_epic_narration(data)
    
    # Ausgabe
    print("=" * 60)
    print(narration)
    print("=" * 60)
    print()
    
    # PDF-Export
    if export_pdf:
        export_narration_pdf(data, narration, mode)
    
    print("✅ Narration abgeschlossen!")


def generate_therapy_narration(data: dict) -> str:
    """Generiert Therapie-Stil Narration"""
    
    # Prüfe ob OpenAI verfügbar
    if os.getenv("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            client = OpenAI()
            
            # Erstelle Prompt
            prompt = create_therapy_prompt(data)
            
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "Du bist ein dramatischer Therapeut der KI-Agenten nach Kämpfen analysiert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"⚠️  GPT-Generierung fehlgeschlagen: {e}")
            return generate_fallback_therapy(data)
    else:
        return generate_fallback_therapy(data)


def generate_commentary_narration(data: dict) -> str:
    """Generiert Sport-Kommentar-Stil Narration"""
    
    if os.getenv("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            client = OpenAI()
            
            prompt = create_commentary_prompt(data)
            
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "Du bist ein aufgeregter Sport-Kommentator für absurde KI-Kämpfe."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except:
            return generate_fallback_commentary(data)
    else:
        return generate_fallback_commentary(data)


def generate_epic_narration(data: dict) -> str:
    """Generiert epische Fantasy-Stil Narration"""
    
    if os.getenv("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            client = OpenAI()
            
            prompt = create_epic_prompt(data)
            
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "Du bist ein epischer Fantasy-Erzähler im Stil von Tolkien."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except:
            return generate_fallback_epic(data)
    else:
        return generate_fallback_epic(data)


def create_therapy_prompt(data: dict) -> str:
    """Erstellt Prompt für Therapie-Narration"""
    if 'champion' in data:  # Tournament
        champion = data['champion']['name']
        wins = data['champion']['wins']
        return f"""Ein Turnier ist vorbei. {champion} hat {wins} Kämpfe gewonnen.

Schreibe eine kurze, übertrieben dramatische therapeutische Reflexion aus Sicht des Champions.
Nutze Fachbegriffe auf absurde Weise. 2-3 Sätze."""
    else:  # Single Battle
        winner = data.get('winner', 'Unknown')
        rounds = data.get('rounds', 0)
        return f"""{winner} hat nach {rounds} Runden gewonnen.

Schreibe eine kurze therapeutische Reflexion aus Sicht des Siegers. Übertrieben emotional. 2-3 Sätze."""


def create_commentary_prompt(data: dict) -> str:
    """Erstellt Prompt für Kommentar-Narration"""
    if 'champion' in data:
        champion = data['champion']['name']
        return f"""Turnier vorbei! {champion} ist Champion!

Schreibe einen aufgeregten Sport-Kommentar. 2-3 Sätze."""
    else:
        winner = data.get('winner', 'Unknown')
        return f"""{winner} gewinnt!

Schreibe einen aufgeregten Sport-Kommentar. 2-3 Sätze."""


def create_epic_prompt(data: dict) -> str:
    """Erstellt Prompt für epische Narration"""
    if 'champion' in data:
        champion = data['champion']['name']
        return f"""Ein episches Turnier endet. {champion} triumphiert.

Schreibe eine kurze epische Erzählung im Fantasy-Stil. 2-3 Sätze."""
    else:
        winner = data.get('winner', 'Unknown')
        return f"""{winner} siegt in einem epischen Kampf.

Schreibe eine kurze epische Erzählung im Fantasy-Stil. 2-3 Sätze."""


# Fallback-Funktionen

def generate_fallback_therapy(data: dict) -> str:
    """Fallback Therapie-Narration"""
    if 'champion' in data:
        name = data['champion']['name']
        return f'"Ich hätte nie gedacht, dass ich es schaffen würde... aber hier bin ich. {name}, der Champion. Diese Siege haben nicht nur meine HP geheilt - sie haben meine Seele transformiert."'
    else:
        winner = data.get('winner', 'Unknown')
        return f'"Dieser Kampf hat mich verändert. Ich, {winner}, bin nicht mehr derselbe Agent. Jede Runde war eine Lektion in Selbstfindung."'


def generate_fallback_commentary(data: dict) -> str:
    """Fallback Kommentar-Narration"""
    if 'champion' in data:
        name = data['champion']['name']
        wins = data['champion']['wins']
        return f"UNGLAUBLICH! {name} dominiert das Turnier mit {wins} Siegen! Die Crowd ist außer sich! Was für eine Performance!"
    else:
        winner = data.get('winner', 'Unknown')
        return f"UND DA IST ES! {winner} GEWINNT! Was für ein Kampf! Die Zuschauer rasten aus!"


def generate_fallback_epic(data: dict) -> str:
    """Fallback epische Narration"""
    if 'champion' in data:
        name = data['champion']['name']
        return f"Und so endete das große Turnier. {name}, der Tapfere, erhob sich über alle anderen. Sein Name wird in den Annalen der Geschichte verewigt sein."
    else:
        winner = data.get('winner', 'Unknown')
        return f"Als der Staub sich legte, stand {winner} als Sieger da. Eine Legende war geboren."


def export_narration_pdf(data: dict, narration: str, mode: str):
    """Exportiert Narration als PDF"""
    try:
        from fpdf import FPDF
    except ImportError:
        print("⚠️  fpdf2 nicht installiert")
        return
    
    output_dir = Path("cline_integration/reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"narration_{mode}_{timestamp}.pdf"
    filepath = output_dir / filename
    
    pdf = FPDF()
    pdf.add_page()
    
    # ASCII-Art Titel
    pdf.set_font('Courier', 'B', 12)
    pdf.multi_cell(0, 5, """
    ⚔️  BATTLE NARRATION  ⚔️
    """)
    pdf.ln(5)
    
    # Modus
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'Modus: {mode.upper()}', 0, 1)
    pdf.ln(5)
    
    # Narration
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 6, narration)
    pdf.ln(10)
    
    # Kampf-Details
    pdf.set_font('Arial', 'I', 9)
    if 'champion' in data:
        pdf.cell(0, 5, f"Champion: {data['champion']['name']}", 0, 1)
        pdf.cell(0, 5, f"Siege: {data['champion']['wins']}", 0, 1)
    elif 'winner' in data:
        pdf.cell(0, 5, f"Sieger: {data['winner']}", 0, 1)
        pdf.cell(0, 5, f"Runden: {data.get('rounds', 'N/A')}", 0, 1)
    
    pdf.output(str(filepath))
    print(f"📄 Narration-PDF exportiert: {filepath}")
