import tkinter
import tkinter.ttk as ttk


# This tab lives inside the view controller, and determines which columns should be included in the view
class CreateDataViewColumnsTab:
    def __init__(self, tab, df, view=None):
        # Get column names (strings) as a list
        columns = list(df.columns.values)

        # If no view is defined, we start with all columns in the visible list as default. If there's already a view
        # and we're here to edit it, make sure the columns appear in the right place
        if view is None:
            included_columns_list = columns
            excluded_columns_list = []
        else:
            included_columns_list = view.get_visible_columns()
            excluded_columns_list = list(filter(lambda x: x not in included_columns_list, columns))

        self.included_columns_list = included_columns_list
        self.excluded_columns_list = excluded_columns_list

        # Use frames to put the list boxes inside, which helps sizing an alignment
        outer_left_frame = ttk.Frame(tab)
        outer_left_frame.pack(side="left", fill="y")
        included_column_frame = ttk.Frame(outer_left_frame)
        included_column_frame.pack(side="top", fill="y")
        ttk.Label(included_column_frame, text="Included Columns").pack(side="top", fill="y")

        outer_right_frame = ttk.Frame(tab)
        outer_right_frame.pack(side="left", fill="y")
        excluded_column_frame = ttk.Frame(outer_right_frame)
        excluded_column_frame.pack(side="top", fill="y")
        ttk.Label(excluded_column_frame, text="Excluded Columns").pack(side="top", fill="y")

        included_columns = tkinter.Listbox(included_column_frame, width=30)
        excluded_columns = tkinter.Listbox(excluded_column_frame, width=30)
        included_columns.pack(side="left", fill="y")
        excluded_columns.pack(side="left", fill="y")

        self.included_columns = included_columns
        self.excluded_columns = excluded_columns

        inc_scrollbar = ttk.Scrollbar(included_column_frame, orient="vertical", command=included_columns.yview)
        exc_scrollbar = ttk.Scrollbar(excluded_column_frame, orient="vertical", command=excluded_columns.yview)

        for (i, column) in enumerate(self.included_columns_list):
            included_columns.insert(i, column)

        for (i, column) in enumerate(self.excluded_columns_list):
            excluded_columns.insert(i, column)

        inc_scrollbar.pack(side="right", fill="y")
        exc_scrollbar.pack(side="right", fill="y")

        included_columns.config(yscrollcommand=inc_scrollbar.set)
        excluded_columns.config(yscrollcommand=exc_scrollbar.set)

        remove_column = ttk.Button(outer_left_frame, text="Remove -->", command=self.remove_column)
        add_column = ttk.Button(outer_right_frame, text="<-- Add", command=self.select_column)

        remove_column.pack(fill="y", side="top")
        add_column.pack(fill="y", side="top")

    def get_included_columns(self):
        return self.included_columns_list

    # Callbacks to add/remove columns from the view
    def remove_column(self):
        selected = self.included_columns.curselection()
        value = self.included_columns.get(selected[0])

        self.included_columns_list.remove(value)
        self.included_columns.delete(selected[0])
        self.excluded_columns_list.append(value)
        self.excluded_columns.insert(len(self.excluded_columns_list), value)

    def select_column(self):
        selected = self.excluded_columns.curselection()
        value = self.excluded_columns.get(selected[0])

        self.included_columns_list.append(value)
        self.included_columns.insert(len(self.included_columns_list), value)
        self.excluded_columns_list.remove(value)
        self.excluded_columns.delete(selected[0])
