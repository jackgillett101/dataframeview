import numpy as np
import pandas as pd

from collections import OrderedDict


# A utility function to aggregate the result of multiple rows. Since we have a pivot tree, any subset of rows sharing
# the same pivot values should show a single aggregate row until the pivot is opened up
def create_sum_row(df, name, column_types):
    series = {'row_tag': ['%s: %s' % (name[0], name[1])]}

    # TODO: Enable other aggregation choices! eg. max/min for numeric, specified by column in the view controller
    # Currently only supported aggregations are summing for integers, or 'uniq'-ing for others, such that only if all
    # underlying values are the same will the aggregate row show a value.
    for (name, column) in df.iteritems():
        # Number aggregation (summing)
        if np.issubdtype(column, np.number):
            series[name] = [column.sum()]

        # Default aggregation (unique values only)
        else:
            first_flag = True
            for value in column:
                if first_flag:
                    initial_value = value
                    series[name] = initial_value
                    first_flag = False
                if value != initial_value:
                    series[name] = None
                    break

    row_frame = pd.DataFrame(series)
    row_frame = row_frame.set_index('row_tag')

    return row_frame


# A class to represent the ultimate tabular form of the table, post pivots and filters
class AggregateTree:
    def __init__(self, pivot_tree, column_types, pivot_value):

        # Use an OrderedDict to insert branches. This way, we can subsequently sort the order of
        # the branches according to the sort columns, and that order will be frozen into the tree
        self.branches = OrderedDict()
        self.pivot_value = pivot_value

        if isinstance(pivot_tree, pd.DataFrame):
            self.leaf = True
            self.data_frame = pivot_tree

            self.aggregate_value = create_sum_row(pivot_tree, pivot_value, column_types)

        else:
            self.leaf = False
            underlying_aggregates = []

            for key in pivot_tree.keys():
                this_branch = AggregateTree(pivot_tree[key], column_types, key)

                self.branches[key] = this_branch
                underlying_aggregates.append(this_branch.aggregate_value)

            combined = pd.concat(underlying_aggregates)

            self.aggregate_value = create_sum_row(combined, pivot_value, column_types)

    def sort(self, sort_column, ascending):
        if not self.leaf:
            self.branches = OrderedDict(sorted(self.branches.items(),
                                               key=lambda (key, value): value.aggregate_value[sort_column][0],
                                               reverse=not ascending))

            for (key, branch) in self.branches.iteritems():
                branch.sort(sort_column, ascending)

        if self.leaf:
            self.data_frame = self.data_frame.sort_values(sort_column, ascending=ascending)

    def is_leaf(self):
        return self.leaf
