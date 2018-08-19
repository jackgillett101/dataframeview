import Tkinter
import ttk
import dataframeviewcontrollerwindow


# From a list of column names, data types and data iterator, create a tree view
class TreeViewWindow:
    def __init__(self, df, view):
        self.df = df
        self.view = view

        (win, tree) = self.create_tkinter_window()

        self.tree = tree
        self.win = win

        # Clicking on a column sorts by that widget, using the underlying view sort functionality. If we click another
        # time, we want to anti-sort. As a hack, use stack-like method - to determine if this is the second click on a
        # given column, keep track of the last column clicked on in the window. If this is clicked on again, set this
        # back to None and sort descending. If any other column is clicked on, replace with that column's name
        self.sort_widget = None

        self.set_up_tree_view_data(df, view, tree, win)

    def set_up_tree_view_data(self, df, view, tree, win, expanded=[]):
        # Get datatypes of columns (controls sort, filter, and aggregation options)
        column_types = df.dtypes

        # Get column names (strings) as a list, and an iterator for the viewer
        columns = list(df.columns.values)

        if len(columns) != len(column_types):
            Exception("Columns and columnTypes should be same size").throw()

        column_data_types = dict(zip(columns, column_types))

        # If specified in the view, we instead use the subset (and ordering) of columns specified there
        view_columns = view.get_visible_columns()
        if len(view_columns) > 0:
            view_columns = filter(lambda x: x in columns, view_columns)  # Sanity check!
            view_column_types = map(lambda x: column_data_types[x], view_columns)

            columns = view_columns
            column_types = view_column_types

        # Choose a sensible column width - optimise later!
        number_of_columns = len(columns)
        column_width = max(min(300, 1000 / number_of_columns), 100)

        # Add a temporary count column
        df_with_count = df.assign(Count=1)

        itertuples = view.iterator_over_visible_rows(df_with_count)

        tree["columns"] = ("Count",) + tuple(columns)
        tree.column("Count", width=50)
        tree.heading("Count", text="Count", command=lambda: self.re_sort_on_column("Count"))

        for (column, column_type) in zip(columns, column_types):
            tree.column(column, width=column_width)
            tree.heading(column, text=('%s (%s)' % (column, column_type)),
                         command=lambda c=column: self.re_sort_on_column(c))
            # tree.bind("<Double-1>", self.OnDoubleClick )

        count = 0
        for data in itertuples:
            parent = data["parent"]

            if parent == 'root':
                parent = ''
            else:
                parent = str(parent)

            name = str(data["name"])
            dataframe = data["value"]

            for (label, row) in dataframe.iterrows():
                cell_data = tuple([row[column] if row[column] != None else "" for column in columns])

                # TODO: Keep track of openness by hashing values - potential conflicts
                row_data = (row['Count'],) + tuple(cell_data)
                node_expanded = hash(row_data) in expanded

                if count % 2 == 0:
                    style = 'evenrow'
                else:
                    style = 'oddrow'

                if name == 'None':
                    tree.insert(parent, count, text=label, values=row_data, open=node_expanded, tags=(style,))
                else:
                    tree.insert(parent, count, name, text=label, values=row_data, open=node_expanded, tags=(style,))

                count = count + 1

        # TODO: Choose a nice colour scheme, and make sure opening/closing pivots still respects it
        #tree.tag_configure('oddrow', background='orange')
        #tree.tag_configure('evenrow', background='purple')

        win.mainloop()

    # If you click on a column, sort by this column! Do this by emptying the view and re-creating the dataview
    # Note this means we need to keep track of what was opened before, in order to re-open in the same way
    def re_sort_on_column(self, column):
        ascending = True

        # This functionality described in comment in __init__
        if self.sort_widget == column:
            ascending = False
            self.sort_widget = None
        else:
            self.sort_widget = column

        # Go through tree, checking what was open
        expanded = self.get_open_tree_nodes()

        self.view.re_sort_on_column(column, ascending)

        self.tree.delete(*self.tree.get_children())

        self.set_up_tree_view_data(self.df, self.view, self.tree, self.win, expanded)

    def get_open_tree_nodes(self):
        expanded_nodes = []
        current_layer = self.tree.get_children()

        while len(current_layer) > 0:
            next_level = []
            for node in current_layer:

                # We're going to save the hash of open items, since this will be the same in the new tree (id changes)
                if self.tree.item(node)["open"]:
                    expanded_nodes.append(hash(tuple(self.tree.item(node)['values'])))
                    children = self.tree.get_children(node)

                    next_level = next_level + list(children)

            current_layer = next_level

        return expanded_nodes

    # Create a Tkinter window and a Treeview, pass links back for data population
    def create_tkinter_window(self):
        win = Tkinter.Tk()
        win.minsize(width=600, height=300)
        win.maxsize(width=1400, height=800)
        win.title('df Viewer')

        # create a menu on the top line for View and View Controller operations
        self.create_menu_options(win)

        # Create a TreeView and some scrollbars for it spanning the x and y axes
        tree = ttk.Treeview(win, padding=3)

        vsb = ttk.Scrollbar(win, orient=Tkinter.VERTICAL, command=tree.yview)
        vsb.pack(side='right', fill='y')
        hsb = ttk.Scrollbar(win, orient=Tkinter.HORIZONTAL, command=tree.xview)
        hsb.pack(side='bottom', fill='y')

        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=1, column=0, sticky=Tkinter.NSEW)
        vsb.grid(row=1, column=1, sticky=Tkinter.NS)
        hsb.grid(row=2, column=0, sticky=Tkinter.EW)

        win.rowconfigure(1, weight=1)
        win.columnconfigure(0, weight=1)

        return win, tree

    def create_menu_options(self, win):
        menu = Tkinter.Menu(win)
        win.config(menu=menu)

        view_menu = Tkinter.Menu(menu, tearoff=0)
        view_menu.add_command(label="Open View Controller", command=self.show_view_controller)
        view_menu.add_separator()
        view_menu.add_command(label="Load View", command=self.to_do)
        view_menu.add_command(label="Save View", command=self.to_do)
        view_menu.add_separator()
        view_menu.add_command(label="Exit", command=win.destroy)
        menu.add_cascade(label="File", menu=view_menu)

    def show_view_controller(self):
        self.win.destroy()
        dataframeviewcontrollerwindow.DataFrameViewControllerWindow(self.df, view=self.view)

    def to_do(self):
        print "Not Yet Implemented!"
