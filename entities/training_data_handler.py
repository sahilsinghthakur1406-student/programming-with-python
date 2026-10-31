"""Select ideal functions and calculate their training deviations."""
import pandas as pd


class TrainingDataHandler:
    """Select the best ideal functions and compute their max training deviations."""

    def __init__(self, db_manager):
        """Store the database manager and prepare empty results."""
        self.db_manager = db_manager
        self.train_df = None
        self.ideal_df = None
        self.best_functions = {}  # { train_y_col: ideal_y_col }
        self.max_deviations = {}  # { ideal_y_col: max_deviation }

    def load_data_from_db(self):
        """Load training and ideal data from the SQLite database."""
        self.train_df = self.db_manager.load_table_as_df('training_data')
        self.ideal_df = self.db_manager.load_table_as_df('ideal_functions')

    def select_best_functions(self, train_y_cols):
        """Pick the ideal function with the smallest SSE for each training column."""
        for y_col in train_y_cols:
            min_sse = float('inf')
            best_func = None

            for ideal_col in self.ideal_df.columns[1:]:  # skip 'x'
                train_sub = self.train_df[['x', y_col]].rename(columns={y_col: 'train_y'})
                ideal_sub = self.ideal_df[['x', ideal_col]].rename(columns={ideal_col: 'ideal_y'})
                merged = pd.merge(train_sub, ideal_sub, on='x', how='inner')

                sse = ((merged['train_y'] - merged['ideal_y']) ** 2).sum()
                if sse < min_sse:
                    min_sse = sse
                    best_func = ideal_col

            self.best_functions[y_col] = best_func

            # Maximum deviation (D_max) between training data and the chosen function
            train_sub = self.train_df[['x', y_col]].rename(columns={y_col: 'train_y'})
            ideal_sub = self.ideal_df[['x', best_func]].rename(columns={best_func: 'ideal_y'})
            merged = pd.merge(train_sub, ideal_sub, on='x', how='inner')
            max_dev = (merged['train_y'] - merged['ideal_y']).abs().max()
            self.max_deviations[best_func] = max_dev

        return self.best_functions