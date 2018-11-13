import tkinter
import tkinter.ttk as ttk
from .dataframeviewcolumnstab import CreateDataViewColumnsTab
from .dataframeviewpivotstab import CreateDataViewPivotsTab
from .dataframeviewfilterstab import CreateDataViewFiltersTab
from dataframeview.dataframeguielements import *
from ..dataframeviewcore.dataframeviewconfig import DataFrameViewConfig


# From a DataFrameViewConfig object, create a view controller window, which allows users to view and alter tha current
# set of filters, visible columns, pivots etc. via GUI manipulations. When they click 'done', this window closes and
# the TreeViewWindow re-opens, with the new view applied
class DataFrameViewControllerWindow:
    def __init__(self, df, view=None):
        self.df = df

        (win, notebook, columns, pivots, filters, submit) = self.create_tkinter_window()

        self.win = win

        self.column_tab = CreateDataViewColumnsTab(columns, df, view=view)
        self.pivot_tab = CreateDataViewPivotsTab(pivots, df, view=view)
        self.filter_tab = CreateDataViewFiltersTab(filters, df, view=view)

        # TODO: add a sorts tab here (to allow multiple sort columns)

        notebook.pack()
        submit.pack()

        win.mainloop()

    def submit_button(self):
        columns = self.column_tab.get_included_columns()
        v_pivots = self.pivot_tab.get_included_pivots()
        filters = self.filter_tab.get_filters()

        self.win.destroy()

        view = DataFrameViewConfig(columns=columns, v_pivots=v_pivots, filters=filters)
        dataframewindow.TreeViewWindow(self.df, view=view)
        #DataFrameViewer(self.df, columns=columns, v_pivots=v_pivots, filters=filters)

    # Create a tkinter window with boxes for filters, columns and pivots
    def create_tkinter_window(self):

        win = tkinter.Tk()

        notebook = ttk.Notebook(win, width=600, height=300)

        columns = ttk.Frame(notebook)
        pivots = ttk.Frame(notebook)
        filters = ttk.Frame(notebook)

        notebook.add(columns, text='Columns')
        notebook.add(pivots, text='Pivots')
        notebook.add(filters, text='Filters')

        win.minsize(width=600, height=300)
        win.maxsize(width=1400, height=800)

        win.title('df View Controller')

        win.rowconfigure(1, weight=1)
        win.columnconfigure(0, weight=1)

        submit = ttk.Button(win, text="Done", command=self.submit_button)

        return win, notebook, columns, pivots, filters, submit
