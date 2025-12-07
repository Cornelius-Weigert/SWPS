import pandas as pd


def outlier_resources(log, case_col="case_id", activity_col="activity", resource_col="resource"):
    
    outliers = {

    }

    #+++++++Wenn die Ressource fehlt+++++++++++++++++++++++++
    missing_resource_rows = log[log[resource_col].isnull()]
    outliers['missing-resource'] = missing_resource_rows.index.tolist() 

    
    #+++++++Wenn eine Ressource ungewöhnlich viele Aktivitäten hat+++++++++++++
    activity_counts = log[resource_col].value_counts()
    threshold = activity_counts.quantile(0.95)  # 95. Perzentil als Schwellenwert
    high_activity_resources = activity_counts[activity_counts > threshold].index
    high_activity_rows = log[log[resource_col].isin(high_activity_resources)]
    outliers['high-activity-resources'] = high_activity_rows.index.tolist()   
    #+++++++Wenn eine Ressource ungewöhnlich wenige Aktivitäten hat+++++++++++++
    low_activity_resources = activity_counts[activity_counts < activity_counts.quantile(0.05)].index
    low_activity_rows = log[log[resource_col].isin(low_activity_resources)]
    outliers['low-activity-resources'] = low_activity_rows.index.tolist()   



    #+++++++Wenn eine Resource viele verschiedene Aktivitäten ausführt+++++++++++++
    resource_activity_counts = log.groupby(resource_col)[activity_col].nunique()
    diverse_activity_resources = resource_activity_counts[resource_activity_counts > resource_activity_counts.quantile(0.95)].index
    diverse_activity_rows = log[log[resource_col].isin(diverse_activity_resources)]
    outliers['many-activity-resources'] = diverse_activity_rows.index.tolist()   


    
    return outliers
