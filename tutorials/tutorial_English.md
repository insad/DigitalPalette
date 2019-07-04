# DigitalPalette
![Sample app icon](../src/main/icons/full/icon_full_256.png)

DigitalPalette is a free software for generating harmonious colors from color wheel and local images.

# Version
1.0.30 (developing)

# Installation
## Download
[Windows (32 bit) Installer (Recommend)](Link)  
[Windows (64 bit) Installer](Link)  
[Windows (32 bit) Packet](Link)  
[Windows (64 bit) Packet](Link)  

## Install
1. Double click the installer and click "Next".  
![Interface](installation/0.png)

2. Read the [License](../LICENSE). Check "I accept the terms of the License Aggrement" if you agree with it, then click "Next".  
![License](installation/1.png)

3. Choose an empty directory and click "Install" to start the installation.  
![Directory](installation/2.png)

4. Click "Finish" to finish the installation and run DigitalPalette.  
![Finish](installation/3.png)

# Usage
## Change the language
Currently we only provide English and Chinese translations. You could generate translation files by PyQt5 tools and put it into the language directory. You could change the language in two steps:  
1. Click "Edit" in the menu bar and select "Settings" to open the settings dialog.  
2. Click the combo box lateral to the "Language" label in "Interface" tab. Select the target language and click "OK" to change the language. 

## Interfacial Layout
The interfacial layout of DigitalPalette is displayed as bellow, where:  
* Title is surrounded by the red square, which indicates the name (DigitalPalette) and current version of this software.
* Menu bar is surrounded by the blue square, which includes the **import** (File -> Import) and **export** actions (File -> Export) of file, **Quit** action (File -> Quit), **create** (Edit -> Create) and **extract** (Edit -> Extract) actions of color set from color wheel and images as well as setup action of the preference **settings** (Edit -> Settings) of this software, etc..
* Option box is surrounded by the orange square, which includes a set of harmony rules.
* Tool box is surrounded by the purple square, which include the common operations and color modes.
* Work area is surrounded by the green square.
* Result area is surrounded by the yellow square, which includes the color set informations such as the **hex** code, **RGB** values and **HSV** values of colors, etc..  
![Layout](usage/1.png)

## Create colors from color wheel
The **color wheel** in the work area of DigitalPalette equips five circular **color tags**. These color tags are corresponding to the color squares in the result area. (The color of middle square determines the main hue of color set.) The color tag with black edge (labelled as "**activated color tag**") is corresponding to the currently selected color. You could change the colors by drag the color tags in wheel, or by double click the color squares, or through input the hex code and adjust the RGB and HSV value slides below the color squares. Meanwhile, other tags (labelled as "**inactivated color tag**") will move along with the activated color tag. The generating and moving methods of color tags are determined by the harmony rules, which will be demonstrate below.

## Harmony Rules
1. **Analogous** (default)
Create a set of colors with hue values in equidistant distributions. The closer of the tags, the more analogous of the colors.  
![Analogous](usage/2.png)

2. **Monochromatic**  
Create a set of colors with same hue and different saturation and lightness values.  
![Monochromatic](usage/3.png)

3. **Triad**  
Create a set of colors with hue values in trisection.  
![Triad](usage/4.png)

4. **Tetrad**  
Create a set of colors with colors complementary to each other in pairs.  
![Tetrad](usage/5.png)

5. **Pentad**  
Create a set of colors with hue values in quinquesection.  
![Pentad](usage/6.png)

6. **Complementary**  
Create a set of Complementary colors.  
![Complementary](usage/7.png)

7. **Shades**  
Create a set of colors with same hue and saturation values and different lightness values.  
![Shades](usage/8.png)

8. **Custom**  
Create a set of colors in custom.  
![Custom](usage/9.png)

## Export Colors
Harmonious colors can be exported to a readable and writable file for subsequent analysis and usage. Steps:  
1. Click the "Export" button in tool box or click "Edit -> Export" from the menu bar to open the file dialog.  
2. Change the directory, file name and extension and save it.

## Data Formats
Currently DigitalPalette can export color data into a file with following formats:  
1. DigitalPalette Json File Format (*.json)  
Data file with this format contains the harmony rule, hex code, RGB and HSV values of colors. This type of file can be imported by DigitalPalette.  

2. Plain Text Format (*.txt)  
Data file with this format contains the hex code, RGB and HSV values of colors. This type of file can be opened by editors.

3. Swatch File Format (*.aco)  
Data file with this format contains twenty-five colors, including five harmonious colors and twenty deuterogenic colors. **Note that** the sequence of colors in swatch are: 1-5 selected harmonious colors (prefixed "N"); 6-10 colors with same hue and 100% saturation and lightness values (prefixed "F"); 11-15 colors with same hue and 50% saturation, 100% lightness values (prefixed "S"); 16-20 colors with same hue and 100% saturation, 50% lightness values (prefixed "V"); and 21-25 colors with same hue and 50% saturation and lightness values (prefixed "H").  

## Import Colors (Swatches)
Currently DigitalPalette can import color data in DigitalPalette Json File Format. You could import color swatches into general image processing softwares, such as GIMP and Photoshop.
1. Import DigitalPalette Json File into DigitalPalette  
Firstly, click the "Import" button in tool box or click "Edit -> Import" from the menu bar to open the file dialog.  
Then, find the pre-saved file in DigitalPalette Json File Format and click "Open".

2. Import Swatch File into GIMP  
Firstly, open GIMP and select "Import Palette" with right-buttom cliced in colormap and open the import dialog.  
Then, find the pre-saved swatch file and click "Import".  
![GIMP](usage/10.png)

3. Import Swatch File into Photoshop  
Firstly, open Photoshop and select "Load" in swatch box and open the file dialog.  
Then, find the pre-saved swatch file and click "Open". The harmonious colors would be added at the end of current swatch.  
![Photoshop](usage/11.png)

4. Import Swatch File into UDongman Paint  
Firstly, open UDongman Paint and select "Load" in swatch box and open the file dialog.  
Then, find the pre-saved swatch file and click "Open". The harmonious colors would be opened in a new swatch.  
![UDongman Paint](usage/12.png)

## Extract Colors from an image
Currently DigitalPalette doesn't support to extract harmonious colors from an image automatically, and only provides tools for analysis and selections.  

# Author
Liu Jia

# License
DigitalPalette is a free software, which is distributed in the hope that it will be useful, but **without any warranty**. You can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation. See the GNU General Public License for more details.
