import exe
import kivy
import numpy as np
import os
import re
import sys

import pathlib


from kivy.app import App
from kivy.uix.image import Image
from kivy.config import Config
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

kivy.require('1.11.1')

MATERIALS = None

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 640
WINDOW_MIN_HEIGHT = 480
WINDOW_MIN_WIDTH = 600

Config.set('graphics', 'width', WINDOW_WIDTH)
Config.set('graphics', 'height', WINDOW_HEIGHT)
Config.set('graphics', 'minimum_width', WINDOW_MIN_WIDTH)
Config.set('graphics', 'minimum_height', WINDOW_MIN_HEIGHT)

#This is the color for the background of the tabs, not the color on each tab.
Window.clearcolor = (.75, .75, .75, 1)

class ArrayPlotButton(Button):
    def __init__(self, **kwargs):
        super(ArrayPlotButton, self).__init__(**kwargs)

    def ArrayPlot(self):
        command = "arrayplot "
        name = ""
        parameters = ""
        for i in self.parent.children:
            if i.name == "array_plot_inputs":
                a2p_inputs = i.children[0].children
                parameters = " -c " + a2p_inputs[2].text + " -g " + a2p_inputs[1].text + " -e " + a2p_inputs[0].text 
                    
            elif i.name == "image_input":
                name = j.current_file_name

        command += name + ".xxx.meta.txt " + parameters
        print (command)
        os.system(command)

class CodisplayButton(Button):
    def __init__(self, **kwargs):
        super(CodisplayButton, self).__init__(**kwargs)

    def Codisplay(self):
        command = "codisplay "
        name = ""
        parameters = ""
        for i in self.parent.children:
            if i.name == "codisplay_input_fields":
                co_input = i.children[0].children
                parameters = " -c " + co_input[2].text + " -g " + co_input[1].text + " -e " + co_input[0].text 
                    
            elif i.name == "image_input":
                name = j.current_file_name

        command += name + ".xxx.meta.txt " + parameters
        print (command)
        os.system(command)

class Image2AnimationButton(Button):
    def __init__(self, **kwargs):
        super(Image2AnimationButton, self).__init__(**kwargs)

    def Image2Animation(self):
        command = "im2anim "
        name = ""
        parameters = ""
        for i in self.parent.children:
            if i.name == "image_2_animation_input":
                i2a_inputs = i.children[0].children
                parameters = " -c " + i2a_inputs[2].text + " -n " + i2a_inputs[1].text + " -f " + i2a_inputs[0].text 
                    
            elif i.name == "image_input":
                name = j.current_file_name

        command += name + ".xxx.meta.txt " + parameters
        print (command)
        #os.system(command)

class ArrayPlotInputFields(RelativeLayout):
    pass

class CodisplayInputFields(RelativeLayout):
    pass

class Image2AnimationInputFields(RelativeLayout):
    pass

class MultiShotInputFields(RelativeLayout):
    pass

class CommonOffsetInputFields(RelativeLayout):
    pass

class CommonMidpointInputFields(RelativeLayout):
    pass

class SeismicInputFields(RelativeLayout):
    pass

class RadarInputFields(RelativeLayout):
    pass

class SpatialInputFields(RelativeLayout):
    pass

class MaterialInputBox(BoxLayout):
    pass

class DimensionButtons(RelativeLayout):
    pass

class GlacierImage(Image):
    pass

class MaterialLabelBox(RelativeLayout):
    pass

class MaterialInputRegion(ScrollView):
    def __init__(self, **kwargs):
        super(MaterialInputRegion, self).__init__(**kwargs)

