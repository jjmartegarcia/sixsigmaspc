"""
Rule #3 Zone B: 4 out of 5 consecutive points in Zone B or beyond.
"""

import pandas as pd
from SPC import Rule
pd.options.mode.chained_assignment = None  # default='warn'

class Rule03(Rule):
    rule_id = "R03" # The unique rule idenfitier.

    def execute(self, df: pd.DataFrame):
        """ Rule execution.

            :param df: The dataframe.
        """

        # Create a new signal column.
        df[self.rule_id] = False

        # Iterate the rows.
        for i in range(5, len(df)):
            # Check lower.
            if((df['value'][i-4] < df['-1s'][i-4] and df['value'][i-3] < df['-1s'][i-3] and df['value'][i-2] < df['-1s'][i-2] and df['value'][i-1] < df['-1s'][i-1]) or
               (df['value'][i-4] < df['-1s'][i-4] and df['value'][i-3] < df['-1s'][i-3] and df['value'][i-2] < df['-1s'][i-2] and df['value'][i] < df['-1s'][i]) or
               (df['value'][i-4] < df['-1s'][i-4] and df['value'][i-2] < df['-1s'][i-2] and df['value'][i-1] < df['-1s'][i-1] and df['value'][i] < df['-1s'][i]) or
               (df['value'][i-4] < df['-1s'][i-4] and df['value'][i-3] < df['-1s'][i-3] and df['value'][i-1] < df['-1s'][i-1] and df['value'][i] < df['-1s'][i]) or
               (df['value'][i-3] < df['-1s'][i-3] and df['value'][i-2] < df['-1s'][i-2] and df['value'][i-1] < df['-1s'][i-1] and df['value'][i] < df['-1s'][i])):
                df[self.rule_id][i] = True
                df["SIGNAL"][i] = True

            # Check upper.
            if((df['value'][i-4] > df['+1s'][i-4] and df['value'][i-3] > df['+1s'][i-3] and df['value'][i-2] > df['+1s'][i-2] and df['value'][i-1] > df['+1s'][i-1]) or
               (df['value'][i-4] > df['+1s'][i-4] and df['value'][i-3] > df['+1s'][i-3] and df['value'][i-2] > df['+1s'][i-2] and df['value'][i] > df['+1s'][i]) or
               (df['value'][i-4] > df['+1s'][i-4] and df['value'][i-2] > df['+1s'][i-2] and df['value'][i-1] > df['+1s'][i-1] and df['value'][i] > df['+1s'][i]) or
               (df['value'][i-4] > df['+1s'][i-4] and df['value'][i-3] > df['+1s'][i-3] and df['value'][i-1] > df['+1s'][i-1] and df['value'][i] > df['+1s'][i]) or
               (df['value'][i-3] > df['+1s'][i-3] and df['value'][i-2] > df['+1s'][i-2] and df['value'][i-1] > df['+1s'][i-1] and df['value'][i] > df['+1s'][i])):
                df[self.rule_id][i] = True
                df["SIGNAL"][i] = True
