"""Map test data points to the selected ideal functions."""
import numpy as np
import pandas as pd


class TestDataMapper:
    """Map test data to chosen ideal functions using the sqrt(2) deviation threshold."""

    def __init__(self, db_manager, ideal_df, chosen_functions, max_deviations):
        """Store the database manager, ideal data, chosen functions and D_max values."""
        self.db_manager = db_manager
        self.ideal_df = ideal_df
        self.chosen_functions = chosen_functions
        self.max_deviations = max_deviations
        self.mapped_df = None

    def map_test_data(self):
        """Map every test point to an ideal function if it is within D_max * sqrt(2)."""
        test_df = self.db_manager.load_table_as_df('test_data')
        y_cols = [col for col in test_df.columns if col != 'x']
        y_col = y_cols[0]

        mapped_data = []
        for _, row in test_df.iterrows():
            x_test, y_test = row['x'], row[y_col]
            ideal_row = self.ideal_df[self.ideal_df['x'] == x_test]

            if ideal_row.empty:
                mapped_data.append({'x': x_test, 'y': y_test,
                                    'matched_ideal_function': None, 'deviation': None})
                continue

            best_match = None
            min_deviation = float('inf')

            for func in self.chosen_functions:
                ideal_y = ideal_row[func].values[0]
                dev = abs(y_test - ideal_y)

                # Threshold constraint: deviation <= D_max * sqrt(2)
                threshold = self.max_deviations[func] * np.sqrt(2)
                if dev <= threshold and dev < min_deviation:
                    min_deviation = dev
                    best_match = func

            mapped_data.append({
                'x': x_test,
                'y': y_test,
                'matched_ideal_function': best_match,
                'deviation': min_deviation if best_match else None
            })

        self.mapped_df = pd.DataFrame(mapped_data)

        # Save only the mapped points, using the column names of Table 3
        to_save = self.mapped_df.dropna(subset=['matched_ideal_function'])
        to_save = to_save.rename(columns={
            'matched_ideal_function': 'ideal_func_no',
            'deviation': 'delta_y',
        })
        to_save = to_save[['x', 'y', 'delta_y', 'ideal_func_no']]
        self.db_manager.insert_dataframe(to_save, 'mapped_test_data')
        return self.mapped_df