import matplotlib.pyplot as plt

# ======================
# 5. Resource / String Analyse mit Diagramm
# ===========================
def resources(df, event_col="concept:name", resource_col="org:resource"):
    if resource_col not in df.columns:
        print("->>>Keine Ressourcenspalten gefunden")
        return
    
    activities=df[event_col].unique()
    
    for act in activities:
        sub = df[df[event_col] == act]
        counts = sub[resource_col].value_counts()

        plt.figure(figsize=(7, 4))
        counts.plot(kind="bar")
        plt.title(f"Ressourcen für Aktivität: {act}")
        plt.xlabel("Resource")
        plt.ylabel("Menge")
        
        plt.tight_layout()
        plt.show()
