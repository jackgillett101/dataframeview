import Tkinter
import ttk


# This tab lives inside the view controller, and determines which columns should be pivoted on in the viewer
class CreateDataViewPivotsTab:
    def __init__(self, tab, df, view=None):
        # Get column names (strings) as a list
        columns = list(df.columns.values)

        # TODO: Filter for pivotable datatypes (eg. can't pivot on doubles - unless we bucket?!)

        # If no view is defined, we start with no pivots. Otherwise populate it with the current pivot columns
        if view is None:
            excluded_pivots_list = columns
            included_pivots_list = []
        else:
            included_pivots_list = view.get_pivot_columns()
            excluded_pivots_list = filter(lambda x: x not in included_pivots_list, columns)

        self.excluded_pivots_list = excluded_pivots_list
        self.included_pivots_list = included_pivots_list

        # Use frames to put the listboxes inside, which helps sizing an alignment
        outer_left_frame = ttk.Frame(tab)
        outer_left_frame.pack(side="left", fill="y")
        excluded_pivots_frame = ttk.Frame(outer_left_frame)
        excluded_pivots_frame.pack(side="top", fill="y")
        ttk.Label(excluded_pivots_frame, text="Select Columns").pack(side="top", fill="y")

        outer_right_frame = ttk.Frame(tab)
        outer_right_frame.pack(side="left", fill="y")
        included_pivots_frame = ttk.Frame(outer_right_frame)
        included_pivots_frame.pack(side="top", fill="y")
        ttk.Label(included_pivots_frame, text="VPivot Columns").pack(side="top", fill="y")

        excluded_pivots = Tkinter.Listbox(excluded_pivots_frame, width=30)
        included_pivots = Tkinter.Listbox(included_pivots_frame, width=30)
        excluded_pivots.pack(side="left", fill="y")
        included_pivots.pack(side="left", fill="y")

        self.excluded_pivots = excluded_pivots
        self.included_pivots = included_pivots

        exc_scrollbar = ttk.Scrollbar(excluded_pivots_frame, orient="vertical", command=excluded_pivots.yview)
        inc_scrollbar = ttk.Scrollbar(included_pivots_frame, orient="vertical", command=included_pivots.yview)

        for (i, column) in enumerate(self.excluded_pivots_list):
            excluded_pivots.insert(i, column)

        for (i, column) in enumerate(self.included_pivots_list):
            included_pivots.insert(i, column)

        exc_scrollbar.pack(side="right", fill="y")
        inc_scrollbar.pack(side="right", fill="y")

        excluded_pivots.config(yscrollcommand=exc_scrollbar.set)
        included_pivots.config(yscrollcommand=inc_scrollbar.set)

        add_pivot = ttk.Button(outer_left_frame, text="Pivot -->", command=self.select_pivot)
        remove_pivot = ttk.Button(outer_right_frame, text="<-- Remove", command=self.remove_pivot)

        add_pivot.pack(fill="y", side="top")
        remove_pivot.pack(fill="y", side="top")

    def get_included_pivots(self):
        return self.included_pivots_list

    # Callbacks to add/remove pivot columns from the view
    def select_pivot(self):
        selected = self.excluded_pivots.curselection()
        value = self.excluded_pivots.get(selected[0])

        self.included_pivots_list.append(value)
        self.included_pivots.insert(len(self.included_pivots_list), value)
        self.excluded_pivots_list.remove(value)
        self.excluded_pivots.delete(selected[0])

    def remove_pivot(self):
        selected = self.included_pivots.curselection()
        value = self.included_pivots.get(selected[0])

        self.included_pivots_list.remove(value)
        self.included_pivots.delete(selected[0])
        self.excluded_pivots_list.append(value)
        self.excluded_pivots.insert(len(self.excluded_pivots_list), value)
