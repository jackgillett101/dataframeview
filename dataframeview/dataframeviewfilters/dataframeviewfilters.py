# A filter is a column and a binary operation to perform on it. Anything returning False is excluded from the table
class DataFrameViewFilter:

    # Create some class static maps linking pretty to functional descriptors
    pretty_filter_name = {"greater_than": "Greater Than", "less_than": "Less Than", "equals": "Equals",
                             "in": "In", "notnull": "Not Null"}
    inverse_pretty_map = {v: k for k, v in pretty_filter_name.iteritems()}

    def __init__(self, column_name, filter_type, value, pretty=False):
        # TODO: check the type of the filter, and sanity-check the values passed in

        self.column_name = column_name
        self.value = value

        if pretty is False:
            self.filter_type = filter_type
        else:
            self.filter_type = self.inverse_pretty_map[filter_type]

    # Apply this filter to a data frame
    def apply_filter(self, df):

        # TODO: make type checking better
        value = self.value
        dtype = df.dtypes[self.column_name]
        if dtype == "int64":
            value = int(value)

        # TODO: increase the number of filter operations, and break the functionality out into their own classes
        # inheriting from a base "FilterOperation" class
        if self.filter_type == "greater_than":
            return df[df[self.column_name] > value]
        if self.filter_type == "less_than":
            return df[df[self.column_name] < value]
        if self.filter_type == "equals":
            return df[df[self.column_name] == value]
        if self.filter_type == "in":
            return df[df[self.column_name].isin(value)]
        if self.filter_type == "notnull":
            return df[df[self.column_name] is not None]

    def get_column_name(self):
        return self.column_name

    def get_pretty_filter_type(self):
        return self.pretty_filter_name[self.filter_type]

    def get_filter_value(self):
        return self.value
