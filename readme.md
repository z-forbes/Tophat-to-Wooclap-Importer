This program allows for the Topat to Wooclap import process to be semi-automated. It runs on Windows. 
The program contains files which cause destructive actions. As outlined in the [license](/LICENSE), I disclaim all liability.

All contents of the [th_to_wc directory](/(program)/th_to_wc) were written by [Tophat](https://tophat.com/). The rest of the program was written as part of my work at the [ISG](https://www.ed.ac.uk/information-services). 

1. Receive access to the Tophat course in question. 
2. Tag questions in the course, see figure 1. Follow these rules: 
    - Tags have the form F_S_Q_ or F_Q_ where _ represents a number. F, S, Q stand for folder, subfolder and question respectively. 
    - Tags should be followed by a space. For example: “F1S2Q1 This is the start of the question”. The space and tag will be removed in the program’s output.  
    - All tags need to be unique.  
3. Request the course extract from Tophat. 
4. Install [Python](https://www.python.org/downloads/) and [Node.js](https://nodejs.org/en/download).
5. Download this repo.
6. Follow the steps outlined. If warnings cannot be ignored, see table below.
   1. Run ``1. move tophat file here``. Place your Tophat extract in the folder opened. 
   2. Run ``2. [optional] import foler names`` if you want to import folder names/counts from a file. 
   3. Run ``3. run me.``
   4. If step ii. was skipped, name the folders and subfolders based on the Tophat names. All folders and folder -> subfolder paths must be uniquely named.
   5. Click ``4. files to import``. This opens a folder containing files to import to Wooclap. Each file represents one event.
   6. The file automatically opened (``img_tol_miss.csv``) tells you of any questions which need to be created/updated manually. 
7. Import the files into Wooclap from the folder opened in step 6v. The filenames in this directory represent one event. 

Although this should not be necessary, running (program)/export.py is the same as turning everything off and on again.  

| File                              | Alternative                              |
|-----------------------------------|------------------------------------------|
| 1. move tophat file here          | Move file into (program)/th_to_wc/input/ |
| 2. [optional] import folder names | Run (program)/file_import.py             |
| 3. run me                         | Run (program)/main.py                    |
| 4. files to import                | Open (program)/output/                   |
