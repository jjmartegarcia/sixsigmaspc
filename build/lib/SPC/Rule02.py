"""
Rule #2 Zone A: 2 out of 3 consecutive points in Zone A or beyond.
"""

import pandas as pd
from SPC import Rule
pd.options.mode.chained_assignment = None  # default='warn'

class Rule02(Rule):
    rule_id = "R02" # The unique rule idenfitier.

    def execute(self, df: pd.DataFrame):
        """ Rule execution.

            :param df: The dataframe.
        """

        # Create a new signal column.
        df[self.rule_id] = False

        # Iterate the rows.
        for i in range(3, len(df)):
            # Check lower.
            if((df['value'][i] < df['-2s'][i] and df['value'][i-1] < df['-2s'][i-1]) or 
               (df['value'][i-1] < df['-2s'][i-1] and df['value'][i-2] < df['-2s'][i-2]) or
               (df['value'][i] < df['-2s'][i] and df['value'][i-2] < df['-2s'][i-2])):
                df[self.rule_id][i] = True
                df["SIGNAL"][i] = True

            # Check upper.
            if((df['value'][i] > df['+2s'][i] and df['value'][i-1] > df['+2s'][i-1]) or
               (df['value'][i-1] > df['+2s'][i-1] and df['value'][i-2] > df['+2s'][i-2]) or
               (df['value'][i] > df['+2s'][i] and df['value'][i-2] > df['+2s'][i-2])):
                df[self.rule_id][i] = True
                df["SIGNAL"][i] = True
