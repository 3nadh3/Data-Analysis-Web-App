import pandas as pd

def analyze_data(df):
    df = pd.DataFrame(df)  # Ensure df is a DataFrame
    df['Gender'] = df['Gender'].str.lower()
    df['Caste'] = df['Caste'].str.lower()

    # Map SC subcastes to SC and ST subcastes to ST
    sc_mapping = {'sc-a': 'sc', 'sc-b': 'sc', 'sc-c': 'sc', 'sc-d': 'sc'}
    st_mapping = {'st-a': 'st', 'st-b': 'st', 'st-c': 'st', 'st-d': 'st'}
    bc_mapping = {'bc-a': 'bc', 'bc-b': 'bc', 'bc-c': 'bc', 'bc-d': 'bc'}
    
    df['Caste'] = df['Caste'].replace(bc_mapping)
    
    df['Caste'] = df['Caste'].replace(sc_mapping)
    df['Caste'] = df['Caste'].replace(st_mapping)

    result_summary = df.groupby(['Caste', 'Gender', 'Result']).size().unstack(fill_value=0)

    result_summary['Total_Pass'] = result_summary['PASS']
    result_summary['Total_Fail'] = result_summary['FAIL']

    result_summary = result_summary[['Total_Pass', 'Total_Fail']]

    analysis_result = []
    for index, row in result_summary.iterrows():
        analysis_result.append({
            'Caste': index[0],
            'Gender': index[1],
            'Total_Pass': row['Total_Pass'],
            'Total_Fail': row['Total_Fail']
        })

    return analysis_result
