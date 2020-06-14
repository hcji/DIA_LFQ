# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 10:28:55 2020

@author: hcji
"""

import subprocess


DDA_File = 'F:/PXD002952/HYE124_TTOF6600_DDA_1ug_Ecoli_lgillet_I150212_001.wiff'
OUT_Dir = 'F:/LFQBench_Data'

# convert and to centroid data
OUT_File = OUT_Dir + '/' + DDA_File.split('/')[-1].replace('wiff', 'mzXML')
cmdline = 'qtofpeakpicker' 
cmdline += ' --resolution=20000' 
cmdline += ' --area=1 --threshold=1 --smoothwidth=1.1'
cmdline += ' --in ' + DDA_File 
cmdline += ' --out ' + OUT_File
subprocess.call(cmdline)

# Reduce fragment ion spectrum complexity by keeping only the top 150 peaks
OUT_File1 = OUT_Dir + '/_' + DDA_File.split('/')[-1].replace('wiff', 'mzXML')
cmdline = 'msconvert '
cmdline += ' ' + OUT_File + ' --mzXML'
cmdline += ' -o ' + OUT_Dir
cmdline += ' --filter "threshold count 150 most-intense"'
cmdline += ' --outfile ' + OUT_File1
subprocess.call(cmdline)

# Database searching
## comet
cwd = 'F:/LFQBench_Data/comet'
cmdline = 'comet ' + OUT_File1
subprocess.call(cmdline, cwd = cwd)

comet_out = OUT_File1.replace('.mzXML', '.pep.xml')
cmdline = 'xinteract -OARPd -dreverse_ -N' + comet_out.split('/')[-1]
cmdline += ' ' + comet_out
subprocess.call(cmdline, cwd = cwd)
