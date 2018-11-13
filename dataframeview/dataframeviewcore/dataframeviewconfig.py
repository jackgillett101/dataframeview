from .dataframepivottree import PivotTree
from .dataframeaggregatetree import AggregateTree


# A DataFrameViewConfig is a set of sorts, v_pivots and filters that map the underlying data in a df into
# a concrete set of pivoted rows that appear in the viewer

# It has methods that take the df underlying data, filter out rows, pivot the remainder (which
# generates additional abstract 'pivot' rows for each pivot category, whose values are the
# aggregate of the underlying values), and finally perform sorts on the values within each pivot
class DataFrameViewConfig:

    def __init__(self, columns=[], sorts=[], v_pivots=[], filters=[]):

        # Columns is the subset of columns we wish to show in the viewer
        self.columns = columns

        # Sorts is an array of tuples of ( Column Name, Bool ) with Bool == True for ascending
        self.sorts = sorts

        # v_pivots is an array of column names to pivot on
        self.v_pivots = v_pivots

        # Filters is an array of Filter-class objects, as defined above, that filter specific columns
        self.filters = filters

    def get_visible_columns(self):
        return self.columns

    def get_pivot_columns(self):
        return self.v_pivots

    def get_filters(self):
        return self.filters

    # This is the function that returns the ultimate payload - an iterator over *visible* rows in the pop-up.
    # This includes the 'base' rows from the original df, but also the aggregate pivot headers - one per
    # pivot value at each level. These get sent to the GUI elements to create visible widgets from
    def iterator_over_visible_rows(self, df):
        filtered_df = self.filter_data_frame(df)
        aggregate_tree = self.v_pivot_data_frame(filtered_df)
        sorted_aggregate_tree = self.sort_aggregate_tree(aggregate_tree)
        sorted_results = self.coalesce_data_tree(sorted_aggregate_tree)

        return sorted_results

    # First step to construction of a data table is application of the filters to the raw data, taking out
    # anything the user doesn't want right at the beginning
    def filter_data_frame(self, df):
        for data_filter in self.filters:
            df = data_filter.apply_filter(df)

        return df

    # To sort a set of aggregate results, simply recurse down the tree, sorting the sub-branchs for a given
    # node according to the specified sorts
    def sort_aggregate_tree(self, aggregate_tree):
        # Sort the tree in reverse sort order - this assumes we use a STABLE SORT
        # TODO: could optimise sort by going the correct way through the sort columns, and only re-sorting
        # sub-elements if strictly required.
        for (sort_column, descending) in reversed(self.sorts):
            # Note usability hack here... default sort is ascending, but I always expect the GUI to sort largest
            # elements to the top on clicking, so I have reversed this below
            aggregate_tree.sort(sort_column, not descending)

        return aggregate_tree

    # To vertical pivot a dataframe, take the pivots one-by-one from the front. Break the df up onto the different
    # values in each pivot column and treat as independent table. Then iteratively pivot each sub-table on
    # the next pivot column, and so on... Call this structure a 'pivotTree'
    def v_pivot_data_frame(self, df):
        if len(self.v_pivots) == 0:
            aggregate_tree = AggregateTree(df, df.dtypes, ("Root", None))
        else:
            pivot_tree = PivotTree(df, self.v_pivots)
            aggregate_tree = pivot_tree.get_aggregate_tree()

        return aggregate_tree

    # Take the datatree's aggregate_tree and return rows
    def coalesce_data_tree(self, aggregate_tree, parent='root'):
        data = [{'parent': parent, 'name': id(aggregate_tree), 'value': aggregate_tree.aggregate_value}]

        for (key, branch) in aggregate_tree.branches.items():
            data += self.coalesce_data_tree(branch, id(aggregate_tree))

        if aggregate_tree.is_leaf():
            data.append({'parent': id(aggregate_tree), 'name': None, 'value': aggregate_tree.data_frame})

        return data

    def re_sort_on_column(self, column, ascending=False):
        self.sorts = [(column, ascending)]
