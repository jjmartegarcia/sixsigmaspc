"""
Rule #8 Over-control: 14 consecutive points alternating up and down.
"""

import pandas as pd
from SPC import Rule
pd.options.mode.chained_assignment = None  # default='warn'

class Rule08(Rule):
    rule_id = "R08" # The unique rule idenfitier.

    def execute(self, df: pd.DataFrame):
        """ Rule execution.

            :param df: The dataframe.
        """
        # Create a new signal column.
        df[self.rule_id] = False

        # Iterate the rows.
        for i in range(14, len(df)):
            # Check.
            if(((df['value'][i] > df['value'][i-1]) and
               (df['value'][i-1] < df['value'][i-2]) and
               (df['value'][i-2] > df['value'][i-3]) and
               (df['value'][i-3] < df['value'][i-4]) and
               (df['value'][i-4] > df['value'][i-5]) and
               (df['value'][i-5] < df['value'][i-6]) and
               (df['value'][i-6] > df['value'][i-7]) and
               (df['value'][i-7] < df['value'][i-8]) and
               (df['value'][i-8] > df['value'][i-9]) and
               (df['value'][i-9] < df['value'][i-10]) and
               (df['value'][i-10] > df['value'][i-11]) and
               (df['value'][i-11] < df['value'][i-12]) and
               (df['value'][i-12] > df['value'][i-13])) or
               ((df['value'][i] < df['value'][i-1]) and
               (df['value'][i-1] > df['value'][i-2]) and
               (df['value'][i-2] < df['value'][i-3]) and
               (df['value'][i-3] > df['value'][i-4]) and
               (df['value'][i-4] < df['value'][i-5]) and
               (df['value'][i-5] > df['value'][i-6]) and
               (df['value'][i-6] < df['value'][i-7]) and
               (df['value'][i-7] > df['value'][i-8]) and
               (df['value'][i-8] < df['value'][i-9]) and
               (df['value'][i-9] > df['value'][i-10]) and
               (df['value'][i-10] < df['value'][i-11]) and
               (df['value'][i-11] > df['value'][i-12]) and
               (df['value'][i-12] < df['value'][i-13]))):
                df[self.rule_id][i] = True
                df["SIGNAL"][i] = True
