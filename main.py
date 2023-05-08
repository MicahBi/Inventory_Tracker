# Imports
from tkinter import ttk
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter.font as font
import numpy as np
import matplotlib.animation as animation

# Globals
global display_label


class Application:
    def __init__(self, master):
        # Create Interface
        # Create Window
        self.master = master
        self.master.title('Item Tracker')
        self.master.geometry(f"{master.winfo_screenwidth()}x{master.winfo_screenheight()}+0+0")

        # Create Frame
        self.main_frame = Frame(master)

        # Create Canvas
        self.main_canvas = Canvas(self.main_frame)

        # Add Scroll Bar
        main_scroll = ttk.Scrollbar(self.main_frame, orient=VERTICAL, command=self.main_canvas.yview)

        # Configure Canvas
        self.main_canvas.configure(yscrollcommand=main_scroll.set)
        self.main_canvas.bind('<Configure>',
                              lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")))

        # Create Frame2
        self.frame_draw = Frame(self.main_canvas)

        # Make Window
        self.main_canvas.create_window((0, 0), window=self.frame_draw, anchor="nw")


        # Title
        my_font = font.Font(family='Bookman Old Style')
        title_label = Label(self.frame_draw, text="Item Tracker", font=my_font)

        # Make Window Dynamically Resizable
        Grid.rowconfigure(master, 0, weight=1)
        Grid.columnconfigure(master, 0, weight=1)

        # Position Canvas anf Frame Backdrop
        main_scroll.pack(side=RIGHT, fill=Y)
        self.main_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.main_frame.pack(fill=BOTH, expand=1)

        # Call Interface Methods (Make Interface Interactive)
        tree_view = self.tree_view()
        tree_view_buttons = self.tree_view_buttons()
        self.display_items_tree()
        graph = self.graph_create()
        graph_buttons = self.graph_buttons()

        # Position Content
        tree_view.grid(row=2, column=0, pady=10, padx=5)
        tree_view_buttons.grid(row=2, column=1, pady=10, padx=5, sticky=N)
        graph_buttons.grid(row=2, column=1, sticky=W + S)
        graph.grid(row=3, column=0, columnspan=2, pady=50)
        title_label.grid(row=0, column=0, pady=15)

    # Declare tree_view to Make Table
    def tree_view(self):
        my_frame = Frame(self.frame_draw)

        # Scrollbar for List
        tree_scroll = Scrollbar(my_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create Treeview List
        self.tv = ttk.Treeview(my_frame, yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=self.tv.yview)
        self.tv.pack()

        # Create Components of Treeview
        self.tv['columns'] = ('Name', 'Amount', 'Price')
        self.tv.column('#0', width=0, stretch=NO)
        self.tv.column('Name', anchor=CENTER, width=80)
        self.tv.column('Amount', anchor=CENTER, width=80)
        self.tv.column('Price', anchor=CENTER, width=80)

        self.tv.heading('#0', text='', anchor=CENTER)
        self.tv.heading('Name', text='Name', anchor=CENTER)
        self.tv.heading('Amount', text='Amount', anchor=CENTER)
        self.tv.heading('Price', text='Price', anchor=CENTER)

        return my_frame

    # Declare tree_view_buttons to Interact with Treeview
    def tree_view_buttons(self):
        my_frame = Frame(self.frame_draw)

        # Create Entry Boxes
        self.price_entry = Entry(my_frame)
        self.item_entry = Entry(my_frame)
        self.name_entry = Entry(my_frame)

        # Create Buttons
        self.change_item_tree = Button(my_frame, text='Change Item', command=self.change_item_tree)
        self.add_item_tree = Button(my_frame, text="Add Item", command=self.add_item_tree)
        self.tree_data = Button(my_frame, text="Show List", command=self.display_items_tree)
        self.delete_all_tree = Button(my_frame, text="Delete All", command=self.delete_all_tree)
        self.delete_tree = Button(my_frame, text="Delete Selected", command=self.delete_tree)

        # Create Labels
        global display_label

        self.price_label = Label(my_frame, text="Price")
        self.item_label = Label(my_frame, text="Amount")
        self.name_label = Label(my_frame, text="Name")
        self.display_label = Label(my_frame, text="")

        # Display & Position
        self.delete_tree.grid(row=0, column=0, pady=5)
        self.delete_all_tree.grid(row=0, column=2, pady=5)
        self.change_item_tree.grid(row=3, column=0, pady=5)
        self.add_item_tree.grid(row=3, column=2, pady=5)
        self.price_entry.grid(row=2, column=2, pady=5)
        self.item_entry.grid(row=2, column=1, pady=5)
        self.name_entry.grid(row=2, column=0, pady=5)
        self.price_label.grid(row=1, column=2, pady=2)
        self.item_label.grid(row=1, column=1, pady=2)
        self.name_label.grid(row=1, column=0, pady=2)
        self.display_label.grid(row=3, column=1, pady=2, padx=5)
        self.tree_data.grid(row=0, column=1, pady=5)

        return my_frame

    # Declare Display to tv Function
    def display_items_tree(self):
        # Delete Existing Content
        for i in self.tv.get_children():
            self.tv.delete(i)

        # Initialize Variables
        count = 0
        data = []

        # Read New Data from Items.txt
        items_file = open("Items.txt", "r")
        items_list = items_file.read().splitlines()
        for x in items_list:
            component = x.split(",")
            data.append(component)

        # Display New Treeview
        for record in data:
            self.tv.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2]))
            count = count + 1
        items_file.close()

    # Declare change_item_tree to Change Treeview Data
    def change_item_tree(self):
        # Retrieve Selection
        selected = self.tv.focus()
        temp = self.tv.item(selected, 'values')
        record = [self.name_entry.get(), self.item_entry.get(), self.price_entry.get()]

        # Check for empty spaces
        if self.name_entry.get() == "" or self.name_entry.get() == " ":
            record[0] = temp[0]

        if self.item_entry.get() == "" or self.item_entry.get() == " ":
            record[1] = temp[1]

        if self.price_entry.get() == "" or self.price_entry.get() == " ":
            record[2] = temp[2]

        elif self.item_entry.get().isdigit() == False or self.price_entry.get().isdigit() == False:
            self.display_label.config(text="Please enter number for Amount & Price.")

        else:
            # Update Items.txt
            items_file = open("Items.txt", "r")
            items_list = items_file.read().splitlines()
            items_list.pop(int(selected))
            items_list.insert(int(selected), ', '.join(map(str, record)))
            items_file.close()
            items_file = open("Items.txt", "w")
            for i in items_list:
                items_file.writelines(str(i) + "\n")
            items_file.close()

            # Update Treeview
            self.tv.item(selected, values=(record[0], record[1], record[2]))

    # Declare delete_all_tree to Delete All Treeview Content
    def delete_all_tree(self):
        # Write Over Items.txt
        items_file = open("Items.txt", "w")
        items_file.write("")
        items_file.close()

        # Delete Info in Treeview
        for record in self.tv.get_children():
            self.tv.delete(record)

    # Declare delete_tree to Delete Selected Item in Treeview
    def delete_tree(self):
        # Get Selected in a List
        x = list(self.tv.selection())
        print(self.tv.selection())
        # Read Items.txt
        items_file = open("Items.txt", "r")
        items_list = items_file.read().splitlines()
        print(x)
        # Delete Items Selected
        for i in sorted(x, reverse=True):
            del items_list[int(i)]
            self.tv.delete(int(i))
        items_file.close()

        # Update Items.txt
        items_file = open("Items.txt", "w")
        for i in items_list:
            items_file.writelines(str(i) + "\n")
        items_file.close()

    # Declare add_item_tree to Add Information to Treeview
    def add_item_tree(self):
        # Call Count
        global count

        # Retrieve Information
        record = [self.name_entry.get(), self.item_entry.get(), self.price_entry.get()]

        if self.item_entry.get().isdigit() is False or self.price_entry.get().isdigit() is False:
            self.display_label.config(text="Please enter number for Amount & Price.")

        else:
            # Update Items.txt
            items_file = open("Items.txt", "r")
            items_list = items_file.read().splitlines()
            items_list.append(', '.join(map(str, record)))
            items_file.close()
            items_file = open("Items.txt", "w")
            for i in items_list:
                items_file.writelines(str(i) + "\n")
            items_file.close()

            # Update Treeview
            self.tv.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2]))
            count += 1

    # Declare graph_create to Display Data in Graph_Items.txt
    def graph_create(self):
        my_frame = Frame(self.frame_draw)

        # The Figure that will Contain the Plot
        fig = Figure(figsize=(6, 3), dpi=100)

        # Adding the Subplot
        self.plot1 = fig.add_subplot(111)

        # Declare Animate to Update Data
        def animate(i):
            # Get Coordinates and Labels from Graph_Items.txt
            items_file = open("Graph_Items.txt", "r")
            items_list = items_file.read().splitlines()

            # Create Lists for Storing Data
            y_price = []
            y_amount = []
            x_price = []
            x_amount = []
            x_labels = []
            ticks = []

            # Compile Data
            for i in range(len(items_list)):
                list_inner = list(items_list[i].split(","))
                y_price.append(float(list_inner[2]))
                y_amount.append(float(list_inner[1]))
                x_price.append(i + 1)
                x_amount.append(i + 1.5)
                x_labels.append(list_inner[0])
                ticks.append(i + 1)
            items_file.close()

            # Clear Previous Graph
            self.plot1.cla()

            # Plotting the Graph
            label_price = self.plot1.bar(x_price, y_price, width=0.25, color=(0.2, 0.4, 0.6, 0.6), label="Price ($)")
            label_amount = self.plot1.bar(x_amount, y_amount, width=0.25, color=(0.2, 0.2, 0.2, 1.0), label="Amount")

            # Labeling Title & Axis
            self.plot1.set_title('Amount vs. Price', loc="center")
            self.plot1.set_xticks(ticks, minor=False)
            self.plot1.set_xticklabels(x_labels, fontsize=6)
            self.plot1.legend(bbox_to_anchor=(0, 1, 1, 0.1), ncol=2, mode="expand", loc="lower left")
            self.plot1.bar_label(label_price, padding=3)
            self.plot1.bar_label(label_amount, padding=3)

        # Creating the Tkinter Canvas for the Matplotlib Figure
        canvas = FigureCanvasTkAgg(fig, master=my_frame)

        # Update in Real-Time
        self.ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), interval=25, blit=False)

        # Draw Graph for TKinter
        canvas.draw()

        # Placing the Canvas on the Tkinter Window
        canvas.get_tk_widget().pack()

        # Creating the Matplotlib Toolbar
        toolbar = NavigationToolbar2Tk(canvas, my_frame)
        toolbar.update()
        plt.show()

        # Placing the Toolbar on the Tkinter Window
        canvas.get_tk_widget().pack()

        return my_frame

    # Declare grph_buttons to Interact with Graph and Graph_Items.txt
    def graph_buttons(self):
        my_frame = Frame(self.frame_draw)

        # Buttons
        self.graph_data_button = Button(my_frame, text="Show Graph Data", command=self.graph_data)
        self.graph_add_button = Button(my_frame, text="Add Data", command=self.graph_add)
        self.graph_delete_button = Button(my_frame, text="Delete Data Item", command=self.graph_delete)

        # Labels
        self.graph_buttons_label = Label(my_frame, text="Graph Data (Manipulate Graph)")

        # Position
        self.graph_buttons_label.grid(column=0, row=0, sticky=W)
        self.graph_data_button.grid(column=0, row=1, sticky=N + W, padx=10)
        self.graph_add_button.grid(column=2, row=1, sticky=N + W, padx=10)
        self.graph_delete_button.grid(column=1, row=1, sticky=N + W, padx=10)

        return my_frame

    # Declare graph_data to show Graph_Items.txt's List in Treeview
    def graph_data(self):
        global count2

        # Clear Treeview
        for i in self.tv.get_children():
            self.tv.delete(i)

        # Declare Variables
        count2 = 0
        data = []

        # Read Graph_Items.txt
        items_file = open("Graph_Items.txt", "r")
        items_list = items_file.read().splitlines()
        for x in items_list:
            component = x.split(",")
            data.append(component)

        # Update Treeview
        for record in data:
            self.tv.insert(parent='', index='end', iid=count2, text="", values=(record[0], record[1], record[2]))
            count2 += 1
        items_file.close()

    # Declare graph_add to Add Data to Graph_Items.txt
    def graph_add(self):
        global count2

        # Retrieve Information
        record = [self.name_entry.get(), self.item_entry.get(), self.price_entry.get()]
        selected = self.tv.focus()
        temp = self.tv.item(selected, 'values')
        if self.name_entry.get() == "" or self.name_entry.get() == " ":
            record[0] = temp[0]

        if self.item_entry.get() == "" or self.item_entry.get() == " ":
            record[1] = temp[1]

        if self.price_entry.get() == "" or self.price_entry.get() == " ":
            record[2] = temp[2]

        elif self.item_entry.get().isdigit() == False or self.price_entry.get().isdigit() == False:
            self.display_label.config(text="Please enter number for Amount & Price.")

        else:
            # Update Items.txt
            items_file = open("Graph_Items.txt", "r")
            items_list = items_file.read().splitlines()
            items_list.append(', '.join(map(str, record)))
            items_file.close()
            items_file = open("Graph_Items.txt", "w")
            for i in items_list:
                items_file.writelines(str(i) + "\n")
            items_file.close()

            # Update Treeview
            self.tv.insert(parent='', index='end', iid=count2, text="", values=(record[0], record[1], record[2]))
            count2 += 1

    def graph_delete(self):
        x = list(self.tv.selection())
        # Update Items.txt
        items_file = open("Graph_Items.txt", "r")
        items_list = items_file.read().splitlines()
        for i in sorted(x, reverse=True):
            del items_list[int(i)]
            self.tv.delete(int(i))
        items_file.close()
        items_file = open("Graph_Items.txt", "w")
        for i in items_list:
            items_file.writelines(str(i) + "\n")
        items_file.close()


root = Tk()
app = Application(root)
root.mainloop()
