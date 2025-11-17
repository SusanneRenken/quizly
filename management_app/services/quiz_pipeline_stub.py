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

# {
#     "id": 2,
#     "title": "Understanding Crowd Dynamics and Safety",
#     "description": "Explore the physics of crowds, personal space preferences, and how density, context, and wave movements contribute to dangerous situations. Learn safety tips.",
#     "created_at": "2025-11-17T11:39:05.742337Z",
#     "updated_at": "2025-11-17T11:39:05.742413Z",
#     "video_url": "https://www.youtube.com/watch?v=xHIydbaz6yg",
#     "questions": [
#         {
#             "id": 11,
#             "question_title": "What specific event or tradition is mentioned as taking place on November 11th in Cologne, making it a 'very special date'?",
#             "question_options": [
#                 "A national holiday",
#                 "The beginning of carnival season",
#                 "A major sporting event",
#                 "A quiet day for reflection"
#             ],
#             "answer": "The beginning of carnival season",
#             "created_at": "2025-11-17T11:39:05.752619Z",
#             "updated_at": "2025-11-17T11:39:05.752677Z"
#         },
#         {
#             "id": 12,
#             "question_title": "Which country's population was found to prefer the largest average personal distance from others, at 1.3 meters?",
#             "question_options": [
#                 "Germany",
#                 "Argentina",
#                 "Romania",
#                 "United States"
#             ],
#             "answer": "Romania",
#             "created_at": "2025-11-17T11:39:05.752748Z",
#             "updated_at": "2025-11-17T11:39:05.752772Z"
#         },
#         {
#             "id": 13,
#             "question_title": "In which country do people on average prefer the smallest personal distance from others, at 80 cm?",
#             "question_options": [
#                 "Germany",
#                 "Argentina",
#                 "Romania",
#                 "India"
#             ],
#             "answer": "Argentina",
#             "created_at": "2025-11-17T11:39:05.752821Z",
#             "updated_at": "2025-11-17T11:39:05.752839Z"
#         },
#         {
#             "id": 14,
#             "question_title": "According to the scientific discussion, what is NOT a key characteristic of a 'crowd' in a scientific context?",
#             "question_options": [
#                 "It should be a larger and not directly surveyable number of people.",
#                 "It should not change significantly if people come or go.",
#                 "It should consist of exactly 100 people.",
#                 "It should form a spatially unified unit."
#             ],
#             "answer": "It should consist of exactly 100 people.",
#             "created_at": "2025-11-17T11:39:05.752885Z",
#             "updated_at": "2025-11-17T11:39:05.752904Z"
#         },
#         {
#             "id": 15,
#             "question_title": "What density of persons per square meter can become dangerous in a moving crowd, according to the research?",
#             "question_options": [
#                 "1 person per square meter",
#                 "2 persons per square meter",
#                 "4 persons per square meter",
#                 "9 persons per square meter"
#             ],
#             "answer": "4 persons per square meter",
#             "created_at": "2025-11-17T11:39:05.752945Z",
#             "updated_at": "2025-11-17T11:39:05.752963Z"
#         },
#         {
#             "id": 16,
#             "question_title": "What approximate pressure, measured in Newtons, can be generated by a pushing crowd?",
#             "question_options": [
#                 "Up to 500 Newtons",
#                 "Over 1000 Newtons",
#                 "Over 4000 Newtons",
#                 "Around 100 Newtons"
#             ],
#             "answer": "Over 4000 Newtons",
#             "created_at": "2025-11-17T11:39:05.753006Z",
#             "updated_at": "2025-11-17T11:39:05.753024Z"
#         },
#         {
#             "id": 17,
#             "question_title": "Which specific location in Pamplona was used by researchers to study crowd dynamics during the San Fermines festival?",
#             "question_options": [
#                 "The main bullring",
#                 "The Plaza del Castillo",
#                 "The Plaza Consistorial",
#                 "A narrow street leading to the arena"
#             ],
#             "answer": "The Plaza Consistorial",
#             "created_at": "2025-11-17T11:39:05.753066Z",
#             "updated_at": "2025-11-17T11:39:05.753084Z"
#         },
#         {
#             "id": 18,
#             "question_title": "When the density in the Pamplona Plaza Consistorial reached approximately 4 persons per square meter, what significant change in dynamics was observed?",
#             "question_options": [
#                 "People started to disperse rapidly.",
#                 "The crowd became completely still and silent.",
#                 "The crowd began to swing, exhibiting wave-like movements.",
#                 "Individuals maintained perfect personal distance."
#             ],
#             "answer": "The crowd began to swing, exhibiting wave-like movements.",
#             "created_at": "2025-11-17T11:39:05.753126Z",
#             "updated_at": "2025-11-17T11:39:05.753144Z"
#         },
#         {
#             "id": 19,
#             "question_title": "What temporal pattern was discovered regarding the circular wave movements in the Pamplona crowd research?",
#             "question_options": [
#                 "They repeated every 60 seconds.",
#                 "They were random and unpredictable.",
#                 "They repeated every 18 seconds.",
#                 "They only occurred during specific musical interludes."
#             ],
#             "answer": "They repeated every 18 seconds.",
#             "created_at": "2025-11-17T11:39:05.753188Z",
#             "updated_at": "2025-11-17T11:39:05.753207Z"
#         },
#         {
#             "id": 20,
#             "question_title": "What is the primary reason mentioned for the danger of high pressure on the human body in a dense crowd?",
#             "question_options": [
#                 "It causes broken bones immediately.",
#                 "It makes movement impossible.",
#                 "It prevents the chest from expanding, leading to suffocation.",
#                 "It causes extreme psychological distress."
#             ],
#             "answer": "It prevents the chest from expanding, leading to suffocation.",
#             "created_at": "2025-11-17T11:39:05.753252Z",
#             "updated_at": "2025-11-17T11:39:05.753271Z"
#         }
#     ]
# }