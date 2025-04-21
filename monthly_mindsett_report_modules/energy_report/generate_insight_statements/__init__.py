from pathlib import Path
import pickle

from .preprocessing_for_statement import preprocessing_for_statement
from .insight_statements import insight_statements


def generate_insight_statements(db, df_meta_with_value, 
                                asset_group = "asset_class",
                                fixed_group_to_filter = [],
                                directory_to_savefile='./files/'): # todo: update the default value for directory

    df_for_statements = preprocessing_for_statement(df_meta_with_value, asset_group=asset_group, fixed_group_to_filter=fixed_group_to_filter)

    statements_list = insight_statements(db, df_for_statements, df_meta_with_value)

    # Specify the directory to save figures, if it does not exist, create it
    Path(directory_to_savefile).mkdir(parents=True, exist_ok=True)

    with open(directory_to_savefile+'statements.pkl', 'wb') as f:
        pickle.dump(statements_list, f)