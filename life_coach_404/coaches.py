"""
Life Coach 404 - Multi-Agent-Ratgeber-System
Verschiedene Coaches für verschiedene Lebensbereiche
"""

import os
import random
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum


class CoachType(Enum):
    """Typen von Coaches"""
    JOB = "job"
    RELATIONSHIP = "relationship"
    FINANCE = "finance"


class Personality(Enum):
    """Coach-Persönlichkeiten"""
    STOIC = "stoic"  # Ruhig, philosophisch
    GOTH = "goth"  # Sarkastisch, düster
    MEME_LORD = "meme_lord"  # Absurd, witzig
    KANT = "kant"  # Kategorischer Imperativ


class LifeCoach:
    """
    Basis-Klasse für Life Coaches
    """
    
    def __init__(self, coach_type: CoachType, personality: Personality):
        self.coach_type = coach_type
        self.personality = personality
        self.sessions: List[Dict] = []
    
    def give_advice(self, problem: str) -> Dict:
        """
        Gibt Ratschlag zu einem Problem
        
        Args:
            problem: Beschreibung des Problems
        
        Returns:
            Dict mit Ratschlag und Metadaten
        """
        
        # Mit OpenAI wenn verfügbar
        if os.getenv("OPENAI_API_KEY"):
            advice_text = self._generate_ai_advice(problem)
        else:
            advice_text = self._generate_fallback_advice(problem)
        
        advice = {
            'timestamp': datetime.now().isoformat(),
            'coach_type': self.coach_type.value,
            'personality': self.personality.value,
            'problem': problem,
            'advice': advice_text,
            'follow_up_questions': self._generate_follow_up_questions(problem)
        }
        
        self.sessions.append(advice)
        
        return advice
    
    def _generate_ai_advice(self, problem: str) -> str:
        """Generiert Ratschlag mit GPT"""
        try:
            from openai import OpenAI
            client = OpenAI()
            
            system_prompt = self._get_system_prompt()
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"Problem: {problem}\n\nGib mir einen Ratschlag!"
                    }
                ],
                temperature=0.8,
                max_tokens=250
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"⚠️  AI-Advice fehlgeschlagen: {e}")
            return self._generate_fallback_advice(problem)
    
    def _get_system_prompt(self) -> str:
        """System-Prompt basierend auf Persönlichkeit"""
        
        base_prompts = {
            CoachType.JOB: "Du bist ein Karriere-Coach. Themen: Job, Kündigung, Bewerbung, Arbeitskollegen.",
            CoachType.RELATIONSHIP: "Du bist ein Beziehungs-Coach. Themen: Liebe, Freunde, Familie, Konflikte.",
            CoachType.FINANCE: "Du bist ein Finanz-Coach. Themen: Geld, Schulden, Investitionen, Sparen."
        }
        
        personality_styles = {
            Personality.STOIC: "Dein Stil ist stoisch und philosophisch. Nutze Weisheiten der Antike. Sei ruhig und bedacht.",
            Personality.GOTH: "Dein Stil ist sarkastisch und düster. Sei zynisch aber hilfreich. Nutze dunklen Humor.",
            Personality.MEME_LORD: "Dein Stil ist absurd und witzig. Nutze Meme-Referenzen. Sei chaotisch aber clever.",
            Personality.KANT: "Dein Stil basiert auf Kant's kategorischem Imperativ. Sei philosophisch und prinzipientreu."
        }
        
        base = base_prompts.get(self.coach_type, "Du bist ein Life Coach.")
        style = personality_styles.get(self.personality, "")
        
        return f"{base} {style} Gib unkonventionelle aber hilfreiche Ratschläge. Sei kurz aber prägnant (max 150 Wörter)."
    
    def _generate_fallback_advice(self, problem: str) -> str:
        """Fallback-Ratschläge ohne AI"""
        
        # Persönlichkeits-spezifische Ratschläge
        advices = {
            (CoachType.JOB, Personality.STOIC): [
                "Betrachte deinen Job als Teil deines Lebenswegs, nicht als dein Leben selbst. Was kannst du kontrollieren? Deine Einstellung und deine Handlungen. Der Rest liegt außerhalb deiner Macht.",
                "Epiktet sagte: 'Es sind nicht die Dinge selbst, die uns beunruhigen, sondern die Meinungen, die wir über sie haben.' Ändere deine Perspektive auf die Situation.",
                "Frage dich: Dient diese Arbeit deiner Tugend? Wenn nein, ist es Zeit für Veränderung. Aber handle bedacht, nicht impulsiv."
            ],
            (CoachType.JOB, Personality.GOTH): [
                "Dein Job ist die Hölle? Willkommen im Kapitalismus. Aber hey, wenigstens hast du was zu hassen. Das ist mehr als viele haben.",
                "Kündigen? Klar. Aber erst wenn du einen Plan hast. Sonst wirst du von der existenziellen Leere verschlungen. Trust me.",
                "Arbeit ist Leiden. Aber Leiden ohne Gehalt ist noch schlimmer. Wäge ab: Welches Leiden ist erträglicher?"
            ],
            (CoachType.JOB, Personality.MEME_LORD): [
                "Bro, dein Job ist sus. Time to yeet yourself out of there? Aber erst den Backup-Plan checken. No cap.",
                "Dein Boss ist ein NPC. Du bist der Protagonist. Main character energy! Aber vergiss nicht: Auch Protagonisten brauchen Geld für Rent.",
                "Job-Situation ist cringe? Das ist der Moment für einen Career-Glow-Up. LinkedIn-Profil pimpen, Bewerbungen raushauen, Boss-Battle vorbereiten."
            ],
            (CoachType.JOB, Personality.KANT): [
                "Handle nur nach derjenigen Maxime, durch die du zugleich wollen kannst, dass sie ein allgemeines Gesetz werde. Würdest du wollen, dass alle in deiner Situation kündigen? Wenn ja, ist es moralisch vertretbar.",
                "Betrachte deine Kollegen nie nur als Mittel, sondern immer zugleich als Zweck an sich selbst. Deine Kündigung sollte niemanden instrumentalisieren.",
                "Pflicht ist das, was aus Achtung fürs Gesetz geschieht. Ist es deine Pflicht zu bleiben oder zu gehen? Prüfe deine Maxime."
            ],
            # Relationship
            (CoachType.RELATIONSHIP, Personality.STOIC): [
                "Liebe ist eine Wahl, keine Emotion. Du kontrollierst nicht, was andere fühlen, nur wie du reagierst. Sei die beste Version deiner selbst.",
                "Marcus Aurelius: 'Das Glück deines Lebens hängt von der Beschaffenheit deiner Gedanken ab.' Ändere deine Gedanken über die Beziehung.",
                "Akzeptiere, was du nicht ändern kannst. Ändere, was du kontrollieren kannst. Und lerne, den Unterschied zu erkennen."
            ],
            (CoachType.RELATIONSHIP, Personality.GOTH): [
                "Beziehungen sind wie Gothic-Romane: Dunkel, kompliziert, und meistens endet jemand emotional tot. Aber hey, wenigstens ist es nicht langweilig.",
                "Liebe ist Schmerz. Aber Einsamkeit ist auch Schmerz. Pick your poison. Ich empfehle den Schmerz mit Netflix-Account.",
                "Red Flags? Bro, das sind Girlanden für deine Emo-Phase. Aber ernsthaft: Renn. Oder bleib und leide. Deine Wahl."
            ],
            (CoachType.RELATIONSHIP, Personality.MEME_LORD): [
                "Relationship Status: It's complicated? Nah fam, it's just broken. Time to hit that 'Block' button IRL?",
                "Dein Partner ist toxic? Das ist nicht very cash money of them. Time for an upgrade. You deserve better, king/queen.",
                "Love is temporary, memes are eternal. Aber real talk: Communication is key. Slide in those DMs (with your partner, not your ex)."
            ],
            (CoachType.RELATIONSHIP, Personality.KANT): [
                "Behandle deinen Partner nie nur als Mittel zur Befriedigung deiner Bedürfnisse, sondern immer auch als Zweck an sich.",
                "Eine Beziehung ist moralisch nur dann gerechtfertigt, wenn beide Partner einander als autonome Wesen respektieren.",
                "Prüfe deine Maxime: Würdest du wollen, dass alle Beziehungen nach deinen Prinzipien funktionieren? Wenn nein, ändere sie."
            ],
            # Finance
            (CoachType.FINANCE, Personality.STOIC): [
                "Reichtum ist nicht, viel zu haben, sondern wenig zu brauchen. Reduziere deine Bedürfnisse, nicht nur deine Ausgaben.",
                "Seneca: 'Es ist nicht der Arme, dem es an vielem fehlt, sondern der Reiche, der nach mehr verlangt.' Finde Genügsamkeit.",
                "Kontrolliere, was du kontrollieren kannst: Deine Ausgaben, deine Arbeit, deine Einstellung zu Geld. Der Rest ist Schicksal."
            ],
            (CoachType.FINANCE, Personality.GOTH): [
                "Geld macht nicht glücklich, aber Armut macht depressiv. Also: Weniger ausgeben, mehr sparen, und dann trotzdem unglücklich sein. Aber mit Geld.",
                "Schulden sind wie emotionale Wunden: Sie heilen nicht von selbst. Budget machen, Raten zahlen, leiden. In dieser Reihenfolge.",
                "Kapitalismus ist Hölle. Aber du musst trotzdem Miete zahlen. Also: Side Hustle starten oder Seele verkaufen. Deine Wahl."
            ],
            (CoachType.FINANCE, Personality.MEME_LORD): [
                "Broke? That's not very stonks of you. Time to level up: Budget spreadsheet, side hustle, maybe some crypto (jk don't).",
                "Your bank account is giving 'error 404: money not found'. Time to debug your spending habits, king.",
                "Financial advice speedrun: Stop buying Starbucks. Start investing. Touch grass. In that order. You're welcome."
            ],
            (CoachType.FINANCE, Personality.KANT): [
                "Handle mit Geld nur nach Maximen, die du als allgemeines Gesetz wollen könntest. Würdest du wollen, dass alle so wirtschaften wie du?",
                "Schulden zu machen bedeutet, andere als Mittel zu deinem Zweck zu nutzen. Zahle zurück, was du schuldest - es ist deine Pflicht.",
                "Investiere nur in das, was du moralisch vertreten kannst. Geld ist kein Selbstzweck, sondern Mittel zum guten Leben."
            ]
        }
        
        key = (self.coach_type, self.personality)
        options = advices.get(key, ["Ich kann dir leider keinen spezifischen Ratschlag geben. Aber: Atme tief durch und denke nach."])
        
        return random.choice(options)
    
    def _generate_follow_up_questions(self, problem: str) -> List[str]:
        """Generiert Follow-Up-Fragen"""
        
        questions = {
            CoachType.JOB: [
                "Was würdest du tun, wenn Geld keine Rolle spielen würde?",
                "Welche Fähigkeiten möchtest du entwickeln?",
                "Was ist das Schlimmste, das passieren könnte, wenn du kündigst?"
            ],
            CoachType.RELATIONSHIP: [
                "Was brauchst du wirklich von dieser Beziehung?",
                "Wie würdest du einem Freund in deiner Situation raten?",
                "Was würde sich ändern, wenn du die Situation akzeptierst?"
            ],
            CoachType.FINANCE: [
                "Wo geht dein Geld wirklich hin?",
                "Was ist dir wichtiger: Sicherheit oder Freiheit?",
                "Welche finanziellen Ziele hast du für die nächsten 5 Jahre?"
            ]
        }
        
        return questions.get(self.coach_type, ["Was möchtest du wirklich?"])
    
    def get_sessions(self) -> List[Dict]:
        """Gibt alle Sessions zurück"""
        return self.sessions


class JobCoach(LifeCoach):
    """Karriere-Coach"""
    
    def __init__(self, personality: Personality = Personality.STOIC):
        super().__init__(CoachType.JOB, personality)


class RelationshipCoach(LifeCoach):
    """Beziehungs-Coach"""
    
    def __init__(self, personality: Personality = Personality.STOIC):
        super().__init__(CoachType.RELATIONSHIP, personality)


class FinanceCoach(LifeCoach):
    """Finanz-Coach"""
    
    def __init__(self, personality: Personality = Personality.STOIC):
        super().__init__(CoachType.FINANCE, personality)
