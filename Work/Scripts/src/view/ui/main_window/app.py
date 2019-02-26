"""
В файле расположены классы отвечающие за визуальную часть
главного окна и таблицы в нем
"""
from tkinter import Frame, Canvas, Button, \
    Tk, Scrollbar, Menu, NSEW, NE, W, NW, NS, EW, Entry, messagebox
from abc import ABC, abstractmethod

from Work.Scripts.res.values.menu import MainMenuFactory, MainMenuListener
from Work.Scripts.src.test.main_table_interactor import MainTableInteractor
from Work.Scripts.src.view.ui.db_editor.db_editor import DbEditorWindow
from Work.Scripts.src.view.ui.main_window.config import WIN_W_START, \
    WIN_H_START, \
    WIDTH_FILR_FRAME, COLOR_TEXT_TABLE, COLOR_BG_ODD_ROW, COLOR_BG_EVENT_ROW, \
    COLOR_BG_TITLE_TABLE, FILTER_TAB_TEXT, TABLES_TAB_TEXT, \
    LAST_CHANGES_CLOSED_TAB, LAST_CHANGES_OPENED_TAB, MENU_FILE_TEXT, \
    MENU_CHANGE_TEXT, MENU_REPORT_TEXT, DEFAULT_SEARCH_TEXT, HEIGHT_ROW, \
    COLOR_BG_SELECT_ROW, COLOR_TEXT_TITLE, COLOR_BG_BOTTOM_BTN, \
    COLOR_FG_BOTTOM_BTN, COLOR_BG_BTN_FILTR, COLOR_BG_BTN_TABLE
from Work.Scripts.src.view.ui.main_window.move_out_panels import \
    ChangeHistoryPanel, ColumnFilterPanel, RowFilterPanel
from Work.Scripts.src.view.ui.reports_settings.settings_bar_chart import \
    SettingsBarChart
from Work.Scripts.src.view.ui.reports_settings.settings_box_and_whisker import \
    SettingsBoxAndWhisker
from Work.Scripts.src.view.ui.reports_settings.settings_histogram import \
    SettingsHistogram
from Work.Scripts.src.view.ui.reports_settings.settings_scatter_chart import \
    SettingsScatterChart

main_table_interactor = MainTableInteractor()


class IWindowListener(ABC):

    @abstractmethod
    def close(self):
        pass


