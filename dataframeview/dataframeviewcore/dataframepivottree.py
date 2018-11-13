import pandas as pd
from collections import defaultdict
from .dataframeaggregatetree import AggregateTree


def tree():
    return defaultdict(tree)


class PivotTree:
    # Create the underlying pivot tree that acts as a map to each ultimate pivot, represented by a small df
    def __init__(self, df, pivots):
        self.data_tree = tree()
        self.column_types = df.dtypes

        # Create the structure of the tree using pd's groupBy
        # TODO: for float datatypes, put some customisable rounding in here! So 'pivoting' becomes 'bucketing'

        group_by = df.groupby(pivots)

        pivot_buckets = pd.DataFrame({'Count': group_by.size()}).reset_index()

        # Using the df's groupby() function breaks the df into the groups that we need. However, for displaying these
        # we'll need to run through the groupby object and assign them to a tree structure. Following this, we'll need
        # to calculate the 'aggregate rows' for each group (and group of groups...) of sub rows to display
        for (label, row) in pivot_buckets.iterrows():
            link = self.data_tree
            pivot_values = []

            for pivot in pivots:
                if pivot != pivots[0]:
                    link = link[pivot_value]

                pivot_value = (pivot, row[pivot])
                pivot_values.append(pivot_value)

                if len(link) == 0:
                    link[pivot_value] = tree()

            data_tree_key = list(map(lambda x: x[1], pivot_values))
            if len(data_tree_key) > 1:
                data_tree_key = tuple(data_tree_key)
            else:
                data_tree_key = data_tree_key[0]
            link[pivot_value] = group_by.get_group(data_tree_key)

        # The dataTree contains the underlying values in the correct groupings, now for each grouping we create an
        # extra aggregate row summarising the underlying data
        self.aggregate_tree = AggregateTree(self.data_tree, self.column_types, ('root', ''))

    def is_leaf(self):
        return self.is_leaf

    # Return the data tree!
    def get_data_tree(self):
        return self.data_tree

    # Return the aggregated tree!
    def get_aggregate_tree(self):
        return self.aggregate_tree
