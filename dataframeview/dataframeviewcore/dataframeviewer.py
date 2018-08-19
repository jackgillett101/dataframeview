import dataframeviewconfig
import dataframeview


# This is the entry point into the rest of the functionality. Create a DataFrameView for a dataframe and everything
# else will kick off!!
class DataFrameViewer:
    def __init__(self, df, columns=[], sorts=[], v_pivots=[], filters=[]):
        # TODO: check if this view and this df are compatible (eg. do the pivots, views etc. exist in the df)
        # ... Should warn/die if not... eg. bad capitalisation!)

        # If columns are empty, we default to 'show all columns' even if an empty array was passed in on purpose,
        # because showing no columns is silly
        if len(columns) == 0:
            columns = list(df.columns.values)

        view = dataframeviewconfig.DataFrameViewConfig(columns, sorts, v_pivots, filters)
        tvw = dataframeview.TreeViewWindow(df, view)
