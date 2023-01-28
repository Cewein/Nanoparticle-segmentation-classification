# This file define the GUI
# The GUI is a python port of DearImGui original writtten in C++
# Import need to run the GUI

import dearpygui.dearpygui as dpg
import src.utils

def resizeCallback():

    #resize the main window
    dpg.set_item_width("main_winow",dpg.get_viewport_width())
    dpg.set_item_height("main_winow",dpg.get_viewport_height())

    height = dpg.get_item_height("main_winow")*0.95
    width = dpg.get_item_width("main_winow")*0.95

    dpg.set_item_height("sub_table",height*0.8)
    dpg.set_item_height("sub_windows_left",height*0.8)
    dpg.set_item_height("sub_windows_center",height*0.8)
    dpg.set_item_height("sub_windows_right",height*0.8)



dpg.get_item_height

#main function
def display():
    #create the window and add the display context
    dpg.create_context()
    dpg.create_viewport(title='NaSe - Segmentation and classification')

    dpg.set_viewport_resize_callback(resizeCallback)

    #draw the GUI
    with dpg.window(label="NaSe", tag="main_winow", width=dpg.get_viewport_width(),height=dpg.get_viewport_height(),
            no_close=True, no_scrollbar=True, no_resize=True, no_collapse=True, no_title_bar=True):
        layout()
        

    #closing setup
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

def layout():

    height = dpg.get_item_height("main_winow")*0.95
    width = dpg.get_item_width("main_winow")*0.95

    #display meny
    with dpg.menu_bar():
        with dpg.menu(label="Menu"):
            dpg.add_button(tag="file_selector", label="Open File", callback=src.utils.fileDialogue)
    
    #create a table for the 3 sub windows on top
    with dpg.table(tag="sub_table", header_row=False, borders_innerH=False,
                borders_outerH=False, borders_innerV=False, borders_outerV=False,height=height*0.8,resizable=True):
                    
        dpg.add_table_column(init_width_or_weight=0.15)
        dpg.add_table_column(init_width_or_weight=0.65)
        dpg.add_table_column(init_width_or_weight=0.25)

        with dpg.table_row():
            with dpg.child_window(tag="sub_windows_left", autosize_x=True, height=height*0.8,border=False):
                with dpg.tree_node(label="Nav 1"):
                    dpg.add_button(label="Button 1")
                with dpg.tree_node(label="Nav 2"):
                    dpg.add_button(label="Button 2")
                with dpg.tree_node(label="Nav 3"):
                    dpg.add_button(label="Button 3")
            with dpg.child_window(tag="sub_windows_center", autosize_x=True, height=height*0.8,border=False):
                dpg.add_button(label="Button 1")
                dpg.add_button(label="Button 2")
                dpg.add_button(label="Button 3")
            with dpg.child_window(tag="sub_windows_right", autosize_x=True, height=height*0.8,border=False):
                dpg.add_button(label="B1", width=25, height=25)
                dpg.add_button(label="B2", width=25, height=25)
                dpg.add_button(label="B3", width=25, height=25)

    #bottom window
    dpg.add_separator()
    with dpg.child_window(autosize_x=True, autosize_y=True,border=False):
        with dpg.group(horizontal=True):
            dpg.add_button(label="Header 1")
            dpg.add_button(label="Header 2")
            dpg.add_button(label="Header 3")