class RunButton(Button):
    def __init__(self, **kwargs):
        super(RunButton, self).__init__(**kwargs)

    def run(self):
        curr_prj_file_name = ""
        for widget in self.parent.children:
            if widget.name == "image_input":
                curr_prj_file_name = widget.current_file_name
                command = "python exe/prjbuild.py -i gui/" + widget.current_file_name + ".png -o gui/" + widget.current_file_name + ".prj"
                os.system(command)

        run_seismic = False
        run_radar = False

        prj_file = open("gui/" + curr_prj_file_name + ".prj", "r+")
        prj_text = prj_file.read()
        for top_level_widget in self.parent.children:
            if top_level_widget.name == "radar":
                radar = top_level_widget.children[0]
                prj_text = re.sub("E,time_steps,", "E,time_steps," + radar.children[6].text, prj_text)
                prj_text = re.sub("E,x,", "E,x," + radar.children[10].text, prj_text)
                prj_text = re.sub("E,y,", "E,y," + radar.children[9].text, prj_text)
                prj_text = re.sub("E,z,", "E,z," + radar.children[8].text, prj_text)
                prj_text = re.sub("E,f0,", "E,f0," + radar.children[2].text, prj_text)
                prj_text = re.sub("E,theta,0", "E,theta," + radar.children[4].text, prj_text)
                prj_text = re.sub("E,phi,0", "E,phi," + radar.children[0].text, prj_text)
                run_radar = radar.children[12].active
            elif top_level_widget.name == "seismic":
                seismic = top_level_widget.children[0]
                prj_text = re.sub("S,time_steps,", "S,time_steps," + seismic.children[6].text, prj_text)
                prj_text = re.sub("S,x,", "S,x," + seismic.children[10].text, prj_text)
                prj_text = re.sub("S,y,", "S,y," + seismic.children[9].text, prj_text)
                prj_text = re.sub("S,z,", "S,z," + seismic.children[8].text, prj_text)
                prj_text = re.sub("S,f0,", "S,f0," + seismic.children[2].text, prj_text)
                prj_text = re.sub("S,theta,0", "S,theta," + seismic.children[4].text, prj_text)
                prj_text = re.sub("S,phi,0", "S,phi," + seismic.children[0].text, prj_text)
                run_seismic = seismic.children[12].active
            elif top_level_widget.name == "spatial_information":
                spatial = top_level_widget.children[0]
                prj_text = re.sub("D,dx,", "D,dx," + spatial.children[4].text, prj_text)
                prj_text = re.sub("D,dy,n/a", "D,dy," + spatial.children[3].text, prj_text)
                prj_text = re.sub("D,dz,", "D,dz," + spatial.children[2].text, prj_text)
                prj_text = re.sub("D,tfile,", "D,tfile," + spatial.children[0].text, prj_text)
                prj_text = re.sub("D,cpml,", "D,cpml," + spatial.children[7].text, prj_text)

            elif top_level_widget.name == "material_window":
                material_box_widget = top_level_widget.children[0]

                materialColors = re.findall("\d+/\d+/\d+", prj_text)
                for material in reversed(material_box_widget.children):

                    curr_material = "M," + str(material.material_number) + "," + material.children[6].text + "," + materialColors[
                        material.material_number]

                    for num in range(5, 1, -1):
                        curr_material += "," + material.children[num].text

                    curr_material += ",0"

                    curr_material += "," + str(material.children[1].active) + ","

                    if material.children[1].active:
                        curr_material += material.children[0].text

                    prj_text = re.sub("M.*,,,,,,,", curr_material, prj_text, count=1)

        
        prj_file.seek(0)
        # Update this so it writes the proper material information
        prj_file.write(prj_text)
        prj_file.truncate()

        run_mode = "n"

        if run_seismic and run_radar:
            run_mode = "b"
        elif run_seismic:
            run_mode = "s"
        elif run_radar:
            run_mode = "r"

        #return file name for higher level button types have access to it
        return curr_prj_file_name, run_mode

class SingleRunButton(RunButton):
    def SingleShot(self):
        file_name, run_mode = super().run()

        #single shot specific stuff
        command = "prjrun " + str(pathlib.Path(__file__).parent.absolute()) + "/" + file_name + ".prj -M " + run_mode

        os.system(command)
        print (command)

class CommonOffsetRunButton(RunButton):
    def CommonOffsetShot(self):
        file_name, run_mode = super().run()

        command = "common_offset -f " + file_name + ".prj -F "

        for i in self.parent.children:
            if i.name == "common_offset_shot_input":
                child = i.children[0]

                command += child.children[6].text + " " 
                command += child.children[5].text + " " 
                command += child.children[4].text + " -o " 
                command += child.children[2].text + " -d " 
                command += child.children[0].text + " "
        print (command)
                
        os.system(command)

