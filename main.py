"""Ideal-function selection and test-data mapping (main program)."""
from pathlib import Path

import pandas as pd

from data_loader import CsvLoader
from entities.database_manager import DatabaseManager
from entities.data_visualizer import DataVisualizer
from entities.test_data_mapper import TestDataMapper
from entities.training_data_handler import TrainingDataHandler


if __name__ == "__main__":
    data_dir = Path(__file__).resolve().parent / "data"
    train_csv_path = str(data_dir / "train.csv")
    ideal_csv_path = str(data_dir / "ideal.csv")
    test_csv_path = str(data_dir / "test.csv")
    db_file_path = Path(__file__).resolve().parent / "assignment.db"

    db_mgr = DatabaseManager(db_file_path)
    db_mgr.create_tables()

    train_df = CsvLoader(train_csv_path, ["x", "y1", "y2", "y3", "y4"]).load()
    ideal_df = CsvLoader(ideal_csv_path, ["x"] + [f"y{i}" for i in range(1, 51)]).load()
    test_df = CsvLoader(test_csv_path, ["x", "y"]).load()

    db_mgr.insert_dataframe(train_df, 'training_data')
    db_mgr.insert_dataframe(ideal_df, 'ideal_functions')
    db_mgr.insert_dataframe(test_df, 'test_data')

    train_handler = TrainingDataHandler(db_mgr)
    train_handler.load_data_from_db()

    best_funcs = train_handler.select_best_functions(['y1', 'y2', 'y3', 'y4'])
    print("Best functions selected:", best_funcs)

    mapper = TestDataMapper(
        db_mgr,
        train_handler.ideal_df,
        list(best_funcs.values()),
        train_handler.max_deviations
    )


    mapped_df = mapper.map_test_data()
    print("Mapped points:", mapped_df['matched_ideal_function'].notna().sum(),
          "of", len(mapped_df))
    print("Mapping completed! All data written to SQLite database.")

    visualizer = DataVisualizer(
        train_handler.train_df,
        train_handler.ideal_df,
        test_df,
        mapped_df,
        best_funcs
    )
    visualizer.plot()

    print("Max deviations (D_max):", train_handler.max_deviations)
    print(mapped_df['matched_ideal_function'].value_counts())
    print("Rows - train:", len(train_df), "ideal:", len(ideal_df), "test:", len(test_df))
    print("All test x in ideal table:", test_df['x'].isin(ideal_df['x']).all())

    unmapped = mapped_df[mapped_df['matched_ideal_function'].isna()]
    ideal_idx = train_handler.ideal_df.set_index('x')
    gaps = []
    for _, r in unmapped.iterrows():
        if r['x'] in ideal_idx.index:
            gaps.append(min(abs(r['y'] - ideal_idx.loc[r['x'], f])
                            for f in best_funcs.values()))
    print("Unmapped:", len(unmapped), "with a matching x:", len(gaps))
    print(pd.Series(gaps).describe())


    