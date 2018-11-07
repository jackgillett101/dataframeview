import tkinter.ttk as ttk
from dataframeview.dataframeguielements.dataframeviewfiltergui import DataFrameViewFilterGUI


# This tab lives inside the view controller, and allows a set of filters to be defined to filter out some rows of data
class CreateDataViewFiltersTab:
    def __init__(self, tab, df, view=None):
        # TODO: This class needs to be improved significantly to support nested and/or logic in filter construction
        # TODO: Also need to check the types of columns for relevant filter types (eg. no 'greater than' for strings)

        self.df = df

        # Our list of filters is empty unless view specifies some, save a list for filters refs to GUI elements
        self.filter_list = []
        if view is not None:
            self.filter_list = view.get_filters()

        self.filter_reference_list = []

        self.filters_frame = self.create_tkinter_window(tab)
        self.populate_filters()

    # When the View Controller window is closed, we want to convert all GUI lines into DFFilters for the new view
    def get_filters(self):
        df_filters = []

        for gui_filter in self.filter_reference_list:
            df_filters.append(gui_filter.create_df_filter())

        return df_filters

    # To add a filter, create new FilterGui object without passing a filter to it, it will do the rest. Keep a reference
    def add_filter(self):
        filter_gui = DataFrameViewFilterGUI(self, self.df, self.filters_frame)
        self.filter_reference_list.append(filter_gui)

    # To remove a filter, forget the reference to it, and call the GUI object's destruct method
    def remove_filter(self, df_filter):
        self.filter_reference_list.remove(df_filter)

    # Create a tkinter window with boxes for filters, columns and pivots
    def create_tkinter_window(self, tab):
        # Use frames to put the list boxes inside, which helps sizing an alignment
        outer_frame = ttk.Frame(tab)
        outer_frame.pack(side="left", fill="y")

        left_row_frame = ttk.Frame(outer_frame)
        left_row_frame.pack(side="left", fill="y")
        add_filter = ttk.Button(left_row_frame, text="+", width=5, command=self.add_filter)
        add_filter.pack(side="top")
        filler_frame = ttk.Frame(left_row_frame)
        filler_frame.pack(side="top", fill="y")

        sub_frame = ttk.Frame(outer_frame)
        sub_frame.pack(side="left", fill="y")
        blank_space_frame = ttk.Frame(sub_frame, height=25)
        blank_space_frame.pack(side="top")
        filters_frame = ttk.Frame(sub_frame)
        filters_frame.pack(side="top", fill="y")

        return filters_frame

    # Take any filters defined in the view and convert them into GUI rows
    def populate_filters(self):
        for data_filter in self.filter_list:
            filter_gui = DataFrameViewFilterGUI(self, self.df, self.filters_frame, df_filter=data_filter)
            self.filter_reference_list.append(filter_gui)