class CommonMidpointRunButton(RunButton):
    def CommonMidpointShot(self):
        file_name, run_mode = super().run()

        command = "common_midoing -f " + file_name + ".prj -t "

        for i in self.parent.children:
            if i.name == "common_midpoint_shot_input":
                child = i.children[0]
                command += child.children[4].text + " -o "
                command += str(float(int(child.children[4].text)/2.0)) + " -d "
                command += child.children[0].text

        if run_mode == "s":
            command += " s"

        print (command)
        os.system(command)

class MultiRunButton(RunButton):
    def __init__(self, **kwargs):
        super(MultiRunButton, self).__init__(**kwargs)
    
    def MultiShot(self):
        file_name, run_mode = super().run()

        command = "wide_angle -f " + file_name + ".prj -I"

        #multi shot specific stuff
        for i in self.parent.children:
            if i.name == "multi_shot_input":
                child = i.children[0]
                command += " " + child.children[8].text
                command += " " + child.children[7].text
                command += " " + child.children[6].text
                command += " -F"
                command += " " + child.children[4].text
                command += " " + child.children[3].text
                command += " " + child.children[2].text
                command += " -d " + child.children[0].text
                command += " -" + run_mode 


        os.system(command)
        print (command)

class MaterialInputFields(GridLayout):
    def __init__(self, **kwargs):
        super(MaterialInputFields, self).__init__(**kwargs)
        self.material_number = None
        self.color = None

class TotalLayout(TabbedPanel):
    def __init__(self, **kwargs):
        super(TotalLayout, self).__init__(**kwargs)

