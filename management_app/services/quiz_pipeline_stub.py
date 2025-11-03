def build_quiz_stub(video_url: str) -> dict:
    return {
        "title": "Stub vs. Prod: Verstehen & Anwenden",
        "description": "Teste dein Wissen zu Stub- und Prod-Pipelines: Zweck, Unterschiede, Einsatz und typische Stolpersteine.",
        "questions": [
            {
                "question_title": "Wozu dient eine Stub-Pipeline in Projekten?",
                "question_options": [
                    "Schnelles End-to-End-Testen ohne echte KI/Infra",
                    "Dauerhafte Produktionslogik",
                    "Frontend-Styles optimieren",
                    "Backup der Datenbank anlegen"
                ],
                "answer": "Schnelles End-to-End-Testen ohne echte KI/Infra"
            },
            {
                "question_title": "Was beschreibt am besten eine Prod-Pipeline?",
                "question_options": [
                    "Gibt Dummy-Daten zurück",
                    "Führt die reale Verarbeitung mit echten Diensten aus",
                    "Deaktiviert alle Validierungen",
                    "Erzeugt ausschließlich zufällige Ergebnisse"
                ],
                "answer": "Führt die reale Verarbeitung mit echten Diensten aus"
            },
            {
                "question_title": "Wann ist eine Stub-Pipeline besonders sinnvoll?",
                "question_options": [
                    "Wenn externe Dienste noch nicht verfügbar sind",
                    "Nur bei UI-Deployments",
                    "Ausschließlich nach dem Go-Live",
                    "Wenn Production schon stabil läuft"
                ],
                "answer": "Wenn externe Dienste noch nicht verfügbar sind"
            },
            {
                "question_title": "Was ist ein Kerunterschied zwischen Stub und Prod?",
                "question_options": [
                    "Stub ist deterministisch, Prod kann variieren",
                    "Beide liefern identische Outputs",
                    "Prod ist ohne Abhängigkeiten",
                    "Stub braucht immer GPU"
                ],
                "answer": "Stub ist deterministisch, Prod kann variieren"
            },
            {
                "question_title": "Welche Gefahr besteht, wenn man zu lange mit Stub testet?",
                "question_options": [
                    "Zu viele echte Kosten durch API-Calls",
                    "UI wird zu schnell",
                    "Fehlende Abdeckung realer Fehlerfälle",
                    "Zu wenige Unit-Tests möglich"
                ],
                "answer": "Fehlende Abdeckung realer Fehlerfälle"
            },
            {
                "question_title": "Welche Voraussetzung gilt typischerweise für die Prod-Pipeline?",
                "question_options": [
                    "Keine Credentials nötig",
                    "Externe Tools wie ffmpeg/yt-dlp/Whisper korrekt installiert",
                    "Nur Offline-Betrieb",
                    "Kein Logging erforderlich"
                ],
                "answer": "Externe Tools wie ffmpeg/yt-dlp/Whisper korrekt installiert"
            },
            {
                "question_title": "Warum ist @transaction.atomic beim Persistieren nützlich?",
                "question_options": [
                    "Sorgt für dunkles Theme im Admin",
                    "Alles-oder-nichts-Speichern bei Quiz + Questions",
                    "Beschleunigt die GPU",
                    "Erlaubt GET ohne Auth"
                ],
                "answer": "Alles-oder-nichts-Speichern bei Quiz + Questions"
            },
            {
                "question_title": "Was gehört NICHT in eine Stub-Pipeline?",
                "question_options": [
                    "Feste Testdaten",
                    "Echte API-Aufrufe an Gemini",
                    "Deterministische Antworten",
                    "Schnelle Ausführung"
                ],
                "answer": "Echte API-Aufrufe an Gemini"
            },
            {
                "question_title": "Wie hilft eine Stub-Pipeline beim Testen?",
                "question_options": [
                    "Reduziert Flakiness durch stabile Outputs",
                    "Deaktiviert alle Tests",
                    "Erzwingt Zeitüberschreitungen",
                    "Verhindert Logging"
                ],
                "answer": "Reduziert Flakiness durch stabile Outputs"
            },
            {
                "question_title": "Wann solltest du von Stub auf Prod wechseln?",
                "question_options": [
                    "Wenn End-to-End-Grundpfad steht und externe Abhängigkeiten bereit sind",
                    "Nie; Stub reicht immer",
                    "Direkt zu Projektstart",
                    "Erst nach dem Release"
                ],
                "answer": "Wenn End-to-End-Grundpfad steht und externe Abhängigkeiten bereit sind"
            }
        ]
    }