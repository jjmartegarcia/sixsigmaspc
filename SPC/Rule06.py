"""
Rule #6 Mixture: 8 consecutive points with no points in Zone C.
"""

import pandas as pd
from SPC import Rule
pd.options.mode.chained_assignment = None  # default='warn'

class Rule06(Rule):
    rule_id = "R06" # The unique rule idenfitier.

    def execute(self, df: pd.DataFrame):
        """ Rule execution.

            :param df: The dataframe.
        """

        # Create a new signal column.
        df[self.rule_id] = False

        # Iterate the rows.
        for i in range(8, len(df)):
            # Check.
            if((df['value'][i] < df['-1s'][i] or df['value'][i] > df['+1s'][i]) and
               (df['value'][i-1] < df['-1s'][i-1] or df['value'][i-1] > df['+1s'][i-1]) and
               (df['value'][i-2] < df['-1s'][i-2] or df['value'][i-2] > df['+1s'][i-2]) and
               (df['value'][i-3] < df['-1s'][i-3] or df['value'][i-3] > df['+1s'][i-3]) and
               (df['value'][i-4] < df['-1s'][i-4] or df['value'][i-4] > df['+1s'][i-4]) and
               (df['value'][i-5] < df['-1s'][i-5] or df['value'][i-5] > df['+1s'][i-5]) and
               (df['value'][i-6] < df['-1s'][i-6] or df['value'][i-6] > df['+1s'][i-6]) and
               (df['value'][i-7] < df['-1s'][i-7] or df['value'][i-7] > df['+1s'][i-7])):
                df[self.rule_id][i] = True
                df["SIGNAL"][i] = True
