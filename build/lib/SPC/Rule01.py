"""
Rule #1 Beyond limits: one or more points are beyond the control limits.
"""

import pandas as pd
from SPC import Rule
pd.options.mode.chained_assignment = None  # default='warn'

class Rule01(Rule):
    rule_id = "R01" # The unique rule idenfitier.

    def execute(self, df: pd.DataFrame):
        """ Rule execution.

            :param df: The dataframe.
        """

        # Create a new signal column.
        df[self.rule_id] = False

        # Iterate the rows.
        for i in range(len(df)):
            # Check lower.
            if df['value'][i] < df['LCL'][i]:
                df[self.rule_id][i] = True
                df["SIGNAL"][i] = True

            # Check upper.
            if df['value'][i] > df['UCL'][i]:
                df[self.rule_id][i] = True
                df["SIGNAL"][i] = True