class MainWindow(IWindowListener):
    """
    Класс отвечает за разметку главного окна и позиционирование его содержимого
    Автор: Озирный Максим
    """
    # Переменные необходимые для отслеживания нажатий на кнопки
    # находящиеся в главном окне
    last_ch_bool = False
    filter_bool = False
    table_bool = False
    plus_bool = False
    # переменные хранящие имена объектов на которых будет находится курсор
    widget = ""
    widget1 = ""

    def __init__(self, master, title="Заголовок"):
        self.master = master

        # Устанавливаем вызов функции при нажатии на крестик окна
        master.protocol('WM_DELETE_WINDOW', self.close)
        # Устанавливаются основные параметры главного окна:
        # заголовок, иконку заголовка, параметры размера и появления на экране
        # минимальный размер, параметры сетки
        master.title(title)
        master.iconbitmap(
            r'D:\main\projects\python\ProductsViewer\Work\Scripts\res\drawable\img.ico')
        master.geometry("{winw}x{winh}+{centerw}+{centerh}".format(
            winw=WIN_W_START,
            winh=WIN_H_START,
            centerw=(master.winfo_screenwidth() - WIN_W_START) // 2,
            centerh=(master.winfo_screenheight() - WIN_H_START - 30) // 2))
        master.minsize(WIN_W_START, WIN_H_START - 20)
        master.resizable(True, True)
        master.grid_rowconfigure(0, minsize=24)
        master.grid_rowconfigure(1, weight=1, minsize=150)
        master.grid_rowconfigure(2, minsize=0)
        master.grid_rowconfigure(3, minsize=24)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, minsize=0)
        master.grid_columnconfigure(2, minsize=0)
        master.grid_columnconfigure(3, minsize=24)

        # Создается верхнее меню
        footbar = OptionsMenu(master, self)
        footbar.create_menu()

        # Создается верхнее поле и устанавливается размерная сетка
        self.search_frame = Frame(master)
        self.search_frame.grid_columnconfigure(0, minsize=30)
        self.search_frame.grid_columnconfigure(1, weight=1)
        self.search_frame.grid_columnconfigure(2, minsize=30)
        self.search_frame.grid_columnconfigure(3, minsize=30)
        self.search_frame.grid_columnconfigure(4, minsize=49)

        # Создаётся и позиционируется содержимое верхнего поля
        self.btn_plus = Btn(self.search_frame, text="+", bd=0,
                               command=self.plus)
        self.btn_plus.grid(row=0, column=0)
        self.search = Entry(self.search_frame, fg="#d0d0d0")
        self.search.insert(0, DEFAULT_SEARCH_TEXT)
        self.search.bind("<Button-1>", self.click_search)
        self.search.grid(row=0, column=1, sticky="w")
        self.btn_save = Btn(self.search_frame, bd=1, relief="ridge",
                               text="save", command=self.save_new_row)
        self.btn_or_no = Btn(self.search_frame, bd=1, relief="ridge",
                                text="or no", command=self.plus)
        self.btn_save.grid(row=0, column=2)
        self.btn_or_no.grid(row=0, column=3)
        self.btn_save.grid_forget()
        self.btn_or_no.grid_forget()

        # Создаётся главное поле (в которое выводится бд)
        self.main_frame = MainTableFrame(master, self,
                                         self.btn_save,
                                         self.btn_or_no,
                                         bg="#f0f0f0")
        # Создаются и заполняются правые поля (фильтр строк и столбцов)
        self.filtr_frame = RowFilterPanel(master)
        self.filtr_frame.content()
        self.table_frame = ColumnFilterPanel(master)
        self.table_frame.content()
        # Создается нижнее поле (последние изменения)
        self.last_ch_frame = ChangeHistoryPanel(self.master)

        # Создаётся кнопка отвечающая за вызов поля последних изменений
        self.bottom_btn = Btn(master, anchor=W, relief="flat",
                              bg=COLOR_BG_BOTTOM_BTN,
                              activebackground=COLOR_BG_BOTTOM_BTN,
                              text=LAST_CHANGES_CLOSED_TAB,
                              fg=COLOR_FG_BOTTOM_BTN)
        self.bottom_btn.bind("<ButtonRelease-1>", self.click_extend_menu)

        # Создается поле для кнопок справа
        self.right_menu = Frame(master)

        # Создаются кнопки для появления перед пользователем полей фильтрации
        self.filter_btn = self.get_tab_btn(FILTER_TAB_TEXT, 55)
        self.filter_btn.bind("<ButtonPress-1>", self.press_right_btn)
        self.filter_btn.bind("<ButtonRelease-1>", self.click_filter)
        self.filter_btn.place(x=0, y=0)
        self.table_btn = self.get_tab_btn(TABLES_TAB_TEXT, 40)
        self.table_btn.bind("<ButtonPress-1>", self.press_right_btn)
        self.table_btn.bind("<ButtonRelease-1>", self.click_table)
        self.table_btn.place(x=0, y=54)

        # Происхожит позиционирование объектов в главном классе
        self.search_frame.grid(row=0, column=0, columnspan=4, sticky=NSEW)
        self.main_frame.grid(row=1, column=0, sticky=NSEW)
        self.filtr_frame.grid(row=1, column=1, sticky=NSEW)
        self.table_frame.grid(row=1, column=2, sticky=NSEW)
        self.right_menu.grid(row=1, column=3, sticky=NSEW)
        self.bottom_btn.grid(row=3, column=0, columnspan=4, sticky=NSEW)

        # Устанавливается вызов функций при соответствующем событии
        self.master.bind_all("<MouseWheel>", self.on_mousewheel)
        self.master.bind('<Left>', self.left_key)
        self.master.bind('<Right>', self.right_key)
        self.master.bind('<Up>', self.top_key)
        self.master.bind('<Down>', self.bottom_key)
        self.master.bind("<Configure>", self.new_height)
        self.master.bind("<Button-1>", self.del_focus)

        master.mainloop()

    def close(self, event=None):
        """
        Функция вызывающая диалоговое окно для дальнейшего
        сохранения или не сохранения последних изменений в базе данных
        Автор: Озирный Максим
        """
        ask = messagebox.askyesnocancel("Выход",
                                        "Сохранить последние изменения?")
        if ask != None:
            if ask:
                print("сохранить")
            else:
                print("не сохраняй")
            self.master.destroy()

    def plus(self, event=None):
        """
        Функция отвечает за создание или удаление элементов,
        необходимых для добавления новой строки в таблицу
        Автор: Озирный Максим
        """
        self.new_xy_menu()
        # Условие необходимо для того, чтоб действия в фукции выполнялись,
        # если на кнопку нажали и на ней же отпустили кнопку мыши
        if self.btn_plus.widget1 == self.widget or \
                self.btn_or_no.widget1 == self.widget:
            if self.plus_bool:
                self.btn_plus.config(text="+")
                self.btn_save.grid_forget()
                self.btn_or_no.grid_forget()
                self.main_frame.del_new_row()
            else:
                self.btn_plus.config(text="×")
                self.main_frame.new_row()
            self.plus_bool = not self.plus_bool

    def save_new_row(self, event=None):
        """
        Функция добавляет новую строку, если введены корректные данные
        Автор: Озирный Максим
        """
        self.new_xy_menu()
        # Условие необходимо для того, чтоб действия в фукции выполнялись,
        # если на кнопку нажали и на ней же отпустили кнопку мыши
        if self.btn_save.widget1 == self.widget:
            self.main_frame._bd_array.append([])
            for ind in range(len(self.main_frame._bd_array[0])):
                self.main_frame._bd_array[
                    len(self.main_frame._bd_array) - 1].append(
                    "{}".format(self.main_frame.list_new_col[ind].get()))
            row = len(self.main_frame._bd_array) - 1
            self.main_frame.frame2.grid_rowconfigure(row, minsize=HEIGHT_ROW)
            for col in range((len(self.main_frame._bd_array[0]))):
                self.new_frame = Frame(self.main_frame.frame2)
                self.cell = Entry(self.new_frame,
                                  disabledforeground=COLOR_TEXT_TABLE,
                                  fg=COLOR_TEXT_TABLE)
                self.cell.bind("<Button-1>", self.main_frame.click_cell)
                self.cell.bind("<Double-1>", self.main_frame.double_click_cell)
                self.cell.bind("<Button-3>", self.main_frame.context_menu)
                self.new_frame.bind("<Button-1>", self.main_frame.click_cell)
                self.new_frame.bind("<Double-1>",
                                    self.main_frame.double_click_cell)
                self.new_frame.bind("<Button-3>", self.main_frame.context_menu)
                self.main_frame._characteristic.update({
                    self.cell: [self.new_frame, "entry", row, col,
                                row * len(self.main_frame._bd_array[0]) + col,
                                False, True]})
                self.main_frame._characteristic.update({
                    self.new_frame: [self.cell, "frame", row, col,
                                     row * len(
                                         self.main_frame._bd_array[0]) + col,
                                     False, True]})
                self.cell.insert(0,
                                 "{}".format(
                                     self.main_frame._bd_array[row][col]))
                self.new_frame.config(bg=COLOR_BG_ODD_ROW, pady=5)
                self.new_frame.grid(row=row, column=col, sticky="nwes")
                self.cell.grid(sticky="nwes")
                self.cell.config(relief="flat", state="disabled", bg="#fff",
                                 width=self.main_frame.list_max[col] + 2,
                                 disabledbackground=COLOR_BG_ODD_ROW
                                 )
            self.main_frame.repaint()

    def click_search(self, event=None):
        """
        Функция, реагируя на нажатие в поле поиска, которое не было заполнено
        пользователем, удаляет из него дефолтную надпись и изменяет цвет текста
        Автор: Озирный Максим
        """
        if self.search.get() == DEFAULT_SEARCH_TEXT:
            self.search.delete(0, "end")
            self.search.config(fg="#000")

    def del_focus(self, event=None):
        """
        Функция в случае если пользователь оставил поле поиска пустым
        заполняет его дефолтной надписью конкретного цвета
        Автор: Озирный Максим
        """
        if ".!frame.!entry" != "{}".format(self.widget_pointer()):
            if self.search.get() == "":
                self.search.config(fg="#d0d0d0")
                self.search.insert(0, DEFAULT_SEARCH_TEXT)
                self.master.focus_set()

    def get_tab_btn(self, text, height):
        """
        Функция создает объект с повернутым на 90 градусов  переданным текстом
        с переданной высотой

        принимает текст и высоту
        """
        tab = Canvas(self.right_menu, height=height, width=20, bd=0,
                     bg="#f0f0f0")
        tab.create_text((20, height-5), angle="-90", anchor=NE, text=text)
        return tab

    def new_height(self, event=None):
        """
        Функция изменяет высоту главного поля (таблицы) при нажатии на кнопку
        'последние изменения'
        """
        if self.last_ch_bool:
            self.main_frame.cont.config(
                height=self.master.winfo_height() - 99 -
                       self.main_frame.titles.winfo_height() -
                       self.last_ch_frame.canvas.winfo_height())
        else:
            self.main_frame.cont.config(
                height=self.master.winfo_height() - 75 -
                       self.main_frame.titles.winfo_height())

    def left_key(self, event=None):
        """
        Функция прокручивает таблицу при нажатии на стрелку
        Автор: Озирный Максим
        """
        self.main_frame.canvas.xview_scroll(-1, "units")

    def right_key(self, event=None):
        """
        Функция прокручивает таблицу при нажатии на стрелку
        Автор: Озирный Максим
        """
        self.main_frame.canvas.xview_scroll(1, "units")

    def top_key(self, event=None):
        """
        Функция прокручивает соответствующий canvas при нажатии на стрелку
        в зависимости местаположения мыши
        Автор: Озирный Максим
        """
        widget = self.widget_pointer()
        if "maintableframe" in widget and "canvas" in widget:
            self.main_frame.cont.yview_scroll(-1, "units")
        elif "changehistorypanel" in widget and "canvas" in widget:
            self.last_ch_frame.canvas.yview_scroll(-1, "units")

    def bottom_key(self, event=None):
        """
        Функция прокручивает соответствующий canvas при нажатии на стрелку
        в зависимости местаположения мыши
        Автор: Озирный Максим
        """
        widget = self.widget_pointer()
        if "maintableframe" in widget and "canvas" in widget:
            self.main_frame.cont.yview_scroll(1, "units")
        elif "changehistorypanel" in widget and "canvas" in widget:
            self.last_ch_frame.canvas.yview_scroll(1, "units")

    def on_mousewheel(self, event=None):
        """
        Функция прокручивает соответствующий canvas при прокрутке колесика
        в зависимости местаположения мыши
        Автор: Озирный Максим
        """
        widget = self.widget_pointer()
        sgn = -1 * (event.delta // 120)
        if "maintableframe" in widget and "canvas" in widget:
            self.main_frame.cont.yview_scroll(sgn, "units")
        elif "changehistorypanel" in widget and "canvas" in widget:
            self.last_ch_frame.canvas.yview_scroll(sgn, "units")

    def new_xy_menu(self, event=None):
        """
        Функция изменяет глобальную для класса переменную, записывая в нее
        название объекта на котором находится курсор
        Автор: Озирный Максим
        """
        self.widget = self.widget_pointer()

    def widget_pointer(self, event=None):
        """
        Функция вычисляет на коком объекте находится курсор

        возвращает имя объекта в виде строки
        Автор: Озирный Максим
        """
        x, y = self.master.winfo_pointerxy()
        widget = self.master.winfo_containing(x, y)
        widget = "{}".format(widget)
        return widget

    def click_extend_menu(self, event=None):
        """
        Функция показывает или скрывает поле 'последние изменения'
        Автор: Озирный Максим
        """
        self.new_xy_menu()
        # Условие необходимо для того, чтоб действия в фукции выполнялись,
        # если на кнопку нажали и на ней же отпустили кнопку мыши
        if self.bottom_btn.widget1 == self.widget:
            if self.last_ch_bool:
                self.bottom_btn.config(text=LAST_CHANGES_CLOSED_TAB)
                self.last_ch_frame.close()
            else:
                self.bottom_btn.config(text=LAST_CHANGES_OPENED_TAB)
                self.last_ch_frame = ChangeHistoryPanel(self.master)
                self.last_ch_frame.open()
            self.last_ch_bool = not self.last_ch_bool

    def press_right_btn(self, event=None):
        """
        Функция изменяет глобальную для класса переменную, записывая в нее
        название объекта на котором находится курсор
        Автор: Озирный Максим
        """
        self.widget1 = self.widget_pointer()

    def click_filter(self, event=None):
        """
        Функция показывает или скрывает поле фильтрации по строкам
        Автор: Озирный Максим
        """
        self.new_xy_menu()
        # Условие необходимо для того, чтоб действия в фукции выполнялись,
        # если на кнопку нажали и на ней же отпустили кнопку мыши
        if self.widget1 == self.widget:
            if self.table_bool:
                self.master.grid_columnconfigure(2, minsize=0)
                self.table_btn.config(bg="#f0f0f0")
                self.table_bool = not self.table_bool
            if self.filter_bool:
                self.master.grid_columnconfigure(1, minsize=0)
                self.filter_btn.config(bg="#f0f0f0")
            else:
                self.filter_btn.config(bg=COLOR_BG_BTN_FILTR)
                self.master.grid_columnconfigure(1, minsize=WIDTH_FILR_FRAME)
            self.filter_bool = not self.filter_bool

    def click_table(self, event=None):
        """
        Функция показывает или скрывает поле фильтрации по столбцам
        Автор: Озирный Максим
        """
        self.new_xy_menu()
        # Условие необходимо для того, чтоб действия в фукции выполнялись,
        # если на кнопку нажали и на ней же отпустили кнопку мыши
        if self.widget1 == self.widget:
            if self.filter_bool:
                self.master.grid_columnconfigure(1, minsize=0)
                self.filter_btn.config(bg="#f0f0f0")
                self.filter_bool = not self.filter_bool
            if self.table_bool:
                self.master.grid_columnconfigure(2, minsize=0)
                self.table_btn.config(bg="#f0f0f0")
            else:
                self.table_btn.config(bg=COLOR_BG_BTN_TABLE)
                self.master.grid_columnconfigure(2, minsize=WIDTH_FILR_FRAME)
            self.table_bool = not self.table_bool

class MainTableFrame(Canvas):
    """
    Класс отвечающий за отображение и взаимодействие с таблицей (базой данных)
    Автор: Озирный Максим
    """
    # Переменная хранящая список строк из базы данных
    _bd_array = main_table_interactor.get_data(None, None)
    # словарь с информацией об объектах в таблице
    # entry или frame :
    # [frame или entry, this_type, строка, столбец, номер, select, grid]
    _characteristic = {}
    list_new_col = []
    list_max = {}
    for ind in range(len(_bd_array[0])):
        list_new_col.append(ind)
    widget = ""
    widget2 = 0
    start_value = ""
    list_row = {}
    list_cell = []
    list_titles = []
    list_frame = []

    def __init__(self, master, main, btn1, btn2, **kw):
        super().__init__(master, {}, **kw)
        # устанавливаем сылку на переданные объекты
        self.btn1 = btn1
        self.btn2 = btn2
        # устанавливаем параметры сетки главного поля для таблицы
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, minsize=24)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, minsize=24)

        self.canvas = Canvas(self)
        self.frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor=NW)
        self.canvas.grid(row=0, column=0, sticky=NSEW)

        self.titles = Canvas(self.frame, bg=COLOR_BG_TITLE_TABLE)
        self.cont = Canvas(self.frame, height=350)
        self.titles.grid(row=0, column=0, sticky=NSEW)
        self.frame2 = Frame(self.cont, background="#f0f0f0")
        self.cont.create_window((0, 0), window=self.frame2, anchor=NW)
        self.cont.grid(row=1, column=0, sticky=NSEW)

        scroll_x = Scrollbar(self, orient="horizontal",
                             command=self.canvas.xview)
        scroll_x.grid(row=1, column=0, sticky=EW)

        scroll_y = Scrollbar(self, orient="vertical", command=self.cont.yview)
        scroll_y.grid(row=0, column=1, sticky=NS)
        self.cont.configure(yscrollcommand=scroll_y.set)
        self.canvas.configure(xscrollcommand=scroll_x.set)
        self.frame.bind("<Configure>", lambda event, canvas=self.canvas:
        self.on_frame_configure(self.canvas))
        self.frame2.bind("<Configure>", lambda event, canvas=self.cont:
        self.on_frame_configure(self.cont))
        self.content(self._bd_array)

        self.btn_on = Button(self.frame2, text="on")
        self.btn_off = Button(self.frame2, text="off")

        self.menu = Menu(self.master, tearoff=0, postcommand=self.new_xy_menu)
        self.menu.add_command(label="Изменить", command=self.before_change)
        self.menu.add_command(label="Добавить строку", command=main.plus)
        self.menu.add_command(label="Удалить строку", command=self.delete_row)

        self.black_menu = Menu(self.master, tearoff=0)
        self.black_menu.add_command(label="Отменить выделение",
                                    command=self.repaint)
        self.black_menu.add_command(label="Удалить строки",
                                    command=self.del_select)
        #self.master.bind("<Escape>", self.deselect)

    def del_select(self, event=None):
        """
        Функция удаляет выбранные строки
        Автор: Озирный Максим
        """
        for key in self._characteristic.keys():
            if self._characteristic[key][-2] == True:
                self._characteristic[key][-2] = False
                self._characteristic[key][-1] = False
                key.grid_forget()
                if self._characteristic[key][4] == \
                        self._characteristic[key][2] * len(self._bd_array[0]) \
                        and self._characteristic[key][4] != 0 \
                        and self._characteristic[key][1] == "entry":
                    self.frame2.grid_rowconfigure(self._characteristic[key][2],
                                                  minsize=0)

        self.repaint()

    def delete_row(self, event=None):
        """
        Функция удаляет выбранную строку
        Автор: Озирный Максим
        """
        self.frame2.grid_rowconfigure(self._characteristic[self.widget][2],
                                      minsize=0)
        for key in self._characteristic.keys():
            if self._characteristic[key][2] == \
                    self._characteristic[self.widget][2]:
                key.grid_forget()
                self._characteristic[key][-1] = False
            # if self._characteristic[key][2] > \
            #         self._characteristic[self.widget][2]:
            #     self._characteristic[key][2] = self._characteristic[key][2] - 1

        self.repaint()

    def repaint(self, num=-1, event=None):
        """
        Функция перекрашивает строки таблицы
        Автор: Озирный Максим
        """
        j = -1
        col = len(self._bd_array[0])

        for key in self._characteristic.keys():
            if self._characteristic[key][4] == \
                    self._characteristic[key][2] * col \
                    and self._characteristic[key][4] != 0 \
                    and self._characteristic[key][1] == "entry":
                if self._characteristic[key][-1]:
                    j += 1
                    if j % 2 == 0:
                        for key2 in self._characteristic.keys():
                            if self._characteristic[key2][2] == \
                                    self._characteristic[key][2] and \
                                    num == -1 or \
                                    self._characteristic[key2][2] == num and \
                                    self._characteristic[key][2] == num:
                                self._characteristic[key2][-2] = False
                                if self._characteristic[key2][1] == "entry":
                                    key2.config(
                                        disabledbackground=COLOR_BG_ODD_ROW)
                                else:
                                    key2.config(bg=COLOR_BG_ODD_ROW)
                    else:
                        for key2 in self._characteristic.keys():
                            if self._characteristic[key2][2] == \
                                    self._characteristic[key][2]and \
                                    num == -1 or \
                                    self._characteristic[key2][2] == num and \
                                    self._characteristic[key][2] == num:
                                self._characteristic[key2][-2] = False
                                if self._characteristic[key2][1] == "entry":
                                    key2.config(
                                        disabledbackground=COLOR_BG_EVENT_ROW)
                                else:
                                    key2.config(bg=COLOR_BG_EVENT_ROW)

    def new_row(self, event=None):
        """
        Функция создаёт елементы в которые вносятся данные новой строки
        Автор: Озирный Максим
        """
        for col in range(len(self._bd_array[0])):
            new = Entry(self.titles, bd=0, width=self.list_max[col]+2)
            self.list_new_col[col] = new
            new.bind("<Key>", self.change_new_row)
            new.grid(row=1, column=1*col, sticky="w")

    def change_new_row(self, event=None):
        """
        Функция делает кнопки видимыми для пользователя (позиционирует их)
        при изменении поля для ввода данных о новой строке
        Автор: Озирный Максим
        """
        self.btn1.grid(row=0, column=2)
        self.btn2.grid(row=0, column=3)

    def del_new_row(self, event=None):
        """
        Функция удаляет елементы в которые вносятся данные новой строки
        Автор: Озирный Максим
        """
        for ind in range(len(self._bd_array[0])):
            self.list_new_col[ind].destroy()

    def new_xy_menu(self, event=None):
        """
        Функция изменяет глобальную для класса переменную, записывая в нее
        название объекта на котором находится курсор
        Автор: Озирный Максим
        """
        self.widget = self.widget_pointer()

    def save_change(self, event=None):
        """
        Функция сохраняет изменение текста в ячейке теблицы
        Автор: Озирный Максим
        """
        self.btn_on.destroy()
        self.btn_off.destroy()
        if self._characteristic[self.widget][1] == "entry":
            value = self.widget.get()
            self.widget.config(state="disabled")
        else:
            value = self._characteristic[self.widget][0].get()
            self._characteristic[self.widget][0].config(state="disabled")
        self._bd_array[self._characteristic[self.widget][2]][
            self._characteristic[self.widget][3]] = value

        self.max_width(self._bd_array, self.list_max,
                       self._characteristic[self.widget][3])
        self.set_max_width()

    def set_max_width(self, event=None):
        """
        Функция устанавливает ширину каждой ячейки таблицы в зависимости
        от максимальной ширины в столбце
        Автор: Озирный Максим
        """
        for key in self._characteristic.keys():
            if self._characteristic[key][1] == "entry":
                key.config(width=self.list_max[self._characteristic[key][3]]+2)

    def del_change(self, event=None):
        """
        Функция удаляет последние изменения ячейки в таблице
        Автор: Озирный Максим
        """
        self.btn_on.destroy()
        self.btn_off.destroy()
        for key in self._characteristic.keys():
            if self._characteristic[key][2] == 0 and \
                    self._characteristic[key][1] == "entry" and \
                    self._characteristic[key][3] == \
                    self._characteristic[self.widget2][3]:
                key.config(
                    width=self.list_max[self._characteristic[key][3]] + 2)
        if self._characteristic[self.widget2][1] == "entry":
            self.widget2.delete(0, "end")
            self.widget2.insert(0, self.start_value)
            self.widget2.config(state="disabled")
            self.widget2.bind("<Double-1>", self.double_click_cell)
        else:
            self._characteristic[self.widget2][0].delete(0, "end")
            self._characteristic[self.widget2][0].insert(0, self.start_value)
            self._characteristic[self.widget2][0].config(state="disabled")

    def before_change(self, event=None):
        """
        Функция удаляет изменения последней ячейки в случае если
        не были сохранены ее изменения
        Автор: Озирный Максим
        """
        if self.widget2 != 0:
            self.del_change()
        self.change()

    def change(self, event=None):
        """
        Функция изменяет состояние ячейки чтоб ее можно было изменять
        Автор: Озирный Максим
        """
        if self._characteristic[self.widget][1] == "entry":
            self.widget.config(state="normal")
            self.start_value = self.widget.get()
            self.btn_on = Button(self._characteristic[self.widget][0],
                                 text="on", bd=0,
                                 command=self.save_change)
            self.btn_off = Button(self._characteristic[self.widget][0],
                                  text="off", bd=0,
                                  command=self.del_change)
            self.widget.bind('<Return>', self.save_change)
            self.widget.bind('<Escape>', self.del_change)
            self.widget.bind('<Double-1>', self.click_cell)
        else:
            self._characteristic[self.widget][0].config(state="normal")
            self.start_value = self._characteristic[self.widget][0].get()
            self.btn_on = Button(self.widget,
                                 text="on", bd=0,
                                 command=self.save_change)
            self.btn_off = Button(self.widget,
                                  text="off", bd=0,
                                  command=self.del_change)
            self._characteristic[self.widget][0].bind('<Return>',
                                                      self.save_change)
            self._characteristic[self.widget][0].bind('<Escape>',
                                                      self.del_change)
            self._characteristic[self.widget][0].bind('<Double-1>',
                                                      self.click_cell)

        for key in self._characteristic.keys():
            if self._characteristic[key][2] == 0 and \
                    self._characteristic[key][1] == "entry":
                key.config(
                    width=self.list_max[self._characteristic[key][3]] + 2)
                if self._characteristic[key][3] == \
                        self._characteristic[self.widget][3]:
                    key.config(
                        width=self.list_max[self._characteristic[key][3]] + 9)

        self.btn_on.grid(row=0, column=1)
        self.btn_off.grid(row=0, column=2)
        self.widget2 = self.widget

    def context_menu(self, event=None):
        """
        Функция вызывает соответсвующее контекстное меню в зависимости от
        параметров ячейки (закрашена она или нет)
        Автор: Озирный Максим
        """
        self.new_xy_menu()
        if self._characteristic[self.widget][-2]:
            self.black_menu.post(event.x_root, event.y_root)
        else:
            self.menu.post(event.x_root, event.y_root)

    def widget_pointer(self, event=None):
        """
        Функция вычисляет на коком объекте находится курсор

        возвращает имя объекта в виде строки
        Автор: Озирный Максим
        """
        x, y = self.master.winfo_pointerxy()
        widget = self.master.winfo_containing(x, y)
        return widget

    def click_title(self, event=None):
        """
        Функия сортирует содержимое по столбцу
        Автор: Озирный Максим
        """
        widget = self.widget_pointer()
        num = self._characteristic[widget][3]

        for key in self._characteristic.keys():
            if not self._characteristic[key][-1] and \
                    self._characteristic[key][4] == \
                    self._characteristic[key][2] * len(self._bd_array[0]):
                self._bd_array[self._characteristic[key][2]] = 0
        i = 0
        while i < len(self._bd_array):
            if self._bd_array[i] == 0:
                del self._bd_array[i]
            else:
                i += 1

        array_titles = self._bd_array[0]
        array_cell = []
        for ind in range(len(self._bd_array) - 1):
            array_cell.append(self._bd_array[ind + 1])
        array_cell.sort(key=lambda x: x[num])
        array = []
        for ind in range(len(array_cell)):
            array.append(array_cell[ind])
        array.insert(0, array_titles)

        self.content(array)

    def click_cell(self, event=None):
        """
        Функция закрашивающая или наоборот строку
        Автор: Озирный Максим
        """
        widget = self.widget_pointer()
        # если нажали на entry
        if self._characteristic[widget][1] == "entry":
            # если ячейка была заблокирована
            if "{}".format(widget["state"]) == "disabled":
                # если ячейка не была выбрана
                if not self._characteristic[widget][-2]:
                    for key in self._characteristic.keys():
                        # если строка совпадает
                        if self._characteristic[key][2] == \
                                self._characteristic[widget][2]:
                            # меняем флаг, отвечающий за выбранность строки
                            self._characteristic[key][-2] = not \
                                self._characteristic[key][-2]
                            # если это фрейм
                            if self._characteristic[key][1] == "frame":
                                key.config(bg=COLOR_BG_SELECT_ROW)
                            else:
                                key.config(
                                    disabledbackground=COLOR_BG_SELECT_ROW)
                else:
                    self.repaint(self._characteristic[widget][2])
                    # for key in self._characteristic.keys():
                    #     # если строка совпадает
                    #     if self._characteristic[key][2] == \
                    #             self._characteristic[widget][2]:
                    #         # меняем флаг, отвечающий за выбранность строки
                    #         self._characteristic[key][-2] = not \
                    #             self._characteristic[key][-2]
                    #         if self._characteristic[key][2] % 2 == 0:
                    #             if self._characteristic[key][1] == "frame":
                    #                 key.config(bg=COLOR_BG_EVENT_ROW)
                    #             else:
                    #                 key.config(
                    #                     disabledbackground=COLOR_BG_EVENT_ROW)
                    #         else:
                    #             if self._characteristic[key][1] == "frame":
                    #                 key.config(bg=COLOR_BG_ODD_ROW)
                    #             else:
                    #                 key.config(
                    #                     disabledbackground=COLOR_BG_ODD_ROW)
        else:
            if not self._characteristic[widget][-2]:
                for key in self._characteristic.keys():
                    if self._characteristic[key][2] == \
                            self._characteristic[widget][2]:
                        self._characteristic[key][-2] = not \
                        self._characteristic[key][-2]
                        if self._characteristic[key][1] == "frame":
                            key.config(bg=COLOR_BG_SELECT_ROW)
                        else:
                            key.config(
                                disabledbackground=COLOR_BG_SELECT_ROW)
            else:
                self.repaint(self._characteristic[widget][2])
                # for key in self._characteristic.keys():
                #     if self._characteristic[key][2] == \
                #             self._characteristic[widget][2]:
                #         self._characteristic[key][-2] = not \
                #         self._characteristic[key][-2]
                #         if self._characteristic[key][2] % 2 == 0:
                #             if self._characteristic[key][1] == "frame":
                #                 key.config(bg=COLOR_BG_EVENT_ROW)
                #             else:
                #                 key.config(
                #                     disabledbackground=COLOR_BG_EVENT_ROW)
                #         else:
                #             if self._characteristic[key][1] == "frame":
                #                 key.config(bg=COLOR_BG_ODD_ROW)
                #             else:
                #                 key.config(disabledbackground=COLOR_BG_ODD_ROW)

    def double_click_cell(self, event=None):
        """
        Функция отменяет закрашивание строки и вызывает функцию позволяющую
        изменять содержимое ячейки
        """
        self.new_xy_menu()
        if self.widget2 != 0:
            self.del_change()
        self.click_cell(event)
        self.change()

    def on_frame_configure(self, main_lab2):
        """
        Функция необходимая для прокрутки содержимого в canvas
        Автор: Озирный Максим

        принимает объект параметры которого нужно изменить при прокрутке
        """
        main_lab2.configure(scrollregion=main_lab2.bbox("all"))

    def max_width(self, array, list, only=-1):
        """
        Функция высчитывает максимальную ширину столбцов в массиве
        Автор: Озирный Максим

        принимает двумерный массив (список списков), список для результата,
        колонку в которой нужно проверить результат
        """
        if only != -1:
            max = len(array[0][only])
            for row in range(len(array)):
                if max < len(array[row][only]):
                    max = len(array[row][only])
                if max < len(array[0][only]) + 3:
                    max = len(array[0][only]) + 3
            list[only] = max
        else:
            for col in range(len(array[0])):
                max = len(array[0][col])
                for row in range(len(array)):
                    if max < len(array[row][col]):
                        max = len(array[row][col])
                    if max < len(array[0][col]) + 3:
                        max = len(array[0][col]) + 3
                list[col] = max

    def add_arrow(self, list):
        """
        Функция изменяющая текст в элементах списка
        Автор: Озирный Максим

        принимает список
        """
        for ind in range(len(list)):
            list[ind] += " ▲▼"

    def content(self, array):
        """
        Функция заполняет таблицу данными
        Автор: Озирный Максим

        принимает двумерный массив (список списков)
        """
        self._bd_array = array
        self.widget2 = 0
        self.max_width(array, self.list_max)
        for child in self.titles.winfo_children():
            for child2 in child.winfo_children():
                child2.destroy()
            child.destroy()

        for child in self.frame2.winfo_children():
            for child2 in child.winfo_children():
                child2.destroy()
            child.destroy()

        self.add_arrow(array[0])
        self._characteristic = {}
        for row in range(len(array)):
            self.frame2.grid_rowconfigure(row, minsize=HEIGHT_ROW)
            for col in range(len(array[0])):
                if row == 0:
                    self.new_frame = Frame(self.titles)
                    self.cell = Entry(self.new_frame,
                                      disabledforeground=COLOR_TEXT_TITLE,
                                      fg=COLOR_TEXT_TITLE)
                    self.cell.bind("<Button-1>", self.click_title)
                    self._characteristic.update({
                        self.cell: [self.new_frame, "entry", row, col,
                                    row * len(array[0]) + col,
                                    False, True]})
                    self._characteristic.update({
                        self.new_frame: [self.cell, "frame", row, col,
                                         row * len(array[0]) + col,
                                         False, True]})
                else:
                    self.new_frame = Frame(self.frame2)
                    self.cell = Entry(self.new_frame,
                                      disabledforeground=COLOR_TEXT_TABLE,
                                      fg=COLOR_TEXT_TABLE)
                    self.cell.bind("<Button-1>", self.click_cell)
                    self.cell.bind("<Double-1>", self.double_click_cell)
                    self.cell.bind("<Button-3>", self.context_menu)
                    self.new_frame.bind("<Button-1>", self.click_cell)
                    self.new_frame.bind("<Double-1>", self.double_click_cell)
                    self.new_frame.bind("<Button-3>", self.context_menu)
                    self._characteristic.update({
                        self.cell: [self.new_frame, "entry", row, col,
                                    row * len(array[0]) + col,
                                    False, True]})
                    self._characteristic.update({
                        self.new_frame: [self.cell, "frame", row, col,
                                         row * len(array[0]) + col,
                                         False, True]})
                self.cell.insert(0, "{}".format(array[row][col]))
                self.new_frame.config(bg=COLOR_BG_ODD_ROW, pady=5)
                self.new_frame.grid(row=row, column=col, sticky="nwes")
                self.cell.grid(sticky="nwes")
                self.cell.config(relief="flat", width=self.list_max[col]+2,
                                 state="disabled",
                                 bg="#fff",
                                 disabledbackground=COLOR_BG_ODD_ROW
                                 )
                if row % 2 == 0:
                    self.new_frame.config(bg=COLOR_BG_EVENT_ROW)
                    self.cell.config(disabledbackground=COLOR_BG_EVENT_ROW)
                if row == 0:
                    self.new_frame.config(bg=COLOR_BG_TITLE_TABLE)
                    self.cell.config(disabledbackground=COLOR_BG_TITLE_TABLE)
        self.frame2.grid_rowconfigure(0, minsize=0)


