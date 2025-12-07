import pandas as pd


def data_attribute_outliers(log, attribute_col):
    
    outliers = {}
    
    #+++++++Wenn das Attribut fehlt+++++++++++++++++++++++++
    missing_attribute_rows = log[log[attribute_col].isnull()]
    outliers['missing-attribute'] = missing_attribute_rows.index.tolist() 


    
    #+++++++Wenn das Attribut ungewöhnliche Werte hat+++++++++++++
    value_counts = log[attribute_col].value_counts()
    threshold = value_counts.quantile(0.95)  # 95. Perzentil als Schwellenwert
    unusual_values = value_counts[value_counts < threshold].index
    unusual_value_rows = log[log[attribute_col].isin(unusual_values)]
    outliers['unusual-values'] = unusual_value_rows.index.tolist()   

    
    #+++++++Wenn das Attribut zu viele verschiedene Werte hat+++++++++++++
    unique_value_count = log[attribute_col].nunique()
    if unique_value_count > 100:  # Beispielschwellenwert
        outliers['too-many-unique-values'] = log.index.tolist()
    
    #+++++Wenn ein Wert unterschiedliche Datentypen hat++++++++++++++
    inconsistent_type_rows = []
    for value in log[attribute_col].dropna().unique():
        types = log[log[attribute_col] == value][attribute_col].apply(lambda x: type(x)).unique()
        if len(types) > 1:
            inconsistent_type_rows.extend(log[log[attribute_col] == value].index.tolist())
    outliers['inconsistent-types'] = inconsistent_type_rows

    
    return outliers
