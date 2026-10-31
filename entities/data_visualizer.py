"""Visualize training data, ideal functions, and mapped test points."""
from bokeh.plotting import figure, show


class DataVisualizer:
    """Draw training data, matched ideal functions and mapped test points."""

    def __init__(self, train_df, ideal_df, test_df, mapped_df, best_funcs):
        """Store the data frames and the chosen function pairs."""
        self.train_df = train_df
        self.ideal_df = ideal_df
        self.test_df = test_df
        self.mapped_df = mapped_df
        self.best_funcs = best_funcs

    def plot(self):
        """Draw training data, matched ideal functions and mapped test points."""
        colors = {'y1': 'blue', 'y2': 'green', 'y3': 'orange', 'y4': 'purple'}
        p = figure(title="Training data, ideal functions and mapped test points",
                   x_axis_label='x', y_axis_label='y',
                   width=900, height=600)

        # Training data: dots, one color per training function
        for y_col in ['y1', 'y2', 'y3', 'y4']:
            p.scatter(self.train_df['x'], self.train_df[y_col],
                      color=colors[y_col], size=3, alpha=0.4,
                      legend_label=f"Training {y_col}")

        # Matching ideal function: line in the same color as its training data
        for train_y, ideal_y in self.best_funcs.items():
            p.line(self.ideal_df['x'], self.ideal_df[ideal_y],
                   color=colors[train_y], line_width=2,
                   legend_label=f"Ideal {ideal_y} (fits {train_y})")

        # Mapped test points: triangles in the color of their ideal function
        mapped = self.mapped_df[self.mapped_df['matched_ideal_function'].notna()]
        for train_y, ideal_y in self.best_funcs.items():
            pts = mapped[mapped['matched_ideal_function'] == ideal_y]
            p.scatter(pts['x'], pts['y'], marker='triangle', size=10,
                      color=colors[train_y], line_color='black',
                      legend_label=f"Test points mapped to {ideal_y}")

        p.legend.click_policy = "hide"
        p.legend.location = "top_left"
        show(p)