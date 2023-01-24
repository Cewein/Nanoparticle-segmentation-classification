# This file define the GUI
# The GUI is a python port of DearImGui original writtten in C++
# Import need to run the GUI

import dearpygui.dearpygui as dpg

def resizeDemo():
    print(dpg.get_viewport_pos())
    print(dpg.get_viewport_height())
    print(dpg.get_viewport_client_height())

#main function
def display():
    #create the window and add the display context
    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=600, height=600)

    #dpg.set_viewport_resize_callback(resizeDemo)

    dpg.add

    #draw the GUI
    with dpg.window(label="NaSe", tag="main_winow", width=dpg.get_viewport_width(),height=dpg.get_viewport_height()):
        layout()
        

    #closing setup
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

def layout():

    dpg.add_text("Containers can be nested for advanced layout options")
    with dpg.child_window(width=500, height=320):
        with dpg.menu_bar():
            dpg.add_menu(label="Menu Options")
        with dpg.child_window(autosize_x=True, height=95):
            with dpg.group(horizontal=True):
                dpg.add_button(label="Header 1", width=75, height=75)
                dpg.add_button(label="Header 2", width=75, height=75)
                dpg.add_button(label="Header 3", width=75, height=75)
        with dpg.child_window(autosize_x=True, height=175):
            with dpg.group(horizontal=True, width=0):
                with dpg.child_window(width=102, height=150):
                    with dpg.tree_node(label="Nav 1"):
                        dpg.add_button(label="Button 1")
                    with dpg.tree_node(label="Nav 2"):
                        dpg.add_button(label="Button 2")
                    with dpg.tree_node(label="Nav 3"):
                        dpg.add_button(label="Button 3")
                with dpg.child_window(width=300, height=150):
                    dpg.add_button(label="Button 1")
                    dpg.add_button(label="Button 2")
                    dpg.add_button(label="Button 3")
                with dpg.child_window(width=50, height=150):
                    dpg.add_button(label="B1", width=25, height=25)
                    dpg.add_button(label="B2", width=25, height=25)
                    dpg.add_button(label="B3", width=25, height=25)
        with dpg.group(horizontal=True):
            dpg.add_button(label="Footer 1", width=175)
            dpg.add_text("Footer 2")
            dpg.add_button(label="Footer 3", width=175)