class ImageInputFields(RelativeLayout):
    def __init__(self, **kwargs):
        super(ImageInputFields, self).__init__(**kwargs)
        
        self.material_box_layout = None
        self.current_image = None
        self.material_scrollview = None
        self.current_file_name = ""
        self.image_input_region_references = []
        self.default_tab = False

    def getImage(self, first_call = True):
        if self.current_image:
            if first_call:
                self.parent.remove_widget(self.material_scrollview)
                self.material_scrollview = None
                self.material_box_layout = None
            self.remove_widget(self.current_image)
            self.current_image = None

        self.current_file_name = self.ids['file_path'].text

        if first_call:
            for i in self.image_input_region_references:
                if not i == self:
                    for j in i.children:
                        if j.name == "file_name":
                            j.text = self.current_file_name
                            i.getImage(first_call= False)
                            break
            

        try:
            test = open("gui/" + self.current_file_name + ".png")
        except:
            print ("Image not found")
            return

        self.current_image = GlacierImage()

        self.current_image.source = "gui/" + self.current_file_name + ".png"

        self.add_widget(self.current_image)

        # prjbuild -i /path/to/geometry/image.png -o project_filename.prj
        if self.default_tab:
            # find a way to call prjbuild
            current_prj = None
            current_prj_exists = False
            try:
                current_prj = open("gui/" + self.current_file_name + ".prj", 'r')
                current_prj_exists = True
            except:
                command = "python exe/prjbuild.py -i gui/" + self.current_file_name + ".png -o gui/" + self.current_file_name + ".prj"
                os.system(command)
                current_prj = open("gui/" + self.current_file_name + ".prj", 'r')

            prj_contents = current_prj.read()

            # Acquire the colors from the prj
            colors = re.findall("\d*/\d*/\d*", prj_contents)
            material_colors = []
            for i in range(len(colors)):
                colors_split = colors[i].split("/")

                colors_tuple = (
                (float(colors_split[0]) / 256), (float(colors_split[1]) / 256), (float(colors_split[2]) / 256), 1)

                material_colors.append(colors_tuple)

            material_count = len(re.findall("M,", prj_contents))

            self.material_scrollview = MaterialInputRegion()

            self.material_box_layout = MaterialInputBox(spacing=5, orientation='vertical', size_hint_y=None, height=0, padding=(35,0,5,0)) #padding(left top right bottom)
            
            y=30*(material_count-1)-1
            for material in range(material_count):
                # Replace this with a row for a material
                # Create a new "structure" in the KV file for a row, given the color from the .prj
                temp = MaterialInputFields(size_hint_y=None, height=25)
                
                temp.canvas.add(Color(rgba=material_colors[material]))
                temp.canvas.add(Rectangle(size=(25,25),pos=(5,y)))

                temp.material_number = material
                temp.color = material_colors[material]

                self.material_box_layout.add_widget(temp)
                y=y-30

            #Box_Layout height = Material input hight + spacing * num of materials
            self.material_box_layout.height += (30 * material_count)

            self.material_scrollview.add_widget(self.material_box_layout)

            self.parent.add_widget(self.material_scrollview)

            if current_prj_exists:
                self.readExisting(prj_contents)

    def readExisting(self, contents):
        for top_level_widget in self.parent.children:
            #radar, seismic, spatial_information, material_window / material_box
            if top_level_widget.name == "radar":
                radar = top_level_widget.children[0]
                #populate radar text fields
                radar.children[6].text = re.findall("E,time_steps,\S*", contents)[0][13:]
                radar.children[10].text = re.findall("E,x,\S*", contents)[0][4:]
                radar.children[9].text = re.findall("E,y,\S*", contents)[0][4:]
                radar.children[8].text = re.findall("E,z,\S*", contents)[0][4:]
                radar.children[2].text = re.findall("E,f0,\S*", contents)[0][5:]
                radar.children[4].text = re.findall("E,theta,\S*", contents)[0][8:]
                radar.children[0].text = re.findall("E,phi,\S*", contents)[0][6:]
                for radar_child in radar.children:
                    try:
                        if radar_child.text == "":
                            radar_child.text = None
                    except:
                        pass
            elif top_level_widget.name == "seismic":
                seismic = top_level_widget.children[0]
                #populate radar text fields
                seismic.children[6].text = re.findall("S,time_steps,\S*", contents)[0][13:]
                seismic.children[10].text = re.findall("S,x,\S*", contents)[0][4:]
                seismic.children[9].text = re.findall("S,y,\S*", contents)[0][4:]
                seismic.children[8].text = re.findall("S,z,\S*", contents)[0][4:]
                seismic.children[2].text = re.findall("S,f0,\S*", contents)[0][5:]
                seismic.children[4].text = re.findall("S,theta,\S*", contents)[0][8:]
                seismic.children[0].text = re.findall("S,phi,\S*", contents)[0][6:]
                for seismic_child in seismic.children:
                    try:
                        if seismic_child.text == "":
                            seismic_child.text = None
                    except:
                        pass

            elif top_level_widget.name == "spatial_information":
                spatial = top_level_widget.children[0]
                spatial.children[4].text = re.findall("D,dx,\S*", contents)[0][5:]
                spatial.children[3].text = re.findall("D,dy,\S*", contents)[0][5:]
                spatial.children[2].text = re.findall("D,dz,\S*", contents)[0][5:]

                for spatial_child in spatial.children:
                    try:
                        if spatial_child.text == "":
                            spatial_child.text = None
                    except:
                        pass

            elif top_level_widget.name == "material_window":
                material_box_widget = top_level_widget.children[0]
                for curr_material in zip(re.findall("M,\S*", contents),reversed(material_box_widget.children)):
                    values = curr_material[0].split(",")
                    curr_widget = curr_material[1]

                    curr_widget.children[6].text = values[2]
                    curr_widget.children[5].text = values[4]
                    curr_widget.children[4].text = values[5]
                    curr_widget.children[3].text = values[6]
                    curr_widget.children[2].text = values[7]
                    curr_widget.children[1].active = True if values[9] == "True" else False
                    curr_widget.children[0].text = values[10]
                    #populate the material sections with this information

