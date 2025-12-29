OUTLIER_DESCRIPTIONS = {
    "Fehlende_Ressource": {
        "description": "Dieses Ereignis hat keine zugeordnete Ressource. "
                       "Dies kann auf unvollständige oder fehlerhafte Log-Daten hinweisen."
    },

    "Ressource_sehr_aktiv": {
        "description": "Diese Ressource führt deutlich mehr Aktivitäten aus als andere. "
                       "Mögliche Ursachen sind Überlastung, Automatisierung oder fehlerhafte Zuordnung."
    },

    "Ressource_wenig_aktiv": {
        "description": "Diese Ressource kommt im Event Log nur sehr selten vor. "
                       "Dies kann auf eine Sonderrolle oder auf fehlende Date"
                       "n hindeuten."
    },

    "Ressource_vielfältige_Aktivitäten": {
        "description": "Die Ressource führt eine ungewöhnlich große Anzahl unterschiedlicher Aktivitäten aus. "
                       "Dies kann auf fehlende Rollentrennung oder inkonsistente Modellierung hinweisen."
    },

    "Zeitstempel_in_Zukunft": {
        "description": "Der Zeitstempel dieses Events liegt nach dem aktuellen Zeitpunkt. "
                       "Dies deutet meist auf fehlerhafte Systemzeiten oder Datenimporte hin."
    },

    "Fehlender_Zeitstempel": {
        "description": "Für dieses Ereignis ist kein Zeitstempel vorhanden. "
                       "Eine zeitliche Analyse des Prozesses ist dadurch eingeschränkt."
    },

    "Lange_Aktivitätsdauer": {
        "description": "Die Zeit zwischen zwei aufeinanderfolgenden Aktivitäten ist ungewöhnlich lang "
                       "im Vergleich zu ähnlichen Aktivitätinstanzen."
    },

    "Kurze_Aktivitätsdauer": {
        "description": "Die Zeit zwischen zwei Aktivitäten ist ungewöhnlich kurz. "
                       "Dies kann auf automatisch erzeugte Events oder Messfehler hinweisen."
    },

    "Negative_Aktivitätsdauer": {
        "description": "Der Zeitstempel eines Events liegt vor dem vorherigen Event im gleichen Case. "
                       "Dies stellt eine zeitliche Inkonsistenz dar."
    },

    "Lange_Traces": {
        "description": "Diese Prozessinstanzrn enthalten deutlich mehr Events als üblich "
                       "und könnte auf Schleifen oder Sonderfälle hindeuten."
    },

    "Kurze_Traces": {
        "description": "Diese Traces enthalten sehr wenige Events, könnte unvollständig oder abgebrochen sein."
    },

    "Traces_viele_Aktivitäten": {
        "description": "Diese Prozessinstanzen zeigen eine ungewöhnlich hohe Variantenvielfalt "
                       "und damit eine hohe Prozesskomplexität."
    },

    "Traces_wenig_Aktivitäten": {
        "description": "Diese Traces bestehen aus sehr wenigen unterschiedlichen Aktivitäten "
                       "und können auf vereinfachte oder fehlerhafte Abläufe hinweisen."
    },

    "Ungewöhnliche_Tracesequenz": {
        "description": "Die Aktivitätsabfolge dieses Traces kommt im gesamten Event Log nur einmal vor "
                       "und stellt daher eine seltene Prozessvariante dar."
    },

    "Fehlende_Aktivitäten_im_Trace": {
        "description": "Diese Prozessinstanzen enthalten weniger als zwei Events "
                       "und sind für eine vollständige Prozessanalyse nur eingeschränkt geeignet."
    }
}