class Btn(Button):
    """
    Класс кнопки со встроенной функцией необходимой для проверки нахождения
    курсора на момент нажатия ЛКМ и ее отжатия
    Автор: Озирный Максим
    """
    widget1 = ""
    def __init__(self, master, **kw):
        super().__init__(master, {}, **kw)
        self.bind("<ButtonPress-1>", self.widget_pointer)

    def widget_pointer(self, event=None):
        """
        Функция вычисляет на коком объекте находится курсор
        Автор: Озирный Максим
        """
        x, y = self.master.winfo_pointerxy()
        widget = self.master.winfo_containing(x, y)
        self.widget1 = "{}".format(widget)

class OptionsMenu(Menu, MainMenuListener):
    """
    Класс отвечающий за создание верхнего меню
    """

    def __init__(self, master,
                 main_wind_listener: IWindowListener, **kw):
        super().__init__(master, {}, **kw)

        self.main_wind_listener = main_wind_listener

    def exit(self):
        self.main_wind_listener.close()

    def create_menu(self):
        """asd"""
        menu_factory = MainMenuFactory(self)

        menu_file = menu_factory.get_menu(MENU_FILE_TEXT,
                                          menu_factory.get_file_items())
        menu_report = menu_factory.get_menu(MENU_REPORT_TEXT,
                                            menu_factory.get_report_items())

        main_menu = Menu()
        main_menu.add_cascade(menu_file)
        main_menu.add_cascade(menu_report)

        self.master.config(menu=main_menu)

    @staticmethod
    def create_simple_report():
        pass

    @staticmethod
    def create_statistic_report():
        pass

    @staticmethod
    def create_pivot_report():
        pass

    @staticmethod
    def create_scatter_chart():
        SettingsScatterChart(Tk())

    @staticmethod
    def create_bar_chart():
        SettingsBarChart(Tk())

    @staticmethod
    def create_box_and_whisker():
        SettingsBoxAndWhisker(Tk())

    @staticmethod
    def create_histogram():
        SettingsHistogram(Tk())

    @staticmethod
    def edit_db():
        DbEditorWindow(Tk(), "Расширенное редактирование БД")
