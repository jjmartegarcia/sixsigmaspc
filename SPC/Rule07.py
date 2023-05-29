"""
Rule #7 Stratification: 15 consecutive points in Zone C.
"""

import pandas as pd
from SPC import Rule
pd.options.mode.chained_assignment = None  # default='warn'

class Rule07(Rule):
    rule_id = "R07" # The unique rule idenfitier.

    def execute(self, df: pd.DataFrame):
        """ Rule execution.

            :param df: The dataframe.
        """

        # Create a new signal column.
        df[self.rule_id] = False

        # Iterate the rows.
        for i in range(15, len(df)):
            # Check.
            if(((df['value'][i] < df['CL'][i] and df['value'][i] > df['-1s'][i]) or (df['value'][i] > df['CL'][i] and df['value'][i] < df['+1s'][i])) and
               ((df['value'][i-1] < df['CL'][i-1] and df['value'][i-1] > df['-1s'][i-1]) or (df['value'][i-1] > df['CL'][i-1] and df['value'][i-1] < df['+1s'][i-1])) and
               ((df['value'][i-2] < df['CL'][i-2] and df['value'][i-2] > df['-1s'][i-2]) or (df['value'][i-2] > df['CL'][i-2] and df['value'][i-2] < df['+1s'][i-2])) and
               ((df['value'][i-3] < df['CL'][i-3] and df['value'][i-3] > df['-1s'][i-3]) or (df['value'][i-3] > df['CL'][i-3] and df['value'][i-3] < df['+1s'][i-3])) and
               ((df['value'][i-4] < df['CL'][i-4] and df['value'][i-4] > df['-1s'][i-4]) or (df['value'][i-4] > df['CL'][i-4] and df['value'][i-4] < df['+1s'][i-4])) and
               ((df['value'][i-5] < df['CL'][i-5] and df['value'][i-5] > df['-1s'][i-5]) or (df['value'][i-5] > df['CL'][i-5] and df['value'][i-5] < df['+1s'][i-5])) and
               ((df['value'][i-6] < df['CL'][i-6] and df['value'][i-6] > df['-1s'][i-6]) or (df['value'][i-6] > df['CL'][i-6] and df['value'][i-6] < df['+1s'][i-6])) and
               ((df['value'][i-7] < df['CL'][i-7] and df['value'][i-7] > df['-1s'][i-7]) or (df['value'][i-7] > df['CL'][i-7] and df['value'][i-7] < df['+1s'][i-7])) and
               ((df['value'][i-8] < df['CL'][i-8] and df['value'][i-8] > df['-1s'][i-8]) or (df['value'][i-8] > df['CL'][i-8] and df['value'][i-8] < df['+1s'][i-8])) and
               ((df['value'][i-9] < df['CL'][i-9] and df['value'][i-9] > df['-1s'][i-9]) or (df['value'][i-9] > df['CL'][i-9] and df['value'][i-9] < df['+1s'][i-9])) and
               ((df['value'][i-10] < df['CL'][i-10] and df['value'][i-10] > df['-1s'][i-10]) or (df['value'][i-10] > df['CL'][i-10] and df['value'][i-10] < df['+1s'][i-10])) and
               ((df['value'][i-11] < df['CL'][i-11] and df['value'][i-11] > df['-1s'][i-11]) or (df['value'][i-11] > df['CL'][i-11] and df['value'][i-11] < df['+1s'][i-11])) and
               ((df['value'][i-12] < df['CL'][i-12] and df['value'][i-12] > df['-1s'][i-12]) or (df['value'][i-12] > df['CL'][i-12] and df['value'][i-12] < df['+1s'][i-12])) and
               ((df['value'][i-13] < df['CL'][i-13] and df['value'][i-13] > df['-1s'][i-13]) or (df['value'][i-13] > df['CL'][i-13] and df['value'][i-13] < df['+1s'][i-13])) and
               ((df['value'][i-14] < df['CL'][i-14] and df['value'][i-14] > df['-1s'][i-14]) or (df['value'][i-14] > df['CL'][i-14] and df['value'][i-14] < df['+1s'][i-14]))):
                df[self.rule_id][i] = True
                df["SIGNAL"][i] = True