class SeidarTGUI(App):
    def build(self):
        # base tabbed thing
        base = TotalLayout(size=(WINDOW_WIDTH, WINDOW_HEIGHT))

        # Creating all tab panels
        prj_input_tab = TabbedPanelItem()
        multi_shot_run_tab = TabbedPanelItem()
        plot_panel = TabbedPanelItem()
        help_panel = TabbedPanelItem()
        
        # Naming all tabs
        prj_input_tab.text = "PRJ Info"
        multi_shot_run_tab.text = "PRJ Run" #all runs
        plot_panel.text = "PRJ Plots"
        help_panel.text = "Help Page"

        # layout for the first tabs
        panel1_layout = RelativeLayout()
        panel2_layout = RelativeLayout()
        panel3_layout = RelativeLayout()
        
        #Image input stuff
        panel1_image_input = ImageInputFields()
        panel2_image_input = ImageInputFields()
        panel3_image_input = ImageInputFields()

        #List of image inputs so that each image input region references the others
        image_inputs = [panel1_image_input, panel2_image_input, panel3_image_input]
        panel1_image_input.image_input_region_references = image_inputs
        panel2_image_input.image_input_region_references = image_inputs
        panel3_image_input.image_input_region_references = image_inputs

        #Assigned so that image propogation through the tabs later is simpler
        panel1_image_input.default_tab = True

        # panel1-------------------------------------------------------------
        # PRJ info: imports image, prj data entry, and uses the build and single shot operations.

        # Elements for panel1, minus image importing
        dimension_input_fields = DimensionButtons()
        Spatial_input_fields = SpatialInputFields()
        radar_input_fields = RadarInputFields()
        seismic_input_fields = SeismicInputFields()
        prj_input_run_button = SingleRunButton()
        material_label_box = MaterialLabelBox()

        # Adding elements to panel1 layout
        panel1_layout.add_widget(panel1_image_input)
        panel1_layout.add_widget(dimension_input_fields)
        panel1_layout.add_widget(Spatial_input_fields)
        panel1_layout.add_widget(radar_input_fields)
        panel1_layout.add_widget(seismic_input_fields)
        panel1_layout.add_widget(prj_input_run_button)
        panel1_layout.add_widget(material_label_box)

        # Assigning layout to panel1
        prj_input_tab.add_widget(panel1_layout)

        # panel2-------------------------------------------------------------
        # Run operations: All extra input fields required for all run types.

        # Elements for panel2
        multi_shot_inputs = MultiShotInputFields()
        multi_shot_run_button = MultiRunButton()
        common_offset_inputs = CommonOffsetInputFields()
        common_offset_run_button = CommonOffsetRunButton()
        common_midpoint_inputs = CommonMidpointInputFields()
        common_midpoint_run_button = CommonMidpointRunButton()
       
        
        # Adding elements to panel2 layout
        panel2_layout.add_widget(panel2_image_input)
        panel2_layout.add_widget(multi_shot_inputs)
        panel2_layout.add_widget(common_offset_inputs)
        panel2_layout.add_widget(common_midpoint_inputs)
        panel2_layout.add_widget(multi_shot_run_button)
        panel2_layout.add_widget(common_offset_run_button)
        panel2_layout.add_widget(common_midpoint_run_button)

        # Assigning layout to panel2
        multi_shot_run_tab.add_widget(panel2_layout)

        # panel3-------------------------------------------------------------
        #Display Plot 
        image2animation_inputs = Image2AnimationInputFields()
        array_plot_inputs = ArrayPlotInputFields()
        codisplay_inputs = CodisplayInputFields()
        image2animation_button = Image2AnimationButton()
        array_plot_button = ArrayPlotButton()
        codisplay_button = CodisplayButton()

        panel3_layout.add_widget(image2animation_inputs)
        panel3_layout.add_widget(array_plot_inputs)
        panel3_layout.add_widget(codisplay_inputs)
        panel3_layout.add_widget(codisplay_button)
        panel3_layout.add_widget(array_plot_button)
        panel3_layout.add_widget(image2animation_button)
        panel3_layout.add_widget(panel3_image_input)


        plot_panel.add_widget(panel3_layout)

        # panel4-------------------------------------------------------------
        # ______: ___________


        # help pannel--------------------------------------------------------
        # Help Page: Contains user manual


        # adding tabs to the window
        base.add_widget(prj_input_tab)
        base.add_widget(multi_shot_run_tab)
        base.add_widget(plot_panel)
        base.add_widget(help_panel)

        # setting the default tab
        base.default_tab = prj_input_tab

        return base

def startGui():
    SeidarTGUI().run()
