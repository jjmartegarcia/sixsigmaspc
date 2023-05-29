"""
Rule #4 Zone C: 7 or more consecutive points on one side of the average (in Zone C or beyond).
"""

import pandas as pd
from SPC import Rule
pd.options.mode.chained_assignment = None  # default='warn'

class Rule04(Rule):
    rule_id = "R04" # The unique rule idenfitier.

    def execute(self, df: pd.DataFrame):
        """ Rule execution.

            :param df: The dataframe.
        """

        # Create a new signal column.
        df[self.rule_id] = False

        # Iterate the rows.
        for i in range(7, len(df)):
            # Check lower.
            if(df['value'][i] < df['CL'][i] and
               df['value'][i-1] < df['CL'][i-1] and
               df['value'][i-2] < df['CL'][i-2] and
               df['value'][i-3] < df['CL'][i-3] and
               df['value'][i-4] < df['CL'][i-4] and
               df['value'][i-5] < df['CL'][i-5] and
               df['value'][i-6] < df['CL'][i-6]):
                df[self.rule_id][i] = True
                df["SIGNAL"][i] = True

            # Check upper.
            if(df['value'][i] > df['CL'][i] and
               df['value'][i-1] > df['CL'][i-1] and
               df['value'][i-2] > df['CL'][i-2] and
               df['value'][i-3] > df['CL'][i-3] and
               df['value'][i-4] > df['CL'][i-4] and
               df['value'][i-5] > df['CL'][i-5] and
               df['value'][i-6] > df['CL'][i-6]):
                df[self.rule_id][i] = True
                df["SIGNAL"][i] = True
