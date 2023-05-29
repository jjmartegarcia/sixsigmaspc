"""
Rule #5 Trend: 7 consecutive points trending up or trending down.
"""

import pandas as pd
from SPC import Rule
pd.options.mode.chained_assignment = None  # default='warn'

class Rule05(Rule):
    rule_id = "R05" # The unique rule idenfitier.

    def execute(self, df: pd.DataFrame):
        """ Rule execution.

            :param df: The dataframe.
        """

        # Create a new signal column.
        df[self.rule_id] = False

        # Iterate the rows.
        for i in range(7, len(df)):
            # Check lower.
            if(df['value'][i] < df['value'][i-1] and
              df['value'][i-1] < df['value'][i-2] and
              df['value'][i-2] < df['value'][i-3] and
              df['value'][i-3] < df['value'][i-4] and
              df['value'][i-4] < df['value'][i-5] and
              df['value'][i-5] < df['value'][i-6]):
                df[self.rule_id][i] = True
                df["SIGNAL"][i] = True

            # Check upper.
            if(df['value'][i] > df['value'][i-1] and
              df['value'][i-1] > df['value'][i-2] and
              df['value'][i-2] > df['value'][i-3] and
              df['value'][i-3] > df['value'][i-4] and
              df['value'][i-4] > df['value'][i-5] and
              df['value'][i-5] > df['value'][i-6]):
                df[self.rule_id][i] = True
                df["SIGNAL"][i] = True
