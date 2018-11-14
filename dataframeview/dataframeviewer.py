from .dataframeviewcore import DataFrameViewConfig
from .dataframeguielements import TreeViewWindow
from .dataframeviewfilters import DataFrameViewFilter


# This is the entry point into the rest of the functionality. Create a DataFrameViewer for a dataframe and
# everything else will kick off!!

# Filters must be specified as a triplet of (column, type, value)
class DataFrameViewer:
    def __init__(self, df, columns=[], sorts=[], v_pivots=[], filters=[]):
        # TODO: check if this view and this df are compatible (eg. do the pivots, views etc. exist in the df)
        # ... Should warn/die if not... eg. bad capitalisation!)

        # If columns are empty, we default to 'show all columns' even if an empty array was passed in on purpose,
        # because showing no columns is silly
        if len(columns) == 0:
            columns = list(df.columns.values)

        self.setup_viewer(df, columns, sorts, v_pivots, filters)

    def setup_viewer(self, df, columns=[], sorts=[], v_pivots=[], filters=[]):

        filter_list = []
        for column, type, value in filters:
            filter_list.append(DataFrameViewFilter(column, type, value, pretty=True))

        view = DataFrameViewConfig(self, columns, sorts, v_pivots, filter_list)
        tvw = TreeViewWindow(self, df, view)
