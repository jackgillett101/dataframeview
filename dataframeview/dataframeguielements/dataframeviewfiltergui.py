import tkinter
import tkinter.ttk as ttk
from dataframeview.dataframeviewfilters.dataframeviewfilters import DataFrameViewFilter


# DataFrameViewFilterGUI is a GUI line representation of a DataFrameViewFilter, used in the View Controller's Filters
# tab. If a filter object is passed in, its properties populate the GUI row. Otherwise a default (empty) entry is used.
# This also has a method to convert all of the GUI rows back into DataFrameViewFilter objects when the View Controller
# is closed
class DataFrameViewFilterGUI:
    def __init__(self, parent_tab, df, filters_frame, df_filter=None):

        # Keep a reference to the parent tab. We will need this to delete the reference to this filter if we remove
        self.parent_tab = parent_tab

        # Get column names (strings) as a list. We add a blank element because OptionMenus seem to lose track of it!!
        self.columns = [""] + list(df.columns.values)
        self.filter_types = ["", "Equals", "Greater Than", "Less Than", "Not Null", "In"]

        this_filter_frame = ttk.Frame(filters_frame, borderwidth=1, relief="sunken")
        this_filter_frame.pack(side="top")

        new_filter = ttk.Button(this_filter_frame, text="-", width=5, command=self.remove_filter)
        new_filter.pack(side="left")

        # Option Menu for the fields to filter on and filter type, with default set by the filter provided (if one is)
        filter_column = tkinter.StringVar()
        filter_type = tkinter.StringVar()
        if df_filter is None:
            filter_column.set(self.columns[1])
            filter_type.set(self.filter_types[1])
            filter_text = ""
        else:
            filter_column.set(df_filter.get_column_name())
            filter_type.set(df_filter.get_pretty_filter_type())
            filter_text = df_filter.get_filter_value()

        new_filter_field = ttk.OptionMenu(this_filter_frame, filter_column, *self.columns)
        new_filter_field.config(width=20)
        new_filter_field.pack(side="left")

        new_filter_type = ttk.OptionMenu(this_filter_frame, filter_type, *self.filter_types)
        new_filter_type.config(width=12)
        new_filter_type.pack(side="left")

        # Finally a text entry field for the value to compare against
        filter_value = ttk.Entry(this_filter_frame, width=40)
        filter_value.insert(0, filter_text)
        filter_value.pack(side="left", fill="y")

        self.this_filter_frame = this_filter_frame

        self.filter_column = filter_column
        self.filter_type = filter_type
        self.filter_value = filter_value

    def remove_filter(self):
        self.parent_tab.remove_filter(self)
        self.this_filter_frame.destroy()

    def create_df_filter(self):
        column = self.filter_column.get()
        type = self.filter_type.get()
        value = self.filter_value.get()

        return DataFrameViewFilter(column, type, value, pretty=True)
