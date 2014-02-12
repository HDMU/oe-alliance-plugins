# -*- coding: utf-8 -*-#
#
# LCD4linux - Pearl DPF LCD Display, Samsung SPF-Line, Grautec-TFT, WLAN-LCDs, internes LCD über Skin
#
# written by joergm6 @ IHAD
# (Meteo-Station @ compilator)
#
#  This plugin is licensed under the Creative Commons 
#  Attribution-NonCommercial-ShareAlike 3.0 Unported 
#  License. To view a copy of this license, visit
#  http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative
#  Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
#
#  This plugin is NOT free software. It is open source, you are allowed to
#  modify it (if you keep the license), but it may not be commercially 
#  distributed other than under the conditions noted above.
#  Advertise with this Plugin is not allowed.
#  For other uses, permission from the author is necessary.
#
Version = "V3.9-r3"
from __init__ import _
from enigma import eConsoleAppContainer, eActionMap, iServiceInformation, iFrontendInformation, eDVBResourceManager, eDVBVolumecontrol
from enigma import getDesktop, getEnigmaVersionString
from enigma import ePicLoad, ePixmap
from Tools.HardwareInfo import HardwareInfo
#from boxbranding import getBrandOEM, getImageDistro

from Screens.Screen import Screen
from Plugins.Plugin import PluginDescriptor
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Language import language
from Components.Network import iNetwork
from Components.Input import Input
from Components.Pixmap import Pixmap
from Components.AVSwitch import AVSwitch
from Components.SystemInfo import SystemInfo
from Screens.InputBox import InputBox
from Screens.MessageBox import MessageBox
from Screens.InfoBar import InfoBar
from Screens import Standby 
from Screens.Standby import TryQuitMainloop
# imports
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps
from PIL import ImageColor
import colorsys
import xml.dom.minidom
import email
from email.header import decode_header
import urllib
import calendar
import math
import gc

url2 = False
try:
	import urllib2
	url2 = True
except:
	pass
import os
import textwrap
import codecs
try:
	import cStringIO
except:
	import StringIO as cStringIO
import ctypes.util
import glob
import random
import struct
import string
from time import gmtime, strftime, localtime, mktime, time, sleep, timezone, altzone, daylight
from datetime import datetime, timedelta, date
dummy = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

from Components.ServiceEventTracker import ServiceEventTracker
from enigma import eTimer, eEPGCache, eServiceReference, eServiceCenter, iPlayableService
from RecordTimer import RecordTimer, RecordTimerEntry, parseEvent
from threading import Thread, Lock
import Queue
import ping

from Components.config import configfile, getConfigListEntry, ConfigEnableDisable, ConfigPassword, \
	ConfigYesNo, ConfigText, ConfigClock, ConfigNumber, ConfigSelectionNumber, ConfigSelection, \
	config, Config, ConfigSubsection, ConfigSubList, ConfigSubDict, ConfigIP, ConfigSlider, ConfigDirectory
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Components.MenuList import MenuList
from Components.NimManager import nimmanager
 
from Tools.BoundFunction import boundFunction
from twisted.internet import reactor, defer
from twisted.web import client
from twisted.web.client import getPage, HTTPClientFactory, downloadPage
from xml.dom.minidom import parse, parseString
from xml.etree.cElementTree import parse as parseE
from urllib import urlencode, quote
import xml.etree.cElementTree
from myFileList import FileList as myFileList
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from module import L4Lelement,L4LVtest

L4LElist = L4Lelement()

try:
	from fcntl import ioctl
	from pngutil import png_util
	pngutil = png_util.PNGUtil()
	pngutilconnect = pngutil.connect()
	PNGutilOK = True
except:
	PNGutilOK = False

# globals
L4LdoThread = True
LCD4config = "/etc/enigma2/lcd4config"
LCD4plugin ="/usr/lib/enigma2/python/Plugins/Extensions/LCD4linux/"
Data = LCD4plugin+"data/"
stb = HardwareInfo().get_device_name()
if stb == 'gbquad':
	LCD4default = Data+"default.gigablue"
else:	
	LCD4default = Data+"default.lcd"
WetterPath = LCD4plugin+"wetter/"
MeteoPath = LCD4plugin+"meteo/"
FONTdefault="/usr/share/fonts/nmsbd.ttf"
FONT=FONTdefault
ClockBack = Data+"PAclock2.png"
Clock = Data+"Clock"
RecPic = Data+"rec.png"
xmlPIC ="/tmp/l4ldisplay.png"
xmlPICtmp ="/tmp/l4ldisplaytmp.png"
if os.path.islink(LCD4plugin+"tmp") == True:
	TMP = os.path.realpath(LCD4plugin+"tmp")+"/"
else:
	TMP = "/tmp/"
TMPL=TMP+"lcd4linux/"
Fritz="%sfritz.txt" % TMPL
FritzFrame = Data+"fritzcallframe.png"
FritzRing = Data+"fritzcallring.png"
FritzPic = Data+"fritzpic.png"
CrashFile="/tmp/L4Lcrash.txt"
PIC="%sdpf" % TMPL
PICtmp="%sdpftmp" % TMPL
PIC2="%sdpf2" % TMPL
PIC2tmp="%sdpf2tmp" % TMPL
PIC3="%sdpf3" % TMPL
PIC3tmp="%sdpf3tmp" % TMPL
PICcal=None
PICwetter=[None,None]
PICmeteo="%sdpfmeteo.png" % TMPL
PICfritz="%sdpffritz.png" % TMPL
HTTPpic="%sdpfhttp.jpg" % TMPL
HTTPpictmp="%sdpfhttptmp.jpg" % TMPL
TXTdemo="%slcd4linux.demo" % TMPL
MP3tmp="%sid3coverart.jpg" % TMPL
GoogleCover="%sgcover.jpg" % TMPL
WWWpic="%swww%%s.jpg" % TMPL
LCDon = True
ConfigMode = False
ConfigStandby = False
ShellRunning = False
OSDon = 0
OSDtimer = -5
OSDdontshow = ["LCD4linux Settings","Virtual Zap","InfoBar","Infobar","SecondInfoBar","FanControl2","Mute","LCD Text","UnhandledKey","QuickZap","Volume","PVRState"]
OSDdontskin = ["LCDdisplayFile","VirtualZap","InfoBar","Infobar","InfoBarSummary","PictureInPicture","SimpleSummary","TimeshiftState","InfoScreen","Standby","EMCMediaCenter","InfoBarMoviePlayerSummary","PVRState","ResolutionLabel","WidgetBackground","camodogFSScreen2","camodogFSmini"]
wwwWetter = ["",""]
WetterType = ""
WetterZoom = ""
CalType = ""
CalZoom = ""
CalColor = ""
wwwMeteo = ""
MeteoType = ""
MeteoZoom = ""
PopText = ["",""]
ScreenActive = ["1","","",""]
ScreenTime= 0
isVideoPlaying = 0
AktHelligkeit = [-1,-1,-1,-1,-1,-1]
AktTFT = ""
PopMail = [[],[],[],[],[],""]
PopMailUid = [["","",""],["","",""],["","",""],["","",""],["","",""]]
Bilder = ["","",""]
BilderIndex = [0,0,0]
BilderTime = 0
FritzTime = 0
FritzList = []
xmlList = []
ThreadRunning = 0
DeviceRemove = []
QuickList = [[],[],[]]
SaveEventList = ["","",""]
SaveEventListChanged = False
ICS = {}
ICSlist = []
ICSrunning = False
ICSdownrun = False
SAT = {}
TunerCount = 0
TunerMask = 0
SamsungDevice = None
SamsungDevice2 = None
SamsungDevice3 = None
isMediaPlayer = ""
GrabRunning = False
GrabTVRunning = False
TVrunning = False
BriefLCD = Queue.Queue()
Briefkasten = Queue.Queue()
Brief1 = Queue.Queue()
Brief2 = Queue.Queue()
Brief3 = Queue.Queue()
CPUtotal = 0
CPUidle = 0
L4LSun = (7,0)
L4LMoon = (19,0)
INFO = ""

USBok = False
if ctypes.util.find_library("usb-0.1") is not None or ctypes.util.find_library("usb-1.0") is not None:
	print "[LCD4linux] libusb found :-)",getEnigmaVersionString()
#	getEnigmaVersionString().split("-")[-1] > "3.2" # /model=dm800
	import Photoframe
	import dpf
	import usb.util
	USBok = True

Farbe = [("black", _("black")), ("white", _("white")), 
 ("gray", _("gray")), ("silver", _("silver")), ("slategray", _("slategray")),
 ("aquamarine", _("aquamarine")),
 ("yellow", _("yellow")), ("greenyellow", _("greenyellow")), ("gold", _("gold")),
 ("red", _("red")), ("tomato", _("tomato")), ("darkred", _("darkred")), ("indianred", _("indianred")), ("orange", _("orange")), ("darkorange", _("darkorange")), ("orangered", _("orangered")),
 ("green", _("green")), ("lawngreen", _("lawngreen")), ("darkgreen", _("darkgreen")), ("lime", _("lime")), ("lightgreen", _("lightgreen")),
 ("blue", _("blue")), ("blueviolet", _("blueviolet")), ("indigo", _("indigo")), ("darkblue", _("darkblue")), ("cadetblue", _("cadetblue")), ("cornflowerblue", _("cornflowerblue")), ("lightblue", _("lightblue")),
 ("magenta", _("magenta")), ("violet", _("violet")), ("darkorchid", _("darkorchid")), ("deeppink", _("deeppink")), ("cyan", _("cyan")),
 ("brown", _("brown")), ("sandybrown", _("sandybrown")), ("moccasin", _("moccasin")), ("rosybrown", _("rosybrown")), ("olive", _("olive")),
]
ScreenSelect = [("0", _("off")), ("1", _("Screen 1")), ("2", _("Screen 2")), ("3", _("Screen 3")), ("12", _("Screen 1+2")), ("13", _("Screen 1+3")), ("23", _("Screen 2+3")), ("123", _("Screen 1+2+3")), ("4", _("Screen 4")), ("14", _("Screen 1+4")), ("24", _("Screen 2+4")), ("34", _("Screen 3+4")), ("124", _("Screen 1+2+4")), ("134", _("Screen 1+3+4")), ("234", _("Screen 2+3+4")), ("1234", _("Screen 1+2+3+4")), ("5", _("Screen 5")), ("6", _("Screen 6")), ("7", _("Screen 7")), ("8", _("Screen 8")), ("9", _("Screen 9")), ("12345", _("Screen 1-5")), ("123456", _("Screen 1-6")), ("1234567", _("Screen 1-7")), ("12345678", _("Screen 1-8")), ("123456789", _("Screen 1-9")), ("56789", _("Screen 5-9")), ("13579", _("Screen 1+3+5+7+9")), ("2468", _("Screen 2+4+6+8"))]
ScreenUse = [("1", _("Screen 1")), ("2", _("Screen 1-2")), ("3", _("Screen 1-3")), ("4", _("Screen 1-4")), ("5", _("Screen 1-5")), ("6", _("Screen 1-6")), ("7", _("Screen 1-7")), ("8", _("Screen 1-8")), ("9", _("Screen 1-9"))]
ScreenSet = [("1", _("Screen 1")), ("2", _("Screen 2")), ("3", _("Screen 3")), ("4", _("Screen 4")), ("5", _("Screen 5")), ("6", _("Screen 6")), ("7", _("Screen 7")), ("8", _("Screen 8")), ("9", _("Screen 9"))]
OnOffSelect = [("0", _("off")), ("1", _("on"))]
TimeSelect = [("1", _("5s")), ("2", _("10s")), ("3", _("15s")), ("4", _("20s")), ("6", _("30s")), ("8", _("40s")), ("10", _("50s")), ("12", _("1min")), ("24", _("2min")), ("36", _("3min")), ("48", _("4min")), ("60", _("5min")), ("120", _("10min")), ("240", _("20min")), ("360", _("30min")), ("720", _("60min"))]
LCDSelect = [("1", _("LCD 1")), ("2", _("LCD 2")), ("12", _("LCD 1+2")), ("3", _("LCD 3")), ("13", _("LCD 1+3")), ("23", _("LCD 2+3")), ("123", _("LCD 1+2+3"))]
LCDType = [("11", _("Pearl (or compatible LCD) 320x240")), ("12", _("Pearl (or compatible LCD) 240x320")),
 ("210", _("Samsung SPF-72H 800x480")), ("23", _("Samsung SPF-75H/76H 800x480")), ("24", _("Samsung SPF-87H 800x480")), ("25", _("Samsung SPF-87H old 800x480")), ("26", _("Samsung SPF-83H 800x600")),
 ("29", _("Samsung SPF-85H/86H 800x600")), ("212", _("Samsung SPF-85P/86P 800x600")), ("28", _("Samsung SPF-105P 1024x600")), ("27", _("Samsung SPF-107H 1024x600")), ("213", _("Samsung SPF-107H old 1024x600")),
 ("211", _("Samsung SPF-700T 800x600")),
 ("430", _("Internal TFT-LCD 400x240")),
 ("50", _("Internal Box-Skin-LCD")),
 ("31", _("only Picture 320x240")), ("33", _("only Picture 800x480")), ("36", _("only Picture 800x600")), ("37", _("only Picture 1024x600")), ("320", _("only Picture Custom Size"))]
if PNGutilOK:
	LCDType.insert(14,("930", _("Internal Vu+ Duo2 LCD 400x240")))
xmlLCDType = [("96x64", _("96x64")), ("132x64", _("132x64")), ("220x176", _("220x176")), ("255x64", _("255x64")), ("400x240", _("400x240"))]
WetterType =  [("12", _("2 Days 1 Line")), ("22", _("2 Days 2 Line")), ("1", _("4 Days 1 Line")), ("2", _("4 Days 2 Lines")), ("11", _("5 Days 1 Line")), ("21", _("5 Days 2 Lines")), ("3", _("Current")), ("4", _("Current Temperature (+C)")), ("41", _("Current Temperature (-C)")), ("5", _("4 Days Vertical View")), ("51", _("5 Days Vertical View"))]
MeteoType = [("1", _("Current")), ("2", _("Current Temperature"))]
NetatmoType = [("THCPN", _("All")), ("T", _("Temperature")), ("TH", _("Temperature+Humidity")), ("TC", _("Temperature+Co2")), ("TCP", _("Temperature+Co2+Pressure"))]
CO2Type = [("0", _("Bar")), ("09", _("Bar+Value")), ("1", _("Knob")), ("19", _("Knob+Value"))]
ClockType = [("12", _("Time")), ("112", _("Date+Time")), ("1123", _("Date+Time+Weekday")), ("11", _("Date")), ("123", _("Time+Weekday")), ("13", _("Weekday")), ("4", _("Flaps Design")), ("51", _("Analog")), ("52", _("Analog+Date")), ("521", _("Analog+Date+Weekday")), ("521+", _("Analog+Date+Weekday 2"))]
AlignType = [("0", _("left")), ("1", _("center")), ("2", _("right")), ("0500", _("5%")), ("1000", _("10%")), ("1500", _("15%")), ("2000", _("20%")), ("2500", _("25%")), ("3000", _("30%")), ("3500", _("35%")), ("4000", _("40%")), ("4500", _("45%")), ("5000", _("50%")), ("5500", _("55%")), ("6000", _("60%")), ("6500", _("65%")), ("7000", _("70%")), ("7500", _("75%")), ("8000", _("80%")), ("8500", _("85%")), ("9000", _("90%")), ("9500", _("95%"))]
DescriptionType = [("10", _("Short")), ("12", _("Short (Extended)")),("01", _("Extended")), ("21", _("Extended (Short)")),("11", _("Short+Extended"))]
CalType = [("9", _("no Calendar")),("0", _("Month")), ("0A", _("Month+Header")), ("1", _("Week")), ("1A", _("Week+Header"))]
CalTypeE = [("0", _("no Dates")), ("D2", _("Dates compact 2 Lines")), ("D3", _("Dates compact 3 Lines")), ("C1", _("Dates 1 Line")), ("C3", _("Dates 3 Lines")), ("C5", _("Dates 5 Lines")), ("C9", _("Dates 9 Lines"))]
CalLayout = [("0", _("Frame")), ("1", _("Underline")), ("2", _("Underline 2"))]
CalListType = [("D", _("Dates compact")), ("D-", _("Dates compact no Icon")), ("C", _("Dates")), ("C-", _("Dates no Icon"))]
FritzType = [("L", _("with Icon")), ("L-", _("no Icon")), ("TL", _("with Icon & Targetnumber")), ("TL-", _("no Icon, with Targetnumber"))]
InfoSensor = [("0", _("no")), ("R", _("rpm/2")), ("r", _("rpm")), ("T", _("C")), ("RT", _("C + rmp/2")), ("rT", _("C + rmp"))]
InfoCPU = [("0", _("no")), ("P", _("%")), ("L0", _("Load@1min")), ("L1", _("Load@5min")), ("PL0", _("% + Load@1min")), ("PL1", _("% + Load@5min"))]
HddType = [("0", _("show run+sleep")), ("1", _("show run"))]
MailType = [("A1", _("Always All")), ("A2", _("Always New")), ("B2", _("Only New"))]
ProzentType = [("30", _("30%")), ("35", _("35%")), ("40", _("40%")), ("45", _("45%")), ("50", _("50%")), ("55", _("55%")), ("60", _("60%")), ("65", _("65%")), ("70", _("70%")), ("75", _("75%")), ("80", _("80%")), ("85", _("85%")), ("90", _("90%")), ("95", _("95%")), ("100", _("100%"))]
MailKonto = [("1", _("1")), ("2", _("1-2")), ("3", _("1-3")), ("4", _("1-4")), ("5", _("1-5"))]
MailConnect = [("0", _("Pop3-SSL")), ("1", _("Pop3")), ("2", _("IMAP-SSL")), ("3", _("IMAP"))]
Split = [("false", _("no")), ("true", _("yes")), ("true25", _("yes +25%"))]
DirType = [("0", _("horizontally")), ("2", _("vertically"))]
FontType = [("0", _("Global")), ("1", _("1")), ("2", _("2")), ("3", _("3"))]
ProgressType = [("1", _("only Progress Bar")),
("2", _("with Remaining Minutes")), ("21", _("with Remaining Minutes (Size 1.5)")), ("22", _("with Remaining Minutes (Size 2)")),
("3", _("with Percent")), ("31", _("with Percent (Size 1.5)")), ("32", _("with Percent (Size 2)")),
("4", _("with Remaining Minutes (above)")), ("41", _("with Remaining Minutes (above/Size 1.5)")), ("42", _("with Remaining Minutes (above/Size 2)")),
("5", _("with Percent (above)")), ("51", _("with Percent (above/Size 1.5)")), ("52", _("with Percent (above/Size 2)")),
("6", _("with Remaining Minutes (below)")), ("61", _("with Remaining Minutes (below/Size 1.5)")), ("62", _("with Remaining Minutes (below/Size 2)")),
("7", _("with Percent (below)")), ("71", _("with Percent (below/Size 1.5)")), ("72", _("with Percent (below/Size 2)")),
("8", _("with Current 00:00")), ("81", _("with Current 00:00 (Size 1.5)")), ("82", _("with Current 00:00 (Size 2)")),
("9", _("with Current 00:00 (above)")), ("91", _("with Current 00:00 (above/Size 1.5)")), ("92", _("with Current 00:00 (above/Size 2)")),
("A", _("with Current 00:00 (below)")), ("A1", _("with Current 00:00 (below/Size 1.5)")), ("A2", _("with Current 00:00 (below/Size 2)"))
]
now = localtime()
begin = mktime((
	now.tm_year, now.tm_mon, now.tm_mday, 06, 00, \
	0, now.tm_wday, now.tm_yday, now.tm_isdst)
)

LCD4linux = Config()
LCD4linux.Enable = ConfigYesNo(default = True)
LCD4linux.FastMode = ConfigSelection(choices = [("5", _("Normal (5s)")), ("2", _("Fastmode (2s)"))], default="5")
LCD4linux.ScreenActive = ConfigSelection(choices = ScreenSet, default="1")
LCD4linux.ScreenMax = ConfigSelection(choices = ScreenUse, default="1")
LCD4linux.ScreenTime = ConfigSelection(choices = [("0", _("off"))] + TimeSelect, default="0")
LCD4linux.ScreenTime2 = ConfigSelection(choices = TimeSelect, default="1")
LCD4linux.ScreenTime3 = ConfigSelection(choices = TimeSelect, default="1")
LCD4linux.ScreenTime4 = ConfigSelection(choices = TimeSelect, default="1")
LCD4linux.ScreenTime5 = ConfigSelection(choices = TimeSelect, default="1")
LCD4linux.ScreenTime6 = ConfigSelection(choices = TimeSelect, default="1")
LCD4linux.ScreenTime7 = ConfigSelection(choices = TimeSelect, default="1")
LCD4linux.ScreenTime8 = ConfigSelection(choices = TimeSelect, default="1")
LCD4linux.ScreenTime9 = ConfigSelection(choices = TimeSelect, default="1")
LCD4linux.BilderTime = ConfigSelection(choices =  [("0", _("off"))] + TimeSelect, default="0")
LCD4linux.BilderSort = ConfigSelection(choices =  [("0", _("off")), ("1", _("alphabetic")), ("2", _("random"))], default="1")
LCD4linux.BilderQuality = ConfigSelection(choices =  [("0", _("low/fast (all)")), ("1", _("low/fast (Picture only)")), ("2", _("better/slow"))], default="1")
LCD4linux.BilderRecursiv = ConfigYesNo(default = False)
LCD4linux.BilderQuick = ConfigSelection(choices =  [("500", _("0.5")), ("1000", _("1")), ("2000", _("2")), ("3000", _("3")), ("5000", _("5")), ("10000", _("10")), ("20000", _("20")), ("30000", _("30"))], default="10000")
LCD4linux.BilderJPEG = ConfigSelectionNumber(20, 100, 5, default = 75)
LCD4linux.BilderJPEGQuick = ConfigSelectionNumber(20, 100, 5, default = 60)
LCD4linux.BilderTyp = ConfigSelection(choices =  [("png", _("PNG")), ("jpg", _("JPG"))], default="png")
LCD4linux.BilderBackground = ConfigSelection(choices =  [("0", _("no cache + no adjustment")), ("1", _("cache + adjustment (high quality, slow)")), ("2", _("cache + adjustment (low quality, fast)"))], default="2")
LCD4linux.Helligkeit = ConfigSelectionNumber(0, 10, 1, default = 5)
LCD4linux.Helligkeit2 = ConfigSelectionNumber(0, 10, 1, default = 5)
LCD4linux.Helligkeit3 = ConfigSelectionNumber(0, 10, 1, default = 5)
LCD4linux.LCDoff = ConfigClock(default = int(begin) ) # ((5 * 60 + 0) * 60)
LCD4linux.LCDon = ConfigClock(default = int(begin) )
LCD4linux.LCDWEoff = ConfigClock(default = int(begin) ) # ((5 * 60 + 0) * 60)
LCD4linux.LCDWEon = ConfigClock(default = int(begin) )
LCD4linux.Delay = ConfigSlider(default = 400,  increment = 50, limits = (50, 2000))
LCD4linux.ElementThreads = ConfigSelectionNumber(1, 2, 1, default = 2)
LCD4linux.DevForceRead = ConfigYesNo(default = True)
LCD4linux.DVBTCorrection = ConfigSelection(choices = [("0", _("no")), ("reverse", _("Plug Tuner")), ("usb", _("USB Tuner"))], default="0")
LCD4linux.ShowNoMsg = ConfigYesNo(default = True)
LCD4linux.SavePicture = ConfigSelection(choices =  [("0", _("no"))] + LCDSelect, default="123")
LCD4linux.WebIfRefresh = ConfigSelectionNumber(1, 60, 1, default = 3)
LCD4linux.WebIfType = ConfigSelection(choices = [("0", _("Javascript")), ("1", _("Reload"))], default="0")
LCD4linux.WebIfInitDelay = ConfigYesNo(default = False)
LCD4linux.WebIfAllow = ConfigText(default="127. 192.168. 172. 10.", fixed_size=False)
LCD4linux.WebIfDeny = ConfigText(default="", fixed_size=False)
LCD4linux.WebIfDesign = ConfigSelection(choices = [("1", _("1 - normal")), ("2", _("2 - side by side"))], default = "2")
LCD4linux.WetterCity = ConfigText(default="London", fixed_size=False)
LCD4linux.Wetter2City = ConfigText(default="Berlin", fixed_size=False)
LCD4linux.WetterPath = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.WetterLowColor = ConfigSelection(choices = Farbe, default="aquamarine")
LCD4linux.WetterHighColor = ConfigSelection(choices = Farbe, default="violet")
LCD4linux.WetterTransparenz = ConfigSelection(choices = [("false", _("no")), ("crop", _("alternative Copy-Mode/DM800hd (24bit)")), ("true", _("yes (32bit)"))], default = "false")
LCD4linux.WetterIconZoom = ConfigSelectionNumber(30, 70, 1, default = 40)
LCD4linux.WetterRain = ConfigSelection(choices = [("false", _("no")), ("true", _("yes")), ("true2", _("yes + %"))], default = "true")
LCD4linux.WetterRainZoom = ConfigSlider(default = 100,  increment = 1, limits = (90, 200))
LCD4linux.WetterRainColor = ConfigSelection(choices = Farbe, default="silver")
LCD4linux.WetterRainColor2use = ConfigSelectionNumber(10, 100, 10, default = 80)
LCD4linux.WetterRainColor2 = ConfigSelection(choices = Farbe, default="cyan")
LCD4linux.WetterLine = ConfigSelection(choices = [("false", _("no")), ("true", _("yes, short")), ("trueLong", _("yes, long"))], default = "trueLong")
LCD4linux.WetterExtra = ConfigYesNo(default = True)
LCD4linux.WetterExtraZoom = ConfigSlider(default = 100,  increment = 1, limits = (90, 200))
LCD4linux.WetterExtraFeel = ConfigSelectionNumber(0, 5, 1, default = 3)
LCD4linux.WetterExtraColorCity = ConfigSelection(choices = Farbe, default="silver")
LCD4linux.WetterExtraColorFeel = ConfigSelection(choices = Farbe, default="silver")
LCD4linux.WetterWind = ConfigSelection(choices = [("0", _("km/h")), ("1", _("m/s"))], default = "0")
LCD4linux.MeteoURL = ConfigText(default="http://", fixed_size=False, visible_width=50)
LCD4linux.MoonPath = ConfigText(default="", fixed_size=False, visible_width=50)
if PNGutilOK:
	LCD4linux.LCDType1 = ConfigSelection(choices = LCDType, default="930")
else:
	LCD4linux.LCDType1 = ConfigSelection(choices = LCDType, default="11")
LCD4linux.LCDType2 = ConfigSelection(choices = [("00", _("off"))] + LCDType, default="00")
LCD4linux.LCDType3 = ConfigSelection(choices = [("00", _("off"))] + LCDType, default="00")
LCD4linux.LCDRotate1 = ConfigSelection(choices = [("0", _("0")), ("90", _("90")), ("180", _("180")), ("270", _("270"))], default="0")
LCD4linux.LCDRotate2 = ConfigSelection(choices = [("0", _("0")), ("90", _("90")), ("180", _("180")), ("270", _("270"))], default="0")
LCD4linux.LCDRotate3 = ConfigSelection(choices = [("0", _("0")), ("90", _("90")), ("180", _("180")), ("270", _("270"))], default="0")
LCD4linux.LCDBild1 = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.LCDBild2 = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.LCDBild3 = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.LCDColor1 = ConfigSelection(choices = Farbe, default="black")
LCD4linux.LCDColor2 = ConfigSelection(choices = Farbe, default="black")
LCD4linux.LCDColor3 = ConfigSelection(choices = Farbe, default="black")
LCD4linux.LCDRefresh1 = ConfigSelection(choices = [("0", _("always")), ("1", _("1 / min"))], default="0")
LCD4linux.LCDRefresh2 = ConfigSelection(choices = [("0", _("always")), ("1", _("1 / min"))], default="0")
LCD4linux.LCDRefresh3 = ConfigSelection(choices = [("0", _("always")), ("1", _("1 / min"))], default="0")
LCD4linux.LCDTFT = ConfigSelection(choices =  [("ABC", _("On+Media+Standby")), ("A", _("On")), ("B", _("Media")), ("C", _("Standby"))], default="ABC")
LCD4linux.xmlLCDType = ConfigSelection(choices = xmlLCDType, default="132x64")
LCD4linux.xmlLCDColor = ConfigSelection(choices = [("8", _("8bit - grayscale/color")), ("32", _("32bit - color"))], default="8")
LCD4linux.xmlType01 = ConfigYesNo(default = False)
LCD4linux.xmlType02 = ConfigYesNo(default = False)
LCD4linux.xmlType03 = ConfigYesNo(default = False)
LCD4linux.SizeW = ConfigSlider(default = 800,  increment = 1, limits = (100, 2000))
LCD4linux.SizeH = ConfigSlider(default = 600,  increment = 1, limits = (100, 1000))
LCD4linux.KeySwitch = ConfigYesNo(default = True)
LCD4linux.KeyScreen = ConfigSelection(choices =  [("999", _("off")),("163", _("2 x FastForwardKey")),("208", _("2 x FastForwardKey Type 2")),("163l", _("Long FastForwardKey")),("2081", _("Long FastForwardKey Type 2")),("358", _("2 x InfoKey")),("3581", _("Long InfoKey")),("113", _("2 x Mute"))], default="163")
LCD4linux.KeyOff = ConfigSelection(choices =  [("999", _("off")),("165", _("2 x FastBackwardKey")),("165l", _("Long FastBackwardKey")),("358", _("2 x InfoKey")),("3581", _("Long InfoKey")),("113", _("2 x Mute"))], default="1651")
LCD4linux.Mail1Pop = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.Mail1Connect = ConfigSelection(choices = MailConnect, default="0")
LCD4linux.Mail1User = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.Mail1Pass = ConfigPassword(default="", fixed_size=False, visible_width=50)
LCD4linux.Mail2Pop = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.Mail2Connect = ConfigSelection(choices = MailConnect, default="0")
LCD4linux.Mail2User = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.Mail2Pass = ConfigPassword(default="", fixed_size=False, visible_width=50)
LCD4linux.Mail3Pop = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.Mail3Connect = ConfigSelection(choices = MailConnect, default="0")
LCD4linux.Mail3User = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.Mail3Pass = ConfigPassword(default="", fixed_size=False, visible_width=50)
LCD4linux.Mail4Pop = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.Mail4Connect = ConfigSelection(choices = MailConnect, default="0")
LCD4linux.Mail4User = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.Mail4Pass = ConfigPassword(default="", fixed_size=False, visible_width=50)
LCD4linux.Mail5Pop = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.Mail5Connect = ConfigSelection(choices = MailConnect, default="0")
LCD4linux.Mail5User = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.Mail5Pass = ConfigPassword(default="", fixed_size=False, visible_width=50)
LCD4linux.MailTime = ConfigSelection(choices = [("01", _("60min")), ("01,31", _("30min")), ("01,21,41", _("20min")), ("01,16,31,46", _("15min")), ("01,11,21,31,41,51", _("10min"))], default="01")
LCD4linux.MailShow0 = ConfigYesNo(default = False)
LCD4linux.Recording = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.RecordingLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.RecordingType = ConfigSelection(choices = [("1", _("Corner")), ("2", _("Picon"))], default="1")
LCD4linux.RecordingSize = ConfigSlider(default = 25,  increment = 1, limits = (10, 100))
LCD4linux.RecordingPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.RecordingAlign = ConfigSelection(choices = AlignType, default="2")
LCD4linux.RecordingSplit = ConfigYesNo(default = False)
LCD4linux.RecordingPath = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.Crash = ConfigYesNo(default = True)
LCD4linux.ConfigPath = ConfigText(default="/tmp/", fixed_size=False, visible_width=50)
LCD4linux.Events = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.EventsLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.EventsSize = ConfigSlider(default = 32,  increment = 1, limits = (10, 150))
LCD4linux.EventsPos = ConfigSlider(default = 120,  increment = 2, limits = (0, 1024))
LCD4linux.EventsAlign = ConfigSelection(choices = AlignType, default="1")
LCD4linux.EventsSplit = ConfigYesNo(default = False)
LCD4linux.EventsType = ConfigSelection(choices = DirType, default="0")
LCD4linux.FritzPath = ConfigText(default="/tmp/", fixed_size=False, visible_width=50)
LCD4linux.FritzFrame = ConfigText(default="", fixed_size=False, visible_width=40)
LCD4linux.FritzLines = ConfigSelectionNumber(0, 20, 1, default = 2)
LCD4linux.FritzPictures = ConfigSelectionNumber(0, 20, 1, default = 0)
LCD4linux.FritzPictureSearch = ConfigSelection(choices = [("0", _("no")), ("1", _("yes")), ("12", _("yes, extended"))], default="1")
LCD4linux.FritzPictureType = ConfigSelection(choices = DirType, default="0")
LCD4linux.FritzRemove = ConfigSelectionNumber(1, 48, 1, default = 12)
LCD4linux.FritzTime = ConfigSelection(choices = TimeSelect, default="3")
LCD4linux.FritzPopupLCD = ConfigSelection(choices = [("0", _("no"))] + LCDSelect, default="1")
LCD4linux.FritzPopupColor = ConfigSelection(choices = Farbe, default="yellow")
LCD4linux.CalPath = ConfigText(default="/tmp/", fixed_size=False, visible_width=40)
LCD4linux.CalPathColor = ConfigSelection(choices = Farbe, default="green")
LCD4linux.CalHttp = ConfigText(default="http...", fixed_size=False, visible_width=50)
LCD4linux.CalHttpColor = ConfigSelection(choices = Farbe, default="lime")
LCD4linux.CalHttp2 = ConfigText(default="http...", fixed_size=False, visible_width=50)
LCD4linux.CalHttp2Color = ConfigSelection(choices = Farbe, default="greenyellow")
LCD4linux.CalHttp3 = ConfigText(default="http...", fixed_size=False, visible_width=50)
LCD4linux.CalHttp3Color = ConfigSelection(choices = Farbe, default="yellow")
LCD4linux.CalPlanerFS = ConfigYesNo(default = False)
LCD4linux.CalPlanerFSColor = ConfigSelection(choices = Farbe, default="orange")
LCD4linux.CalLine = ConfigSelectionNumber(1, 2, 1, default = 1)
LCD4linux.CalDays = ConfigSelection(choices = [("0", "0"), ("3", "3"), ("7", "7"), ("14", "14"), ("21", "21"), ("31", "31")], default="7")
LCD4linux.CalTime = ConfigSelection(choices = [("03", _("60min")), ("03,33", _("30min")), ("03,23,43", _("20min")), ("03,18,33,48", _("15min"))], default="03")
LCD4linux.CalTransparenz = ConfigSelection(choices = [("false", _("no")), ("crop", _("alternative Copy-Mode/DM800hd (24bit)")), ("true", _("yes (32bit)"))], default = "false")
LCD4linux.CalTimeZone = ConfigSelection(choices = [("-3", "-3"), ("-2", "-2"), ("-1", "-1"), ("0", "0"), ("1", "1"), ("2", "2"), ("3", "3")], default="0")
LCD4linux.Cal = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.CalLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.CalPos = ConfigSlider(default = 50,  increment = 2, limits = (0, 1024))
LCD4linux.CalAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.CalSplit = ConfigYesNo(default = False)
LCD4linux.CalZoom = ConfigSlider(default = 10,  increment = 1, limits = (3, 50))
LCD4linux.CalType = ConfigSelection(choices = CalType, default="0A")
LCD4linux.CalTypeE = ConfigSelection(choices = CalTypeE, default="D2")
LCD4linux.CalLayout = ConfigSelection(choices = CalLayout, default="0")
LCD4linux.CalColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.CalBackColor = ConfigSelection(choices = Farbe, default="gray")
LCD4linux.CalCaptionColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.CalShadow = ConfigYesNo(default = False)
LCD4linux.CalFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.CalList = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.CalListLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.CalListSize = ConfigSlider(default = 12,  increment = 1, limits = (5, 150))
LCD4linux.CalListPos = ConfigSlider(default = 50,  increment = 2, limits = (0, 1024))
LCD4linux.CalListAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.CalListSplit = ConfigYesNo(default = False)
LCD4linux.CalListLines = ConfigSelectionNumber(1, 20, 1, default = 3)
LCD4linux.CalListProzent = ConfigSelection(choices = ProzentType, default="50")
LCD4linux.CalListType = ConfigSelection(choices = CalListType, default="C")
LCD4linux.CalListColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.CalListShadow = ConfigYesNo(default = False)
LCD4linux.CalListFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.Font = ConfigText(default=FONTdefault, fixed_size=False, visible_width=50)
LCD4linux.Font1 = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.Font2 = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.Font3 = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.EnableEventLog = ConfigSelection(choices = [("0", _("off")), ("1", _("Logfile normal")), ("2", _("Logfile extensive")), ("3", _("Console normal"))], default = "0")
LCD4linux.TunerColor = ConfigSelection(choices = Farbe, default="slategray")
LCD4linux.TunerColorActive = ConfigSelection(choices = Farbe, default="lime")
LCD4linux.TunerColorOn = ConfigSelection(choices = Farbe, default="yellow")
LCD4linux.OSD = ConfigSelection(choices =  [("0", _("disabled"))] + TimeSelect + [("9999", _("always"))], default="0")
LCD4linux.OSDLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.OSDsize = ConfigSlider(default = 425,  increment = 5, limits = (320, 1280))
LCD4linux.OSDshow = ConfigSelection(choices = [("TRM", _("TV+Radio+Media")), ("TR", _("TV+Radio")), ("RM", _("Radio+Media")), ("T", _("TV")), ("R", _("Radio")), ("M", _("Media"))], default = "TRM")
LCD4linux.OSDTransparenz = ConfigSelection(choices = [("0", _("normal (full)")), ("1", _("trimmed (transparent)")), ("2", _("trimmed (black)"))], default = "1")
LCD4linux.OSDfast = ConfigYesNo(default = False)
LCD4linux.Popup = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.PopupLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.PopupSize = ConfigSlider(default = 30,  increment = 1, limits = (10, 150))
LCD4linux.PopupPos = ConfigSlider(default = 30,  increment = 2, limits = (0, 1024))
LCD4linux.PopupAlign = ConfigSelection(choices = [("0", _("left")), ("1", _("center")), ("2", _("right"))], default="0")
LCD4linux.PopupColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.PopupBackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="brown")
LCD4linux.Mail = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MailLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MailSize = ConfigSlider(default = 12,  increment = 1, limits = (5, 150))
LCD4linux.MailPos = ConfigSlider(default = 30,  increment = 2, limits = (0, 1024))
LCD4linux.MailAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MailSplit = ConfigYesNo(default = False)
LCD4linux.MailColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MailBackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.MailKonto = ConfigSelection(choices = MailKonto, default="1")
LCD4linux.MailLines = ConfigSelectionNumber(1, 20, 1, default = 3)
LCD4linux.MailType = ConfigSelection(choices = MailType, default="A1")
LCD4linux.MailProzent = ConfigSelection(choices = ProzentType, default="50")
LCD4linux.MailShadow = ConfigYesNo(default = False)
LCD4linux.MailFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.IconBar = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.IconBarLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.IconBarSize = ConfigSlider(default = 20,  increment = 1, limits = (10, 150))
LCD4linux.IconBarPos = ConfigSlider(default = 120,  increment = 2, limits = (0, 1024))
LCD4linux.IconBarAlign = ConfigSelection(choices = AlignType, default="1")
LCD4linux.IconBarSplit = ConfigYesNo(default = False)
LCD4linux.IconBarType = ConfigSelection(choices = DirType, default="0")
LCD4linux.IconBarPopup = ConfigSelection(choices = [("0", _("off"))] + ScreenSet, default="0")
LCD4linux.IconBarPopupLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.Sun = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.SunLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.SunSize = ConfigSlider(default = 20,  increment = 1, limits = (5, 150))
LCD4linux.SunPos = ConfigSlider(default = 20,  increment = 2, limits = (0, 1024))
LCD4linux.SunAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.SunSplit = ConfigYesNo(default = False)
LCD4linux.SunColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.SunBackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.SunShadow = ConfigYesNo(default = False)
LCD4linux.SunFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.SunType = ConfigSelection(choices = DirType, default="2")
LCD4linux.Fritz = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.FritzLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.FritzSize = ConfigSlider(default = 22,  increment = 1, limits = (10, 150))
LCD4linux.FritzPos = ConfigSlider(default = 130,  increment = 2, limits = (0, 1024))
LCD4linux.FritzAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.FritzColor = ConfigSelection(choices = Farbe, default="yellow")
LCD4linux.FritzBackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.FritzType = ConfigSelection(choices = FritzType, default="TL")
LCD4linux.FritzPicSize = ConfigSlider(default = 100,  increment = 1, limits = (10, 1024))
LCD4linux.FritzPicPos = ConfigSlider(default = 30,  increment = 2, limits = (0, 1024))
LCD4linux.FritzPicAlign = ConfigSlider(default = 0,  increment = 10, limits = (0, 1024))
LCD4linux.FritzShadow = ConfigYesNo(default = False)
LCD4linux.FritzFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.Picon = ConfigSelection(choices = ScreenSelect, default="1")
LCD4linux.PiconLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.PiconPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.PiconSize = ConfigSlider(default = 200,  increment = 10, limits = (10, 1024))
LCD4linux.PiconFullScreen = ConfigYesNo(default = False)
LCD4linux.PiconAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.PiconSplit = ConfigYesNo(default = False)
LCD4linux.PiconTextSize = ConfigSlider(default = 30,  increment = 2, limits = (10, 150))
LCD4linux.PiconPath = ConfigText(default="/picon/", fixed_size=False, visible_width=50)
LCD4linux.PiconPathAlt = ConfigText(default="/media/hdd/picon/", fixed_size=False, visible_width=50)
LCD4linux.PiconTransparenz = ConfigSelection(choices = [("0", _("no")), ("2", _("yes (32bit)"))], default="2")
LCD4linux.PiconCache = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.Picon2 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.Picon2LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.Picon2Pos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.Picon2Size = ConfigSlider(default = 240,  increment = 10, limits = (10, 1024))
LCD4linux.Picon2FullScreen = ConfigYesNo(default = False)
LCD4linux.Picon2Align = ConfigSelection(choices = AlignType, default="1")
LCD4linux.Picon2Split = ConfigYesNo(default = False)
LCD4linux.Picon2TextSize = ConfigSlider(default = 30,  increment = 2, limits = (10, 150))
LCD4linux.Picon2Path = ConfigText(default="/usr/share/enigma2/picon/", fixed_size=False, visible_width=50)
LCD4linux.Picon2PathAlt = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.Picon2Cache = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.Clock = ConfigSelection(choices = ScreenSelect, default="1")
LCD4linux.ClockLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.ClockType = ConfigSelection(choices = ClockType, default="12")
LCD4linux.ClockSpacing = ConfigSelectionNumber(0, 3, 1, default = 2)
LCD4linux.ClockAnalog = ConfigSelectionNumber(1, 6, 1, default = 1)
LCD4linux.ClockSize = ConfigSlider(default = 70,  increment = 2, limits = (10, 400))
LCD4linux.ClockPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.ClockAlign = ConfigSelection(choices = AlignType, default="2")
LCD4linux.ClockSplit = ConfigYesNo(default = False)
LCD4linux.ClockColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.ClockShadow = ConfigYesNo(default = False)
LCD4linux.ClockFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.Clock2 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.Clock2LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.Clock2Type = ConfigSelection(choices = ClockType, default="12")
LCD4linux.Clock2Spacing = ConfigSelectionNumber(0, 3, 1, default = 0)
LCD4linux.Clock2Analog = ConfigSelectionNumber(1, 6, 1, default = 1)
LCD4linux.Clock2Size = ConfigSlider(default = 70,  increment = 2, limits = (10, 400))
LCD4linux.Clock2Pos = ConfigSlider(default = 150,  increment = 2, limits = (0, 1024))
LCD4linux.Clock2Align = ConfigSelection(choices = AlignType, default="1")
LCD4linux.Clock2Split = ConfigYesNo(default = False)
LCD4linux.Clock2Color = ConfigSelection(choices = Farbe, default="white")
LCD4linux.Clock2Shadow = ConfigYesNo(default = False)
LCD4linux.Clock2Font = ConfigSelection(choices = FontType, default="0")
LCD4linux.Channel = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.ChannelLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.ChannelSize = ConfigSlider(default = 50,  increment = 2, limits = (10, 300))
LCD4linux.ChannelPos = ConfigSlider(default = 10,  increment = 2, limits = (0, 1024))
LCD4linux.ChannelLines = ConfigSelectionNumber(1, 9, 1, default = 1)
LCD4linux.ChannelAlign = ConfigSelection(choices = AlignType, default="1")
LCD4linux.ChannelSplit = ConfigYesNo(default = False)
LCD4linux.ChannelColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.ChannelShadow = ConfigYesNo(default = False)
LCD4linux.ChannelFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.ChannelNum = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.ChannelNumLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.ChannelNumSize = ConfigSlider(default = 60,  increment = 2, limits = (10, 300))
LCD4linux.ChannelNumPos = ConfigSlider(default = 10,  increment = 2, limits = (0, 1024))
LCD4linux.ChannelNumAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.ChannelNumShadow = ConfigYesNo(default = False)
LCD4linux.ChannelNumColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.ChannelNumBackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.ChannelNumFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.Desc = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.DescLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.DescType = ConfigSelection(choices = DescriptionType, default="01")
LCD4linux.DescSize = ConfigSlider(default = 32,  increment = 1, limits = (10, 150))
LCD4linux.DescLines = ConfigSelectionNumber(1, 20, 1, default = 3)
LCD4linux.DescPos = ConfigSlider(default = 130,  increment = 2, limits = (0, 1024))
LCD4linux.DescAlign = ConfigSelection(choices = AlignType, default="1")
LCD4linux.DescSplit = ConfigYesNo(default = False)
LCD4linux.DescColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.DescShadow = ConfigYesNo(default = False)
LCD4linux.DescFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.Prog = ConfigSelection(choices = ScreenSelect, default="1")
LCD4linux.ProgLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.ProgType = ConfigSelection(choices = [("1", _("Time+Info")), ("2", _("Info")), ("3", _("Time+Duration+Info"))], default="2")
LCD4linux.ProgSize = ConfigSlider(default = 43,  increment = 1, limits = (10, 150))
LCD4linux.ProgLines = ConfigSelectionNumber(1, 9, 1, default = 1)
LCD4linux.ProgPos = ConfigSlider(default = 150,  increment = 2, limits = (0, 1024))
LCD4linux.ProgAlign = ConfigSelection(choices = AlignType, default="1")
LCD4linux.ProgSplit = ConfigYesNo(default = False)
LCD4linux.ProgColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.ProgShadow = ConfigYesNo(default = False)
LCD4linux.ProgFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.ProgNext = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.ProgNextLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.ProgNextType = ConfigSelection(choices = [("1", _("Time+Info")), ("2", _("Info")), ("3", _("Time+Length+Info")), ("4", _("Mini-EPG"))], default="1")
LCD4linux.ProgNextSize = ConfigSlider(default = 32,  increment = 1, limits = (10, 150))
LCD4linux.ProgNextLines = ConfigSelectionNumber(1, 20, 1, default = 3)
LCD4linux.ProgNextPos = ConfigSlider(default = 120,  increment = 2, limits = (0, 1024))
LCD4linux.ProgNextAlign = ConfigSelection(choices = AlignType, default="1")
LCD4linux.ProgNextSplit = ConfigYesNo(default = False)
LCD4linux.ProgNextColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.ProgNextShadow = ConfigYesNo(default = False)
LCD4linux.ProgNextFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.Progress = ConfigSelection(choices = ScreenSelect, default="1")
LCD4linux.ProgressLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.ProgressType = ConfigSelection(choices = ProgressType, default="21")
LCD4linux.ProgressSize = ConfigSlider(default = 25,  increment = 1, limits = (5, 100))
LCD4linux.ProgressLen = ConfigSelection(choices = ProzentType, default="100")
LCD4linux.ProgressAlign = ConfigSelection(choices = [("5", _("half left")), ("6", _("half right"))] + AlignType, default="1")
LCD4linux.ProgressPos = ConfigSlider(default = 210,  increment = 2, limits = (0, 1024))
LCD4linux.ProgressColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.ProgressShadow = ConfigYesNo(default = False)
LCD4linux.ProgressShadow2 = ConfigYesNo(default = False)
LCD4linux.Sat = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.SatLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.SatSize = ConfigSlider(default = 32,  increment = 1, limits = (10, 150))
LCD4linux.SatPos = ConfigSlider(default = 120,  increment = 2, limits = (0, 1024))
LCD4linux.SatAlign = ConfigSelection(choices = AlignType, default="1")
LCD4linux.SatSplit = ConfigYesNo(default = False)
LCD4linux.SatColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.SatType = ConfigSelection(choices = [("0", _("Position")), ("1", _("Name")), ("2", _("Picon")), ("2A", _("Picon+Position left")), ("2B", _("Picon+Position below")), ("2C", _("Picon+Position right"))], default="1")
LCD4linux.SatPath = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.SatShadow = ConfigYesNo(default = False)
LCD4linux.SatFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.Prov = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.ProvLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.ProvSize = ConfigSlider(default = 32,  increment = 1, limits = (10, 150))
LCD4linux.ProvPos = ConfigSlider(default = 120,  increment = 2, limits = (0, 1024))
LCD4linux.ProvAlign = ConfigSelection(choices = AlignType, default="1")
LCD4linux.ProvSplit = ConfigYesNo(default = False)
LCD4linux.ProvColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.ProvType = ConfigSelection(choices = [("1", _("Name")), ("2", _("Picon"))], default="1")
LCD4linux.ProvPath = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.ProvShadow = ConfigYesNo(default = False)
LCD4linux.ProvFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.Info = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.InfoLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.InfoTuner = ConfigSelection(choices = [("0", _("no")), ("A", _("db")), ("B", _("%")), ("AB", _("db + %")), ("ABC", _("db + % + BER")), ("AC", _("db + BER")), ("BC", _("% + BER"))], default="0")
LCD4linux.InfoSensor = ConfigSelection(choices = InfoSensor, default="0")
LCD4linux.InfoCPU = ConfigSelection(choices = InfoCPU, default="0")
LCD4linux.InfoSize = ConfigSlider(default = 20,  increment = 1, limits = (10, 150))
LCD4linux.InfoPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.InfoAlign = ConfigSelection(choices = AlignType, default="1")
LCD4linux.InfoSplit = ConfigYesNo(default = False)
LCD4linux.InfoLines = ConfigSelectionNumber(1, 9, 1, default = 1)
LCD4linux.InfoColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.InfoShadow = ConfigYesNo(default = False)
LCD4linux.InfoFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.Signal = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.SignalLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.SignalSize = ConfigSlider(default = 15,  increment = 1, limits = (5, 150))
LCD4linux.SignalPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.SignalLen = ConfigSelection(choices = ProzentType, default="100")
LCD4linux.SignalAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.SignalSplit = ConfigYesNo(default = False)
LCD4linux.SignalColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.SignalGradient = ConfigYesNo(default = False)
LCD4linux.SignalMin = ConfigSlider(default = 40,  increment = 5, limits = (0, 50))
LCD4linux.SignalMax = ConfigSlider(default = 90,  increment = 5, limits = (50, 100))
LCD4linux.Tuner = ConfigSelection(choices = ScreenSelect, default="1")
LCD4linux.TunerLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.TunerSize = ConfigSlider(default = 48,  increment = 1, limits = (10, 150))
LCD4linux.TunerPos = ConfigSlider(default = 70,  increment = 2, limits = (0, 1024))
LCD4linux.TunerAlign = ConfigSelection(choices = AlignType, default="2")
LCD4linux.TunerSplit = ConfigYesNo(default = False)
LCD4linux.TunerType = ConfigSelection(choices = DirType, default="0")
LCD4linux.TunerActive = ConfigYesNo(default = False)
LCD4linux.TunerFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.Vol = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.VolLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.VolSize = ConfigSlider(default = 22,  increment = 1, limits = (5, 150))
LCD4linux.VolPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.VolAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.VolLen = ConfigSelection(choices = ProzentType, default="100")
LCD4linux.VolSplit = ConfigYesNo(default = False)
LCD4linux.VolColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.VolShadow = ConfigYesNo(default = False)
LCD4linux.Ping = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.PingLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.PingSize = ConfigSlider(default = 15,  increment = 2, limits = (10, 100))
LCD4linux.PingPos = ConfigSlider(default = 20,  increment = 2, limits = (0, 1024))
LCD4linux.PingAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.PingSplit = ConfigYesNo(default = False)
LCD4linux.PingColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.PingShadow = ConfigYesNo(default = False)
LCD4linux.PingFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.PingShow = ConfigSelection(choices = [("0", _("Online+Offline")), ("1", _("Online")), ("2", _("Offline"))], default="0")
LCD4linux.PingType = ConfigSelection(choices = DirType, default="0")
LCD4linux.PingTimeout = ConfigSlider(default = 50,  increment = 5, limits = (5, 1000))
LCD4linux.PingName1 = ConfigText(default="Internet:www.google.de", fixed_size=False)
LCD4linux.PingName2 = ConfigText(default="", fixed_size=False)
LCD4linux.PingName3 = ConfigText(default="", fixed_size=False)
LCD4linux.PingName4 = ConfigText(default="", fixed_size=False)
LCD4linux.PingName5 = ConfigText(default="", fixed_size=False)
LCD4linux.AV = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.AVLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.AVSize = ConfigSlider(default = 22,  increment = 1, limits = (10, 150))
LCD4linux.AVPos = ConfigSlider(default = 100,  increment = 2, limits = (0, 1024))
LCD4linux.AVAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.AVSplit = ConfigYesNo(default = False)
LCD4linux.AVColor = ConfigSelection(choices = Farbe, default="gold")
LCD4linux.AVShadow = ConfigYesNo(default = False)
LCD4linux.AVType = ConfigSelection(choices = [("1", _("one line")), ("2", _("two lines"))], default="1")
LCD4linux.AVFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.Bitrate = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.BitrateLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.BitrateSize = ConfigSlider(default = 22,  increment = 1, limits = (10, 150))
LCD4linux.BitratePos = ConfigSlider(default = 100,  increment = 2, limits = (0, 1024))
LCD4linux.BitrateAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.BitrateSplit = ConfigYesNo(default = False)
LCD4linux.BitrateColor = ConfigSelection(choices = Farbe, default="gold")
LCD4linux.BitrateShadow = ConfigYesNo(default = False)
LCD4linux.BitrateFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.Dev = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.DevLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.DevSize = ConfigSlider(default = 15,  increment = 2, limits = (10, 300))
LCD4linux.DevPos = ConfigSlider(default = 20,  increment = 2, limits = (0, 1024))
LCD4linux.DevAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.DevSplit = ConfigYesNo(default = False)
LCD4linux.DevColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.DevShadow = ConfigYesNo(default = False)
LCD4linux.DevFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.DevType = ConfigSelection(choices = DirType, default="0")
LCD4linux.DevExtra = ConfigSelection(choices = [("0", _("no")), ("RAM", _("Memory"))], default="RAM")
LCD4linux.DevName1 = ConfigText(default="/media/hdd", fixed_size=False)
LCD4linux.DevName2 = ConfigText(default="", fixed_size=False)
LCD4linux.DevName3 = ConfigText(default="", fixed_size=False)
LCD4linux.DevName4 = ConfigText(default="", fixed_size=False)
LCD4linux.DevName5 = ConfigText(default="", fixed_size=False)
LCD4linux.Hdd = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.HddLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.HddSize = ConfigSlider(default = 32,  increment = 1, limits = (10, 150))
LCD4linux.HddPos = ConfigSlider(default = 120,  increment = 2, limits = (0, 1024))
LCD4linux.HddAlign = ConfigSelection(choices = AlignType, default="1")
LCD4linux.HddSplit = ConfigYesNo(default = False)
LCD4linux.HddType = ConfigSelection(choices = HddType, default="0")
LCD4linux.Timer = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.TimerLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.TimerSize = ConfigSlider(default = 22,  increment = 1, limits = (10, 150))
LCD4linux.TimerLines = ConfigSelectionNumber(1, 20, 1, default = 1)
LCD4linux.TimerType = ConfigSelection(choices = [("0", _("use lead-time")), ("1", _("only use Timer"))], default="0")
LCD4linux.TimerPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.TimerAlign = ConfigSelection(choices = [("0", _("left")), ("2", _("half right"))], default="0")
LCD4linux.TimerSplit = ConfigYesNo(default = False)
LCD4linux.TimerColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.TimerShadow = ConfigYesNo(default = False)
LCD4linux.TimerFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.Wetter = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.WetterLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.WetterPos = ConfigSlider(default = 50,  increment = 2, limits = (0, 1024))
LCD4linux.WetterAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.WetterSplit = ConfigYesNo(default = False)
LCD4linux.WetterZoom = ConfigSlider(default = 10,  increment = 1, limits = (7, 60))
LCD4linux.WetterType = ConfigSelection(choices = WetterType, default="1")
LCD4linux.WetterColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.WetterShadow = ConfigYesNo(default = False)
LCD4linux.WetterFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.Wetter2 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.Wetter2LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.Wetter2Pos = ConfigSlider(default = 50,  increment = 2, limits = (0, 1024))
LCD4linux.Wetter2Align = ConfigSelection(choices = AlignType, default="0")
LCD4linux.Wetter2Split = ConfigYesNo(default = False)
LCD4linux.Wetter2Zoom = ConfigSlider(default = 10,  increment = 1, limits = (7, 60))
LCD4linux.Wetter2Type = ConfigSelection(choices = WetterType, default="1")
LCD4linux.Wetter2Color = ConfigSelection(choices = Farbe, default="white")
LCD4linux.Wetter2Shadow = ConfigYesNo(default = False)
LCD4linux.Wetter2Font = ConfigSelection(choices = FontType, default="0")
LCD4linux.Meteo = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MeteoLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MeteoPos = ConfigSlider(default = 50,  increment = 2, limits = (0, 1024))
LCD4linux.MeteoAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MeteoSplit = ConfigYesNo(default = False)
LCD4linux.MeteoZoom = ConfigSlider(default = 10,  increment = 1, limits = (7, 60))
LCD4linux.MeteoType = ConfigSelection(choices = MeteoType, default="1")
LCD4linux.MeteoColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.Moon = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MoonLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MoonSize = ConfigSlider(default = 60,  increment = 2, limits = (10, 300))
LCD4linux.MoonPos = ConfigSlider(default = 10,  increment = 2, limits = (0, 1024))
LCD4linux.MoonAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MoonSplit = ConfigYesNo(default = False)
LCD4linux.MoonColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="white")
LCD4linux.MoonShadow = ConfigYesNo(default = False)
LCD4linux.MoonFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.NetAtmoCO2Min = ConfigSlider(default = 200,  increment = 100, limits = (0, 1000))
LCD4linux.NetAtmoCO2Max = ConfigSlider(default = 1500,  increment = 100, limits = (500, 10000))
LCD4linux.NetAtmo = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.NetAtmoLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.NetAtmoPos = ConfigSlider(default = 50,  increment = 2, limits = (0, 1024))
LCD4linux.NetAtmoAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.NetAtmoSplit = ConfigYesNo(default = False)
LCD4linux.NetAtmoType = ConfigSelection(choices = NetatmoType, default="THCPN")
LCD4linux.NetAtmoType2 = ConfigSelection(choices = DirType, default="0")
LCD4linux.NetAtmoSize = ConfigSlider(default = 30,  increment = 1, limits = (10, 100))
LCD4linux.NetAtmoColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.NetAtmoShadow = ConfigYesNo(default = False)
LCD4linux.NetAtmoFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.NetAtmoCO2 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.NetAtmoCO2LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.NetAtmoCO2Size = ConfigSlider(default = 30,  increment = 1, limits = (5, 500))
LCD4linux.NetAtmoCO2Len = ConfigSlider(default = 200,  increment = 5, limits = (100, 1024))
LCD4linux.NetAtmoCO2Pos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.NetAtmoCO2Align = ConfigSelection(choices = AlignType, default="0")
LCD4linux.NetAtmoCO2Split = ConfigYesNo(default = False)
LCD4linux.NetAtmoCO2Type = ConfigSelection(choices = CO2Type, default="1")
LCD4linux.NetAtmoIDX = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.NetAtmoIDXLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.NetAtmoIDXSize = ConfigSlider(default = 30,  increment = 1, limits = (5, 500))
LCD4linux.NetAtmoIDXLen = ConfigSlider(default = 200,  increment = 5, limits = (100, 1024))
LCD4linux.NetAtmoIDXPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.NetAtmoIDXAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.NetAtmoIDXSplit = ConfigYesNo(default = False)
LCD4linux.NetAtmoIDXType = ConfigSelection(choices = CO2Type, default="1")
LCD4linux.OSCAM = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.OSCAMLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.OSCAMFile = ConfigText(default="/tmp/.oscam/oscam.lcd", fixed_size=False)
LCD4linux.OSCAMSize = ConfigSlider(default = 10,  increment = 1, limits = (9, 50))
LCD4linux.OSCAMPos = ConfigSlider(default = 20,  increment = 2, limits = (0, 1024))
LCD4linux.OSCAMAlign = ConfigSelection(choices = [("0", _("left")), ("2", _("right"))], default="0")
LCD4linux.OSCAMSplit = ConfigYesNo(default = False)
LCD4linux.OSCAMColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.OSCAMBackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="black")
LCD4linux.ECM = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.ECMLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.ECMSize = ConfigSlider(default = 10,  increment = 1, limits = (9, 50))
LCD4linux.ECMPos = ConfigSlider(default = 20,  increment = 2, limits = (0, 1024))
LCD4linux.ECMAlign = ConfigSelection(choices = [("0", _("left")), ("2", _("right"))], default="0")
LCD4linux.ECMSplit = ConfigYesNo(default = False)
LCD4linux.ECMColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.ECMBackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="black")
LCD4linux.Text = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.TextLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.TextFile = ConfigText(default="/tmp/lcd4linux.txt", fixed_size=False, visible_width=50)
LCD4linux.TextSize = ConfigSlider(default = 32,  increment = 1, limits = (10, 300))
LCD4linux.TextFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.TextPos = ConfigSlider(default = 120,  increment = 2, limits = (0, 1024))
LCD4linux.TextAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.TextShadow = ConfigYesNo(default = False)
LCD4linux.TextColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.TextBackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.Text2 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.Text2LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.Text2File = ConfigText(default="/tmp/lcd4linux.txt", fixed_size=False, visible_width=50)
LCD4linux.Text2Size = ConfigSlider(default = 32,  increment = 1, limits = (10, 300))
LCD4linux.Text2Font = ConfigSelection(choices = FontType, default="0")
LCD4linux.Text2Pos = ConfigSlider(default = 120,  increment = 2, limits = (0, 1024))
LCD4linux.Text2Align = ConfigSelection(choices = AlignType, default="0")
LCD4linux.Text2Shadow = ConfigYesNo(default = False)
LCD4linux.Text2Color = ConfigSelection(choices = Farbe, default="white")
LCD4linux.Text2BackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.Text3 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.Text3LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.Text3File = ConfigText(default="/tmp/lcd4linux.txt", fixed_size=False, visible_width=50)
LCD4linux.Text3Size = ConfigSlider(default = 32,  increment = 1, limits = (10, 300))
LCD4linux.Text3Font = ConfigSelection(choices = FontType, default="0")
LCD4linux.Text3Pos = ConfigSlider(default = 120,  increment = 2, limits = (0, 1024))
LCD4linux.Text3Align = ConfigSelection(choices = AlignType, default="0")
LCD4linux.Text3Shadow = ConfigYesNo(default = False)
LCD4linux.Text3Color = ConfigSelection(choices = Farbe, default="white")
LCD4linux.Text3BackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.HTTP = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.HTTPLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.HTTPURL = ConfigText(default="http://", fixed_size=False, visible_width=50)
LCD4linux.HTTPSize = ConfigSlider(default = 20,  increment = 1, limits = (10, 300))
LCD4linux.HTTPPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.HTTPAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.HTTPColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.HTTPBackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.HTTPShadow = ConfigYesNo(default = False)
LCD4linux.HTTPFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.WWWTime = ConfigSelection(choices = [("10", _("60min")), ("10,40", _("30min"))], default="10")
LCD4linux.WWW1 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.WWW1LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.WWW1Size = ConfigSlider(default = 200,  increment = 1, limits = (50, 1024))
LCD4linux.WWW1Pos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.WWW1Align = ConfigSelection(choices = AlignType, default="0")
LCD4linux.WWW1url = ConfigText(default="http://", fixed_size=False, visible_width=50)
LCD4linux.WWW1w = ConfigSlider(default = 800,  increment = 50, limits = (600, 2000))
LCD4linux.WWW1h = ConfigSlider(default = 600,  increment = 50, limits = (100, 2000))
LCD4linux.WWW1CutX = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.WWW1CutY = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.WWW1CutW = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.WWW1CutH = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.Bild = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.BildLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.BildFile = ConfigText(default="/tmp/lcd4linux.jpg", fixed_size=False, visible_width=50)
LCD4linux.BildSize = ConfigSlider(default = 240,  increment = 10, limits = (10, 1024))
LCD4linux.BildPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.BildAlign = ConfigSelection(choices = AlignType + [("9", _("full Screen"))], default="0")
LCD4linux.BildQuick = ConfigYesNo(default = False)
LCD4linux.BildTransp = ConfigYesNo(default = False)
LCD4linux.Bild2 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.Bild2LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.Bild2File = ConfigText(default="/tmp/lcd4linux.jpg", fixed_size=False, visible_width=50)
LCD4linux.Bild2Size = ConfigSlider(default = 240,  increment = 10, limits = (10, 1024))
LCD4linux.Bild2Pos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.Bild2Align = ConfigSelection(choices = AlignType + [("9", _("full Screen"))], default="0")
LCD4linux.Bild2Quick = ConfigYesNo(default = False)
LCD4linux.Bild2Transp = ConfigYesNo(default = False)
LCD4linux.Bild3 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.Bild3LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.Bild3File = ConfigText(default="/tmp/lcd4linux.jpg", fixed_size=False, visible_width=50)
LCD4linux.Bild3Size = ConfigSlider(default = 240,  increment = 10, limits = (10, 1024))
LCD4linux.Bild3Pos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.Bild3Align = ConfigSelection(choices = AlignType + [("9", _("full Screen"))], default="0")
LCD4linux.Bild3Quick = ConfigYesNo(default = False)
LCD4linux.Bild3Transp = ConfigYesNo(default = False)
LCD4linux.Bild4 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.Bild4LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.Bild4File = ConfigText(default="/tmp/lcd4linux.jpg", fixed_size=False, visible_width=50)
LCD4linux.Bild4Size = ConfigSlider(default = 240,  increment = 10, limits = (10, 1024))
LCD4linux.Bild4Pos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.Bild4Align = ConfigSelection(choices = AlignType + [("9", _("full Screen"))], default="0")
LCD4linux.Bild4Quick = ConfigYesNo(default = False)
LCD4linux.Bild4Transp = ConfigYesNo(default = False)
LCD4linux.TV = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.TVLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.TVType = ConfigSelection(choices = [("0", _("TV")), ("1", _("TV+OSD"))], default="0")
LCD4linux.Box1 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.Box1LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.Box1x1 = ConfigSlider(default = 10,  increment = 1, limits = (0, 1024))
LCD4linux.Box1y1 = ConfigSlider(default = 10,  increment = 1, limits = (0, 1024))
LCD4linux.Box1x2 = ConfigSlider(default = 200,  increment = 1, limits = (0, 1024))
LCD4linux.Box1y2 = ConfigSlider(default = 1,  increment = 1, limits = (0, 1024))
LCD4linux.Box1Color = ConfigSelection(choices = Farbe, default="white")
LCD4linux.Box1BackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.Box2 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.Box2LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.Box2x1 = ConfigSlider(default = 20,  increment = 1, limits = (0, 1024))
LCD4linux.Box2y1 = ConfigSlider(default = 20,  increment = 1, limits = (0, 1024))
LCD4linux.Box2x2 = ConfigSlider(default = 200,  increment = 1, limits = (0, 1024))
LCD4linux.Box2y2 = ConfigSlider(default = 1,  increment = 1, limits = (0, 1024))
LCD4linux.Box2Color = ConfigSelection(choices = Farbe, default="white")
LCD4linux.Box2BackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.MPHelligkeit = ConfigSelectionNumber(0, 10, 1, default = 5)
LCD4linux.MPHelligkeit2 = ConfigSelectionNumber(0, 10, 1, default = 5)
LCD4linux.MPHelligkeit3 = ConfigSelectionNumber(0, 10, 1, default = 5)
LCD4linux.MPScreenMax = ConfigSelection(choices = ScreenUse, default="1")
LCD4linux.MPLCDBild1 = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.MPLCDBild2 = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.MPLCDBild3 = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.MPLCDColor1 = ConfigSelection(choices = Farbe, default="black")
LCD4linux.MPLCDColor2 = ConfigSelection(choices = Farbe, default="black")
LCD4linux.MPLCDColor3 = ConfigSelection(choices = Farbe, default="black")
LCD4linux.MPDesc = ConfigSelection(choices = ScreenSelect, default="1")
LCD4linux.MPDescLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPDescType = ConfigSelection(choices = DescriptionType, default="12")
LCD4linux.MPDescSize = ConfigSlider(default = 31,  increment = 1, limits = (10, 150))
LCD4linux.MPDescLines = ConfigSelectionNumber(1, 20, 1, default = 3)
LCD4linux.MPDescPos = ConfigSlider(default = 130,  increment = 2, limits = (0, 1024))
LCD4linux.MPDescAlign = ConfigSelection(choices = AlignType, default="1")
LCD4linux.MPDescSplit = ConfigYesNo(default = False)
LCD4linux.MPDescColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPDescShadow = ConfigYesNo(default = False)
LCD4linux.MPDescFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPTitle = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPTitleLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPTitleSize = ConfigSlider(default = 32,  increment = 1, limits = (10, 150))
LCD4linux.MPTitleLines = ConfigSelectionNumber(1, 9, 1, default = 2)
LCD4linux.MPTitlePos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.MPTitleAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MPTitleSplit = ConfigYesNo(default = False)
LCD4linux.MPTitleColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPTitleShadow = ConfigYesNo(default = False)
LCD4linux.MPTitleFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPComm = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPCommLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPCommSize = ConfigSlider(default = 32,  increment = 1, limits = (10, 150))
LCD4linux.MPCommLines = ConfigSelectionNumber(1, 9, 1, default = 3)
LCD4linux.MPCommPos = ConfigSlider(default = 130,  increment = 2, limits = (0, 1024))
LCD4linux.MPCommAlign = ConfigSelection(choices = AlignType, default="1")
LCD4linux.MPCommSplit = ConfigYesNo(default = False)
LCD4linux.MPCommColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPCommShadow = ConfigYesNo(default = False)
LCD4linux.MPCommFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPChannel = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPChannelLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPChannelSize = ConfigSlider(default = 50,  increment = 2, limits = (10, 300))
LCD4linux.MPChannelPos = ConfigSlider(default = 10,  increment = 2, limits = (0, 1024))
LCD4linux.MPChannelLines = ConfigSelectionNumber(1, 9, 1, default = 1)
LCD4linux.MPChannelAlign = ConfigSelection(choices = AlignType, default="1")
LCD4linux.MPChannelSplit = ConfigYesNo(default = False)
LCD4linux.MPChannelColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPChannelShadow = ConfigYesNo(default = False)
LCD4linux.MPChannelFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPProgress = ConfigSelection(choices = ScreenSelect, default="1")
LCD4linux.MPProgressLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPProgressType = ConfigSelection(choices = ProgressType, default="61")
LCD4linux.MPProgressSize = ConfigSlider(default = 23,  increment = 1, limits = (5, 100))
LCD4linux.MPProgressLen = ConfigSelection(choices = ProzentType, default="100")
LCD4linux.MPProgressPos = ConfigSlider(default = 6,  increment = 2, limits = (0, 1024))
LCD4linux.MPProgressAlign = ConfigSelection(choices = [("0", _("half left")), ("1", _("center")), ("2", _("half right"))], default="0")
LCD4linux.MPProgressColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPProgressShadow = ConfigYesNo(default = False)
LCD4linux.MPProgressShadow2 = ConfigYesNo(default = False)
LCD4linux.MPVol = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPVolLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPVolSize = ConfigSlider(default = 22,  increment = 1, limits = (10, 150))
LCD4linux.MPVolPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.MPVolAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MPVolLen = ConfigSelection(choices = ProzentType, default="100")
LCD4linux.MPVolSplit = ConfigYesNo(default = False)
LCD4linux.MPVolColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPVolShadow = ConfigYesNo(default = False)
LCD4linux.MPPing = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPPingLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPPingSize = ConfigSlider(default = 15,  increment = 2, limits = (10, 100))
LCD4linux.MPPingPos = ConfigSlider(default = 20,  increment = 2, limits = (0, 1024))
LCD4linux.MPPingAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MPPingSplit = ConfigYesNo(default = False)
LCD4linux.MPPingColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPPingShadow = ConfigYesNo(default = False)
LCD4linux.MPPingFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPPingShow = ConfigSelection(choices = [("0", _("Online+Offline")), ("1", _("Online")), ("2", _("Offline"))], default="0")
LCD4linux.MPPingType = ConfigSelection(choices = DirType, default="0")
LCD4linux.MPPingTimeout = ConfigSlider(default = 50,  increment = 5, limits = (5, 1000))
LCD4linux.MPPingName1 = ConfigText(default="Internet:www.google.de", fixed_size=False)
LCD4linux.MPPingName2 = ConfigText(default="", fixed_size=False)
LCD4linux.MPPingName3 = ConfigText(default="", fixed_size=False)
LCD4linux.MPPingName4 = ConfigText(default="", fixed_size=False)
LCD4linux.MPPingName5 = ConfigText(default="", fixed_size=False)
LCD4linux.MPClock = ConfigSelection(choices = ScreenSelect, default="1")
LCD4linux.MPClockLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPClockType = ConfigSelection(choices = ClockType, default="12")
LCD4linux.MPClockSpacing = ConfigSelectionNumber(0, 3, 1, default = 0)
LCD4linux.MPClockAnalog = ConfigSelectionNumber(1, 6, 1, default = 1)
LCD4linux.MPClockSize = ConfigSlider(default = 70,  increment = 2, limits = (10, 400))
LCD4linux.MPClockPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.MPClockAlign = ConfigSelection(choices = AlignType, default="2")
LCD4linux.MPClockSplit = ConfigYesNo(default = False)
LCD4linux.MPClockColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPClockShadow = ConfigYesNo(default = False)
LCD4linux.MPClockFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPClock2 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPClock2LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPClock2Type = ConfigSelection(choices = ClockType, default="12")
LCD4linux.MPClock2Spacing = ConfigSelectionNumber(0, 3, 1, default = 0)
LCD4linux.MPClock2Analog = ConfigSelectionNumber(1, 6, 1, default = 1)
LCD4linux.MPClock2Size = ConfigSlider(default = 70,  increment = 2, limits = (10, 400))
LCD4linux.MPClock2Pos = ConfigSlider(default = 150,  increment = 2, limits = (0, 1024))
LCD4linux.MPClock2Align = ConfigSelection(choices = AlignType, default="1")
LCD4linux.MPClock2Split = ConfigYesNo(default = False)
LCD4linux.MPClock2Color = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPClock2Shadow = ConfigYesNo(default = False)
LCD4linux.MPClock2Font = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPTuner = ConfigSelection(choices = ScreenSelect, default="1")
LCD4linux.MPTunerLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPTunerSize = ConfigSlider(default = 48,  increment = 1, limits = (10, 150))
LCD4linux.MPTunerPos = ConfigSlider(default = 70,  increment = 2, limits = (0, 1024))
LCD4linux.MPTunerAlign = ConfigSelection(choices = AlignType, default="2")
LCD4linux.MPTunerSplit = ConfigYesNo(default = False)
LCD4linux.MPTunerType = ConfigSelection(choices = DirType, default="0")
LCD4linux.MPTunerActive = ConfigYesNo(default = False)
LCD4linux.MPTunerFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPInfo = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPInfoLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPInfoSensor = ConfigSelection(choices = InfoSensor, default="0")
LCD4linux.MPInfoCPU = ConfigSelection(choices = InfoCPU, default="0")
LCD4linux.MPInfoSize = ConfigSlider(default = 20,  increment = 1, limits = (10, 150))
LCD4linux.MPInfoPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.MPInfoAlign = ConfigSelection(choices = AlignType, default="1")
LCD4linux.MPInfoSplit = ConfigYesNo(default = False)
LCD4linux.MPInfoLines = ConfigSelectionNumber(1, 9, 1, default = 1)
LCD4linux.MPInfoColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPInfoShadow = ConfigYesNo(default = False)
LCD4linux.MPInfoFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPAV = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPAVLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPAVSize = ConfigSlider(default = 22,  increment = 1, limits = (10, 150))
LCD4linux.MPAVPos = ConfigSlider(default = 100,  increment = 2, limits = (0, 1024))
LCD4linux.MPAVAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MPAVSplit = ConfigYesNo(default = False)
LCD4linux.MPAVColor = ConfigSelection(choices = Farbe, default="gold")
LCD4linux.MPAVShadow = ConfigYesNo(default = False)
LCD4linux.MPAVType = ConfigSelection(choices = [("1", _("one line")), ("2", _("two lines"))], default="1")
LCD4linux.MPAVFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPBitrate = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPBitrateLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPBitrateSize = ConfigSlider(default = 22,  increment = 1, limits = (10, 150))
LCD4linux.MPBitratePos = ConfigSlider(default = 100,  increment = 2, limits = (0, 1024))
LCD4linux.MPBitrateAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MPBitrateSplit = ConfigYesNo(default = False)
LCD4linux.MPBitrateColor = ConfigSelection(choices = Farbe, default="gold")
LCD4linux.MPBitrateShadow = ConfigYesNo(default = False)
LCD4linux.MPBitrateFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPDev = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPDevLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPDevSize = ConfigSlider(default = 15,  increment = 2, limits = (10, 300))
LCD4linux.MPDevPos = ConfigSlider(default = 20,  increment = 2, limits = (0, 1024))
LCD4linux.MPDevAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MPDevSplit = ConfigYesNo(default = False)
LCD4linux.MPDevColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPDevShadow = ConfigYesNo(default = False)
LCD4linux.MPDevFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPDevType = ConfigSelection(choices = DirType, default="0")
LCD4linux.MPDevExtra = ConfigSelection(choices = [("0", _("no")), ("RAM", _("Memory"))], default="RAM")
LCD4linux.MPDevName1 = ConfigText(default="/media/hdd", fixed_size=False)
LCD4linux.MPDevName2 = ConfigText(default="", fixed_size=False)
LCD4linux.MPDevName3 = ConfigText(default="", fixed_size=False)
LCD4linux.MPDevName4 = ConfigText(default="", fixed_size=False)
LCD4linux.MPDevName5 = ConfigText(default="", fixed_size=False)
LCD4linux.MPHdd = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPHddLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPHddSize = ConfigSlider(default = 32,  increment = 1, limits = (10, 150))
LCD4linux.MPHddPos = ConfigSlider(default = 120,  increment = 2, limits = (0, 1024))
LCD4linux.MPHddAlign = ConfigSelection(choices = AlignType, default="1")
LCD4linux.MPHddSplit = ConfigYesNo(default = False)
LCD4linux.MPHddType = ConfigSelection(choices = HddType, default="0")
LCD4linux.MPTimer = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPTimerLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPTimerSize = ConfigSlider(default = 22,  increment = 1, limits = (10, 150))
LCD4linux.MPTimerLines = ConfigSelectionNumber(1, 20, 1, default = 1)
LCD4linux.MPTimerType = ConfigSelection(choices = [("0", _("use lead-time")), ("1", _("only use Timer"))], default="0")
LCD4linux.MPTimerPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.MPTimerAlign = ConfigSelection(choices = [("0", _("left")), ("2", _("half right"))], default="0")
LCD4linux.MPTimerSplit = ConfigYesNo(default = False)
LCD4linux.MPTimerColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPTimerShadow = ConfigYesNo(default = False)
LCD4linux.MPTimerFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPWetter = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPWetterLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPWetterPos = ConfigSlider(default = 50,  increment = 2, limits = (0, 1024))
LCD4linux.MPWetterAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MPWetterSplit = ConfigYesNo(default = False)
LCD4linux.MPWetterZoom = ConfigSlider(default = 10,  increment = 1, limits = (7, 60))
LCD4linux.MPWetterType = ConfigSelection(choices = WetterType, default="1")
LCD4linux.MPWetterColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPWetterShadow = ConfigYesNo(default = False)
LCD4linux.MPWetterFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPWetter2 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPWetter2LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPWetter2Pos = ConfigSlider(default = 50,  increment = 2, limits = (0, 1024))
LCD4linux.MPWetter2Align = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MPWetter2Split = ConfigYesNo(default = False)
LCD4linux.MPWetter2Zoom = ConfigSlider(default = 10,  increment = 1, limits = (7, 60))
LCD4linux.MPWetter2Type = ConfigSelection(choices = WetterType, default="1")
LCD4linux.MPWetter2Color = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPWetter2Shadow = ConfigYesNo(default = False)
LCD4linux.MPWetter2Font = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPMeteo = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPMeteoLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPMeteoPos = ConfigSlider(default = 50,  increment = 2, limits = (0, 1024))
LCD4linux.MPMeteoAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MPMeteoSplit = ConfigYesNo(default = False)
LCD4linux.MPMeteoZoom = ConfigSlider(default = 10,  increment = 1, limits = (7, 60))
LCD4linux.MPMeteoType = ConfigSelection(choices = MeteoType, default="1")
LCD4linux.MPMeteoColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPMoon = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPMoonLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPMoonSize = ConfigSlider(default = 60,  increment = 2, limits = (10, 300))
LCD4linux.MPMoonPos = ConfigSlider(default = 10,  increment = 2, limits = (0, 1024))
LCD4linux.MPMoonAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MPMoonSplit = ConfigYesNo(default = False)
LCD4linux.MPMoonColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="white")
LCD4linux.MPMoonShadow = ConfigYesNo(default = False)
LCD4linux.MPMoonFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPNetAtmo = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPNetAtmoLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPNetAtmoPos = ConfigSlider(default = 50,  increment = 2, limits = (0, 1024))
LCD4linux.MPNetAtmoAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MPNetAtmoSplit = ConfigYesNo(default = False)
LCD4linux.MPNetAtmoType = ConfigSelection(choices = NetatmoType, default="THCPN")
LCD4linux.MPNetAtmoType2 = ConfigSelection(choices = DirType, default="0")
LCD4linux.MPNetAtmoSize = ConfigSlider(default = 30,  increment = 1, limits = (10, 100))
LCD4linux.MPNetAtmoColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPNetAtmoShadow = ConfigYesNo(default = False)
LCD4linux.MPNetAtmoFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPNetAtmoCO2 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPNetAtmoCO2LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPNetAtmoCO2Size = ConfigSlider(default = 30,  increment = 1, limits = (5, 500))
LCD4linux.MPNetAtmoCO2Len = ConfigSlider(default = 200,  increment = 5, limits = (100, 1024))
LCD4linux.MPNetAtmoCO2Pos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.MPNetAtmoCO2Align = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MPNetAtmoCO2Split = ConfigYesNo(default = False)
LCD4linux.MPNetAtmoCO2Type = ConfigSelection(choices = CO2Type, default="1")
LCD4linux.MPNetAtmoIDX = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPNetAtmoIDXLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPNetAtmoIDXSize = ConfigSlider(default = 30,  increment = 1, limits = (5, 500))
LCD4linux.MPNetAtmoIDXLen = ConfigSlider(default = 200,  increment = 5, limits = (100, 1024))
LCD4linux.MPNetAtmoIDXPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.MPNetAtmoIDXAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MPNetAtmoIDXSplit = ConfigYesNo(default = False)
LCD4linux.MPNetAtmoIDXType = ConfigSelection(choices = CO2Type, default="1")
LCD4linux.MPBild = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPBildLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPBildFile = ConfigText(default="/tmp/lcd4linux.jpg", fixed_size=False, visible_width=50)
LCD4linux.MPBildSize = ConfigSlider(default = 240,  increment = 10, limits = (10, 1024))
LCD4linux.MPBildPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.MPBildAlign = ConfigSelection(choices = AlignType + [("9", _("full Screen"))], default="0")
LCD4linux.MPBildQuick = ConfigYesNo(default = False)
LCD4linux.MPBildTransp = ConfigYesNo(default = False)
LCD4linux.MPBild2 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPBild2LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPBild2File = ConfigText(default="/tmp/lcd4linux.jpg", fixed_size=False, visible_width=50)
LCD4linux.MPBild2Size = ConfigSlider(default = 240,  increment = 10, limits = (10, 1024))
LCD4linux.MPBild2Pos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.MPBild2Align = ConfigSelection(choices = AlignType + [("9", _("full Screen"))], default="0")
LCD4linux.MPBild2Quick = ConfigYesNo(default = False)
LCD4linux.MPBild2Transp = ConfigYesNo(default = False)
LCD4linux.MPText = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPTextLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPTextFile = ConfigText(default="/tmp/lcd4linux.txt", fixed_size=False, visible_width=50)
LCD4linux.MPTextSize = ConfigSlider(default = 32,  increment = 1, limits = (10, 300))
LCD4linux.MPTextFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPTextPos = ConfigSlider(default = 120,  increment = 2, limits = (0, 1024))
LCD4linux.MPTextAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MPTextShadow = ConfigYesNo(default = False)
LCD4linux.MPTextColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPTextBackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.MPCover = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPCoverLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPCoverPath1 = ConfigText(default="/tmp", fixed_size=False, visible_width=50)
LCD4linux.MPCoverPath2 = ConfigText(default="/tmp", fixed_size=False, visible_width=50)
LCD4linux.MPCoverFile = ConfigText(default="/tmp/lcd4linux.jpg", fixed_size=False, visible_width=50)
LCD4linux.MPCoverSize = ConfigSlider(default = 240,  increment = 10, limits = (10, 1024))
LCD4linux.MPCoverSizeH = ConfigSlider(default = 400,  increment = 10, limits = (10, 800))
LCD4linux.MPCoverPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.MPCoverAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MPCoverGoogle = ConfigSelection(choices = [("0", _("no")), ("1", _("yes")), ("2", _("yes except records"))], default="1")
LCD4linux.MPCoverTransp = ConfigYesNo(default = False)
LCD4linux.MPCoverPiconFirst = ConfigYesNo(default = True)
LCD4linux.MPOSCAM = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPOSCAMLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPOSCAMSize = ConfigSlider(default = 10,  increment = 1, limits = (9, 50))
LCD4linux.MPOSCAMPos = ConfigSlider(default = 20,  increment = 2, limits = (0, 1024))
LCD4linux.MPOSCAMAlign = ConfigSelection(choices = [("0", _("left")), ("2", _("right"))], default="0")
LCD4linux.MPOSCAMSplit = ConfigYesNo(default = False)
LCD4linux.MPOSCAMColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPOSCAMBackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="black")
LCD4linux.MPMail = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPMailLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPMailSize = ConfigSlider(default = 12,  increment = 1, limits = (5, 150))
LCD4linux.MPMailPos = ConfigSlider(default = 30,  increment = 2, limits = (0, 1024))
LCD4linux.MPMailAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MPMailSplit = ConfigYesNo(default = False)
LCD4linux.MPMailColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPMailBackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.MPMailKonto = ConfigSelection(choices = MailKonto, default="1")
LCD4linux.MPMailLines = ConfigSelectionNumber(1, 20, 1, default = 3)
LCD4linux.MPMailType = ConfigSelection(choices = MailType, default="A1")
LCD4linux.MPMailProzent = ConfigSelection(choices = ProzentType, default="50")
LCD4linux.MPMailShadow = ConfigYesNo(default = False)
LCD4linux.MPMailFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPIconBar = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPIconBarLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPIconBarSize = ConfigSlider(default = 20,  increment = 1, limits = (10, 150))
LCD4linux.MPIconBarPos = ConfigSlider(default = 120,  increment = 2, limits = (0, 1024))
LCD4linux.MPIconBarAlign = ConfigSelection(choices = AlignType, default="1")
LCD4linux.MPIconBarSplit = ConfigYesNo(default = False)
LCD4linux.MPIconBarType = ConfigSelection(choices = DirType, default="0")
LCD4linux.MPIconBarPopup = ConfigSelection(choices = [("0", _("off"))] + ScreenSet, default="0")
LCD4linux.MPIconBarPopupLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPSun = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPSunLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPSunSize = ConfigSlider(default = 20,  increment = 1, limits = (5, 150))
LCD4linux.MPSunPos = ConfigSlider(default = 20,  increment = 2, limits = (0, 1024))
LCD4linux.MPSunAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MPSunSplit = ConfigYesNo(default = False)
LCD4linux.MPSunColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPSunBackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.MPSunShadow = ConfigYesNo(default = False)
LCD4linux.MPSunFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPSunType = ConfigSelection(choices = DirType, default="2")
LCD4linux.MPFritz = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPFritzLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPFritzSize = ConfigSlider(default = 22,  increment = 1, limits = (10, 150))
LCD4linux.MPFritzPos = ConfigSlider(default = 130,  increment = 2, limits = (0, 1024))
LCD4linux.MPFritzAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MPFritzColor = ConfigSelection(choices = Farbe, default="yellow")
LCD4linux.MPFritzBackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.MPFritzType = ConfigSelection(choices = FritzType, default="TL")
LCD4linux.MPFritzPicSize = ConfigSlider(default = 100,  increment = 1, limits = (10, 800))
LCD4linux.MPFritzPicPos = ConfigSlider(default = 30,  increment = 2, limits = (0, 1024))
LCD4linux.MPFritzPicAlign = ConfigSlider(default = 0,  increment = 10, limits = (0, 1024))
LCD4linux.MPFritzShadow = ConfigYesNo(default = False)
LCD4linux.MPFritzFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPCal = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPCalLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPCalPos = ConfigSlider(default = 50,  increment = 2, limits = (0, 1024))
LCD4linux.MPCalAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MPCalSplit = ConfigYesNo(default = False)
LCD4linux.MPCalZoom = ConfigSlider(default = 10,  increment = 1, limits = (3, 50))
LCD4linux.MPCalType = ConfigSelection(choices = CalType, default="0A")
LCD4linux.MPCalTypeE = ConfigSelection(choices = CalTypeE, default="D2")
LCD4linux.MPCalColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPCalBackColor = ConfigSelection(choices = Farbe, default="gray")
LCD4linux.MPCalCaptionColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPCalLayout = ConfigSelection(choices = CalLayout, default="0")
LCD4linux.MPCalShadow = ConfigYesNo(default = False)
LCD4linux.MPCalFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPCalList = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPCalListLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPCalListSize = ConfigSlider(default = 12,  increment = 1, limits = (5, 150))
LCD4linux.MPCalListPos = ConfigSlider(default = 50,  increment = 2, limits = (0, 1024))
LCD4linux.MPCalListAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.MPCalListSplit = ConfigYesNo(default = False)
LCD4linux.MPCalListLines = ConfigSelectionNumber(1, 20, 1, default = 3)
LCD4linux.MPCalListProzent = ConfigSelection(choices = ProzentType, default="50")
LCD4linux.MPCalListType = ConfigSelection(choices = CalListType, default="C")
LCD4linux.MPCalListColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPCalListShadow = ConfigYesNo(default = False)
LCD4linux.MPCalListFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.MPBox1 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPBox1LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPBox1x1 = ConfigSlider(default = 10,  increment = 1, limits = (0, 1024))
LCD4linux.MPBox1y1 = ConfigSlider(default = 10,  increment = 1, limits = (0, 1024))
LCD4linux.MPBox1x2 = ConfigSlider(default = 200,  increment = 1, limits = (0, 1024))
LCD4linux.MPBox1y2 = ConfigSlider(default = 1,  increment = 1, limits = (0, 1024))
LCD4linux.MPBox1Color = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPBox1BackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.MPBox2 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPBox2LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPBox2x1 = ConfigSlider(default = 20,  increment = 1, limits = (0, 1024))
LCD4linux.MPBox2y1 = ConfigSlider(default = 20,  increment = 1, limits = (0, 1024))
LCD4linux.MPBox2x2 = ConfigSlider(default = 200,  increment = 1, limits = (0, 1024))
LCD4linux.MPBox2y2 = ConfigSlider(default = 1,  increment = 1, limits = (0, 1024))
LCD4linux.MPBox2Color = ConfigSelection(choices = Farbe, default="white")
LCD4linux.MPBox2BackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.MPRecording = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.MPRecordingLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.MPRecordingType = ConfigSelection(choices = [("1", _("Corner")), ("2", _("Picon"))], default="1")
LCD4linux.MPRecordingSize = ConfigSlider(default = 25,  increment = 1, limits = (10, 100))
LCD4linux.MPRecordingPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.MPRecordingAlign = ConfigSelection(choices = AlignType, default="2")
LCD4linux.MPRecordingSplit = ConfigYesNo(default = False)
LCD4linux.Standby = ConfigSelection(choices = [("0", _("off")), ("1", _("on"))], default="1")
LCD4linux.StandbyScreenMax = ConfigSelection(choices = ScreenUse, default="1")
LCD4linux.StandbyHelligkeit = ConfigSelectionNumber(0, 10, 1, default = 1)
LCD4linux.StandbyHelligkeit2 = ConfigSelectionNumber(0, 10, 1, default = 1)
LCD4linux.StandbyHelligkeit3 = ConfigSelectionNumber(0, 10, 1, default = 1)
LCD4linux.StandbyLCDoff = ConfigClock(default = int(begin) )
LCD4linux.StandbyLCDon = ConfigClock(default = int(begin) )
LCD4linux.StandbyLCDWEoff = ConfigClock(default = int(begin) )
LCD4linux.StandbyLCDWEon = ConfigClock(default = int(begin) )
LCD4linux.StandbyLCDBild1 = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.StandbyLCDBild2 = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.StandbyLCDBild3 = ConfigText(default="", fixed_size=False, visible_width=50)
LCD4linux.StandbyLCDColor1 = ConfigSelection(choices = Farbe, default="black")
LCD4linux.StandbyLCDColor2 = ConfigSelection(choices = Farbe, default="black")
LCD4linux.StandbyLCDColor3 = ConfigSelection(choices = Farbe, default="black")
LCD4linux.StandbyScreenTime = ConfigSelection(choices = [("0", _("off"))] + TimeSelect, default="0")
LCD4linux.StandbyScreenTime2 = ConfigSelection(choices = TimeSelect, default="1")
LCD4linux.StandbyScreenTime3 = ConfigSelection(choices = TimeSelect, default="1")
LCD4linux.StandbyScreenTime4 = ConfigSelection(choices = TimeSelect, default="1")
LCD4linux.StandbyScreenTime5 = ConfigSelection(choices = TimeSelect, default="1")
LCD4linux.StandbyScreenTime6 = ConfigSelection(choices = TimeSelect, default="1")
LCD4linux.StandbyScreenTime7 = ConfigSelection(choices = TimeSelect, default="1")
LCD4linux.StandbyScreenTime8 = ConfigSelection(choices = TimeSelect, default="1")
LCD4linux.StandbyScreenTime9 = ConfigSelection(choices = TimeSelect, default="1")
LCD4linux.StandbyClock = ConfigSelection(choices = ScreenSelect, default="1")
LCD4linux.StandbyClockLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyClockType = ConfigSelection(choices = ClockType, default="12")
LCD4linux.StandbyClockSpacing = ConfigSelectionNumber(0, 3, 1, default = 0)
LCD4linux.StandbyClockAnalog = ConfigSelectionNumber(1, 6, 1, default = 1)
LCD4linux.StandbyClockSize = ConfigSlider(default = 110,  increment = 2, limits = (10, 400))
LCD4linux.StandbyClockPos = ConfigSlider(default = 100,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyClockAlign = ConfigSelection(choices = AlignType, default="1")
LCD4linux.StandbyClockSplit = ConfigYesNo(default = False)
LCD4linux.StandbyClockColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.StandbyClockShadow = ConfigYesNo(default = False)
LCD4linux.StandbyClockFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.StandbyClock2 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyClock2LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyClock2Type = ConfigSelection(choices = ClockType, default="12")
LCD4linux.StandbyClock2Spacing = ConfigSelectionNumber(0, 3, 1, default = 0)
LCD4linux.StandbyClock2Analog = ConfigSelectionNumber(1, 6, 1, default = 1)
LCD4linux.StandbyClock2Size = ConfigSlider(default = 110,  increment = 2, limits = (10, 400))
LCD4linux.StandbyClock2Pos = ConfigSlider(default = 100,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyClock2Align = ConfigSelection(choices = AlignType, default="1")
LCD4linux.StandbyClock2Split = ConfigYesNo(default = False)
LCD4linux.StandbyClock2Color = ConfigSelection(choices = Farbe, default="white")
LCD4linux.StandbyClock2Shadow = ConfigYesNo(default = False)
LCD4linux.StandbyClock2Font = ConfigSelection(choices = FontType, default="0")
LCD4linux.StandbyTimer = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyTimerLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyTimerSize = ConfigSlider(default = 22,  increment = 1, limits = (10, 150))
LCD4linux.StandbyTimerLines = ConfigSelectionNumber(1, 20, 1, default = 1)
LCD4linux.StandbyTimerType = ConfigSelection(choices = [("0", _("use lead-time")), ("1", _("only use Timer"))], default="0")
LCD4linux.StandbyTimerPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyTimerAlign = ConfigSelection(choices = [("0", _("left")), ("2", _("half right"))], default="0")
LCD4linux.StandbyTimerSplit = ConfigYesNo(default = False)
LCD4linux.StandbyTimerColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.StandbyTimerShadow = ConfigYesNo(default = False)
LCD4linux.StandbyTimerFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.StandbyTuner = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyTunerLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyTunerSize = ConfigSlider(default = 22,  increment = 1, limits = (10, 150))
LCD4linux.StandbyTunerPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyTunerAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.StandbyTunerSplit = ConfigYesNo(default = False)
LCD4linux.StandbyTunerType = ConfigSelection(choices = DirType, default="0")
LCD4linux.StandbyTunerActive = ConfigYesNo(default = False)
LCD4linux.StandbyTunerFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.StandbyInfo = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyInfoLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyInfoSensor = ConfigSelection(choices = InfoSensor, default="0")
LCD4linux.StandbyInfoCPU = ConfigSelection(choices = InfoCPU, default="0")
LCD4linux.StandbyInfoSize = ConfigSlider(default = 20,  increment = 1, limits = (10, 150))
LCD4linux.StandbyInfoPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyInfoAlign = ConfigSelection(choices = AlignType, default="1")
LCD4linux.StandbyInfoSplit = ConfigYesNo(default = False)
LCD4linux.StandbyInfoLines = ConfigSelectionNumber(1, 9, 1, default = 1)
LCD4linux.StandbyInfoColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.StandbyInfoShadow = ConfigYesNo(default = False)
LCD4linux.StandbyInfoFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.StandbyPing = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyPingLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyPingSize = ConfigSlider(default = 15,  increment = 2, limits = (10, 100))
LCD4linux.StandbyPingPos = ConfigSlider(default = 20,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyPingAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.StandbyPingSplit = ConfigYesNo(default = False)
LCD4linux.StandbyPingColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.StandbyPingShadow = ConfigYesNo(default = False)
LCD4linux.StandbyPingFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.StandbyPingShow = ConfigSelection(choices = [("0", _("Online+Offline")), ("1", _("Online")), ("2", _("Offline"))], default="0")
LCD4linux.StandbyPingType = ConfigSelection(choices = DirType, default="0")
LCD4linux.StandbyPingTimeout = ConfigSlider(default = 50,  increment = 5, limits = (5, 1000))
LCD4linux.StandbyPingName1 = ConfigText(default="Internet:www.google.de", fixed_size=False)
LCD4linux.StandbyPingName2 = ConfigText(default="", fixed_size=False)
LCD4linux.StandbyPingName3 = ConfigText(default="", fixed_size=False)
LCD4linux.StandbyPingName4 = ConfigText(default="", fixed_size=False)
LCD4linux.StandbyPingName5 = ConfigText(default="", fixed_size=False)
LCD4linux.StandbyDev = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyDevLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyDevSize = ConfigSlider(default = 15,  increment = 2, limits = (10, 300))
LCD4linux.StandbyDevPos = ConfigSlider(default = 20,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyDevAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.StandbyDevSplit = ConfigYesNo(default = False)
LCD4linux.StandbyDevColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.StandbyDevShadow = ConfigYesNo(default = False)
LCD4linux.StandbyDevFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.StandbyDevType = ConfigSelection(choices = DirType, default="0")
LCD4linux.StandbyDevExtra = ConfigSelection(choices = [("0", _("no")), ("RAM", _("Memory"))], default="RAM")
LCD4linux.StandbyDevName1 = ConfigText(default="/media/hdd", fixed_size=False)
LCD4linux.StandbyDevName2 = ConfigText(default="", fixed_size=False)
LCD4linux.StandbyDevName3 = ConfigText(default="", fixed_size=False)
LCD4linux.StandbyDevName4 = ConfigText(default="", fixed_size=False)
LCD4linux.StandbyDevName5 = ConfigText(default="", fixed_size=False)
LCD4linux.StandbyHdd = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyHddLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyHddSize = ConfigSlider(default = 32,  increment = 1, limits = (10, 150))
LCD4linux.StandbyHddPos = ConfigSlider(default = 120,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyHddAlign = ConfigSelection(choices = AlignType, default="1")
LCD4linux.StandbyHddSplit = ConfigYesNo(default = False)
LCD4linux.StandbyHddType = ConfigSelection(choices = HddType, default="0")
LCD4linux.StandbyWetter = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyWetterLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyWetterPos = ConfigSlider(default = 50,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyWetterAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.StandbyWetterSplit = ConfigYesNo(default = False)
LCD4linux.StandbyWetterZoom = ConfigSlider(default = 10,  increment = 1, limits = (7, 60))
LCD4linux.StandbyWetterType = ConfigSelection(choices = WetterType, default="1")
LCD4linux.StandbyWetterColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.StandbyWetterShadow = ConfigYesNo(default = False)
LCD4linux.StandbyWetterFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.StandbyWetter2 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyWetter2LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyWetter2Pos = ConfigSlider(default = 50,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyWetter2Align = ConfigSelection(choices = AlignType, default="0")
LCD4linux.StandbyWetter2Split = ConfigYesNo(default = False)
LCD4linux.StandbyWetter2Zoom = ConfigSlider(default = 10,  increment = 1, limits = (7, 60))
LCD4linux.StandbyWetter2Type = ConfigSelection(choices = WetterType, default="1")
LCD4linux.StandbyWetter2Color = ConfigSelection(choices = Farbe, default="white")
LCD4linux.StandbyWetter2Shadow = ConfigYesNo(default = False)
LCD4linux.StandbyWetter2Font = ConfigSelection(choices = FontType, default="0")
LCD4linux.StandbyMeteo = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyMeteoLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyMeteoPos = ConfigSlider(default = 50,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyMeteoAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.StandbyMeteoSplit = ConfigYesNo(default = False)
LCD4linux.StandbyMeteoZoom = ConfigSlider(default = 10,  increment = 1, limits = (7, 60))
LCD4linux.StandbyMeteoType = ConfigSelection(choices = MeteoType, default="1")
LCD4linux.StandbyMeteoColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.StandbyMoon = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyMoonLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyMoonSize = ConfigSlider(default = 60,  increment = 2, limits = (10, 300))
LCD4linux.StandbyMoonPos = ConfigSlider(default = 10,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyMoonAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.StandbyMoonSplit = ConfigYesNo(default = False)
LCD4linux.StandbyMoonColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="white")
LCD4linux.StandbyMoonShadow = ConfigYesNo(default = False)
LCD4linux.StandbyMoonFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.StandbyNetAtmo = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyNetAtmoLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyNetAtmoPos = ConfigSlider(default = 50,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyNetAtmoAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.StandbyNetAtmoSplit = ConfigYesNo(default = False)
LCD4linux.StandbyNetAtmoType = ConfigSelection(choices = NetatmoType, default="THCPN")
LCD4linux.StandbyNetAtmoType2 = ConfigSelection(choices = DirType, default="0")
LCD4linux.StandbyNetAtmoSize = ConfigSlider(default = 30,  increment = 1, limits = (10, 100))
LCD4linux.StandbyNetAtmoColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.StandbyNetAtmoShadow = ConfigYesNo(default = False)
LCD4linux.StandbyNetAtmoFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.StandbyNetAtmoCO2 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyNetAtmoCO2LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyNetAtmoCO2Size = ConfigSlider(default = 30,  increment = 1, limits = (5, 500))
LCD4linux.StandbyNetAtmoCO2Len = ConfigSlider(default = 200,  increment = 5, limits = (100, 1024))
LCD4linux.StandbyNetAtmoCO2Pos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyNetAtmoCO2Align = ConfigSelection(choices = AlignType, default="0")
LCD4linux.StandbyNetAtmoCO2Split = ConfigYesNo(default = False)
LCD4linux.StandbyNetAtmoCO2Type = ConfigSelection(choices = CO2Type, default="1")
LCD4linux.StandbyNetAtmoIDX = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyNetAtmoIDXLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyNetAtmoIDXSize = ConfigSlider(default = 30,  increment = 1, limits = (5, 500))
LCD4linux.StandbyNetAtmoIDXLen = ConfigSlider(default = 200,  increment = 5, limits = (100, 1024))
LCD4linux.StandbyNetAtmoIDXPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyNetAtmoIDXAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.StandbyNetAtmoIDXSplit = ConfigYesNo(default = False)
LCD4linux.StandbyNetAtmoIDXType = ConfigSelection(choices = CO2Type, default="1")
LCD4linux.StandbyOSCAM = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyOSCAMLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyOSCAMSize = ConfigSlider(default = 10,  increment = 1, limits = (9, 50))
LCD4linux.StandbyOSCAMPos = ConfigSlider(default = 20,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyOSCAMAlign = ConfigSelection(choices = [("0", _("left")), ("2", _("right"))], default="0")
LCD4linux.StandbyOSCAMSplit = ConfigYesNo(default = False)
LCD4linux.StandbyOSCAMColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.StandbyOSCAMBackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="black")
LCD4linux.StandbyText = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyTextLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyTextFile = ConfigText(default="/tmp/lcd4linux.txt", fixed_size=False, visible_width=50)
LCD4linux.StandbyTextSize = ConfigSlider(default = 32,  increment = 1, limits = (10, 300))
LCD4linux.StandbyTextFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.StandbyTextAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.StandbyTextPos = ConfigSlider(default = 120,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyTextShadow = ConfigYesNo(default = False)
LCD4linux.StandbyTextColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.StandbyTextBackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.StandbyText2 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyText2LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyText2File = ConfigText(default="/tmp/lcd4linux.txt", fixed_size=False, visible_width=50)
LCD4linux.StandbyText2Size = ConfigSlider(default = 32,  increment = 1, limits = (10, 300))
LCD4linux.StandbyText2Font = ConfigSelection(choices = FontType, default="0")
LCD4linux.StandbyText2Align = ConfigSelection(choices = AlignType, default="0")
LCD4linux.StandbyText2Pos = ConfigSlider(default = 120,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyText2Shadow = ConfigYesNo(default = False)
LCD4linux.StandbyText2Color = ConfigSelection(choices = Farbe, default="white")
LCD4linux.StandbyText2BackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.StandbyText3 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyText3LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyText3File = ConfigText(default="/tmp/lcd4linux.txt", fixed_size=False, visible_width=50)
LCD4linux.StandbyText3Size = ConfigSlider(default = 32,  increment = 1, limits = (10, 300))
LCD4linux.StandbyText3Font = ConfigSelection(choices = FontType, default="0")
LCD4linux.StandbyText3Align = ConfigSelection(choices = AlignType, default="0")
LCD4linux.StandbyText3Pos = ConfigSlider(default = 120,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyText3Shadow = ConfigYesNo(default = False)
LCD4linux.StandbyText3Color = ConfigSelection(choices = Farbe, default="white")
LCD4linux.StandbyText3BackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.StandbyHTTP = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyHTTPLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyHTTPURL = ConfigText(default="http://", fixed_size=False, visible_width=50)
LCD4linux.StandbyHTTPSize = ConfigSlider(default = 20,  increment = 1, limits = (10, 300))
LCD4linux.StandbyHTTPPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyHTTPAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.StandbyHTTPColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.StandbyHTTPBackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.StandbyHTTPShadow = ConfigYesNo(default = False)
LCD4linux.StandbyHTTPFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.StandbyWWW1 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyWWW1LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyWWW1Size = ConfigSlider(default = 200,  increment = 1, limits = (50, 1024))
LCD4linux.StandbyWWW1Pos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyWWW1Align = ConfigSelection(choices = AlignType, default="0")
LCD4linux.StandbyWWW1url = ConfigText(default="http://", fixed_size=False, visible_width=50)
LCD4linux.StandbyWWW1w = ConfigSlider(default = 800,  increment = 50, limits = (600, 2000))
LCD4linux.StandbyWWW1h = ConfigSlider(default = 600,  increment = 50, limits = (100, 2000))
LCD4linux.StandbyWWW1CutX = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyWWW1CutY = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyWWW1CutW = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyWWW1CutH = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyBild = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyBildLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyBildFile = ConfigText(default="/tmp/lcd4linux.jpg", fixed_size=False, visible_width=50)
LCD4linux.StandbyBildSize = ConfigSlider(default = 240,  increment = 10, limits = (10, 1024))
LCD4linux.StandbyBildPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyBildAlign = ConfigSelection(choices = AlignType + [("9", _("full Screen"))], default="0")
LCD4linux.StandbyBildQuick = ConfigYesNo(default = False)
LCD4linux.StandbyBildTransp = ConfigYesNo(default = False)
LCD4linux.StandbyBild2 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyBild2LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyBild2File = ConfigText(default="/tmp/lcd4linux.jpg", fixed_size=False, visible_width=50)
LCD4linux.StandbyBild2Size = ConfigSlider(default = 240,  increment = 10, limits = (10, 1024))
LCD4linux.StandbyBild2Pos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyBild2Align = ConfigSelection(choices = AlignType + [("9", _("full Screen"))], default="0")
LCD4linux.StandbyBild2Quick = ConfigYesNo(default = False)
LCD4linux.StandbyBild2Transp = ConfigYesNo(default = False)
LCD4linux.StandbyBild3 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyBild3LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyBild3File = ConfigText(default="/tmp/lcd4linux.jpg", fixed_size=False, visible_width=50)
LCD4linux.StandbyBild3Size = ConfigSlider(default = 240,  increment = 10, limits = (10, 1024))
LCD4linux.StandbyBild3Pos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyBild3Align = ConfigSelection(choices = AlignType + [("9", _("full Screen"))], default="0")
LCD4linux.StandbyBild3Quick = ConfigYesNo(default = False)
LCD4linux.StandbyBild3Transp = ConfigYesNo(default = False)
LCD4linux.StandbyBild4 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyBild4LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyBild4File = ConfigText(default="/tmp/lcd4linux.jpg", fixed_size=False, visible_width=50)
LCD4linux.StandbyBild4Size = ConfigSlider(default = 240,  increment = 10, limits = (10, 1024))
LCD4linux.StandbyBild4Pos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyBild4Align = ConfigSelection(choices = AlignType + [("9", _("full Screen"))], default="0")
LCD4linux.StandbyBild4Quick = ConfigYesNo(default = False)
LCD4linux.StandbyBild4Transp = ConfigYesNo(default = False)
LCD4linux.StandbyMail = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyMailLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyMailSize = ConfigSlider(default = 12,  increment = 1, limits = (5, 150))
LCD4linux.StandbyMailPos = ConfigSlider(default = 30,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyMailAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.StandbyMailSplit = ConfigYesNo(default = False)
LCD4linux.StandbyMailColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.StandbyMailBackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.StandbyMailKonto = ConfigSelection(choices = MailKonto, default="1")
LCD4linux.StandbyMailLines = ConfigSelectionNumber(1, 20, 1, default = 3)
LCD4linux.StandbyMailType = ConfigSelection(choices = MailType, default="A1")
LCD4linux.StandbyMailProzent = ConfigSelection(choices = ProzentType, default="50")
LCD4linux.StandbyMailShadow = ConfigYesNo(default = False)
LCD4linux.StandbyMailFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.StandbyIconBar = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyIconBarLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyIconBarSize = ConfigSlider(default = 20,  increment = 1, limits = (10, 150))
LCD4linux.StandbyIconBarPos = ConfigSlider(default = 120,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyIconBarAlign = ConfigSelection(choices = AlignType, default="1")
LCD4linux.StandbyIconBarSplit = ConfigYesNo(default = False)
LCD4linux.StandbyIconBarType = ConfigSelection(choices = DirType, default="0")
LCD4linux.StandbyIconBarPopup = ConfigSelection(choices = [("0", _("off"))] + ScreenSet, default="0")
LCD4linux.StandbyIconBarPopupLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbySun = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbySunLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbySunSize = ConfigSlider(default = 20,  increment = 1, limits = (5, 150))
LCD4linux.StandbySunPos = ConfigSlider(default = 20,  increment = 2, limits = (0, 1024))
LCD4linux.StandbySunAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.StandbySunSplit = ConfigYesNo(default = False)
LCD4linux.StandbySunColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.StandbySunBackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.StandbySunShadow = ConfigYesNo(default = False)
LCD4linux.StandbySunFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.StandbySunType = ConfigSelection(choices = DirType, default="2")
LCD4linux.StandbyFritz = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyFritzLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyFritzSize = ConfigSlider(default = 22,  increment = 1, limits = (10, 150))
LCD4linux.StandbyFritzPos = ConfigSlider(default = 130,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyFritzAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.StandbyFritzColor = ConfigSelection(choices = Farbe, default="yellow")
LCD4linux.StandbyFritzBackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.StandbyFritzType = ConfigSelection(choices = FritzType, default="TL")
LCD4linux.StandbyFritzPicSize = ConfigSlider(default = 100,  increment = 1, limits = (10, 800))
LCD4linux.StandbyFritzPicPos = ConfigSlider(default = 30,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyFritzPicAlign = ConfigSlider(default = 0,  increment = 10, limits = (0, 1024))
LCD4linux.StandbyFritzShadow = ConfigYesNo(default = False)
LCD4linux.StandbyFritzFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.StandbyCal = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyCalLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyCalPos = ConfigSlider(default = 50,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyCalAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.StandbyCalSplit = ConfigYesNo(default = False)
LCD4linux.StandbyCalZoom = ConfigSlider(default = 10,  increment = 1, limits = (3, 50))
LCD4linux.StandbyCalType = ConfigSelection(choices = CalType, default="0A")
LCD4linux.StandbyCalTypeE = ConfigSelection(choices = CalTypeE, default="D2")
LCD4linux.StandbyCalLayout = ConfigSelection(choices = CalLayout, default="0")
LCD4linux.StandbyCalColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.StandbyCalBackColor = ConfigSelection(choices = Farbe, default="gray")
LCD4linux.StandbyCalCaptionColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.StandbyCalShadow = ConfigYesNo(default = False)
LCD4linux.StandbyCalFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.StandbyCalList = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyCalListLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyCalListSize = ConfigSlider(default = 12,  increment = 1, limits = (5, 150))
LCD4linux.StandbyCalListPos = ConfigSlider(default = 50,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyCalListAlign = ConfigSelection(choices = AlignType, default="0")
LCD4linux.StandbyCalListSplit = ConfigYesNo(default = False)
LCD4linux.StandbyCalListLines = ConfigSelectionNumber(1, 20, 1, default = 3)
LCD4linux.StandbyCalListProzent = ConfigSelection(choices = ProzentType, default="50")
LCD4linux.StandbyCalListType = ConfigSelection(choices = CalListType, default="C")
LCD4linux.StandbyCalListColor = ConfigSelection(choices = Farbe, default="white")
LCD4linux.StandbyCalListShadow = ConfigYesNo(default = False)
LCD4linux.StandbyCalListFont = ConfigSelection(choices = FontType, default="0")
LCD4linux.StandbyBox1 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyBox1LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyBox1x1 = ConfigSlider(default = 10,  increment = 1, limits = (0, 1024))
LCD4linux.StandbyBox1y1 = ConfigSlider(default = 10,  increment = 1, limits = (0, 1024))
LCD4linux.StandbyBox1x2 = ConfigSlider(default = 200,  increment = 1, limits = (0, 1024))
LCD4linux.StandbyBox1y2 = ConfigSlider(default = 1,  increment = 1, limits = (0, 1024))
LCD4linux.StandbyBox1Color = ConfigSelection(choices = Farbe, default="white")
LCD4linux.StandbyBox1BackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.StandbyBox2 = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyBox2LCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyBox2x1 = ConfigSlider(default = 20,  increment = 1, limits = (0, 1024))
LCD4linux.StandbyBox2y1 = ConfigSlider(default = 20,  increment = 1, limits = (0, 1024))
LCD4linux.StandbyBox2x2 = ConfigSlider(default = 200,  increment = 1, limits = (0, 1024))
LCD4linux.StandbyBox2y2 = ConfigSlider(default = 1,  increment = 1, limits = (0, 1024))
LCD4linux.StandbyBox2Color = ConfigSelection(choices = Farbe, default="white")
LCD4linux.StandbyBox2BackColor = ConfigSelection(choices = [("0", _("off"))] + Farbe, default="0")
LCD4linux.StandbyRecording = ConfigSelection(choices = ScreenSelect, default="0")
LCD4linux.StandbyRecordingLCD = ConfigSelection(choices = LCDSelect, default="1")
LCD4linux.StandbyRecordingType = ConfigSelection(choices = [("1", _("Corner")), ("2", _("Picon"))], default="1")
LCD4linux.StandbyRecordingSize = ConfigSlider(default = 25,  increment = 1, limits = (10, 100))
LCD4linux.StandbyRecordingPos = ConfigSlider(default = 0,  increment = 2, limits = (0, 1024))
LCD4linux.StandbyRecordingAlign = ConfigSelection(choices = AlignType, default="2")
LCD4linux.StandbyRecordingSplit = ConfigYesNo(default = False)

class MyTimer: # only for debug
	import traceback
	def __init__(self):
		print "L4L create timer at:"
		traceback.print_stack(limit=2)
		self.timer = eTimer()
		print "L4L created timer", self.timer
	def __del__(self):
		print "L4L destruct timer", self.timer
		traceback.print_stack(limit=2)
		del self.timer
	def start(self, msecs, singleShot=False):
		print "L4L start timer", msecs, singleShot, self.timer
		traceback.print_stack(limit=2)
		self.timer.start(msecs, singleShot)
	def	startLongTimer(self, secs):
		print "L4L start longtimer", secs, self.timer
		traceback.print_stack(limit=2)
		self.timer.startLongTimer(secs)
	def stop(self):
		print "L4L stopped timer", self.timer
		traceback.print_stack(limit=2)
		self.timer.stop()
	def getCallback(self):
		return self.timer.callback
	callback = property(getCallback)

def Code_utf8(wert):
	wert = wert.replace('\xc2\x86', '').replace('\xc2\x87', '').decode("utf-8", "ignore").encode("utf-8") or ""
	return codecs.decode(wert, 'UTF-8')

def L4log(nfo,wert=""):
	if LCD4linux.EnableEventLog.value != "0":
		print "[LCD4linux]",nfo,wert
		if LCD4linux.EnableEventLog.value != "3":
			try:
				f = open("/tmp/L4log.txt","a")
				try:
					f.write(strftime("%H:%M:%S") + " %s %s\r\n" % (str(nfo), str(wert)))
				finally:
					f.close()
			except IOError:
				print "[LCD4linux]",strftime("%H:%M:%S"),"Logging-Error"

def L4logE(nfo,wert=""):
	if LCD4linux.EnableEventLog.value == "2":
		L4log(nfo,wert)

def GetBox():
	B = ""
	if os.path.exists("/proc/stb/info/model"):
		f = open("/proc/stb/info/model")
		B = f.readline()
		f.close()
		L4logE("Boxtype",B)
	return B

def setConfigMode(w):
	global ConfigMode
	ConfigMode = w
def setConfigStandby(w):
	global ConfigStandby
	ConfigStandby = w
def setisMediaPlayer(w):
	global isMediaPlayer
	isMediaPlayer = w
def setScreenActive(w,lcd=""):
	global ScreenActive
	global ScreenTime
	if lcd=="":
		if w=="0":
			ScreenActive[-3:]=["","",""]
			L4LElist.setHold(False)
		else:
			ScreenActive[0] = w
	else:
		if w=="0":
			w=""
		ScreenActive[int(lcd)] = w
	LCD4linux.ScreenActive.value = ScreenActive[0]
	ScreenTime=0
def setLCDon(w):
	global LCDon
	LCDon = w
def setSaveEventListChanged(w):
	global SaveEventListChanged
	SaveEventListChanged = w
def execexec(w):
	exec(w)
def getScreenActive(All=False):
	if All:
		return ScreenActive
	else:
		return ScreenActive[0]
def getConfigStandby():
	return ConfigStandby
def getConfigMode():
	return ConfigMode
def getisMediaPlayer():
	return isMediaPlayer
def getTMP():
	return TMP
def getTMPL():
	return TMPL
def getINFO():
	return INFO
def getSaveEventListChanged():
	return SaveEventListChanged
def setPopText(w):
	global PopText
	PopText[0] = Code_utf8(_(strftime("%A"))) + strftime(" %H:%M")
	PopText[1] = w
def resetWetter():
	global wwwWetter
	global PICwetter
	wwwWetter = ["",""]
	PICwetter=[None,None]
def resetCal():
	global PICcal
	PICcal=None

def getSA(w):
	return ScreenActive[0] if ScreenActive[w]=="" else ScreenActive[w]

def rmFile(fn):
	if os.path.isfile(fn):
		try:
			L4logE("delete",fn)
			os.remove(fn)
		except:
			L4logE("Error delete",fn)

def rmFiles(fn):
	try:
		fl=glob.glob(fn)
		L4logE("delete*",fn)
		for f in fl:
			os.remove(f)
	except:
		L4logE("Error delete*",fn)

def getTimeDiff():
	offset = timezone if (localtime().tm_isdst == 0) else altzone
	return offset / -3600                                                   

def getTimeDiffUTC():
	t=datetime.now() - datetime.utcnow()
	return int(t.days*24+round(t.seconds/3600.0))

def getTimeDiffUTC2():
	is_dst = daylight and localtime().tm_isdst > 0
	return -((altzone if is_dst else timezone)/3600)

def ConfTime(F,W):
	try:
		if os.path.exists(LCD4config) and W != [6,0]:
			fconfig = open(LCD4config,"r")
			if f.read().find("config."+F) == -1:
				L4log("write alternate TimeConfig "+F,W)
				f = open(LCD4config,"a")
				f.write("config.%s=%d:%d\n" % (F,W[0],W[1]))
				f.close()
			fconfig.close()
	except:
		L4log("Errot: write alternate TimeConfig "+F,W)

def ScaleGtoR(PROZ):
	if PROZ < 50:
		R=max((255*PROZ)/50,0)
		G=255
	else:
		R=255
		G=max((255*(100-PROZ))/50,0)
	B=0
	return "#%02x%02x%02x" % (R,G,B)

def ICSdownloads():
	global ICS
	global ICSlist
	global ICSdownrun
	L4logE("ICSdownloads...",len(ICSlist))
	if len(ICSlist)==0 and LCD4linux.CalPlanerFS.value == False:
		return
	ICSdownrun = True
	ICS.clear()
	if LCD4linux.CalPlanerFS.value == True:
		try:
			from Plugins.Extensions.PlanerFS.PFSl4l import l4l_export
			liste=l4l_export("2").planerfs_liste
			PlanerFSok = True
			L4logE("PlanerFS registered")
		except:
			PlanerFSok = False
			L4logE("PlanerFS not registered")

		if PlanerFSok == True:
			for Icomp in liste:
				DT=Icomp[0]
				L4logE(Icomp)
				D = "%04d-%02d-%02d"  % (DT.year,DT.month,DT.day)
				if Icomp[4] == (0,0):
					dateT = date(DT.year,DT.month,DT.day)
				else:
					dateT = DT
				if Icomp[6] == 0:
					dateS = Code_utf8(Icomp[1])
				else:
					dateS = "%s (%d)" % (Code_utf8(Icomp[1]),Icomp[6])
				inew=[dateS,dateT,4]
				Doppel = False
				if ICS.get(D,None) is None:
					ICS[D]=[]
				else:
					for ii in ICS[D]:
						if ii[:2] == inew[:2]:
							Doppel = True
							L4logE("ICS ignore",inew)
				if Doppel == False:
					ICS[D].append(inew)
					L4logE(D,inew)

	import icalendar
	for name in ICSlist:
		L4log("ICS read Col",name[1])
		try:
			gcal = icalendar.Calendar().from_string(name[0])
			L4log("use iCal 2.x")
		except:
			try:
				gcal = icalendar.Calendar().from_ical(name[0])
				L4log("use iCal 3.x")
			except:
				from traceback import format_exc
				L4log("Error: ICS not readable!",format_exc() )
				continue
		try:
			for Icomp in gcal.walk("VEVENT"):
				if Icomp.name == "VEVENT":
					L4logE(Icomp["dtstart"],Icomp.get('summary'))
					rrule=str(Icomp.get("rrule",""))
					if "YEARLY" in rrule:
						dt=str(Icomp.decoded("dtstart"))
#						L4log(dt, date(datetime.now().year, int(dt[5:7]),int(dt[8:10])))
						Icomp.set('dtstart', date(datetime.now().year,int(dt[5:7]),int(dt[8:10])))
					today=date.today()
					WEEKLY = []
					if "WEEKLY" in rrule:
						for i in range(1,5):
							WEEKLY.append(Icomp.decoded("dtstart") + timedelta(i*7))
					nextmonth=today + timedelta(calendar.mdays[today.month]) # 2012-01-23
					nextmonth2=today + timedelta(calendar.mdays[today.month]-3) # save Month+1 if days to long
					DTstart = str(Icomp.decoded("dtstart"))
					if strftime("%Y-%m") == DTstart[:7] or nextmonth.strftime("%Y-%m") == DTstart[:7] or nextmonth2.strftime("%Y-%m") == DTstart[:7]:
						D = DTstart[:10]
						inew=[Code_utf8(Icomp.get('summary')),Icomp.decoded("dtstart"),name[1]]
						Doppel = False
						if ICS.get(D,None) is None:
							ICS[D]=[]
						else:
							for ii in ICS[D]:
								if ii[:2] == inew[:2]:
									Doppel = True
									L4log("ICS ignore",inew)
						if Doppel == False:
							ICS[D].append(inew)
							L4log(D,inew)
							for w in WEEKLY:
								D = str(w)[:10]
								if ICS.get(D,None) is None:
									ICS[D]=[]
								ICS[D].append([inew[0],w,inew[2]])
								L4log("weekly",w)
		except:
			from traceback import format_exc
			L4log("Error ICS",name)
			L4log("Error:",format_exc() )
			try:
				open(CrashFile,"w").write(format_exc())
			except:
				pass
	ICSlist = []
	L4logE("ICS laenge",len(ICS))
	ICSdownrun = False

def getResolution(t,r):
	if t[:1] == "5":
		ttt = LCD4linux.xmlLCDType.value.split("x")
		MAX_W,MAX_H = int(ttt[0]),int(ttt[1])
	elif t[1:] == "1":
		MAX_W,MAX_H = 320,240
	elif t[1:] == "2":
		MAX_W,MAX_H = 240,320
	elif t[1:] in ["3","4","5","10"]:
		MAX_W,MAX_H = 800,480
	elif t[1:] in ["6","9","11","12"]:
		MAX_W,MAX_H = 800,600
	elif t[1:] in ["7","8","13"]:
		MAX_W,MAX_H = 1024,600
	elif t[1:] == "17":
		MAX_W,MAX_H = 220,176
	elif t[1:] == "18":
		MAX_W,MAX_H = 255,64
	elif t[1:] == "30":
		MAX_W,MAX_H = 400,240
	elif t[1:] == "20":
		MAX_W,MAX_H = LCD4linux.SizeW.value,LCD4linux.SizeH.value 
	if r in ["90","270"]:
		MAX_W,MAX_H = MAX_H,MAX_W
	return MAX_W,MAX_H

def OSDclose():
	global OSDon
	OSDon = 0
	L4log("Screen close")
	rmFile("%sdpfgrab.jpg" % TMPL)
	return

def replacement_Screen_show(self):
	global OSDon
	global OSDtimer
	if LCD4linux.OSD.value != "0":
		L4log("Skin", self.skinName)
		doSkinOpen = True
		if len(self.skinName[0])>1:
			for s in self.skinName:
				if s in OSDdontskin:
					doSkinOpen = False
		else:
			if self.skinName in OSDdontskin:
				doSkinOpen = False	
		if doSkinOpen and OSDtimer >= 0:
			if "Title" in self:
				ib = self["Title"].getText()
				L4log("Screen", ib)
#			print "[LCD4linux] Screen", ib
				if ib not in OSDdontshow:
					L4log("Open Screen:"+ str(ib), "Skin:"+ str(self.skinName))
					OSDon = 3
					self.onClose.append(OSDclose)
				else:
					if OSDon != 1:
						OSDon = 0
			else:
				L4log("Open Screen no Title, Skin:", self.skinName)
				OSDon = 3
				self.onClose.append(OSDclose)
		else:
			if OSDon != 1:
				OSDon = 0
	Screen.show_old(self)

Screen.show_old = Screen.show
Screen.show = replacement_Screen_show

def find_dev(Anzahl, idVendor, idProduct):
	gefunden = False
	if os.path.isfile("/proc/bus/usb/devices"):
		i = open("/proc/bus/usb/devices", "r").read().lower()
		pos = i.find("vendor=%04x prodid=%04x" % (idVendor,idProduct))
#		print "[LCD4linux] find",pos, Anzahl
		if pos > 0:
			if Anzahl == 2:
				pos = i.find("vendor=%04x prodid=%04x" % (idVendor,idProduct),pos+10)
#				print "[LCD4linux] find2",pos
				if pos > 0:
					gefunden = True
			else:
				gefunden = True
	elif USBok == True:
		try:
			if len(usb.core.find(idVendor=idVendor, idProduct=idProduct, find_all=True)) >= Anzahl:
				L4logE("usb.core find")
				gefunden = True
		except:
			L4log("Error usb.core find")
	L4log("%d. Vendor=%04x ProdID=%04x" % (Anzahl,idVendor,idProduct), gefunden)
	return gefunden
	
def find_dev2(idVendor, idProduct, idVendor2, idProduct2):
	gefunden = False
	if find_dev(2,idVendor, idProduct) or find_dev(2,idVendor2, idProduct2) or (find_dev(1,idVendor, idProduct) and find_dev(1,idVendor2, idProduct2)):
		gefunden = True
	L4log("Vendor=%04x ProdID=%04x or Vendor=%04x ProdID=%04x" % (idVendor,idProduct,idVendor2,idProduct2), gefunden)
	return gefunden

# get picon path
def getpiconres(x, y, full, picon, P2, P2A, P2C):
	if len(P2C) < 3:
		return ""
	PD=os.path.join(P2C,picon)
	L4logE("get Picon",PD)
	if os.path.isdir(P2C):
		if not os.path.isfile(PD):
			L4log("Resize Picon")
			PD = ""
			PIC = []
			PIC.append(os.path.join(P2,picon))
			if len(P2A) > 3:
				PIC.append(os.path.join(P2A,picon))
			fields = picon.split("_", 3)
			if len(fields) > 2 and fields[2] not in ["1","2"]:
				fields[2] = "1"
				picon = "_".join(fields)
				PIC.append(os.path.join(P2,picon))
				if len(P2A) > 3:
					PIC.append(os.path.join(P2A,picon))
			for Pic in PIC:
				if os.path.isfile(Pic):
					PD=Pic
					break
			L4logE("read Picon",PD)
			if PD != "":
				try:
					pil_image = Image.open(PD)
					if LCD4linux.PiconTransparenz.value == "2":
						pil_image = pil_image.convert("RGBA")
					xx,yy = pil_image.size
					if full == False:
						y=int(float(x)/xx*yy)
					if LCD4linux.BilderQuality.value == "0":
						pil_image = pil_image.resize((x, y))
					else:
						pil_image = pil_image.resize((x, y), Image.ANTIALIAS)
					s = os.statvfs(P2C)
					if (s.f_bsize * s.f_bavail / 1024) < 100:
						L4log("Error: Cache Directory near full")
						return ""			
					PD = os.path.join(P2C,os.path.basename(PD))
					L4logE("save Picon",PD)
					pil_image.save(PD)
				except:
					L4log("Error: create Cache-Picon")
					return ""
			else:
				L4logE("no Picon found")
				return ""
		return PD
	else:
		L4logE("no Cache")
		# no picon for channel
		if not os.path.exists(P2C):
			L4logE("no Picon-Cachedir",P2C)
			try:
				os.mkdir(P2C)
			except:
				L4log("Error: create Picon-Cache-Dir")
		return ""

def writeHelligkeit(hell,hell2,hell3,STOP = False):
	global SamsungDevice
	global SamsungDevice2
	global SamsungDevice3
	global AktHelligkeit
	def BRI(w1,w2):
		return int(w1) if L4LElist.getBrightness(w2,False)==-1 else L4LElist.getBrightness(w2,False)
	R=""
	if BRI(hell,1) == 0:
		R += "1"
	if BRI(hell2,2) == 0:
		R += "2"
	if BRI(hell3,3) == 0:
		R += "3"
	if AktHelligkeit == [hell,hell2,hell3]+L4LElist.getBrightness(0,False) and OSDtimer >= 0:
		return R
	AktHelligkeit = [hell,hell2,hell3]+L4LElist.getBrightness(0,False)
	L4LElist.resetBrightness([hell,hell2,hell3])
	L4logE("write Bright",AktHelligkeit)
	if SamsungDevice is not None and LCD4linux.LCDType1.value[0] == "1":
		if dpf.setBacklight(SamsungDevice,BRI(hell,1) if BRI(hell,1) < 8 else 7) == False:
			dpf.close(SamsungDevice)
			SamsungDevice = None
	if SamsungDevice2 is not None and LCD4linux.LCDType2.value[0] == "1":
		if dpf.setBacklight(SamsungDevice2,BRI(hell2,2) if BRI(hell2,2) < 8 else 7) == False:
			dpf.close(SamsungDevice2)
			SamsungDevice2 = None
	if SamsungDevice3 is not None and LCD4linux.LCDType3.value[0] == "1":
		if dpf.setBacklight(SamsungDevice3,BRI(hell3,3) if BRI(hell3,3) < 8 else 7) == False:
			dpf.close(SamsungDevice3)
			SamsungDevice3 = None
	if os.path.isfile("/etc/grautec/settings/takeownership") and STOP == False:
		try:
			if LCD4linux.LCDType1.value[0] == "4":
				if os.path.isfile("/tmp/usbtft-brightness"):
					open("/tmp/usbtft-brightness","w").write(str(int(BRI(hell,1)*6.3)))
				elif os.path.isfile("/proc/stb/lcd/oled_brightness"):
					open("/proc/stb/lcd/oled_brightness","w").write(str(int(int(hell)*25.5)))
			if LCD4linux.LCDType2.value[0] == "4":
				if os.path.isfile("/tmp/usbtft-brightness"):
					open("/tmp/usbtft-brightness","w").write(str(int(BRI(hell2,2)*6.3)))
				elif os.path.isfile("/proc/stb/lcd/oled_brightness"):
					open("/proc/stb/lcd/oled_brightness","w").write(str(int(int(hell2)*25.5)))
			if LCD4linux.LCDType3.value[0] == "4":
				if os.path.isfile("/tmp/usbtft-brightness"):
					open("/tmp/usbtft-brightness","w").write(str(int(BRI(hell3,3)*6.3)))
				elif os.path.isfile("/proc/stb/lcd/oled_brightness"):
					open("/proc/stb/lcd/oled_brightness","w").write(str(int(int(hell3)*25.5)))
		except:
			pass
	H = -1
	if LCD4linux.LCDType1.value[0] == "9":
		H = BRI(hell,1)
	elif LCD4linux.LCDType2.value[0] == "9":
		H = BRI(hell2,2)
	elif LCD4linux.LCDType3.value[0] == "9":
		H = BRI(hell3,3)
	if H != -1:
		H = int(H) * 25
		if H >= 250:
			H = 255
		led_fd = open("/dev/lcd2",'w')
		ioctl(led_fd, 0x10, H)
		led_fd.close()
	return R

def doDPF(dev,im,s):
	global SamsungDevice
	global SamsungDevice2
	global SamsungDevice3
	if dev == 1:
		if dpf.showImage(SamsungDevice,s.im[im]) == False:
			L4log("Error writing DPF Device")
			dpf.close(SamsungDevice)
			SamsungDevice = None
	elif dev == 2:
		if dpf.showImage(SamsungDevice2,s.im[im]) == False:
			L4log("Error writing DPF2 Device")
			dpf.close(SamsungDevice2)
			SamsungDevice2 = None
	elif dev == 3:
		if dpf.showImage(SamsungDevice3,s.im[im]) == False:
			L4log("Error writing DPF3 Device")
			dpf.close(SamsungDevice3)
			SamsungDevice3 = None

def writeLCD1(s,im,quality,SAVE=True):
	global SamsungDevice
	if LCD4linux.LCDType1.value[0] == "1":
		if SamsungDevice is not None and not (TVrunning == True and "1" in LCD4linux.TVLCD.value):
			L4log("writing to DPF Device")
			doDPF(1,im,s)
		if "1" in LCD4linux.SavePicture.value and SAVE==True:
			if LCD4linux.LCDRotate1.value != "0":
				s.im[im]=s.im[im].rotate(-int(LCD4linux.LCDRotate1.value))
			try:
				s.im[im].save(PICtmp+".png", "PNG")
				if os.path.isfile(PICtmp+".png"):
					os.rename(PICtmp+".png",PIC+".png")
			except:
				L4log("Error write Picture")
	elif LCD4linux.LCDType1.value[0] == "3":
		L4log("writing Picture")
		try:
			s.im[im].save(PICtmp+"."+LCD4linux.BilderTyp.value, "PNG" if LCD4linux.BilderTyp.value=="png" else "JPEG")
			if os.path.isfile(PICtmp+"."+LCD4linux.BilderTyp.value):
				os.rename(PICtmp+"."+LCD4linux.BilderTyp.value,PIC+"."+LCD4linux.BilderTyp.value)
		except:
			L4log("Error write Picture")
	elif LCD4linux.LCDType1.value[0] == "4":
		L4log("writing TFT-LCD")
		try:
			s.im[im].save("/tmp/usbtft-bmp", "BMP")
			if "1" in LCD4linux.SavePicture.value and SAVE==True:
				if LCD4linux.LCDRotate1.value != "0":
					s.im[im]=s.im[im].rotate(-int(LCD4linux.LCDRotate1.value))
				s.im[im].save(PICtmp+".png", "PNG")
				if os.path.isfile(PICtmp+".png"):
					os.rename(PICtmp+".png",PIC+".png")
		except:
			L4log("Error write Picture")
	elif LCD4linux.LCDType1.value[0] == "5":
		L4log("writing Internal-LCD")
		try:
			if LCD4linux.xmlLCDColor.value=="8":
				s.im[im].convert("P", colors= 254).save(xmlPICtmp, "PNG")
			else:
				s.im[im].save(xmlPICtmp, "PNG")
			if os.path.isfile(xmlPICtmp):
				os.rename(xmlPICtmp,xmlPIC)
			if "1" in LCD4linux.SavePicture.value and SAVE==True:
				if LCD4linux.LCDRotate1.value != "0":
					s.im[im]=s.im[im].rotate(-int(LCD4linux.LCDRotate1.value))
				s.im[im].save(PICtmp+".png", "PNG")
				if os.path.isfile(PICtmp+".png"):
					os.rename(PICtmp+".png",PIC+".png")
		except:
			L4log("Error write Picture")
	elif LCD4linux.LCDType1.value[0] == "9":
		L4log("writing to Vu+ LCD")
		try:
			s.im[im].save(PICtmp+".png", "PNG")
			if os.path.isfile(PICtmp+".png"):
				os.rename(PICtmp+".png",PIC+".png")
		except:
			L4log("Error write Picture")
		if pngutilconnect != 0:
			pngutil.send(PIC+".png")
	else:
		if SamsungDevice is not None and not (TVrunning == True and "1" in LCD4linux.TVLCD.value):
			L4log("writing to Samsung Device")
			output = cStringIO.StringIO()
			s.im[im].save(output, "JPEG") # ,quality=int(quality)
			pic = output.getvalue()
			output.close()
			try:
				Photoframe.write_jpg2frame(SamsungDevice, pic)
			except:
				SamsungDevice = None
				L4log("Samsung 1 write error")
		if "1" in LCD4linux.SavePicture.value and SAVE==True:
			try:
				if LCD4linux.LCDRotate1.value != "0":
					s.im[im]=s.im[im].rotate(-int(LCD4linux.LCDRotate1.value))
					s.im[im].save(PICtmp+".jpg", "JPEG")
				else:
					open(PICtmp+".jpg","wb").write(pic)
				if os.path.isfile(PICtmp+".jpg"):
					os.rename(PICtmp+".jpg",PIC+".jpg")
			except:
				L4log("Error write Picture")

def writeLCD2(s,im,quality,SAVE=True):
	global SamsungDevice2
	if LCD4linux.LCDType2.value[0] == "1":
		if SamsungDevice2 is not None and not (TVrunning == True and "2" in LCD4linux.TVLCD.value):
			L4log("writing to DPF2 Device")
			doDPF(2,im,s)
		if "2" in LCD4linux.SavePicture.value and SAVE==True:
			if LCD4linux.LCDRotate2.value != "0":
				s.im[im]=s.im[im].rotate(-int(LCD4linux.LCDRotate2.value))
			try:
				s.im[im].save(PIC2tmp+".png", "PNG")
				if os.path.isfile(PIC2tmp+".png"):
					os.rename(PIC2tmp+".png",PIC2+".png")
			except:
				L4log("Error write Picture2")
	elif LCD4linux.LCDType2.value[0] == "3":
		L4log("writing Picture2")
		try:
			s.im[im].save(PIC2tmp+"."+LCD4linux.BilderTyp.value, "PNG" if LCD4linux.BilderTyp.value=="png" else "JPEG")
			if os.path.isfile(PIC2tmp+"."+LCD4linux.BilderTyp.value):
				os.rename(PIC2tmp+"."+LCD4linux.BilderTyp.value,PIC2+"."+LCD4linux.BilderTyp.value)
		except:
			L4log("Error write Picture2")
	elif LCD4linux.LCDType2.value[0] == "4":
		L4log("writing TFT-LCD2")
		try:
			s.im[im].save("/tmp/usbtft-bmp", "BMP")
			if "2" in LCD4linux.SavePicture.value and SAVE==True:
				if LCD4linux.LCDRotate2.value != "0":
					s.im[im]=s.im[im].rotate(-int(LCD4linux.LCDRotate2.value))
				s.im[im].save(PIC2tmp+".png", "PNG")
				if os.path.isfile(PIC2tmp+".png"):
					os.rename(PIC2tmp+".png",PIC2+".png")
		except:
			L4log("Error write Picture2")
	elif LCD4linux.LCDType2.value[0] == "5":
		L4log("writing Internal-LCD2")
		try:
			if LCD4linux.xmlLCDColor.value=="8":
				s.im[im].convert("P", colors= 254).save(xmlPICtmp, "PNG")
			else:
				s.im[im].save(xmlPICtmp, "PNG")
			if os.path.isfile(xmlPICtmp):
				os.rename(xmlPICtmp,xmlPIC)
			if "2" in LCD4linux.SavePicture.value and SAVE==True:
				if LCD4linux.LCDRotate2.value != "0":
					s.im[im]=s.im[im].rotate(-int(LCD4linux.LCDRotate2.value))
				s.im[im].save(PIC2tmp+".png", "PNG")
				if os.path.isfile(PIC2tmp+".png"):
					os.rename(PIC2tmp+".png",PIC2+".png")
		except:
			L4log("Error write Picture2")
	elif LCD4linux.LCDType2.value[0] == "9":
		L4log("writing to Vu+ LCD2")
		try:
			s.im[im].save(PIC2tmp+".png", "PNG")
			if os.path.isfile(PIC2tmp+".png"):
				os.rename(PIC2tmp+".png",PIC2+".png")
		except:
			L4log("Error write Picture2")
		if pngutilconnect != 0:
			pngutil.send(PIC2+".png")
	else:
		if SamsungDevice2 is not None and not (TVrunning == True and "2" in LCD4linux.TVLCD.value):
			L4log("writing to Samsung2 Device")
			output = cStringIO.StringIO()
			s.im[im].save(output, "JPEG") # ,quality=int(quality)
			pic = output.getvalue()
			output.close()
			try:
				Photoframe.write_jpg2frame(SamsungDevice2, pic)       
			except:
				SamsungDevice2 = None
				L4log("Samsung 2 write error")
		if "2" in LCD4linux.SavePicture.value and SAVE==True:
			try:
				if LCD4linux.LCDRotate2.value != "0":
					s.im[im]=s.im[im].rotate(-int(LCD4linux.LCDRotate2.value))
					s.im[im].save(PIC2tmp+".jpg", "JPEG")
				else:
					open(PIC2tmp+".jpg","wb").write(pic)
				if os.path.isfile(PIC2tmp+".jpg"):
					os.rename(PIC2tmp+".jpg",PIC2+".jpg")
			except:
				L4log("Error write Picture2")

def writeLCD3(s,im,quality,SAVE=True):
	global SamsungDevice3
	if LCD4linux.LCDType3.value[0] == "1":
		if SamsungDevice3 is not None and not (TVrunning == True and "3" in LCD4linux.TVLCD.value):
			L4log("writing to DPF3 Device")
			doDPF(3,im,s)
		if "3" in LCD4linux.SavePicture.value and SAVE==True:
			if LCD4linux.LCDRotate3.value != "0":
				s.im[im]=s.im[im].rotate(-int(LCD4linux.LCDRotate3.value))
			try:
				s.im[im].save(PIC3tmp+".png", "PNG")
				if os.path.isfile(PIC3tmp+".png"):
					os.rename(PIC3tmp+".png",PIC3+".png")
			except:
				L4log("Error write Picture3")
	elif LCD4linux.LCDType3.value[0] == "3":
		L4log("writing Picture3")
		try:
			s.im[im].save(PIC3tmp+"."+LCD4linux.BilderTyp.value, "PNG" if LCD4linux.BilderTyp.value=="png" else "JPEG")
			if os.path.isfile(PIC3tmp+"."+LCD4linux.BilderTyp.value):
				os.rename(PIC3tmp+"."+LCD4linux.BilderTyp.value,PIC3+"."+LCD4linux.BilderTyp.value)
		except:
			L4log("Error write Picture3")
	elif LCD4linux.LCDType3.value[0] == "4":
		L4log("writing TFT-LCD3")
		try:
			s.im[im].save("/tmp/usbtft-bmp", "BMP")
			if "3" in LCD4linux.SavePicture.value and SAVE==True:
				if LCD4linux.LCDRotate3.value != "0":
					s.im[im]=s.im[im].rotate(-int(LCD4linux.LCDRotate3.value))
				s.im[im].save(PIC3tmp+".png", "PNG")
				if os.path.isfile(PIC3tmp+".png"):
					os.rename(PIC3tmp+".png",PIC3+".png")
		except:
			L4log("Error write Picture3")
	elif LCD4linux.LCDType3.value[0] == "5":
		L4log("writing Internal-LCD3")
		try:
			if LCD4linux.xmlLCDColor.value=="8":
				s.im[im].convert("P", colors= 254).save(xmlPICtmp, "PNG")
			else:
				s.im[im].save(xmlPICtmp, "PNG")
			if os.path.isfile(xmlPICtmp):
				os.rename(xmlPICtmp,xmlPIC)
			if "3" in LCD4linux.SavePicture.value and SAVE==True:
				if LCD4linux.LCDRotate3.value != "0":
					s.im[im]=s.im[im].rotate(-int(LCD4linux.LCDRotate3.value))
				s.im[im].save(PIC3tmp+".png", "PNG")
				if os.path.isfile(PIC3tmp+".png"):
					os.rename(PIC3tmp+".png",PIC3+".png")
		except:
			L4log("Error write Picture3")
	elif LCD4linux.LCDType3.value[0] == "9":
		L4log("writing to Vu+ LCD3")
		try:
			s.im[im].save(PIC3tmp+".png", "PNG")
			if os.path.isfile(PIC3tmp+".png"):
				os.rename(PIC3tmp+".png",PIC3+".png")
		except:
			L4log("Error write Picture3")
		if pngutilconnect != 0:
			pngutil.send(PIC3+".png")
	else:
		if SamsungDevice3 is not None and not (TVrunning == True and "3" in LCD4linux.TVLCD.value):
			L4log("writing to Samsung3 Device")
			output = cStringIO.StringIO()
			s.im[im].save(output, "JPEG") # ,quality=int(quality)
			pic = output.getvalue()
			output.close()
			try:
				Photoframe.write_jpg2frame(SamsungDevice3, pic)       
			except:
				SamsungDevice3 = None
				L4log("Samsung 3 write error")
		if "3" in LCD4linux.SavePicture.value and SAVE==True:
			try:
				if LCD4linux.LCDRotate3.value != "0":
					s.im[im]=s.im[im].rotate(-int(LCD4linux.LCDRotate3.value))
					s.im[im].save(PIC3tmp+".jpg", "JPEG")
				else:
					open(PIC3tmp+".jpg","wb").write(pic)
				if os.path.isfile(PIC3tmp+".jpg"):
					os.rename(PIC3tmp+".jpg",PIC3+".jpg")
			except:
				L4log("Error write Picture3")

def NextScreen(PRESS):
	global ScreenActive
	global ScreenTime
	if SaveEventListChanged == True:
		L4log("Event Change Aktive")
		return
	if Standby.inStandby or ConfigStandby:
		if ScreenActive[0] == "1":
			ST = LCD4linux.StandbyScreenTime.value
		elif ScreenActive[0] == "2":
			ST = LCD4linux.StandbyScreenTime2.value
		elif ScreenActive[0] == "3":
			ST = LCD4linux.StandbyScreenTime3.value
		elif ScreenActive[0] == "4":
			ST = LCD4linux.StandbyScreenTime4.value
		elif ScreenActive[0] == "5":
			ST = LCD4linux.StandbyScreenTime5.value
		elif ScreenActive[0] == "6":
			ST = LCD4linux.StandbyScreenTime6.value
		elif ScreenActive[0] == "7":
			ST = LCD4linux.StandbyScreenTime7.value
		elif ScreenActive[0] == "8":
			ST = LCD4linux.StandbyScreenTime8.value
		elif ScreenActive[0] == "9":
			ST = LCD4linux.StandbyScreenTime9.value
		else:
			ST = "1"
	else:
		if ScreenActive[0] == "1":
			ST = LCD4linux.ScreenTime.value
		elif ScreenActive[0] == "2":
			ST = LCD4linux.ScreenTime2.value
		elif ScreenActive[0] == "3":
			ST = LCD4linux.ScreenTime3.value
		elif ScreenActive[0] == "4":
			ST = LCD4linux.ScreenTime4.value
		elif ScreenActive[0] == "5":
			ST = LCD4linux.ScreenTime5.value
		elif ScreenActive[0] == "6":
			ST = LCD4linux.ScreenTime6.value
		elif ScreenActive[0] == "7":
			ST = LCD4linux.ScreenTime7.value
		elif ScreenActive[0] == "8":
			ST = LCD4linux.ScreenTime8.value
		elif ScreenActive[0] == "9":
			ST = LCD4linux.ScreenTime9.value
		else:
			ST = "1"
	if ScreenTime >= int(ST) and int(ST) > 0 or PRESS == True:
		ScreenTime=0
		ScreenActive[0] = str(int(ScreenActive[0])+1)
		if Standby.inStandby or ConfigStandby:
			if int(ScreenActive[0]) > int(LCD4linux.StandbyScreenMax.value):
				ScreenActive[0] = "1"
		elif (isMediaPlayer != "" and isMediaPlayer != "radio"):
			if int(ScreenActive[0]) > int(LCD4linux.MPScreenMax.value):
				ScreenActive[0] = "1"
		else:
			if int(ScreenActive[0]) > int(LCD4linux.ScreenMax.value):
				ScreenActive[0] = "1"
	if LCD4linux.StandbyScreenTime.value > 0 or LCD4linux.ScreenTime.value > 0:
		ScreenTime += 1

def _getDirs(base):
	return [x for x in glob.iglob(os.path.join( base, '*')) if os.path.isdir(x) ]

def rglob(base, pattern):
	list = []
	list.extend(glob.glob(os.path.join(base,pattern)))
	dirs = _getDirs(base)
	L4logE("Picturedirectorys", dirs)
	if len(dirs):
		for d in dirs:
			list.extend(rglob(os.path.join(base,d), pattern))
	return list

def getBilder():
	global Bilder
	global BilderIndex
	BilderOrt = ["","",""]
	Bilder = [[],[],[]]
	SuchExt = ["*.png","*.PNG","*.jpg","*.JPG"]
	if Standby.inStandby or ConfigStandby:
		if LCD4linux.StandbyBild.value !=0:
			BilderOrt[0] = LCD4linux.StandbyBildFile.value
		if LCD4linux.StandbyBild2.value !=0:
			BilderOrt[1] = LCD4linux.StandbyBild2File.value
		if LCD4linux.StandbyBild3.value !=0:
			BilderOrt[2] = LCD4linux.StandbyBild3File.value
	elif isMediaPlayer == "" or isMediaPlayer == "radio":
		if LCD4linux.Bild.value !=0:
			BilderOrt[0] = LCD4linux.BildFile.value
		if LCD4linux.Bild2.value !=0:
			BilderOrt[1] = LCD4linux.Bild2File.value
		if LCD4linux.Bild3.value !=0:
			BilderOrt[2] = LCD4linux.Bild3File.value
	else:
		if LCD4linux.MPBild.value !=0:
			BilderOrt[0] = LCD4linux.MPBildFile.value
		if LCD4linux.MPBild2.value !=0:
			BilderOrt[1] = LCD4linux.MPBild2File.value
		BilderOrt[2]=""
	L4logE("BilderOrt",BilderOrt)
	if os.path.isdir(BilderOrt[0]):
		L4log("read Pictures0")
		BilderIndex[0] = 0
		if LCD4linux.BilderRecursiv.value == False:
			for EXT in SuchExt:
				Bilder[0] += glob.glob(os.path.normpath(BilderOrt[0])+"/"+EXT)
		else:
			for EXT in SuchExt:
				Bilder[0] += rglob(os.path.normpath(BilderOrt[0]),EXT)
		if LCD4linux.BilderSort.value == "2":
			random.shuffle(Bilder[0])
		elif LCD4linux.BilderSort.value == "1":
			Bilder[0].sort()
		L4logE("Pictures",Bilder[0])
	if os.path.isdir(BilderOrt[1]):
		L4log("read Pictures1")
		BilderIndex[1] = 0
		if LCD4linux.BilderRecursiv.value == False:
			for EXT in SuchExt:
				Bilder[1] += glob.glob(os.path.normpath(BilderOrt[1])+"/"+EXT)
		else:
			for EXT in SuchExt:
				Bilder[1] += rglob(os.path.normpath(BilderOrt[1]),EXT)
		if LCD4linux.BilderSort.value == "2":
			random.shuffle(Bilder[1])
		elif LCD4linux.BilderSort.value == "1":
			Bilder[1].sort()
		L4logE("Pictures",Bilder[1])
	if os.path.isdir(BilderOrt[2]):
		L4log("read Pictures2")
		BilderIndex[2] = 0
		if LCD4linux.BilderRecursiv.value == False:
			for EXT in SuchExt:
				Bilder[2] += glob.glob(os.path.normpath(BilderOrt[2])+"/"+EXT)
		else:
			for EXT in SuchExt:
				Bilder[2] += rglob(os.path.normpath(BilderOrt[2]),EXT)
		if LCD4linux.BilderSort.value == "2":
			random.shuffle(Bilder[2])
		elif LCD4linux.BilderSort.value == "1":
			Bilder[2].sort()
		L4logE("Pictures",Bilder[2])

def getWWW():
#	print LCD4linux.WWW1.value , LCD4linux.WWW1url.value , Standby.inStandby, not Standby.inStandby
	if (LCD4linux.WWW1.value != "0" and len(LCD4linux.WWW1url.value)>10) and not Standby.inStandby:
		L4log("WWW Converter check on")
		getHTMLwww(1,LCD4linux.WWW1url.value,LCD4linux.WWW1w.value,LCD4linux.WWW1h.value)
	elif (LCD4linux.StandbyWWW1.value != "0" and len(LCD4linux.StandbyWWW1url.value)>10) and Standby.inStandby:
		L4log("WWW Converter check stb")
		getHTMLwww(1,LCD4linux.StandbyWWW1url.value,LCD4linux.StandbyWWW1w.value,LCD4linux.StandbyWWW1h.value)

def HTMLwwwDownloadFailed(result):
	L4log("HTMLwww download failed:",result)

def HTMLwwwDownloadFinished(filename, result):
	if os.path.isfile(filename):
		L4log("HTMLwww download finished")
		rmFile(WWWpic % "1p")
	else:
		L4log("HTMLwww download finished, no file found")

def getHTMLwww(fn,www,pw,ph):
	filename=WWWpic % str(fn)
	url="http://do.convertapi.com/web2image?curl=%s&PageWidth=%d&PageHight=%d&outputformat=jpg" % (www,pw,ph)
	L4log("downloading HTMLwww from",url)
	downloadPage(url , filename).addCallback(boundFunction(HTMLwwwDownloadFinished, filename)).addErrback(HTMLwwwDownloadFailed)

def xmlFind(Num):
	for i in xmlList:
		if i.startswith("<!--L4L%02d" % Num):
			return i
	return -1

def xmlScreens(Lis2):
	sl = []
	for i in Lis2:
		if i.find("<screen ") != -1:
			b = i.replace("\"","").split("name=")
			sl.append(b[1].split()[0])
	return sl

def xmlInsert(Lis2):
	global xmlList
	if len(Lis2) == 0:
		L4log("insert no Skindata")
		return
	xl = xmlScreens(Lis2)
	for i in range(0,len(xmlList)):
		if xmlList[i].find("<screen ") != -1:
			for i2 in range(0,len(xl)):
				if xmlList[i].find("\"%s\"" % xl[i2]) != -1:
					L4log("disable Screen",xl[i2])
					xmlList[i]=xmlList[i].replace("\"%s\"" % xl[i2],"\"L4L%s\"" % xl[i2])
	L4log("insert Skindata")
	for i in Lis2:
		ttt = LCD4linux.xmlLCDType.value.split("x")
		if LCD4linux.xmlLCDType.value == "96x64":
			i = i.replace("\">","\" id=\"2\">")
		xmlList.insert(-1,i.replace("$w$",ttt[0]).replace("$h$",ttt[1]))

def xmlDelete(Num):
	global xmlList
	delON = False
	isDelete = False
	sli = xmlReadData()
	xl = xmlScreens(sli[Num])
	for i in range(0,len(xmlList)):
		if xmlList[i].find("<screen ") != -1:
			for i2 in range(0,len(xl)):
				if xmlList[i].find("\"L4L%s\"" % xl[i2]) != -1:
					L4log("enable Screen",xl[i2])
					xmlList[i]=xmlList[i].replace("\"L4L%s\"" % xl[i2],"\"%s\"" % xl[i2])
	L4log("remove Skindata",Num)
	i = 0
	aa = 0
	while i<len(xmlList):
		if xmlList[i].startswith("<!--L4L%02d " % Num):
			delON = True
			isDelete = True
		if delON==True:
			if xmlList[i].startswith("<!--L4L%02d-" % Num):
				delON = False
			del xmlList[i]
		else:
			i+=1
	return isDelete

def xmlClear():
	global xmlList
	xmlList = []

def xmlRead():
	global xmlList
	xmlList = []
	if os.path.isfile("/etc/enigma2/skin_user.xml"):
		for i in open("/etc/enigma2/skin_user.xml").read().splitlines():
			xmlList.append(i)
		if len(xmlList)>1:
			while len(xmlList[-1]) < 2 and len(xmlList)>1:
				del xmlList[-1]
	else:
		xmlList=["<skin>","</skin>"]

def xmlReadData():
	sld=[[],[],[],[]]
	if os.path.isfile(Data+"skin_data.xml"):
		aa = 0
		for i in open(Data+"skin_data.xml").read().splitlines():
			if i.startswith("###"):
				break
			if i.startswith("<!--L4L"):
				aa=int(i[7:9])
			sld[aa].append(i)
	return sld

def xmlWrite():
	if len(xmlList)>1:
		L4log("write SkinData")
		fw = open("/etc/enigma2/skin_user.xml","w")
		for i in xmlList:
			fw.write(i+"\n")
		fw.close()

def xmlSkin():
	change=False
	xmlRead()
	if xmlList[-1].find("/skin") == -1:
		L4log("Error xmlSkin")
		return False
	sli=xmlReadData()
	xf = xmlFind(1)
	if xf == -1 and LCD4linux.xmlType01.value == True:
		change=True
		xmlInsert(sli[1])
	elif xf >= 0 and LCD4linux.xmlType01.value == False:
		change=True
		ok=xmlDelete(1)
	xf = xmlFind(2)
	if xf == -1 and LCD4linux.xmlType02.value == True:
		change=True
		xmlInsert(sli[2])
	elif xf >= 0 and LCD4linux.xmlType02.value == False:
		change=True
		ok=xmlDelete(2)
	xf = xmlFind(3)
	if xf == -1 and LCD4linux.xmlType03.value == True:
		change=True
		xmlInsert(sli[3])
	elif xf >= 0 and LCD4linux.xmlType03.value == False:
		change=True
		ok=xmlDelete(3)
	return change
		
class RunShell:
	def __init__(self, cmd):
		global ShellRunning
		ShellRunning = True
		L4log("Shell",cmd)
		self.container = eConsoleAppContainer()
		self.container.appClosed.append(self.cmdFinished)
		self.container.dataAvail.append(self.dataAvail)
		self.container.execute(cmd)

	def cmdFinished(self, data):
		global ShellRunning
		ShellRunning = False
		L4log("Shell Stop")

	def dataAvail(self, data):
		global ShellRunning
		ShellRunning = False
		L4log("Shell Data")

def TFTCheck(Force,SetMode=""):
	global AktTFT
	if os.path.isfile("/usr/bin/tft-bmp-mode.sh") == True and os.path.isfile("/usr/bin/tft-dream-mode.sh") == True:
		CurTFT = os.path.isfile("/etc/grautec/settings/takeownership")
		L4logE("TFT mode...",CurTFT)
		if LCD4linux.LCDType1.value[0] == "4" or LCD4linux.LCDType2.value[0] == "4" or LCD4linux.LCDType3.value[0] == "4" and SetMode != "DREAM":
			L4logE("TFT enabled")
			if AktTFT != "BMP" or Force == True or SetMode == "BMP":
				i=10
				while ShellRunning == True and i > 0:
					sleep(0.5)
					i -= 1
				RunShell("/usr/bin/tft-bmp-mode.sh")
				AktTFT = "BMP"
		else:
			L4logE("TFT not")
			if (AktTFT != "DREAM" and CurTFT == True) or Force == True or SetMode == "DREAM":
				i=10
				while ShellRunning == True and i > 0:
					sleep(0.5)
					i -= 1
				RunShell("/usr/bin/tft-dream-mode.sh")
				AktTFT = "DREAM"

def SamsungCheck():
	global SamsungDevice
	global SamsungDevice2
	global SamsungDevice3
	if USBok == False:
		return True
	if LCD4linux.LCDType1.value[0] == "2":
		known_devices_list = Photoframe.get_known_devices()
		device0 = known_devices_list[(int(LCD4linux.LCDType1.value[1:])-3)*2]
		if find_dev(1,device0["idVendor"],device0["idProduct"]) == False:
			L4log("Samsung 1 Stat failed")
			SamsungDevice = None
			return True
		if Photoframe.name(SamsungDevice) is None:
			L4log("Samsung 1 no answer")
			SamsungDevice = None
			return True
	if LCD4linux.LCDType2.value[0] == "2":
		known_devices_list = Photoframe.get_known_devices()
		device0 = known_devices_list[(int(LCD4linux.LCDType2.value[1:])-3)*2]
		Anz=2 if LCD4linux.LCDType1.value == LCD4linux.LCDType2.value else 1
		if find_dev(Anz,device0["idVendor"],device0["idProduct"]) == False:
			L4log("Samsung 2 Stat failed")
			SamsungDevice2 = None
			return True
		if Photoframe.name(SamsungDevice2) is None:
			L4log("Samsung 2 no answer")
			SamsungDevice2 = None
			return True
	if LCD4linux.LCDType3.value[0] == "2":
		known_devices_list = Photoframe.get_known_devices()
		device0 = known_devices_list[(int(LCD4linux.LCDType3.value[1:])-3)*2]
		Anz=2 if LCD4linux.LCDType1.value == LCD4linux.LCDType3.value else 1
		if find_dev(Anz,device0["idVendor"],device0["idProduct"]) == False:
			L4log("Samsung 3 Stat failed")
			SamsungDevice3 = None
			return True
		if Photoframe.name(SamsungDevice3) is None:
			L4log("Samsung 3 no answer")
			SamsungDevice3 = None
			return True
	return False

def getSamsungDevice():
	global SamsungDevice
	global SamsungDevice2
	global SamsungDevice3
	if USBok == True:
		if LCD4linux.LCDType1.value[0] == "2":
			if SamsungDevice is None:
				L4log("get Samsung Device...")
				known_devices_list = Photoframe.get_known_devices()
				device0 = known_devices_list[(int(LCD4linux.LCDType1.value[1:])-3)*2]
				device1 = known_devices_list[(int(LCD4linux.LCDType1.value[1:])-3)*2+1]
				if find_dev(1,device0["idVendor"],device0["idProduct"]) == True or find_dev(1,device1["idVendor"],device1["idProduct"]) == True:
					try:
						SamsungDevice = Photoframe.init_device(1, device0, device1)
					except:
						pass
		if LCD4linux.LCDType2.value[0] == "2":
			if SamsungDevice2 is None:
				L4log("get Samsung2 Device...")
				known_devices_list = Photoframe.get_known_devices()
				device0 = known_devices_list[(int(LCD4linux.LCDType2.value[1:])-3)*2]
				device1 = known_devices_list[(int(LCD4linux.LCDType2.value[1:])-3)*2+1]
				Anz=2 if LCD4linux.LCDType1.value == LCD4linux.LCDType2.value else 1
				if Anz == 2:
					if find_dev2(device0["idVendor"],device0["idProduct"],device1["idVendor"],device1["idProduct"]) == True:
						try:
							SamsungDevice2 = Photoframe.init_device(Anz, device0, device1)
						except:
							pass
				else:
					if find_dev(Anz,device0["idVendor"],device0["idProduct"]) == True or find_dev(Anz,device1["idVendor"],device1["idProduct"]) == True:
						try:
							SamsungDevice2 = Photoframe.init_device(Anz, device0, device1)
						except:
							pass
		if LCD4linux.LCDType3.value[0] == "2":
			if SamsungDevice3 is None:
				L4log("get Samsung3 Device...")
				known_devices_list = Photoframe.get_known_devices()
				device0 = known_devices_list[(int(LCD4linux.LCDType3.value[1:])-3)*2]
				device1 = known_devices_list[(int(LCD4linux.LCDType3.value[1:])-3)*2+1]
				Anz=2 if LCD4linux.LCDType1.value == LCD4linux.LCDType3.value else 1
				if Anz == 2:
					if find_dev2(device0["idVendor"],device0["idProduct"],device1["idVendor"],device1["idProduct"]) == True:
						try:
							SamsungDevice3 = Photoframe.init_device(Anz, device0, device1)
						except:
							pass
				else:
					if find_dev(Anz,device0["idVendor"],device0["idProduct"]) == True or find_dev(Anz,device1["idVendor"],device1["idProduct"]) == True:
						try:
							SamsungDevice3 = Photoframe.init_device(Anz, device0, device1)
						except:
							pass

def DpfCheck():
	global SamsungDevice
	global SamsungDevice2
	global SamsungDevice3
	if USBok == False:
		return True
	if LCD4linux.LCDType1.value[0] == "1":
		if find_dev(1,0x1908,0x0102) == False or SamsungDevice is None:
			L4log("DPF 1 Stat failed")
			dpf.close(SamsungDevice)
			SamsungDevice = None
			return True
	if LCD4linux.LCDType2.value[0] == "1":
		Anz=2 if LCD4linux.LCDType1.value == LCD4linux.LCDType2.value else 1
		if find_dev(Anz,0x1908,0x0102) == False or SamsungDevice2 is None:
			L4log("DPF 2 Stat failed")
			dpf.close(SamsungDevice2)
			SamsungDevice2 = None
			return True
	if LCD4linux.LCDType3.value[0] == "1":
		Anz=2 if LCD4linux.LCDType1.value == LCD4linux.LCDType3.value else 1
		if find_dev(Anz,0x1908,0x0102) == False or SamsungDevice3 is None:
			L4log("DPF 3 Stat failed")
			dpf.close(SamsungDevice3)
			SamsungDevice3 = None
			return True
	return False

def getDpfDevice():
	global SamsungDevice
	global SamsungDevice2
	global SamsungDevice3
	if USBok == False:
		return
	if LCD4linux.LCDType1.value[0] == "1":
		if SamsungDevice is None:
			L4log("get DPF Device...")
			if find_dev(1,0x1908,0x0102) == True:
				try:
					L4log("open DPF Device0...")
					SamsungDevice = dpf.open("usb0")
				except:
					L4log("open Error DPF1 Device0")
					SamsungDevice = None
			else:
				L4log("DPF1 Device0 not found")
	if LCD4linux.LCDType2.value[0] == "1":
		if SamsungDevice2 is None:
			L4log("get DPF2 Device...")
			Anz=2 if LCD4linux.LCDType1.value == LCD4linux.LCDType2.value else 1
			if Anz == 2:
				if find_dev(2,0x1908,0x0102) == True:
					try:
						L4log("open DPF2 Device1...")
						SamsungDevice2 =  dpf.open("usb1")
					except:
						L4log("open Error DPF2 Device1")
						SamsungDevice2 = None
				else:
					L4log("DPF2 Device1 not found")
			else:
				if find_dev(1,0x1908,0x0102) == True:
					try:
						L4log("open DPF2 Device0...")
						SamsungDevice2 = dpf.open("usb0")
					except:
						L4log("open Error DPF2 Device0")
						SamsungDevice2 = None
				else:
					L4log("DPF2 Device0 not found")
	if LCD4linux.LCDType3.value[0] == "1":
		if SamsungDevice3 is None:
			L4log("get DPF3 Device...")
			Anz=2 if LCD4linux.LCDType1.value == LCD4linux.LCDType3.value else 1
			if Anz == 2:
				if find_dev(2,0x1908,0x0102) == True:
					try:
						L4log("open DPF3 Device1...")
						SamsungDevice3 =  dpf.open("usb1")
					except:
						L4log("open Error DPF3 Device1")
						SamsungDevice3 = None
				else:
					L4log("DPF2 Device1 not found")
			else:
				if find_dev(1,0x1908,0x0102) == True:
					try:
						L4log("open DPF3 Device0...")
						SamsungDevice3 = dpf.open("usb0")
					except:
						L4log("open Error DPF3 Device0")
						SamsungDevice3 = None
				else:
					L4log("DPF3 Device0 not found")

def DpfCheckSerial():
	global SamsungDevice
	global SamsungDevice2
	global SamsungDevice3
	if LCD4linux.LCDType1.value[0] == "1" and LCD4linux.LCDType1.value == LCD4linux.LCDType2.value:
		if SamsungDevice is not None and SamsungDevice2 is not None:
			s1,s2 = "",""
			try:
				s1 = "".join(struct.unpack("sxsxsx",SamsungDevice.readFlash(0x180ED3,6)))
			except:
				dpf.close(SamsungDevice)
				SamsungDevice = None
				L4log("Error Read DPF Device")
				return
			try:
				s2 = "".join(struct.unpack("sxsxsx",SamsungDevice2.readFlash(0x180ED3,6)))
			except:
				dpf.close(SamsungDevice2)
				SamsungDevice2 = None
				L4log("Error Read DPF2 Device")
				return
			L4log(s1,s2)
			if s1.startswith("0.") and s2.startswith("0."):
				if s1 > s2:
					Exchange()
	
def Exchange():
	global SamsungDevice
	global SamsungDevice2
	global SamsungDevice3
	if LCD4linux.LCDType1.value == LCD4linux.LCDType2.value:
		SamsungDevice, SamsungDevice2 = SamsungDevice2, SamsungDevice

def CheckFstab():
	if os.path.isfile("/etc/fstab"):
		f = open("/etc/fstab","r")
		if f.read().lower().find("usbfs") == -1:
			L4log("Info: no usbfs-Line in fstab")
		f.close()

def FritzCallLCD4Linux(event,Date,number,caller,phone):
	global FritzTime
	if (LCD4linux.Fritz.value != "0" or LCD4linux.MPFritz.value != "0" or LCD4linux.StandbyFritz.value != "0"):
		L4log("FritzCall",[event,Date,number,caller,phone])
		if len(FritzList)>0:
			if Date==FritzList[-1][1]:
				L4log("FritzCall ignore")
				return
		rmFile(PICfritz)
		FritzList.append([event,Date,number,caller,phone])
		FritzTime = int(LCD4linux.FritzTime.value) + 2
		while len(FritzList) > 20:
			del FritzList[0]
		if BriefLCD.qsize()<=2:
			BriefLCD.put(1) 

def NcidLCD4Linux(Date,number,caller):
	global FritzTime
	if (LCD4linux.Fritz.value != "0" or LCD4linux.MPFritz.value != "0" or LCD4linux.StandbyFritz.value != "0"):
		L4log("Ncid",[Date,number,caller])
		rmFile(PICfritz)
		dt = datetime.strptime(Date, "%d.%m.%Y - %H:%M")
		Date = dt.strftime("%d.%m.%y %H:%M:%S")
		FritzList.append(["RING",Date,number,caller,""])
		FritzTime = int(LCD4linux.FritzTime.value) + 2
		while len(FritzList) > 20:
			del FritzList[0]
		if BriefLCD.qsize()<=2:
			BriefLCD.put(1) 

# Load Config
if os.path.isfile(LCD4config):
	f=open(LCD4config,"r")
	L = f.read()
	f.close()
	if "Netatmo" in L:
		L=L.replace("Netatmo","NetAtmo")
		w = open(LCD4config,"w")
		w.write(L)
		w.close()
	LCD4linux.loadFromFile(LCD4config)
	LCD4linux.load()
else:
	L4log("no config found!")

try:
	from Plugins.Extensions.FritzCall.plugin import registerUserAction as FritzCallRegisterUserAction
	FritzCallRegisterUserAction(FritzCallLCD4Linux)
	L4log("Register FritzCall ok")
except:
	L4log("FritCall not registered")

try:
	from Plugins.Extensions.NcidClient.plugin import registerUserAction as NcidClientRegisterUserAction
	NcidClientRegisterUserAction(NcidLCD4Linux)
	L4log("Register NcidClient ok")
except:
	L4log("NcidClient not registered")

try:
	from Plugins.Extensions.BitrateViewer.bitratecalc import eBitrateCalculator
	BitrateRegistred = True
	L4log("Register Bitrate ok")
except:
	BitrateRegistred = False
	L4log("Bitrate not registered")

try:
	from Plugins.Extensions.webradioFS.ext import ext_l4l
	WebRadioFS = ext_l4l()
	WebRadioFSok = True
	L4log("Register WebRadioFS ok")
except:
	WebRadioFSok = False
	L4log("WebRadioFS not registered")

try:
	from Plugins.Extensions.Netatmo.Netatmo import netatmo
	from Plugins.Extensions.Netatmo.NetatmoCore import NetatmoUnit
	NetatmoOK = True
	L4log("Register Netatmo ok")
except:
	NetatmoOK = False
	L4log("Netatmo not registered")

class GrabOSD:
	def __init__(self, cmd):
		global GrabRunning
		GrabRunning = True
		L4logE("Grab Run")

#		self.container = eConsoleAppContainer()
#		self.container.appClosed.append(self.cmdFinished)
#		self.container.dataAvail.append(self.dataAvail)

#		self.container.execute(cmd)
		os.system(cmd + " >/dev/null 2>&1")
		self.cmdFinished("")

	def cmdFinished(self, data):
		global GrabRunning
		L4logE("Grab Stop")
		GrabRunning = False

	def dataAvail(self, data):
		pass


# Grab
def doGrab(i,ConfigFast,ConfigSize):
	CF = "" if ConfigFast == True else "-b"
	GrabOSD("/usr/bin/grab -o -p -j 95 %s -r %d %sdpfgrab.jpg" % (CF,ConfigSize,TMPL) ) 

def InitWebIF():
	L4log("WebIf-Init...")
	i=20
	if LCD4linux.WebIfInitDelay.value == True:
		while len(glob.glob("/usr/lib/enigma2/python/Plugins/Extensions/WebInterface/__init__.py*")) == 0 and i > 0:
			sleep(0.5)
			i-=1
	if i > 0 and len(glob.glob("/usr/lib/enigma2/python/Plugins/Extensions/WebInterface/__init__.py*")) > 0:
		if i<20:
			L4log("WebIf-Wait %d s" % int((20-i)/2))
			sleep(5)
		from Plugins.Extensions.WebInterface.WebChilds.Toplevel import addExternalChild
		from twisted.web import static
		from WebSite import LCD4linuxweb,LCD4linuxwebView
		from WebConfigSite import LCD4linuxConfigweb
		L4log("Child to WebIf...")
		root = static.File("%slcd4linux" % TMP)
		root.putChild("", LCD4linuxweb())
		root.putChild("view", LCD4linuxwebView())
		root.putChild("config", LCD4linuxConfigweb())
		root.putChild("data",static.File(Data[:-1]))
		if os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/WebInterface/web/external.xml"):
			try:
				addExternalChild( ("lcd4linux", root, "LCD4linux", Version, True) )
				L4log("use new WebIf")
			except:
				addExternalChild( ("lcd4linux", root) )
				L4log("Error, fall back to old WebIf")
		else:
			addExternalChild( ("lcd4linux", root) )
			L4log("use old WebIf")
		if os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/OpenWebif/pluginshook.src"):
			try:
				addExternalChild( ("lcd4linux", root, "LCD4linux", Version) )
				L4log("use OpenWebIf")
			except:
				pass
	else:
		L4log("no WebIf found")

class L4LWorker1(Thread): 
	def __init__(self,index,s,session):
		Thread.__init__(self)
		self.index = index
		self.session = session
		self.s = s
 
	def run(self): 
		while True:
			try:
				para = Brief1.get()
#				print "1:",para[0]
				if len(para) == 2:
					para[0](para[1])
				elif len(para) == 4:
					para[0](para[1],para[2],para[3])
				elif len(para) == 5:
					para[0](para[1],para[2],para[3],para[4])
				elif len(para) == 3:
					para[0](para[1],para[2])
				elif len(para) == 7:
					para[0](para[1],para[2],para[3],para[4],para[5],para[6])
				elif len(para) == 8:
					para[0](para[1],para[2],para[3],para[4],para[5],para[6],para[7])
			except:
				from traceback import format_exc
				L4log("Error1:",format_exc() )
				try:
					open(CrashFile,"w").write(format_exc())
				except:
					pass
			Brief1.task_done() 

class L4LWorker2(Thread): 
	def __init__(self,index,s,session):
		Thread.__init__(self)
		self.index = index
		self.session = session
		self.s = s
 
	def run(self): 
		while True:
			try:
				para = Brief2.get()
#				print "2:",para[0]
				if len(para) == 2:
					para[0](para[1])
				elif len(para) == 4:
					para[0](para[1],para[2],para[3])
				elif len(para) == 5:
					para[0](para[1],para[2],para[3],para[4])
				elif len(para) == 3:
					para[0](para[1],para[2])
				elif len(para) == 7:
					para[0](para[1],para[2],para[3],para[4],para[5],para[6])
				elif len(para) == 8:
					para[0](para[1],para[2],para[3],para[4],para[5],para[6],para[7])
			except:
				from traceback import format_exc
				L4log("Error2:",format_exc() )
				try:
					open(CrashFile,"w").write(format_exc())
				except:
					pass
			Brief2.task_done() 

class L4LWorker3(Thread): 
	def __init__(self,index,s,session):
		Thread.__init__(self)
		self.index = index
		self.session = session
		self.s = s
 
	def run(self): 
		while True:
			try:
				para = Brief3.get()
#				print "2:",para[0]
				if len(para) == 2:
					para[0](para[1])
				elif len(para) == 4:
					para[0](para[1],para[2],para[3])
				elif len(para) == 5:
					para[0](para[1],para[2],para[3],para[4])
				elif len(para) == 3:
					para[0](para[1],para[2])
				elif len(para) == 7:
					para[0](para[1],para[2],para[3],para[4],para[5],para[6])
				elif len(para) == 8:
					para[0](para[1],para[2],para[3],para[4],para[5],para[6],para[7])
			except:
				from traceback import format_exc
				L4log("Error3:",format_exc() )
				try:
					open(CrashFile,"w").write(format_exc())
				except:
					pass
			Brief3.task_done() 

class L4LWorkerLCD(Thread): 
	def __init__(self,index,s,session):
		Thread.__init__(self)
		self.index = index
		self.session = session
		self.s = s
 
	def run(self): 
		global FritzTime
		while True:
			zahl = BriefLCD.get()
			if zahl == 1:
				ergebnis = self.GeneratePicture(self.index)
 
			BriefLCD.task_done() 
 
	def GeneratePicture(self,i): 
		L4logE("Run Worker Pic",i)
		gc.disable()
		LCD4linuxPICThread(self.s,self.session)
		gc.enable()
		L4logE("Done Worker Pic",i)
		return "ok"

class L4LWorker(Thread): 
	QuickRunning = False
	def __init__(self,index,s,session):
		Thread.__init__(self)
		self.index = index
		self.session = session
		self.s = s
 
	def run(self): 
		global FritzTime
		while True:
			zahl = Briefkasten.get()
			if zahl == 1:
				pass
			elif zahl == 2:
				doGrab(self.index,LCD4linux.OSDfast.value, LCD4linux.OSDsize.value)
			elif zahl == 3:
				if (LCD4linux.Fritz.value != "0" or LCD4linux.MPFritz.value != "0" or LCD4linux.StandbyFritz.value != "0"):
					if os.path.isfile(Fritz):
						FritzList.append(open(Fritz,"r").read().split(";"))
						rmFile(Fritz)
						rmFile(PICfritz)
						FritzTime = int(LCD4linux.FritzTime.value) + 2
						while len(FritzList) > 20:
							del FritzList[0]
						ergebnis = self.GeneratePicture(self.index)
			elif zahl == 4:
				self.runICS()
			elif zahl == 5:
				self.hookWebif()
			elif zahl == 6:
				self.runMail()
			elif zahl == 7:
				if QuickList != [[],[],[]] and L4LWorker.QuickRunning == False and ThreadRunning == 0 and OSDon == 0 and FritzTime == 0:
					self.QuickBild(self.s)
			elif zahl == 8:
				ICSdownloads()
 
			Briefkasten.task_done() 

	def getICS(self,name,col):
		global ICS
		global ICSlist
		if len(name)<3 or "..." in name:
			L4logE("ignore ICS",name)
			return
		try:
			r=None
			rs=""
			try:
				if name.startswith("http") and len(name) > 10:
					r=urllib2.urlopen(name, timeout = 10)
				elif os.path.isfile(name):
					r=open(name,"rb")
				else:
					L4log("Error: no ICS found",name)
					return
			except:
				L4log("Error: ICS Open",name)
				return
			if r is not None:
				L4log("Read ICS",name)
				try:
					rs = r.read()
					r.close()
					ICSlist.append([rs,col])
					return
				except:
					L4log("Error: ICS not readable!",name)
					return
			else:
				L4logE("Error Read ICS",name)

		except:
			from traceback import format_exc
			L4log("Error ICS",name)
			L4log("Error:",format_exc() )
			try:
				open(CrashFile,"w").write(format_exc())
			except:
				pass

	def runICS(self):
		global ICSrunning
		global PICcal
		if ICSrunning == True:
			L4log("Block ICS...")
			return
		ICSrunning = True
		L4log("Reading ICS...")
		for dics in glob.glob(os.path.join(LCD4linux.CalPath.value,"*.ics")):
			self.getICS(dics,0)
		self.getICS(LCD4linux.CalHttp.value,1)
		self.getICS(LCD4linux.CalHttp2.value,2)
		self.getICS(LCD4linux.CalHttp3.value,3)
		ICSdownloads()
		PICcal=None
		ICSrunning = False
	
	def hookWebif(self):
		InitWebIF()
	
	def runMail(self):
		global PopMail
		global PopMailUid
		import poplib
		import imaplib
		
		def MailDecode(Sdecode):
			try:
				H = decode_header(Sdecode)
				W = ""
				for HH in H:
					if HH[1] == None:
						W += HH[0]
					else:
						W += HH[0].decode(HH[1])
			except:
				L4logE("Info, can not decode:",Sdecode)
				W = Sdecode
			return W

		S = [LCD4linux.Mail1Pop.value,LCD4linux.Mail2Pop.value,LCD4linux.Mail3Pop.value,LCD4linux.Mail4Pop.value,LCD4linux.Mail5Pop.value]
		U = [LCD4linux.Mail1User.value,LCD4linux.Mail2User.value,LCD4linux.Mail3User.value,LCD4linux.Mail4User.value,LCD4linux.Mail5User.value]
		P = [LCD4linux.Mail1Pass.value,LCD4linux.Mail2Pass.value,LCD4linux.Mail3Pass.value,LCD4linux.Mail4Pass.value,LCD4linux.Mail5Pass.value]
		C = [LCD4linux.Mail1Connect.value,LCD4linux.Mail2Connect.value,LCD4linux.Mail3Connect.value,LCD4linux.Mail4Connect.value,LCD4linux.Mail5Connect.value]
		if P == ["","","","",""]:
			return
		if int(strftime("%H")) == 0:
			PopMailUid = [["","",""],["","",""],["","",""],["","",""],["","",""]]
		for i in range(0,5):
			if len(PopMail[i]) > 0 and PopMail[i][0][2]<>"":
				PopMailUid[i][1] = PopMail[i][0][2]
		PopMail = [[],[],[],[],[],"Run"]
		for i in range(0,5):
			if S[i].find(".")<S[i].rfind("."):
				L4log("Mailserver",S[i])
				if C[i] in ["0","1"]:
					try:
						if C[i] == "0":
							mailserver = poplib.POP3_SSL(S[i])
						elif C[i] == "1":
							mailserver = poplib.POP3(S[i])
					except:
						L4log("Error:",S[i])
						PopMail[i].append(["Server Error","",""])
						continue
					try:
						ret=mailserver.user(U[i].split(":")[-1])
						L4log(ret)
						if ret.upper().find("OK")>=0:
							ret=mailserver.pass_(P[i])
							L4log(ret)
						PopMailUid[i][2] = ret
					except:
						L4log("Error:",U[i])
						PopMail[i].append(["User Error","",""])
						continue
					try:
						L4logE(mailserver.stat())
						for M in range(1,int(mailserver.stat()[0])+1):
							From = ""
							Subj = ""
							for R in mailserver.retr(M)[1]:
								if R.upper().startswith("FROM:"):
									From = R[R.find(" "):].strip()
								elif R.upper().startswith("SUBJECT:"):
									Subj = R[R.find(" "):].strip()
								if From != "" and Subj != "":
									break
							Subj = MailDecode(Subj)
							From = MailDecode(From)
							L4logE([From,Subj,mailserver.uidl()[1][M-1].split()[1]])
							PopMail[i].append([From,Subj,mailserver.uidl()[1][M-1].split()[1]])
					except:
						L4log("Mail Error:",U[i])
						PopMail[i].append(["Mail Error","",""])
						from traceback import format_exc
						L4log("Error:",format_exc() )
#						try:
#							open(CrashFile,"w").write(format_exc())
#						except:
#							pass
						continue
					try:
						mailserver.quit()
						del mailserver
					except:
						L4Log("Mail-Error Quit")
				elif C[i] in ["2","3"]:
					try:
						if C[i] == "2":
							mailserver = imaplib.IMAP4_SSL(S[i])
						elif C[i] == "3":
							mailserver = imaplib.IMAP4(S[i])
					except:
						L4log("Error:",S[i])
						PopMail[i].append(["Server Error","",""])
						continue
					try:
						ret = mailserver.login(U[i].split(":")[-1], P[i])
						L4log(ret)
						PopMailUid[i][2] = ret
					except:
						L4log("Error:",U[i])
						PopMail[i].append(["User Error","",""])
						continue
					try:
						mailserver.select('inbox')
						typ, data = mailserver.search(None, 'ALL')
						ids = data[0]
						id_list = ids.split()
						if len(id_list)>0:
							latest_email_id = int( id_list[-1] )
							L4logE(typ, data)
							for M in range(1,int(latest_email_id)+1):
								From = ""
								Subj = ""
								ID = ""
								typ, data = mailserver.fetch( str(M), '(RFC822)' )
								for response_part in data:
									if isinstance(response_part, tuple):
										msg = email.message_from_string(response_part[1])
										Subj = msg['subject']
										From = msg['from']
										ID = msg["Message-ID"]
								Subj = MailDecode(Subj)
								From = MailDecode(From)
								L4logE([From,Subj,ID])
								PopMail[i].append([From,Subj,ID])
					except:
						L4log("Mail Error:",U[i])
						PopMail[i].append(["Mail Error","",""])
						from traceback import format_exc
						L4log("Error:",format_exc() )
#						try:
#							open(CrashFile,"w").write(format_exc())
#						except:
#							pass
						continue
					try:
						mailserver.close()
						del mailserver
					except:
						L4Log("Mail-Error Close")

				if len(PopMail[i]) > 0:
					PopMail[i] = list(reversed(PopMail[i]))
					L4logE("currend ID",PopMailUid[i][0])
					if PopMailUid[i][0] == "" or not (PopMailUid[i][0] in (e[2] for e in PopMail[i]) ):
						if len(PopMail[i]) > 1 or PopMailUid[i][0] != "-":
							PopMailUid[i][0] = PopMail[i][0][2]
							L4logE("new ID",PopMailUid[i][0])
				else:
					PopMailUid[i][0] = "-"
		PopMail[5]=""

	def QuickLoad(self,s,Pim,P0,P1,P2,P3,P4):
		ShowPicture = getShowPicture(P0,0)
		if os.path.isfile(ShowPicture):
			try:
				Pimg = Image.open(ShowPicture)
				Pimg = Pimg.resize((P3, P4))
				s.im[Pim].paste(Pimg,(P1,P2))
				Pimg=None
			except:
				L4log("Error Quick Pic")

	def QuickBild(self,s):
		pt = time()
		L4LWorker.QuickRunning = True
		try:
			if len(QuickList[0]) > 0:
				if s.im[1] != None:
					for P in QuickList[0]:
						Brief1.put([self.QuickLoad,s,1,P[0],P[1],P[2],P[3],P[4]])
					Brief1.join()
					Brief1.put([writeLCD1,s,1,LCD4linux.BilderJPEGQuick.value,False])
			if len(QuickList[1]) > 0:
				if s.im[2] != None:
					for P in QuickList[1]:
						Brief2.put([self.QuickLoad,s,2,P[0],P[1],P[2],P[3],P[4]])
					Brief2.join()
					Brief2.put([writeLCD2,s,2,LCD4linux.BilderJPEGQuick.value,False])
			if len(QuickList[2]) > 0:
				if s.im[3] != None:
					for P in QuickList[2]:
						Brief2.put([self.QuickLoad,s,3,P[0],P[1],P[2],P[3],P[4]])
					Brief3.join()
					Brief3.put([writeLCD3,s,3,LCD4linux.BilderJPEGQuick.value,False])
			Brief1.join()
			Brief2.join()
			Brief3.join()
			L4LWorker.QuickRunning = False
			L4log("QuickTime: %.3f " % (time()-pt))
		except:
			L4LWorker.QuickRunning = False
			from traceback import format_exc
			L4log("QuickPic Error:",format_exc() )
			try:
				open(CrashFile,"w").write(format_exc())
			except:
				pass

class LCDdisplayMenu(Screen):
	skin = """
		<screen position="center,center" size="600,380" title="LCD4linux - Config" >
			<widget name="menu" position="10,20" size="580,350" scrollbarMode="showOnDemand" />
		</screen>"""

	def __init__(self, session, args = None):
		Screen.__init__(self, session)
		self.session = session

		self.list = []
		self.SetList()
		self["menu"] = MenuList(self.list)
		self["actions"] = ActionMap(["OkCancelActions","ColorActions"], 
		{
			"ok": self.keyOK,
			"cancel": self.cancel,
			"red": self.entfernen
		}, -1)

	def SetList(self):
		self.list = []
		self.list.append((_("Load Active Config-File"), "LoadConfig", ""))
		self.list.append((_("Load Defaults"), "LoadDefault", ""))
		self.list.append((_("Save Config to File... (%s)") % LCD4linux.ConfigPath.value, "SaveToConfig", ""))
		Cdir = glob.glob(os.path.join(LCD4linux.ConfigPath.value,"*.lcd"))
		Cdir.sort()
		xx = 3
		for ii in Cdir:
			self.list.append((_("Load File : %s") % os.path.basename(ii), "LoadFile %d" % xx, ii))
			xx += 1

	def entfernen(self):
		current = self["menu"].getCurrent()
		if current:
			currentEntry = current[1]
			if currentEntry.startswith("LoadFile") and current[0].find(" : ")>0:
				if os.path.isfile(current[2]):
					self.session.openWithCallback(self.askForDelete, MessageBox, _("Delete File?"),type = MessageBox.TYPE_YESNO,timeout = 60)

	def keyOK(self):
		current = self["menu"].getCurrent()
		if current:
			currentEntry = current[1]
			L4log(currentEntry) 
			if currentEntry == "LoadConfig":
				if os.path.isfile(LCD4config):
					L4log("Config-Load",LCD4config) 
					LCD4linux.loadFromFile(LCD4default)
					LCD4linux.loadFromFile(LCD4config)
					LCD4linux.load()
			elif currentEntry == "SaveToConfig":
				self.session.openWithCallback(self.askForConfigName,InputBox, title="Save Filename", text="LCD4linux-%s" % (strftime("%Y%m%d_%H%M")), type=Input.TEXT)
			elif currentEntry.startswith("LoadFile"):
				if os.path.isfile(current[2]):
					P1=LCD4linux.ConfigPath.value
					P2=LCD4linux.PiconPath.value
					P3=LCD4linux.PiconPathAlt.value
					P4=LCD4linux.PiconCache.value
					P5=LCD4linux.WetterPath.value
					if os.path.isfile(LCD4default):
						LCD4linux.loadFromFile(LCD4default)
					L4log("Config-Load",current[2]) 
					LCD4linux.loadFromFile(current[2])
					LCD4linux.load()
					LCD4linux.ConfigPath.value=P1
					LCD4linux.PiconPath.value=P2
					LCD4linux.PiconPathAlt.value=P3
					LCD4linux.PiconCache.value=P4
					LCD4linux.WetterPath.value=P5
			elif currentEntry == "LoadDefault":
				if os.path.isfile(LCD4default):
					L4log("Config-Load",LCD4default) 
					LCD4linux.loadFromFile(LCD4default)
					LCD4linux.load()

	def askForConfigName(self,name):
		if name is not None and os.path.isdir(LCD4linux.ConfigPath.value):
			LCD4linux.save()
			LCD4linux.saveToFile(os.path.join(LCD4linux.ConfigPath.value,name + ".lcd"))
			self.list.append((_("Load File : %s") % (name+".lcd"), "LoadFile", os.path.join(LCD4linux.ConfigPath.value,name + ".lcd")))


	def askForDelete(self,retval):
		if (retval):
			current = self["menu"].getCurrent()
			if current:
				if os.path.isfile(current[2]):
					currentEntry = current[1]
					i = int(currentEntry.split()[1])
					self.list[i] = (_("deleted"),) + self.list[i][1:]
					rmFile(current[2])

	def cancel(self):
		self.close(False,self.session)

	def selectionChanged(self):
		a=0

class LCDdisplayFile(Screen):
	skin = """
		<screen position="center,center" size="620,460" title="Select File/Dir...">
			<widget source="File" render="Label" font="Regular;20" halign="center" position="5,0" size="610,100" transparent="1" valign="center" zPosition="4"/>
			<widget name="LCDfile" position="5,100" scrollbarMode="showOnDemand" size="610,312" zPosition="4"/>
			<eLabel backgroundColor="#555555" position="5,420" size="610,2" zPosition="5"/>
			<ePixmap alphatest="on" pixmap="skin_default/buttons/green.png" position="0,425" size="140,40" zPosition="5"/>
			<eLabel font="Regular;18" halign="center" position="0,425" size="140,40" text="Select" transparent="1" valign="center" zPosition="6"/>
		</screen>"""

	def __init__(self, session, FileName = "/tmp/none", showFiles = True, text = "Text", matchingPattern = None):
		Screen.__init__(self, session)
		self.sesion = session
		if not FileName.startswith("/"):
			FileName = "/"+FileName
		self["File"] = StaticText(_("currently set : %s") % FileName)
		self["LCDfile"] = myFileList(FileName, showDirectories = True, showFiles = showFiles, useServiceRef = False, matchingPattern = matchingPattern)
		self["actions"] = ActionMap(["WizardActions", "ColorActions"],
		{
			"ok": self.ok,
			"back": self.NothingToDo,
			"green": self.SelectFile,
			"yellow": self.SelectFile
		}, -1)
		self.onLayoutFinish.append(self.OneDescent)

	def OneDescent(self):
		if self["LCDfile"].canDescent():
			self["LCDfile"].descent()
	
	def ok(self):
		if self["LCDfile"].canDescent():
			self["LCDfile"].descent()

	def NothingToDo(self):
		self.close("","")

	def SelectFile(self):
		dest = ""
		dest1 = ""
		if self["LCDfile"].getSelectionIndex()!=0:
			dest = self["LCDfile"].getCurrentDirectory()
			dest1 = self["LCDfile"].getFilename()
		self.close(dest,dest1)

class LCDdisplayConfig(ConfigListScreen,Screen):
	skin = ""
		
	def __init__(self, session, args = 0):
		global ConfigMode
		global OSDon
		size_w = getDesktop(0).size().width()-100
		size_h = getDesktop(0).size().height()-100 #870x400 conf 600x328 (25*Lines)
		if size_w<700:
			size_w = 600
		self.ConfLines = (size_h-72)//25 
		conf_h = self.ConfLines*25
		int_y = size_h-65
		key_y = size_h-40
		pic_w = size_w-600
		if LCD4linux.LCDType3.value != "00":
			pic_h = int(size_h/3)
		else:
			pic_h = int(size_h/2)
		pic_h2 = pic_h*2
		skin = """
			<screen position="center,%d" size="%d,%d" title="LCD4linux Settings" >
			<widget name="config" position="0,0" size="600,%d" scrollbarMode="showOnDemand" enableWrapAround="1" />
			<widget source="introduction" render="Label" position="5,%d" size="580,30" zPosition="10" font="Regular;21" halign="center" valign="center" backgroundColor="#25062748" transparent="1" />
			
			<widget name="key_red" position="0,%d" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;18" transparent="1"/> 
			<widget name="key_green" position="140,%d" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;18" transparent="1"/> 
			<widget name="key_yellow" position="280,%d" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;18" transparent="1"/> 
			<widget name="key_blue" position="420,%d" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="white" font="Regular;18" transparent="1"/> 

			<ePixmap name="red"    position="0,%d"   zPosition="2" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
			<ePixmap name="green"  position="140,%d" zPosition="2" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
			<ePixmap name="yellow" position="280,%d" zPosition="2" size="140,40" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on" />
			<ePixmap name="blue"   position="420,%d" zPosition="2" size="140,40" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/key_menu.png" position="560,%d" zPosition="4" size="35,25"  transparent="1" alphatest="on" />

			<widget source="Version" render="Label" position="500,%d" size="100,20" zPosition="1" font="Regular;11" halign="right" valign="center" backgroundColor="#25062748" transparent="1" />
			<widget source="LibUSB" render="Label" position="500,%d" size="100,20" zPosition="1" font="Regular;11" halign="right" valign="center" foregroundColor="red" backgroundColor="#25062748" transparent="1" />
			<widget source="About" render="Label" position="500,%d" size="100,20" zPosition="1" font="Regular;10" halign="right" valign="center" backgroundColor="#25062748" transparent="1" />

			<widget name="LCD1" position="600,0" zPosition="1" size="%d,%d" transparent="1" alphatest="on" />
			<widget name="LCD2" position="600,%d" zPosition="1" size="%d,%d" transparent="1" alphatest="on" />
			<widget name="LCD3" position="600,%d" zPosition="1" size="%d,%d" transparent="1" alphatest="on" />
			<widget source="LCD1text" render="Label" position="600,5" size="200,20" zPosition="1" font="Regular;11" halign="left" valign="center" backgroundColor="#25062748" transparent="1" />
			<widget source="LCD2text" render="Label" position="600,%d" size="200,20" zPosition="1" font="Regular;11" halign="left" valign="center" backgroundColor="#25062748" transparent="1" />
			<widget source="LCD3text" render="Label" position="600,%d" size="200,20" zPosition="1" font="Regular;11" halign="left" valign="center" backgroundColor="#25062748" transparent="1" />
			
			</screen>""" % (75, size_w,size_h, conf_h, int_y, key_y,key_y,key_y,key_y, key_y,key_y,key_y,key_y,
			key_y+15, key_y-10,key_y-30,key_y-30,  pic_w,pic_h, pic_h,pic_w,pic_h, pic_h2,pic_w,pic_h, pic_h+5, pic_h2+5 )
		self.skin = skin
		self.session = session
		Screen.__init__(self, session)
		L4log("init Start")
		ConfigMode = True
		OSDon = 0
		getBilder()
		self.SavePiconSize = LCD4linux.PiconSize.value
		self.SavePiconFullScreen = LCD4linux.PiconFullScreen.value
		self.SavePiconTransparenz = LCD4linux.PiconTransparenz.value
		self.SaveWetter = LCD4linux.WetterCity.value
		self.SaveWetter2 = LCD4linux.Wetter2City.value
		self.SaveMeteo = LCD4linux.MeteoURL.value
		self.SaveMeteoType = LCD4linux.MeteoType.value
		self.SaveMeteoZoom = LCD4linux.MeteoZoom.value
		self.SaveStandbyMeteoType = LCD4linux.StandbyMeteoType.value
		self.SaveStandbyMeteoZoom = LCD4linux.StandbyMeteoZoom.value
		self.SaveScreenActive = LCD4linux.ScreenActive.value
		self.SavePicture = LCD4linux.SavePicture.value
		self.WWWischanged = False
		self.Aktuell = " "
		self.LastSelect = "   "
		self.LastSelectT = ""
		self.SaveisMediaPlayer = isMediaPlayer
		self.list = []
		self.mtime1 = 0.0
		self.mtime2 = 0.0
		self.mtime3 = 0.0
		if os.path.isfile("/etc/enigma2/skin_user.xml"):
			xmlRead()
			LCD4linux.xmlType01.value = False if xmlFind(1) == -1 else True
			LCD4linux.xmlType02.value = False if xmlFind(2) == -1 else True
			LCD4linux.xmlType03.value = False if xmlFind(3) == -1 else True
			xmlClear()

		self.toggle = time()
	
		self.picload = ePicLoad()
		self.picload.PictureData.get().append(self.setPictureCB)		
		sc = AVSwitch().getFramebufferScale()
		self.picload.setPara((pic_w, pic_h, sc[0], sc[1], False, 1, '#00000000'))
		
		self.picload2 = ePicLoad()
		self.picload2.PictureData.get().append(self.setPictureCB2)		
		sc = AVSwitch().getFramebufferScale()
		self.picload2.setPara((pic_w, pic_h, sc[0], sc[1], False, 1, '#00000000'))

		self.picload3 = ePicLoad()
		self.picload3.PictureData.get().append(self.setPictureCB3)		
		sc = AVSwitch().getFramebufferScale()
		self.picload3.setPara((pic_w, pic_h, sc[0], sc[1], False, 1, '#00000000'))

		ConfigListScreen.__init__(self, self.list, on_change = self.selectionChanged)

		self.PicTimer = eTimer()
		self.PicTimer.callback.append(self.showpic)

		self["introduction"] = StaticText()
		self["Version"] = StaticText(Version if L4LVtest(Version)==True else Version+"?")
		self["LibUSB"] = StaticText()
		self["About"] = StaticText()
		self["LCD1"] = Pixmap()
		self["LCD2"] = Pixmap()
		self["LCD3"] = Pixmap()
		self["LCD1text"] = StaticText()
		self["LCD2text"] = StaticText()
		self["LCD3text"] = StaticText()

		self["key_red"] = Button(_("Cancel"))
		self["key_green"] = Button(_("Save"))
		self["key_yellow"] = Button(_("Restart Displays"))
		self["key_blue"] = Button("")
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "MenuActions", "EPGSelectActions", "HelpActions","InfobarSeekActions"],
		{
			"red": self.cancel,
			"green": self.save,
			"yellow": self.LCDrestart,
			"blue": self.Page,
			"nextBouquet": self.KeyUp,
			"prevBouquet": self.KeyDown,
 			"save": self.save,
			"cancel": self.cancel,
			"menu": self.SetupMenu,
			"displayHelp": self.Exchange,
			"ok": self.keyOK,
			"seekFwd": self.NextScreenKey,
			"info": self.ResetInfos
		}, -1)
		self.mode = "On"
		self.LastSelect="1"
		self.SetList()
		self.mode = "Media"
		self.LastSelect="2"
		self.SetList()
		self.mode = "Idle"
		self.LastSelect="3"
		self.SetList()
		self.mode = "Global"
		self.LastSelect="4"
		self.SetList()
		self.mode = "Idle"
		self.LastSelect="5"
		self.Page()
		self.selectionChanged()
		if not self.selectionChanged in self["config"].onSelectionChanged:
			self["config"].onSelectionChanged.append(self.selectionChanged)
		if LCD4linux.LCDType3.value == "00":
			self["LCD3"].hide()
		if getDesktop(0).size().width() < 1000:
			self["LCD1"].hide()
			self["LCD2"].hide()
			self["LCD3"].hide()
		else:
			self.onLayoutFinish.append(self.showpic)
		self.onLayoutFinish.append(self.layoutFinished)
		L4log("init Ende")

	def layoutFinished(self):
		self["config"].l.setSeperation(int(self["config"].l.getItemSize().width()*.7)) # use 30% of list width for sliders

	def NextScreenKey(self):
		NextScreen(True)

	def ResetInfos(self):
		global FritzList
		global PopMailUid
		FritzList = []
		PopMailUid = [["","",""],["","",""],["","",""],["","",""],["","",""]]
		if Briefkasten.qsize()<=3:
			Briefkasten.put(6) 

	def showpic(self):
		self.PicTimer.stop()
		ff=False
		fn=PIC+".jpg"
		try:
			if os.path.isfile(fn):
				ft=os.stat(fn).st_mtime
				ff=True
				if ft != self.mtime1:
					self.picload.startDecode(fn)
					self.mtime1=ft
			else:
				fn=PIC+".png"
				ft=0.0
				if os.path.isfile(fn):
					ft=os.stat(fn).st_mtime
					ff=True
					if ft != self.mtime1:
						self.picload.startDecode(fn)
						self.mtime1=ft
		except:
			L4log("Error Pic1 not found")
		if ff==False:
			self["LCD1text"].setText(_("no LCD1 Picture-File"))
			self["LCD1"].hide()
		else:
			self["LCD1text"].setText("")
		ff=False
		fn=PIC2+".jpg"
		try:
			if os.path.isfile(fn):
				ft=os.stat(fn).st_mtime
				ff=True
				if ft != self.mtime2:
					self.picload2.startDecode(fn)
					self.mtime2=ft
			else:
				fn=PIC2+".png"
				ft=0.0
				if os.path.isfile(fn):
					ft=os.stat(fn).st_mtime
					ff=True
					if ft != self.mtime2:
						self.picload2.startDecode(fn)
						self.mtime2=ft
		except:
			L4log("Error Pic2 not found")
		if ff==False:
			self["LCD2text"].setText(_("no LCD2 Picture-File"))
			self["LCD2"].hide()
		else:
			self["LCD2text"].setText("")
		if LCD4linux.LCDType3.value != "00":
			ff=False
			fn=PIC3+".jpg"
			try:
				if os.path.isfile(fn):
					ft=os.stat(fn).st_mtime
					ff=True
					if ft != self.mtime3:
						self.picload3.startDecode(fn)
						self.mtime3=ft
				else:
					fn=PIC3+".png"
					ft=0.0
					if os.path.isfile(fn):
						ft=os.stat(fn).st_mtime
						ff=True
						if ft != self.mtime3:
							self.picload3.startDecode(fn)
							self.mtime3=ft
			except:
				L4log("Error Pic3 not found")
			if ff==False:
				self["LCD3text"].setText(_("no LCD3 Picture-File"))
				self["LCD3"].hide()
			else:
				self["LCD3text"].setText("")
		self.PicTimer.start(500,True)

	def setPictureCB(self, picInfo = None):
		ptr = self.picload.getData()
		if ptr is not None:
			self["LCD1"].instance.setPixmap(ptr)
			self["LCD1"].show()

	def setPictureCB2(self, picInfo = None):
		ptr = self.picload2.getData()
		if ptr is not None:
			self["LCD2"].instance.setPixmap(ptr)
			self["LCD2"].show()
 
	def setPictureCB3(self, picInfo = None):
		ptr = self.picload3.getData()
		if ptr is not None:
			self["LCD3"].instance.setPixmap(ptr)
			self["LCD3"].show()

	def SetupMenu(self):
		self.session.open(LCDdisplayMenu)

	def Exchange(self):
		Exchange()
		
	def SetList(self):
		L4log("SetList",self.mode)
		if (self.Aktuell.startswith("-") or self.LastSelectT == self.LastSelect) and not self.Aktuell.startswith("-  "):
			return
		self.LastSelectT = self.LastSelect
		if self.mode == "Global":
			self.list1 = []
			self.list1.append(getConfigListEntry(_("LCD4linux enabled"), LCD4linux.Enable))
			self.list1.append(getConfigListEntry(_("LCD 1 Type"), LCD4linux.LCDType1))
			self.list1.append(getConfigListEntry(_("- LCD 1 Rotate"), LCD4linux.LCDRotate1))
			self.list1.append(getConfigListEntry(_("- LCD 1 Background Color"), LCD4linux.LCDColor1))
			self.list1.append(getConfigListEntry(_("- LCD 1 Background-Picture [ok]>"), LCD4linux.LCDBild1))
			self.list1.append(getConfigListEntry(_("- LCD 1 Brightness [no SPF]"), LCD4linux.Helligkeit))
			self.list1.append(getConfigListEntry(_("- LCD 1 Refresh"), LCD4linux.LCDRefresh1))
			self.list1.append(getConfigListEntry(_("LCD 2 Type"), LCD4linux.LCDType2))
			if LCD4linux.LCDType2.value != "00":
				self.list1.append(getConfigListEntry(_("- LCD 2 Rotate"), LCD4linux.LCDRotate2))
				self.list1.append(getConfigListEntry(_("- LCD 2 Background Color"), LCD4linux.LCDColor2))
				self.list1.append(getConfigListEntry(_("- LCD 2 Background-Picture [ok]>"), LCD4linux.LCDBild2))
				self.list1.append(getConfigListEntry(_("- LCD 2 Brightness [no SPF]"), LCD4linux.Helligkeit2))
				self.list1.append(getConfigListEntry(_("- LCD 2 Refresh"), LCD4linux.LCDRefresh2))
			self.list1.append(getConfigListEntry(_("LCD 3 Type"), LCD4linux.LCDType3))
			if LCD4linux.LCDType3.value != "00":
				self.list1.append(getConfigListEntry(_("- LCD 3 Rotate"), LCD4linux.LCDRotate3))
				self.list1.append(getConfigListEntry(_("- LCD 3 Background Color"), LCD4linux.LCDColor3))
				self.list1.append(getConfigListEntry(_("- LCD 3 Background-Picture [ok]>"), LCD4linux.LCDBild3))
				self.list1.append(getConfigListEntry(_("- LCD 3 Brightness [no SPF]"), LCD4linux.Helligkeit3))
				self.list1.append(getConfigListEntry(_("- LCD 3 Refresh"), LCD4linux.LCDRefresh3))
			if LCD4linux.LCDType1.value[0] == "5" or LCD4linux.LCDType2.value[0] == "5" or LCD4linux.LCDType3.value[0] == "5":
				self.list1.append(getConfigListEntry(_("Box-Skin-LCD Dimension"), LCD4linux.xmlLCDType))
				self.list1.append(getConfigListEntry(_("Box-Skin-LCD Color"), LCD4linux.xmlLCDColor))
				self.list1.append(getConfigListEntry(_("Box-Skin-LCD Enable On-Mode"), LCD4linux.xmlType01))
				self.list1.append(getConfigListEntry(_("Box-Skin-LCD Enable Media-Mode"), LCD4linux.xmlType02))
				self.list1.append(getConfigListEntry(_("Box-Skin-LCD Enable Idle-Mode"), LCD4linux.xmlType03))
			self.list1.append(getConfigListEntry(_("OSD [display time]"), LCD4linux.OSD))
			if LCD4linux.OSD.value != "0":
				self.list1.append(getConfigListEntry(_("- which LCD"), LCD4linux.OSDLCD))
				self.list1.append(getConfigListEntry(_("- Show in Mode"), LCD4linux.OSDshow))
				self.list1.append(getConfigListEntry(_("- OSD Size"), LCD4linux.OSDsize))
				self.list1.append(getConfigListEntry(_("- Background/Transparency"), LCD4linux.OSDTransparenz))
				self.list1.append(getConfigListEntry(_("- Fast Grab lower quality"), LCD4linux.OSDfast))
			self.list1.append(getConfigListEntry(_("Popup Text"), LCD4linux.Popup))
			if LCD4linux.Popup.value != "0":
				self.list1.append(getConfigListEntry(_("- which LCD"), LCD4linux.PopupLCD))
				self.list1.append(getConfigListEntry(_("- Font Size"), LCD4linux.PopupSize))
				self.list1.append(getConfigListEntry(_("- Position"), LCD4linux.PopupPos))
				self.list1.append(getConfigListEntry(_("- Alignment"), LCD4linux.PopupAlign))
				self.list1.append(getConfigListEntry(_("- Color"), LCD4linux.PopupColor))
				self.list1.append(getConfigListEntry(_("- Background Color"), LCD4linux.PopupBackColor))
#			if LCD4linux.LCDType1.value[0] == "4" or LCD4linux.LCDType2.value[0] == "4":
#				self.list1.append(getConfigListEntry(_("Internal TFT Active"), LCD4linux.LCDTFT))
			self.list1.append(getConfigListEntry(_("Active Screen"), LCD4linux.ScreenActive))
			self.list1.append(getConfigListEntry(_("Screens used for Changing"), LCD4linux.ScreenMax))
			self.list1.append(getConfigListEntry(_("Screen 1 Changing Time"), LCD4linux.ScreenTime))
			if LCD4linux.ScreenTime.value != "0":
				self.list1.append(getConfigListEntry(_("- Screen 2 Changing Time"), LCD4linux.ScreenTime2))
				self.list1.append(getConfigListEntry(_("- Screen 3 Changing Time"), LCD4linux.ScreenTime3))
				self.list1.append(getConfigListEntry(_("- Screen 4 Changing Time"), LCD4linux.ScreenTime4))
				self.list1.append(getConfigListEntry(_("- Screen 5 Changing Time"), LCD4linux.ScreenTime5))
				self.list1.append(getConfigListEntry(_("- Screen 6 Changing Time"), LCD4linux.ScreenTime6))
				self.list1.append(getConfigListEntry(_("- Screen 7 Changing Time"), LCD4linux.ScreenTime7))
				self.list1.append(getConfigListEntry(_("- Screen 8 Changing Time"), LCD4linux.ScreenTime8))
				self.list1.append(getConfigListEntry(_("- Screen 9 Changing Time"), LCD4linux.ScreenTime9))
			self.list1.append(getConfigListEntry(_("Picture Changing Time"), LCD4linux.BilderTime))
			self.list1.append(getConfigListEntry(_("Picture Sort"), LCD4linux.BilderSort))
			self.list1.append(getConfigListEntry(_("Picture Directory Recursive"), LCD4linux.BilderRecursiv))
			self.list1.append(getConfigListEntry(_("Picture Quality for Resizing"), LCD4linux.BilderQuality))
#			self.list1.append(getConfigListEntry(_("Picture JPEG-Quality [%]"), LCD4linux.BilderJPEG))
			self.list1.append(getConfigListEntry(_("Picture Quick Update Time [s]"), LCD4linux.BilderQuick))
#			self.list1.append(getConfigListEntry(_("Picture Quick JPEG-Quality [%]"), LCD4linux.BilderJPEGQuick))
			self.list1.append(getConfigListEntry(_("Picture Type [only Picture]"), LCD4linux.BilderTyp))
			self.list1.append(getConfigListEntry(_("Background-Picture Type"), LCD4linux.BilderBackground))
			self.list1.append(getConfigListEntry(_("Weather City"), LCD4linux.WetterCity))
			self.list1.append(getConfigListEntry(_("Weather City 2"), LCD4linux.Wetter2City))
			self.list1.append(getConfigListEntry(_("Weather-Icon-Path [ok]>"), LCD4linux.WetterPath))
			self.list1.append(getConfigListEntry(_("Weather-Icon Zoom"), LCD4linux.WetterIconZoom))
			self.list1.append(getConfigListEntry(_("Weather Low Temperature Color"), LCD4linux.WetterLowColor))
			self.list1.append(getConfigListEntry(_("Weather High Temperature Color"), LCD4linux.WetterHighColor))
			self.list1.append(getConfigListEntry(_("Weather Transparency"), LCD4linux.WetterTransparenz))
			self.list1.append(getConfigListEntry(_("Weather Rain Chance"), LCD4linux.WetterRain))
			self.list1.append(getConfigListEntry(_("Weather Wind speed unit"), LCD4linux.WetterWind))
			if LCD4linux.WetterRain.value != "false":
				self.list1.append(getConfigListEntry(_("- Rain Zoom"), LCD4linux.WetterRainZoom))
				self.list1.append(getConfigListEntry(_("- Rain Color"), LCD4linux.WetterRainColor))
				self.list1.append(getConfigListEntry(_("- Rain use Color 2 from"), LCD4linux.WetterRainColor2use))
				self.list1.append(getConfigListEntry(_("- Rain Color 2"), LCD4linux.WetterRainColor2))
			self.list1.append(getConfigListEntry(_("Weather Lines"), LCD4linux.WetterLine))
			self.list1.append(getConfigListEntry(_("Weather Extra Infos"), LCD4linux.WetterExtra))
			if LCD4linux.WetterExtra.value == True:
				self.list1.append(getConfigListEntry(_("- Extra Zoom"), LCD4linux.WetterExtraZoom))
				self.list1.append(getConfigListEntry(_("- Show chill temperature from difference"), LCD4linux.WetterExtraFeel))
				self.list1.append(getConfigListEntry(_("- Extra Color City"), LCD4linux.WetterExtraColorCity))
				self.list1.append(getConfigListEntry(_("- Extra Color Chill"), LCD4linux.WetterExtraColorFeel))
			self.list1.append(getConfigListEntry(_("Netatmo CO2 Min Range"), LCD4linux.NetAtmoCO2Min))
			self.list1.append(getConfigListEntry(_("Netatmo CO2 Max Range"), LCD4linux.NetAtmoCO2Max))
			self.list1.append(getConfigListEntry(_("Meteo URL"), LCD4linux.MeteoURL))
			self.list1.append(getConfigListEntry(_("Moon-Icon-Path [ok]>"), LCD4linux.MoonPath))
			self.list1.append(getConfigListEntry(_("Recording Picture [ok]>"), LCD4linux.RecordingPath))
			self.list1.append(getConfigListEntry(_("Double-button switches"), LCD4linux.KeySwitch))
			self.list1.append(getConfigListEntry(_("Key for Screen Change"), LCD4linux.KeyScreen))
			self.list1.append(getConfigListEntry(_("Key for Screen On/Off"), LCD4linux.KeyOff))
			self.list1.append(getConfigListEntry(_("FritzCall Picture Path [ok]>"), LCD4linux.FritzPath))
			self.list1.append(getConfigListEntry(_("FritzCall Number of List Entries"), LCD4linux.FritzLines))
			self.list1.append(getConfigListEntry(_("FritzCall Number of Pictures"), LCD4linux.FritzPictures))
			self.list1.append(getConfigListEntry(_("FritzCall Picture Orientation"), LCD4linux.FritzPictureType))
			self.list1.append(getConfigListEntry(_("FritzCall Pictures Search"), LCD4linux.FritzPictureSearch))
			self.list1.append(getConfigListEntry(_("FritzCall remove Calls after hours"), LCD4linux.FritzRemove))
			self.list1.append(getConfigListEntry(_("FritzCall Popup-Time"), LCD4linux.FritzTime))
			self.list1.append(getConfigListEntry(_("FritzCall Popup LCD"), LCD4linux.FritzPopupLCD))
			self.list1.append(getConfigListEntry(_("FritzCall Popup Color"), LCD4linux.FritzPopupColor))
			self.list1.append(getConfigListEntry(_("FritzCall Frame Picture [ok]>"), LCD4linux.FritzFrame))
			self.list1.append(getConfigListEntry(_("Calendar ics-Path [ok]>"), LCD4linux.CalPath))
			self.list1.append(getConfigListEntry(_("- Color"), LCD4linux.CalPathColor))
			self.list1.append(getConfigListEntry(_("Calendar ics-URL"), LCD4linux.CalHttp))
			self.list1.append(getConfigListEntry(_("- Color"), LCD4linux.CalHttpColor))
			self.list1.append(getConfigListEntry(_("Calendar ics-URL"), LCD4linux.CalHttp2))
			self.list1.append(getConfigListEntry(_("- Color"), LCD4linux.CalHttp2Color))
			self.list1.append(getConfigListEntry(_("Calendar ics-URL"), LCD4linux.CalHttp3))
			self.list1.append(getConfigListEntry(_("- Color"), LCD4linux.CalHttp3Color))
			self.list1.append(getConfigListEntry(_("Calendar planerFS"), LCD4linux.CalPlanerFS))
			self.list1.append(getConfigListEntry(_("- Color"), LCD4linux.CalPlanerFSColor))
			self.list1.append(getConfigListEntry(_("Calendar Line Thickness"), LCD4linux.CalLine))
			self.list1.append(getConfigListEntry(_("Calendar Day Event Preview"), LCD4linux.CalDays))
			self.list1.append(getConfigListEntry(_("Calendar Timezone Correction"), LCD4linux.CalTimeZone))
			self.list1.append(getConfigListEntry(_("Calendar Transparency"), LCD4linux.CalTransparenz))
			self.list1.append(getConfigListEntry(_("Calendar Poll Interval"), LCD4linux.CalTime))
			self.list1.append(getConfigListEntry(_("Tuner Color"), LCD4linux.TunerColor))
			self.list1.append(getConfigListEntry(_("Tuner Color Active"), LCD4linux.TunerColorActive))
			self.list1.append(getConfigListEntry(_("Tuner Color On"), LCD4linux.TunerColorOn))
			self.list1.append(getConfigListEntry(_("DVB-T Signal-Quality Correction"), LCD4linux.DVBTCorrection))
			self.list1.append(getConfigListEntry(_("Font global [ok]>"), LCD4linux.Font))
			self.list1.append(getConfigListEntry(_("Font 1 [ok]>"), LCD4linux.Font1))
			self.list1.append(getConfigListEntry(_("Font 2 [ok]>"), LCD4linux.Font2))
			self.list1.append(getConfigListEntry(_("Font 3 [ok]>"), LCD4linux.Font3))
			self.list1.append(getConfigListEntry(_("Mail 1 Connect"), LCD4linux.Mail1Connect))
			self.list1.append(getConfigListEntry(_("Mail 1 Server"), LCD4linux.Mail1Pop))
			self.list1.append(getConfigListEntry(_("Mail 1 [Displayname:]Username"), LCD4linux.Mail1User))
			self.list1.append(getConfigListEntry(_("Mail 1 Password"), LCD4linux.Mail1Pass))
			self.list1.append(getConfigListEntry(_("Mail 2 Connect"), LCD4linux.Mail2Connect))
			self.list1.append(getConfigListEntry(_("Mail 2 Server"), LCD4linux.Mail2Pop))
			self.list1.append(getConfigListEntry(_("Mail 2 [Displayname:]Username"), LCD4linux.Mail2User))
			self.list1.append(getConfigListEntry(_("Mail 2 Password"), LCD4linux.Mail2Pass))
			self.list1.append(getConfigListEntry(_("Mail 3 Connect"), LCD4linux.Mail3Connect))
			self.list1.append(getConfigListEntry(_("Mail 3 Server"), LCD4linux.Mail3Pop))
			self.list1.append(getConfigListEntry(_("Mail 3 [Displayname:]Username"), LCD4linux.Mail3User))
			self.list1.append(getConfigListEntry(_("Mail 3 Password"), LCD4linux.Mail3Pass))
			self.list1.append(getConfigListEntry(_("Mail 4 Connect"), LCD4linux.Mail4Connect))
			self.list1.append(getConfigListEntry(_("Mail 4 Server"), LCD4linux.Mail4Pop))
			self.list1.append(getConfigListEntry(_("Mail 4 [Displayname:]Username"), LCD4linux.Mail4User))
			self.list1.append(getConfigListEntry(_("Mail 4 Password"), LCD4linux.Mail4Pass))
			self.list1.append(getConfigListEntry(_("Mail 5 Connect"), LCD4linux.Mail5Connect))
			self.list1.append(getConfigListEntry(_("Mail 5 Server"), LCD4linux.Mail5Pop))
			self.list1.append(getConfigListEntry(_("Mail 5 [Displayname:]Username"), LCD4linux.Mail5User))
			self.list1.append(getConfigListEntry(_("Mail 5 Password"), LCD4linux.Mail5Pass))
			self.list1.append(getConfigListEntry(_("Mail Poll Interval"), LCD4linux.MailTime))
			self.list1.append(getConfigListEntry(_("Mail Show Empty Mailboxes"), LCD4linux.MailShow0))
			self.list1.append(getConfigListEntry(_("WWW Converter Poll Interval"), LCD4linux.WWWTime))
			self.list1.append(getConfigListEntry(_("WebIF Refresh [s]"), LCD4linux.WebIfRefresh))
			self.list1.append(getConfigListEntry(_("WebIF Refresh Type"), LCD4linux.WebIfType))
			self.list1.append(getConfigListEntry(_("WebIF Init Delay"), LCD4linux.WebIfInitDelay))
			self.list1.append(getConfigListEntry(_("WebIF IP Allow"), LCD4linux.WebIfAllow))
			self.list1.append(getConfigListEntry(_("WebIF IP Deny"), LCD4linux.WebIfDeny))
			self.list1.append(getConfigListEntry(_("WebIF Design"), LCD4linux.WebIfDesign))
			self.list1.append(getConfigListEntry(_("Save as Picture for WebIF"), LCD4linux.SavePicture))
			self.list1.append(getConfigListEntry(_("LCD Custom Width"), LCD4linux.SizeW))
			self.list1.append(getConfigListEntry(_("LCD Custom Height"), LCD4linux.SizeH))
			self.list1.append(getConfigListEntry(_("Timing ! calc all Times to Time/5*2 in Fastmode"), LCD4linux.FastMode))
			self.list1.append(getConfigListEntry(_("Display Delay [ms]"), LCD4linux.Delay))
			self.list1.append(getConfigListEntry(_("Threads per LCD"), LCD4linux.ElementThreads))
			self.list1.append(getConfigListEntry(_("Show Crash Corner"), LCD4linux.Crash))
			self.list1.append(getConfigListEntry(_("Show 'no ....' Messages"), LCD4linux.ShowNoMsg))
			self.list1.append(getConfigListEntry(_("Storage-Devices: Force Read"), LCD4linux.DevForceRead))
			self.list1.append(getConfigListEntry(_("Config Backup Path [ok]>"), LCD4linux.ConfigPath))
			self.list1.append(getConfigListEntry(_("Debug-Logging > /tmp/L4log.txt"), LCD4linux.EnableEventLog))
			self["config"].setList(self.list1)
		elif self.mode == "On":
			self.list2 = []
			self.list2.append(getConfigListEntry(_("- Backlight Off [disable set Off=On]"), LCD4linux.LCDoff))
			self.list2.append(getConfigListEntry(_("- Backlight On"), LCD4linux.LCDon))
			self.list2.append(getConfigListEntry(_("- Backlight Weekend Off [disable set Off=On]"), LCD4linux.LCDWEoff))
			self.list2.append(getConfigListEntry(_("- Backlight Weekend On"), LCD4linux.LCDWEon))
			self.list2.append(getConfigListEntry(_("Picon"), LCD4linux.Picon))
			if LCD4linux.Picon.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.PiconLCD))
				self.list2.append(getConfigListEntry(_("- Picon Size"), LCD4linux.PiconSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.PiconPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.PiconAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.PiconSplit))
				self.list2.append(getConfigListEntry(_("- Full Screen"), LCD4linux.PiconFullScreen))
				self.list2.append(getConfigListEntry(_("- Text Size"), LCD4linux.PiconTextSize))
				self.list2.append(getConfigListEntry(_("- Transparency"), LCD4linux.PiconTransparenz))
				self.list2.append(getConfigListEntry(_("- Picon Path [ok]>"), LCD4linux.PiconPath))
				self.list2.append(getConfigListEntry(_("- Picon Path 2 [ok]>"), LCD4linux.PiconPathAlt))
				self.list2.append(getConfigListEntry(_("- Picon Cache Path [ok]>"), LCD4linux.PiconCache))
			self.list2.append(getConfigListEntry(_("Picon 2"), LCD4linux.Picon2))
			if LCD4linux.Picon2.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.Picon2LCD))
				self.list2.append(getConfigListEntry(_("- Picon Size"), LCD4linux.Picon2Size))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.Picon2Pos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.Picon2Align))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.Picon2Split))
				self.list2.append(getConfigListEntry(_("- Full Screen"), LCD4linux.Picon2FullScreen))
				self.list2.append(getConfigListEntry(_("- Text Size"), LCD4linux.Picon2TextSize))
				self.list2.append(getConfigListEntry(_("- Picon Path [ok]>"), LCD4linux.Picon2Path))
				self.list2.append(getConfigListEntry(_("- Picon Path 2 [ok]>"), LCD4linux.Picon2PathAlt))
				self.list2.append(getConfigListEntry(_("- Picon Cache Path [ok]>"), LCD4linux.Picon2Cache))
			self.list2.append(getConfigListEntry(_("Clock"), LCD4linux.Clock))
			if LCD4linux.Clock.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.ClockLCD))
				self.list2.append(getConfigListEntry(_("-  Type"), LCD4linux.ClockType))
				if LCD4linux.ClockType.value[0] == "5":
					self.list2.append(getConfigListEntry(_("- Analog Clock"), LCD4linux.ClockAnalog))
				elif LCD4linux.ClockType.value[0] == "1":
					self.list2.append(getConfigListEntry(_("- Spacing"), LCD4linux.ClockSpacing))
				self.list2.append(getConfigListEntry(_("- Size"), LCD4linux.ClockSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.ClockPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.ClockAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.ClockSplit))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.ClockColor))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.ClockShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.ClockFont))
			self.list2.append(getConfigListEntry(_("Clock 2"), LCD4linux.Clock2))
			if LCD4linux.Clock2.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.Clock2LCD))
				self.list2.append(getConfigListEntry(_("-  Type"), LCD4linux.Clock2Type))
				if LCD4linux.Clock2Type.value[0] == "5":
					self.list2.append(getConfigListEntry(_("- Analog Clock"), LCD4linux.Clock2Analog))
				elif LCD4linux.Clock2Type.value[0] == "1":
					self.list2.append(getConfigListEntry(_("- Spacing"), LCD4linux.Clock2Spacing))
				self.list2.append(getConfigListEntry(_("- Size"), LCD4linux.Clock2Size))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.Clock2Pos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.Clock2Align))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.Clock2Split))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.Clock2Color))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.Clock2Shadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.Clock2Font))
			self.list2.append(getConfigListEntry(_("Program Name"), LCD4linux.Channel))
			if LCD4linux.Channel.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.ChannelLCD))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.ChannelSize))
				self.list2.append(getConfigListEntry(_("- maximum Lines"), LCD4linux.ChannelLines))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.ChannelPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.ChannelAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.ChannelSplit))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.ChannelColor))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.ChannelShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.ChannelFont))
			self.list2.append(getConfigListEntry(_("Program Number"), LCD4linux.ChannelNum))
			if LCD4linux.ChannelNum.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.ChannelNumLCD))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.ChannelNumSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.ChannelNumPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.ChannelNumAlign))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.ChannelNumColor))
				self.list2.append(getConfigListEntry(_("- Background Color"), LCD4linux.ChannelNumBackColor))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.ChannelNumShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.ChannelNumFont))
			self.list2.append(getConfigListEntry(_("Program Info"), LCD4linux.Prog))
			if LCD4linux.Prog.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.ProgLCD))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.ProgType))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.ProgSize))
				self.list2.append(getConfigListEntry(_("- maximum Lines"), LCD4linux.ProgLines))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.ProgPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.ProgAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.ProgSplit))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.ProgColor))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.ProgShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.ProgFont))
			self.list2.append(getConfigListEntry(_("Next Program Info"), LCD4linux.ProgNext))
			if LCD4linux.ProgNext.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.ProgNextLCD))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.ProgNextType))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.ProgNextSize))
				self.list2.append(getConfigListEntry(_("- maximum Lines"), LCD4linux.ProgNextLines))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.ProgNextPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.ProgNextAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.ProgNextSplit))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.ProgNextColor))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.ProgNextShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.ProgNextFont))
			self.list2.append(getConfigListEntry(_("Extended Description"), LCD4linux.Desc))
			if LCD4linux.Desc.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.DescLCD))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.DescType))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.DescSize))
				self.list2.append(getConfigListEntry(_("- maximum Lines"), LCD4linux.DescLines))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.DescPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.DescAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.DescSplit))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.DescColor))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.DescShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.DescFont))
			self.list2.append(getConfigListEntry(_("Progress Bar"), LCD4linux.Progress))
			if LCD4linux.Progress.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.ProgressLCD))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.ProgressType))
				self.list2.append(getConfigListEntry(_("- Size"), LCD4linux.ProgressSize))
				self.list2.append(getConfigListEntry(_("- Length"), LCD4linux.ProgressLen))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.ProgressPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.ProgressAlign))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.ProgressColor))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.ProgressShadow2))
				self.list2.append(getConfigListEntry(_("- Shaded"), LCD4linux.ProgressShadow))
			self.list2.append(getConfigListEntry(_("Informations"), LCD4linux.Info))
			if LCD4linux.Info.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.InfoLCD))
				self.list2.append(getConfigListEntry(_("- Tunerinfo"), LCD4linux.InfoTuner))
				self.list2.append(getConfigListEntry(_("- Sensors"), LCD4linux.InfoSensor))
				self.list2.append(getConfigListEntry(_("- CPU"), LCD4linux.InfoCPU))
				self.list2.append(getConfigListEntry(_("- Size"), LCD4linux.InfoSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.InfoPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.InfoAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.InfoSplit))
				self.list2.append(getConfigListEntry(_("- maximum Lines"), LCD4linux.InfoLines))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.InfoColor))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.InfoShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.InfoFont))
			self.list2.append(getConfigListEntry(_("Signal Quality Bar"), LCD4linux.Signal))
			if LCD4linux.Signal.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.SignalLCD))
				self.list2.append(getConfigListEntry(_("- Size"), LCD4linux.SignalSize))
				self.list2.append(getConfigListEntry(_("- Length"), LCD4linux.ProgressLen))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.SignalPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.SignalAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.SignalSplit))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.SignalColor))
				self.list2.append(getConfigListEntry(_("- Gradient"), LCD4linux.SignalGradient))
				self.list2.append(getConfigListEntry(_("- Bar Range Min"), LCD4linux.SignalMin))
				self.list2.append(getConfigListEntry(_("- Bar Range Max"), LCD4linux.SignalMax))
			self.list2.append(getConfigListEntry(_("Satellite"), LCD4linux.Sat))
			if LCD4linux.Sat.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.SatLCD))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.SatSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.SatPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.SatAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.SatSplit))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.SatColor))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.SatType))
				self.list2.append(getConfigListEntry(_("- Picon Path [ok]>"), LCD4linux.SatPath))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.SatShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.SatFont))
			self.list2.append(getConfigListEntry(_("Provider"), LCD4linux.Prov))
			if LCD4linux.Prov.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.ProvLCD))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.ProvSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.ProvPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.ProvAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.ProvSplit))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.ProvColor))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.ProvType))
				self.list2.append(getConfigListEntry(_("- Picon Path [ok]>"), LCD4linux.ProvPath))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.ProvShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.ProvFont))
			self.list2.append(getConfigListEntry(_("Used Tuner"), LCD4linux.Tuner))
			if LCD4linux.Tuner.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.TunerLCD))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.TunerSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.TunerPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.TunerAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.TunerSplit))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.TunerType))
				self.list2.append(getConfigListEntry(_("- only active Tuner"), LCD4linux.TunerActive))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.TunerFont))
			self.list2.append(getConfigListEntry(_("Next Timer Event"), LCD4linux.Timer))
			if LCD4linux.Timer.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.TimerLCD))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.TimerSize))
				self.list2.append(getConfigListEntry(_("- maximum Lines"), LCD4linux.TimerLines))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.TimerType))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.TimerPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.TimerAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.TimerSplit))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.TimerColor))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.TimerShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.TimerFont))
			self.list2.append(getConfigListEntry(_("Volume"), LCD4linux.Vol))
			if LCD4linux.Vol.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.VolLCD))
				self.list2.append(getConfigListEntry(_("- Size"), LCD4linux.VolSize))
				self.list2.append(getConfigListEntry(_("- Length"), LCD4linux.VolLen))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.VolPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.VolAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.VolSplit))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.VolColor))
				self.list2.append(getConfigListEntry(_("- Shaded"), LCD4linux.VolShadow))
			self.list2.append(getConfigListEntry(_("Audio/Video"), LCD4linux.AV))
			if LCD4linux.AV.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.AVLCD))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.AVSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.AVPos))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.AVType))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.AVAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.AVSplit))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.AVColor))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.AVShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.AVFont))
			self.list2.append(getConfigListEntry(_("Bitrate"), LCD4linux.Bitrate))
			if LCD4linux.Bitrate.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.BitrateLCD))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.BitrateSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.BitratePos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.BitrateAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.BitrateSplit))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.BitrateColor))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.BitrateShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.BitrateFont))
			self.list2.append(getConfigListEntry(_("Online [Ping]"), LCD4linux.Ping))
			if LCD4linux.Ping.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.PingLCD))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.PingSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.PingPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.PingAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.PingSplit))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.PingColor))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.PingShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.PingFont))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.PingType))
				self.list2.append(getConfigListEntry(_("- Show State"), LCD4linux.PingShow))
				self.list2.append(getConfigListEntry(_("- Timeout"), LCD4linux.PingTimeout))
				self.list2.append(getConfigListEntry(_("- Online Name:Address"), LCD4linux.PingName1))
				self.list2.append(getConfigListEntry(_("- Online Name:Address"), LCD4linux.PingName2))
				self.list2.append(getConfigListEntry(_("- Online Name:Address"), LCD4linux.PingName3))
				self.list2.append(getConfigListEntry(_("- Online Name:Address"), LCD4linux.PingName4))
				self.list2.append(getConfigListEntry(_("- Online Name:Address"), LCD4linux.PingName5))
			self.list2.append(getConfigListEntry(_("Storage-Devices"), LCD4linux.Dev))
			if LCD4linux.Dev.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.DevLCD))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.DevSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.DevPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.DevAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.DevSplit))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.DevColor))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.DevShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.DevFont))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.DevType))
				self.list2.append(getConfigListEntry(_("- extra Info"), LCD4linux.DevExtra))
				self.list2.append(getConfigListEntry(_("- Device Name"), LCD4linux.DevName1))
				self.list2.append(getConfigListEntry(_("- Device Name"), LCD4linux.DevName2))
				self.list2.append(getConfigListEntry(_("- Device Name"), LCD4linux.DevName3))
				self.list2.append(getConfigListEntry(_("- Device Name"), LCD4linux.DevName4))
				self.list2.append(getConfigListEntry(_("- Device Name"), LCD4linux.DevName5))
			self.list2.append(getConfigListEntry(_("HDD"), LCD4linux.Hdd))
			if LCD4linux.Hdd.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.HddLCD))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.HddSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.HddPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.HddAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.HddSplit))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.HddType))
			self.list2.append(getConfigListEntry(_("Weather"), LCD4linux.Wetter))
			if LCD4linux.Wetter.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.WetterLCD))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.WetterPos))
				self.list2.append(getConfigListEntry(_("- Zoom"), LCD4linux.WetterZoom))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.WetterAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.WetterSplit))
				self.list2.append(getConfigListEntry(_("- Weather Type"), LCD4linux.WetterType))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.WetterColor))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.WetterShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.WetterFont))
			self.list2.append(getConfigListEntry(_("Weather 2"), LCD4linux.Wetter2))
			if LCD4linux.Wetter2.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.Wetter2LCD))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.Wetter2Pos))
				self.list2.append(getConfigListEntry(_("- Zoom"), LCD4linux.Wetter2Zoom))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.Wetter2Align))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.Wetter2Split))
				self.list2.append(getConfigListEntry(_("- Weather Type"), LCD4linux.Wetter2Type))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.Wetter2Color))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.Wetter2Shadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.Wetter2Font))
			self.list2.append(getConfigListEntry(_("Meteo-Weather Station"), LCD4linux.Meteo))
			if LCD4linux.Meteo.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.MeteoLCD))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.MeteoPos))
				self.list2.append(getConfigListEntry(_("- Zoom"), LCD4linux.MeteoZoom))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.MeteoAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MeteoSplit))
				self.list2.append(getConfigListEntry(_("- Weather Type"), LCD4linux.MeteoType))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.MeteoColor))
			self.list2.append(getConfigListEntry(_("Netatmo"), LCD4linux.NetAtmo))
			if LCD4linux.NetAtmo.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.NetAtmoLCD))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.NetAtmoPos))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.NetAtmoSize))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.NetAtmoAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.NetAtmoSplit))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.NetAtmoType))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.NetAtmoType2))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.NetAtmoColor))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.NetAtmoShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.NetAtmoFont))
			self.list2.append(getConfigListEntry(_("Netatmo CO2 Indicator"), LCD4linux.NetAtmoCO2))
			if LCD4linux.NetAtmoCO2.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.NetAtmoCO2LCD))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.NetAtmoCO2Pos))
				self.list2.append(getConfigListEntry(_("- Size"), LCD4linux.NetAtmoCO2Size))
				self.list2.append(getConfigListEntry(_("- Length [Bar]"), LCD4linux.NetAtmoCO2Len))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.NetAtmoCO2Align))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.NetAtmoCO2Split))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.NetAtmoCO2Type))
			self.list2.append(getConfigListEntry(_("Netatmo Comfort Indicator"), LCD4linux.NetAtmoIDX))
			if LCD4linux.NetAtmoIDX.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.NetAtmoIDXLCD))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.NetAtmoIDXPos))
				self.list2.append(getConfigListEntry(_("- Size"), LCD4linux.NetAtmoIDXSize))
				self.list2.append(getConfigListEntry(_("- Length [Bar]"), LCD4linux.NetAtmoIDXLen))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.NetAtmoIDXAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.NetAtmoIDXSplit))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.NetAtmoIDXType))
			self.list2.append(getConfigListEntry(_("Moonphase"), LCD4linux.Moon))
			if LCD4linux.Moon.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.MoonLCD))
				self.list2.append(getConfigListEntry(_("- Size"), LCD4linux.MoonSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.MoonPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.MoonAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MoonSplit))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.MoonColor))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MoonShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.MoonFont))
			self.list2.append(getConfigListEntry(_("Sunrise"), LCD4linux.Sun))
			if LCD4linux.Sun.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.SunLCD))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.SunSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.SunPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.SunAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.SunSplit))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.SunColor))
				self.list2.append(getConfigListEntry(_("- Background Color"), LCD4linux.SunBackColor))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.SunType))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.SunShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.SunFont))
			self.list2.append(getConfigListEntry(_("Show oscam.lcd"), LCD4linux.OSCAM))
			if LCD4linux.OSCAM.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.OSCAMLCD))
				self.list2.append(getConfigListEntry(_("- File [ok]>"), LCD4linux.OSCAMFile))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.OSCAMSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.OSCAMPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.OSCAMAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.OSCAMSplit))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.OSCAMColor))
				self.list2.append(getConfigListEntry(_("- Background Color"), LCD4linux.OSCAMBackColor))
			self.list2.append(getConfigListEntry(_("Show ecm.info"), LCD4linux.ECM))
			if LCD4linux.ECM.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.ECMLCD))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.ECMSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.ECMPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.ECMAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.ECMSplit))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.ECMColor))
				self.list2.append(getConfigListEntry(_("- Background Color"), LCD4linux.ECMBackColor))
			self.list2.append(getConfigListEntry(_("Show Textfile"), LCD4linux.Text))
			if LCD4linux.Text.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.TextLCD))
				self.list2.append(getConfigListEntry(_("- File [ok]>"), LCD4linux.TextFile))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.TextSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.TextPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.TextAlign))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.TextColor))
				self.list2.append(getConfigListEntry(_("- Background Color"), LCD4linux.TextBackColor))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.TextShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.TextFont))
			self.list2.append(getConfigListEntry(_("Show Textfile 2"), LCD4linux.Text2))
			if LCD4linux.Text2.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.Text2LCD))
				self.list2.append(getConfigListEntry(_("- File [ok]>"), LCD4linux.Text2File))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.Text2Size))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.Text2Pos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.Text2Align))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.Text2Color))
				self.list2.append(getConfigListEntry(_("- Background Color"), LCD4linux.Text2BackColor))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.Text2Shadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.Text2Font))
			self.list2.append(getConfigListEntry(_("Show Textfile 3"), LCD4linux.Text3))
			if LCD4linux.Text3.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.Text3LCD))
				self.list2.append(getConfigListEntry(_("- File [ok]>"), LCD4linux.Text3File))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.Text3Size))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.Text3Pos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.Text3Align))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.Text3Color))
				self.list2.append(getConfigListEntry(_("- Background Color"), LCD4linux.Text3BackColor))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.Text3Shadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.Text3Font))
			self.list2.append(getConfigListEntry(_("Show HTTP Text"), LCD4linux.HTTP))
			if LCD4linux.HTTP.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.HTTPLCD))
				self.list2.append(getConfigListEntry(_("- URL"), LCD4linux.HTTPURL))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.HTTPSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.HTTPPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.HTTPAlign))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.HTTPColor))
				self.list2.append(getConfigListEntry(_("- Background Color"), LCD4linux.HTTPBackColor))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.HTTPShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.HTTPFont))
			self.list2.append(getConfigListEntry(_("WWW-Internet Converter"), LCD4linux.WWW1))
			if LCD4linux.WWW1.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.WWW1LCD))
				self.list2.append(getConfigListEntry(_("- Size"), LCD4linux.WWW1Size))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.WWW1Pos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.WWW1Align))
				self.list2.append(getConfigListEntry(_("- URL"), LCD4linux.WWW1url))
				self.list2.append(getConfigListEntry(_("- HTTP Width"), LCD4linux.WWW1w))
				self.list2.append(getConfigListEntry(_("- HTTP Height"), LCD4linux.WWW1h))
				self.list2.append(getConfigListEntry(_("- Cut from X"), LCD4linux.WWW1CutX))
				self.list2.append(getConfigListEntry(_("- Cut from Y"), LCD4linux.WWW1CutY))
				self.list2.append(getConfigListEntry(_("- Cut Width [disable = 0]"), LCD4linux.WWW1CutW))
				self.list2.append(getConfigListEntry(_("- Cut Height [disable = 0]"), LCD4linux.WWW1CutH))
			self.list2.append(getConfigListEntry(_("Show Picture"), LCD4linux.Bild))
			if LCD4linux.Bild.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.BildLCD))
				self.list2.append(getConfigListEntry(_("- File or Path [ok]>"), LCD4linux.BildFile))
				self.list2.append(getConfigListEntry(_("- Size"), LCD4linux.BildSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.BildPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.BildAlign))
				self.list2.append(getConfigListEntry(_("- Quick Update"), LCD4linux.BildQuick))
				self.list2.append(getConfigListEntry(_("- Transparency"), LCD4linux.BildTransp))
			self.list2.append(getConfigListEntry(_("Show Picture 2"), LCD4linux.Bild2))
			if LCD4linux.Bild2.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.Bild2LCD))
				self.list2.append(getConfigListEntry(_("- File or Path [ok]>"), LCD4linux.Bild2File))
				self.list2.append(getConfigListEntry(_("- Size"), LCD4linux.Bild2Size))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.Bild2Pos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.Bild2Align))
				self.list2.append(getConfigListEntry(_("- Quick Update"), LCD4linux.Bild2Quick))
				self.list2.append(getConfigListEntry(_("- Transparency"), LCD4linux.Bild2Transp))
			self.list2.append(getConfigListEntry(_("Show Picture 3"), LCD4linux.Bild3))
			if LCD4linux.Bild3.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.Bild3LCD))
				self.list2.append(getConfigListEntry(_("- File or Path [ok]>"), LCD4linux.Bild3File))
				self.list2.append(getConfigListEntry(_("- Size"), LCD4linux.Bild3Size))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.Bild3Pos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.Bild3Align))
				self.list2.append(getConfigListEntry(_("- Quick Update"), LCD4linux.Bild3Quick))
				self.list2.append(getConfigListEntry(_("- Transparency"), LCD4linux.Bild3Transp))
			self.list2.append(getConfigListEntry(_("Show Picture 4"), LCD4linux.Bild4))
			if LCD4linux.Bild4.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.Bild4LCD))
				self.list2.append(getConfigListEntry(_("- File [ok]>"), LCD4linux.Bild4File))
				self.list2.append(getConfigListEntry(_("- Size"), LCD4linux.Bild4Size))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.Bild4Pos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.Bild4Align))
				self.list2.append(getConfigListEntry(_("- Quick Update"), LCD4linux.Bild4Quick))
				self.list2.append(getConfigListEntry(_("- Transparency"), LCD4linux.Bild4Transp))
			self.list2.append(getConfigListEntry(_("Mail"), LCD4linux.Mail))
			if LCD4linux.Mail.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.MailLCD))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.MailSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.MailPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.MailAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MailSplit))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.MailColor))
				self.list2.append(getConfigListEntry(_("- Background Color"), LCD4linux.MailBackColor))
				self.list2.append(getConfigListEntry(_("- Lines"), LCD4linux.MailLines))
				self.list2.append(getConfigListEntry(_("- Mail Konto"), LCD4linux.MailKonto))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.MailType))
				self.list2.append(getConfigListEntry(_("- max Width"), LCD4linux.MailProzent))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MailShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.MailFont))
			self.list2.append(getConfigListEntry(_("FritzCall"), LCD4linux.Fritz))
			if LCD4linux.Fritz.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.FritzLCD))
				self.list2.append(getConfigListEntry(_("- Font Size"), LCD4linux.FritzSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.FritzPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.FritzAlign))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.FritzColor))
				self.list2.append(getConfigListEntry(_("- Background Color"), LCD4linux.FritzBackColor))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.FritzType))
				self.list2.append(getConfigListEntry(_("- Picture Size"), LCD4linux.FritzPicSize))
				self.list2.append(getConfigListEntry(_("- Picture Position"), LCD4linux.FritzPicPos))
				self.list2.append(getConfigListEntry(_("- Picture Alignment"), LCD4linux.FritzPicAlign))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.FritzShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.FritzFont))
			self.list2.append(getConfigListEntry(_("Calendar"), LCD4linux.Cal))
			if LCD4linux.Cal.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.CalLCD))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.CalPos))
				self.list2.append(getConfigListEntry(_("- Zoom"), LCD4linux.CalZoom))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.CalAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.CalSplit))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.CalType))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.CalTypeE))
				self.list2.append(getConfigListEntry(_("- Layout"), LCD4linux.CalLayout))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.CalColor))
				self.list2.append(getConfigListEntry(_("- Current Day Background Color"), LCD4linux.CalBackColor))
				self.list2.append(getConfigListEntry(_("- Caption Color"), LCD4linux.CalCaptionColor))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.CalShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.CalFont))
			self.list2.append(getConfigListEntry(_("Dates List"), LCD4linux.CalList))
			if LCD4linux.CalList.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.CalListLCD))
				self.list2.append(getConfigListEntry(_("- Size"), LCD4linux.CalListSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.CalListPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.CalListAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.CalListSplit))
				self.list2.append(getConfigListEntry(_("- maximum Lines"), LCD4linux.CalListLines))
				self.list2.append(getConfigListEntry(_("- max Width"), LCD4linux.CalListProzent))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.CalListType))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.CalListColor))
				self.list2.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.CalListShadow))
				self.list2.append(getConfigListEntry(_("- Font"), LCD4linux.CalListFont))
			self.list2.append(getConfigListEntry(_("Event Icon Bar"), LCD4linux.IconBar))
			if LCD4linux.IconBar.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.IconBarLCD))
				self.list2.append(getConfigListEntry(_("- Size"), LCD4linux.IconBarSize))
				self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.IconBarPos))
				self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.IconBarAlign))
				self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.IconBarSplit))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.IconBarType))
				self.list2.append(getConfigListEntry(_("- Popup Screen"), LCD4linux.IconBarPopup))
				self.list2.append(getConfigListEntry(_("- Popup LCD"), LCD4linux.IconBarPopupLCD))
			self.list2.append(getConfigListEntry(_("Rectangle 1"), LCD4linux.Box1))
			if LCD4linux.Box1.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.Box1LCD))
				self.list2.append(getConfigListEntry(_("- Position x"), LCD4linux.Box1x1))
				self.list2.append(getConfigListEntry(_("- Position y"), LCD4linux.Box1y1))
				self.list2.append(getConfigListEntry(_("- Size x"), LCD4linux.Box1x2))
				self.list2.append(getConfigListEntry(_("- Size y"), LCD4linux.Box1y2))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.Box1Color))
				self.list2.append(getConfigListEntry(_("- Background Color"), LCD4linux.Box1BackColor))
			self.list2.append(getConfigListEntry(_("Rectangle 2"), LCD4linux.Box2))
			if LCD4linux.Box2.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.Box2LCD))
				self.list2.append(getConfigListEntry(_("- Position x"), LCD4linux.Box2x1))
				self.list2.append(getConfigListEntry(_("- Position y"), LCD4linux.Box2y1))
				self.list2.append(getConfigListEntry(_("- Size x"), LCD4linux.Box2x2))
				self.list2.append(getConfigListEntry(_("- Size y"), LCD4linux.Box2y2))
				self.list2.append(getConfigListEntry(_("- Color"), LCD4linux.Box2Color))
				self.list2.append(getConfigListEntry(_("- Background Color"), LCD4linux.Box2BackColor))
			self.list2.append(getConfigListEntry(_("Recording"), LCD4linux.Recording))
			if LCD4linux.Recording.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.RecordingLCD))
				self.list2.append(getConfigListEntry(_("-  Type"), LCD4linux.RecordingType))
				self.list2.append(getConfigListEntry(_("- Size"), LCD4linux.RecordingSize))
				if LCD4linux.RecordingType.value == "2":
					self.list2.append(getConfigListEntry(_("- Position"), LCD4linux.RecordingPos))
					self.list2.append(getConfigListEntry(_("- Alignment"), LCD4linux.RecordingAlign))
					self.list2.append(getConfigListEntry(_("- Split Screen"), LCD4linux.RecordingSplit))
			self.list2.append(getConfigListEntry(_("Stutter TV"), LCD4linux.TV))
			if LCD4linux.TV.value != "0":
				self.list2.append(getConfigListEntry(_("- which LCD"), LCD4linux.TVLCD))
				self.list2.append(getConfigListEntry(_("- Type"), LCD4linux.TVType))
			self["config"].setList(self.list2)
		elif self.mode == "Media":
			self.list3 = []
			self.list3.append(getConfigListEntry(_("- LCD 1 Background Color"), LCD4linux.MPLCDColor1))
			self.list3.append(getConfigListEntry(_("- LCD 1 Background-Picture [ok]>"), LCD4linux.MPLCDBild1))
			self.list3.append(getConfigListEntry(_("- LCD 1 Brightness [no SPF]"), LCD4linux.MPHelligkeit))
			self.list3.append(getConfigListEntry(_("- LCD 2 Background Color"), LCD4linux.MPLCDColor2))
			self.list3.append(getConfigListEntry(_("- LCD 2 Background-Picture [ok]>"), LCD4linux.MPLCDBild2))
			self.list3.append(getConfigListEntry(_("- LCD 2 Brightness [no SPF]"), LCD4linux.MPHelligkeit2))
			self.list3.append(getConfigListEntry(_("- LCD 3 Background Color"), LCD4linux.MPLCDColor3))
			self.list3.append(getConfigListEntry(_("- LCD 3 Background-Picture [ok]>"), LCD4linux.MPLCDBild3))
			self.list3.append(getConfigListEntry(_("- LCD 3 Brightness [no SPF]"), LCD4linux.MPHelligkeit3))
			self.list3.append(getConfigListEntry(_("- Screens used for Changing"), LCD4linux.MPScreenMax))
			self.list3.append(getConfigListEntry(_("Title"), LCD4linux.MPTitle))
			if LCD4linux.MPTitle.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPTitleLCD))
				self.list3.append(getConfigListEntry(_("- Font Size"), LCD4linux.MPTitleSize))
				self.list3.append(getConfigListEntry(_("- maximum Lines"), LCD4linux.MPTitleLines))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPTitlePos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPTitleAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPTitleSplit))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPTitleColor))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPTitleShadow))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPTitleFont))
			self.list3.append(getConfigListEntry(_("Infos"), LCD4linux.MPComm))
			if LCD4linux.MPComm.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPCommLCD))
				self.list3.append(getConfigListEntry(_("- Font Size"), LCD4linux.MPCommSize))
				self.list3.append(getConfigListEntry(_("- maximum Lines"), LCD4linux.MPCommLines))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPCommPos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPCommAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPCommSplit))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPCommColor))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPCommShadow))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPCommFont))
			self.list3.append(getConfigListEntry(_("Extended Description"), LCD4linux.MPDesc))
			if LCD4linux.MPDesc.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPDescLCD))
				self.list3.append(getConfigListEntry(_("- Type"), LCD4linux.MPDescType))
				self.list3.append(getConfigListEntry(_("- Font Size"), LCD4linux.MPDescSize))
				self.list3.append(getConfigListEntry(_("- maximum Lines"), LCD4linux.MPDescLines))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPDescPos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPDescAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPDescSplit))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPDescColor))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPDescShadow))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPDescFont))
			self.list3.append(getConfigListEntry(_("Program Name"), LCD4linux.MPChannel))
			if LCD4linux.MPChannel.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPChannelLCD))
				self.list3.append(getConfigListEntry(_("- Font Size"), LCD4linux.MPChannelSize))
				self.list3.append(getConfigListEntry(_("- maximum Lines"), LCD4linux.MPChannelLines))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPChannelPos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPChannelAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPChannelSplit))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPChannelColor))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPChannelShadow))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPChannelFont))
			self.list3.append(getConfigListEntry(_("Progress Bar"), LCD4linux.MPProgress))
			if LCD4linux.MPProgress.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPProgressLCD))
				self.list3.append(getConfigListEntry(_("- Type"), LCD4linux.MPProgressType))
				self.list3.append(getConfigListEntry(_("- Size"), LCD4linux.MPProgressSize))
				self.list3.append(getConfigListEntry(_("- Length"), LCD4linux.MPProgressLen))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPProgressPos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPProgressAlign))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPProgressColor))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPProgressShadow2))
				self.list3.append(getConfigListEntry(_("- Shaded"), LCD4linux.MPProgressShadow))
			self.list3.append(getConfigListEntry(_("Volume"), LCD4linux.MPVol))
			if LCD4linux.MPVol.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPVolLCD))
				self.list3.append(getConfigListEntry(_("- Size"), LCD4linux.MPVolSize))
				self.list3.append(getConfigListEntry(_("- Length"), LCD4linux.MPVolLen))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPVolPos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPVolAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPVolSplit))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPVolColor))
				self.list3.append(getConfigListEntry(_("- Shaded"), LCD4linux.MPVolShadow))
			self.list3.append(getConfigListEntry(_("Clock"), LCD4linux.MPClock))
			if LCD4linux.MPClock.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPClockLCD))
				self.list3.append(getConfigListEntry(_("- Type"), LCD4linux.MPClockType))
				if LCD4linux.MPClockType.value[0] == "5":
					self.list3.append(getConfigListEntry(_("- Analog Clock"), LCD4linux.MPClockAnalog))
				elif LCD4linux.MPClockType.value[0] == "1":
					self.list3.append(getConfigListEntry(_("- Spacing"), LCD4linux.MPClockSpacing))
				self.list3.append(getConfigListEntry(_("- Size"), LCD4linux.MPClockSize))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPClockPos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPClockAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPClockSplit))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPClockColor))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPClockShadow))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPClockFont))
			self.list3.append(getConfigListEntry(_("Clock 2"), LCD4linux.MPClock2))
			if LCD4linux.MPClock2.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPClock2LCD))
				self.list3.append(getConfigListEntry(_("- Type"), LCD4linux.MPClock2Type))
				if LCD4linux.MPClock2Type.value[0] == "5":
					self.list3.append(getConfigListEntry(_("- Analog Clock"), LCD4linux.MPClock2Analog))
				elif LCD4linux.MPClock2Type.value[0] == "1":
					self.list3.append(getConfigListEntry(_("- Spacing"), LCD4linux.MPClock2Spacing))
				self.list3.append(getConfigListEntry(_("- Size"), LCD4linux.MPClock2Size))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPClock2Pos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPClock2Align))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPClock2Split))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPClock2Color))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPClock2Shadow))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPClock2Font))
			self.list3.append(getConfigListEntry(_("Informations"), LCD4linux.MPInfo))
			if LCD4linux.MPInfo.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPInfoLCD))
				self.list3.append(getConfigListEntry(_("- Sensors"), LCD4linux.MPInfoSensor))
				self.list3.append(getConfigListEntry(_("- CPU"), LCD4linux.MPInfoCPU))
				self.list3.append(getConfigListEntry(_("- Size"), LCD4linux.MPInfoSize))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPInfoPos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPInfoAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPInfoSplit))
				self.list3.append(getConfigListEntry(_("- maximum Lines"), LCD4linux.MPInfoLines))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPInfoColor))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPInfoShadow))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPInfoFont))
			self.list3.append(getConfigListEntry(_("Used Tuner"), LCD4linux.MPTuner))
			if LCD4linux.MPTuner.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPTunerLCD))
				self.list3.append(getConfigListEntry(_("- Font Size"), LCD4linux.MPTunerSize))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPTunerPos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPTunerAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPTunerSplit))
				self.list3.append(getConfigListEntry(_("- Type"), LCD4linux.MPTunerType))
				self.list3.append(getConfigListEntry(_("- only active Tuner"), LCD4linux.MPTunerActive))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPTunerFont))
			self.list3.append(getConfigListEntry(_("Next Timer Event"), LCD4linux.MPTimer))
			if LCD4linux.MPTimer.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPTimerLCD))
				self.list3.append(getConfigListEntry(_("- Font Size"), LCD4linux.MPTimerSize))
				self.list3.append(getConfigListEntry(_("- maximum Lines"), LCD4linux.MPTimerLines))
				self.list3.append(getConfigListEntry(_("- Type"), LCD4linux.MPTimerType))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPTimerPos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPTimerAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPTimerSplit))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPTimerColor))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPTimerShadow))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPTimerFont))
			self.list3.append(getConfigListEntry(_("Audio/Video"), LCD4linux.MPAV))
			if LCD4linux.MPAV.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPAVLCD))
				self.list3.append(getConfigListEntry(_("- Font Size"), LCD4linux.MPAVSize))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPAVPos))
				self.list3.append(getConfigListEntry(_("- Type"), LCD4linux.MPAVType))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPAVAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPAVSplit))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPAVColor))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPAVShadow))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPAVFont))
			self.list3.append(getConfigListEntry(_("Bitrate"), LCD4linux.MPBitrate))
			if LCD4linux.MPBitrate.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPBitrateLCD))
				self.list3.append(getConfigListEntry(_("- Font Size"), LCD4linux.MPBitrateSize))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPBitratePos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPBitrateAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPBitrateSplit))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPBitrateColor))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPBitrateShadow))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPBitrateFont))
			self.list3.append(getConfigListEntry(_("Online [Ping]"), LCD4linux.MPPing))
			if LCD4linux.MPPing.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPPingLCD))
				self.list3.append(getConfigListEntry(_("- Font Size"), LCD4linux.MPPingSize))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPPingPos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPPingAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPPingSplit))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPPingColor))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPPingShadow))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPPingFont))
				self.list3.append(getConfigListEntry(_("- Type"), LCD4linux.MPPingType))
				self.list3.append(getConfigListEntry(_("- Show State"), LCD4linux.MPPingShow))
				self.list3.append(getConfigListEntry(_("- Timeout"), LCD4linux.MPPingTimeout))
				self.list3.append(getConfigListEntry(_("- Online Name:Address"), LCD4linux.MPPingName1))
				self.list3.append(getConfigListEntry(_("- Online Name:Address"), LCD4linux.MPPingName2))
				self.list3.append(getConfigListEntry(_("- Online Name:Address"), LCD4linux.MPPingName3))
				self.list3.append(getConfigListEntry(_("- Online Name:Address"), LCD4linux.MPPingName4))
				self.list3.append(getConfigListEntry(_("- Online Name:Address"), LCD4linux.MPPingName5))
			self.list3.append(getConfigListEntry(_("Storage-Devices"), LCD4linux.MPDev))
			if LCD4linux.MPDev.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPDevLCD))
				self.list3.append(getConfigListEntry(_("- Font Size"), LCD4linux.MPDevSize))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPDevPos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPDevAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPDevSplit))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPDevColor))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPDevShadow))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPDevFont))
				self.list3.append(getConfigListEntry(_("- Type"), LCD4linux.MPDevType))
				self.list3.append(getConfigListEntry(_("- extra Info"), LCD4linux.MPDevExtra))
				self.list3.append(getConfigListEntry(_("- Device Name"), LCD4linux.MPDevName1))
				self.list3.append(getConfigListEntry(_("- Device Name"), LCD4linux.MPDevName2))
				self.list3.append(getConfigListEntry(_("- Device Name"), LCD4linux.MPDevName3))
				self.list3.append(getConfigListEntry(_("- Device Name"), LCD4linux.MPDevName4))
				self.list3.append(getConfigListEntry(_("- Device Name"), LCD4linux.MPDevName5))
			self.list3.append(getConfigListEntry(_("HDD"), LCD4linux.MPHdd))
			if LCD4linux.MPHdd.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPHddLCD))
				self.list3.append(getConfigListEntry(_("- Font Size"), LCD4linux.MPHddSize))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPHddPos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPHddAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPHddSplit))
				self.list3.append(getConfigListEntry(_("- Type"), LCD4linux.MPHddType))
			self.list3.append(getConfigListEntry(_("Weather"), LCD4linux.MPWetter))
			if LCD4linux.MPWetter.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPWetterLCD))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPWetterPos))
				self.list3.append(getConfigListEntry(_("- Zoom"), LCD4linux.MPWetterZoom))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPWetterAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPWetterSplit))
				self.list3.append(getConfigListEntry(_("- Weather Type"), LCD4linux.MPWetterType))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPWetterColor))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPWetterShadow))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPWetterFont))
			self.list3.append(getConfigListEntry(_("Weather 2"), LCD4linux.MPWetter2))
			if LCD4linux.MPWetter2.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPWetter2LCD))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPWetter2Pos))
				self.list3.append(getConfigListEntry(_("- Zoom"), LCD4linux.MPWetter2Zoom))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPWetter2Align))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPWetter2Split))
				self.list3.append(getConfigListEntry(_("- Weather Type"), LCD4linux.MPWetter2Type))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPWetter2Color))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPWetter2Shadow))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPWetter2Font))
			self.list3.append(getConfigListEntry(_("Meteo-Weather Station"), LCD4linux.MPMeteo))
			if LCD4linux.MPMeteo.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPMeteoLCD))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPMeteoPos))
				self.list3.append(getConfigListEntry(_("- Zoom"), LCD4linux.MPMeteoZoom))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPMeteoAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPMeteoSplit))
				self.list3.append(getConfigListEntry(_("- Weather Type"), LCD4linux.MPMeteoType))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPMeteoColor))
			self.list3.append(getConfigListEntry(_("Netatmo"), LCD4linux.MPNetAtmo))
			if LCD4linux.MPNetAtmo.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPNetAtmoLCD))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPNetAtmoPos))
				self.list3.append(getConfigListEntry(_("- Font Size"), LCD4linux.MPNetAtmoSize))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPNetAtmoAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPNetAtmoSplit))
				self.list3.append(getConfigListEntry(_("- Type"), LCD4linux.MPNetAtmoType))
				self.list3.append(getConfigListEntry(_("- Type"), LCD4linux.MPNetAtmoType2))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPNetAtmoColor))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPNetAtmoShadow))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPNetAtmoFont))
			self.list3.append(getConfigListEntry(_("Netatmo CO2 Indicator"), LCD4linux.MPNetAtmoCO2))
			if LCD4linux.MPNetAtmoCO2.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPNetAtmoCO2LCD))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPNetAtmoCO2Pos))
				self.list3.append(getConfigListEntry(_("- Size"), LCD4linux.MPNetAtmoCO2Size))
				self.list3.append(getConfigListEntry(_("- Length [Bar]"), LCD4linux.MPNetAtmoCO2Len))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPNetAtmoCO2Align))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPNetAtmoCO2Split))
				self.list3.append(getConfigListEntry(_("- Type"), LCD4linux.MPNetAtmoCO2Type))
			self.list3.append(getConfigListEntry(_("Netatmo Comfort Indicator"), LCD4linux.MPNetAtmoIDX))
			if LCD4linux.MPNetAtmoIDX.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPNetAtmoIDXLCD))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPNetAtmoIDXPos))
				self.list3.append(getConfigListEntry(_("- Size"), LCD4linux.MPNetAtmoIDXSize))
				self.list3.append(getConfigListEntry(_("- Length [Bar]"), LCD4linux.MPNetAtmoIDXLen))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPNetAtmoIDXAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPNetAtmoIDXSplit))
				self.list3.append(getConfigListEntry(_("- Type"), LCD4linux.MPNetAtmoIDXType))
			self.list3.append(getConfigListEntry(_("Moonphase"), LCD4linux.MPMoon))
			if LCD4linux.MPMoon.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPMoonLCD))
				self.list3.append(getConfigListEntry(_("- Size"), LCD4linux.MPMoonSize))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPMoonPos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPMoonAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPMoonSplit))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPMoonColor))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPMoonShadow))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPMoonFont))
			self.list3.append(getConfigListEntry(_("Sunrise"), LCD4linux.MPSun))
			if LCD4linux.MPSun.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPSunLCD))
				self.list3.append(getConfigListEntry(_("- Font Size"), LCD4linux.MPSunSize))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPSunPos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPSunAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPSunSplit))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPSunColor))
				self.list3.append(getConfigListEntry(_("- Background Color"), LCD4linux.MPSunBackColor))
				self.list3.append(getConfigListEntry(_("- Type"), LCD4linux.MPSunType))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPSunShadow))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPSunFont))
			self.list3.append(getConfigListEntry(_("Show Textfile"), LCD4linux.MPText))
			if LCD4linux.MPText.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPTextLCD))
				self.list3.append(getConfigListEntry(_("- File [ok]>"), LCD4linux.MPTextFile))
				self.list3.append(getConfigListEntry(_("- Font Size"), LCD4linux.MPTextSize))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPTextPos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPTextAlign))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPTextColor))
				self.list3.append(getConfigListEntry(_("- Background Color"), LCD4linux.MPTextBackColor))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPTextShadow))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPTextFont))
			self.list3.append(getConfigListEntry(_("Show Picture"), LCD4linux.MPBild))
			if LCD4linux.MPBild.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPBildLCD))
				self.list3.append(getConfigListEntry(_("- File or Path [ok]>"), LCD4linux.MPBildFile))
				self.list3.append(getConfigListEntry(_("- Size"), LCD4linux.MPBildSize))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPBildPos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPBildAlign))
				self.list3.append(getConfigListEntry(_("- Quick Update"), LCD4linux.MPBildQuick))
				self.list3.append(getConfigListEntry(_("- Transparency"), LCD4linux.MPBildTransp))
			self.list3.append(getConfigListEntry(_("Show Picture 2"), LCD4linux.MPBild2))
			if LCD4linux.MPBild2.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPBild2LCD))
				self.list3.append(getConfigListEntry(_("- File or Path [ok]>"), LCD4linux.MPBild2File))
				self.list3.append(getConfigListEntry(_("- Size"), LCD4linux.MPBild2Size))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPBild2Pos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPBild2Align))
				self.list3.append(getConfigListEntry(_("- Quick Update"), LCD4linux.MPBild2Quick))
				self.list3.append(getConfigListEntry(_("- Transparency"), LCD4linux.MPBild2Transp))
			self.list3.append(getConfigListEntry(_("Show Cover"), LCD4linux.MPCover))
			if LCD4linux.MPCover.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPCoverLCD))
				self.list3.append(getConfigListEntry(_("- Size"), LCD4linux.MPCoverSize))
				self.list3.append(getConfigListEntry(_("- Size max Height"), LCD4linux.MPCoverSizeH))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPCoverPos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPCoverAlign))
				self.list3.append(getConfigListEntry(_("- Search Path [ok]>"), LCD4linux.MPCoverPath1))
				self.list3.append(getConfigListEntry(_("- Search Path [ok]>"), LCD4linux.MPCoverPath2))
				self.list3.append(getConfigListEntry(_("- Default Cover [ok]>"), LCD4linux.MPCoverFile))
				self.list3.append(getConfigListEntry(_("- Download Cover from Google"), LCD4linux.MPCoverGoogle))
				self.list3.append(getConfigListEntry(_("- Picon First"), LCD4linux.MPCoverPiconFirst))
				self.list3.append(getConfigListEntry(_("- Transparency"), LCD4linux.MPCoverTransp))
			self.list3.append(getConfigListEntry(_("Show oscam.lcd"), LCD4linux.MPOSCAM))
			if LCD4linux.MPOSCAM.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPOSCAMLCD))
				self.list3.append(getConfigListEntry(_("- Font Size"), LCD4linux.MPOSCAMSize))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPOSCAMPos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPOSCAMAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPOSCAMSplit))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPOSCAMColor))
				self.list3.append(getConfigListEntry(_("- Background Color"), LCD4linux.MPOSCAMBackColor))
			self.list3.append(getConfigListEntry(_("Mail"), LCD4linux.MPMail))
			if LCD4linux.MPMail.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPMailLCD))
				self.list3.append(getConfigListEntry(_("- Font Size"), LCD4linux.MPMailSize))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPMailPos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPMailAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPMailSplit))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPMailColor))
				self.list3.append(getConfigListEntry(_("- Background Color"), LCD4linux.MPMailBackColor))
				self.list3.append(getConfigListEntry(_("- Lines"), LCD4linux.MPMailLines))
				self.list3.append(getConfigListEntry(_("- Mail Konto"), LCD4linux.MPMailKonto))
				self.list3.append(getConfigListEntry(_("- Type"), LCD4linux.MPMailType))
				self.list3.append(getConfigListEntry(_("- max Width"), LCD4linux.MPMailProzent))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPMailShadow))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPMailFont))
			self.list3.append(getConfigListEntry(_("FritzCall"), LCD4linux.MPFritz))
			if LCD4linux.MPFritz.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPFritzLCD))
				self.list3.append(getConfigListEntry(_("- Font Size"), LCD4linux.MPFritzSize))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPFritzPos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPFritzAlign))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPFritzColor))
				self.list3.append(getConfigListEntry(_("- Background Color"), LCD4linux.MPFritzBackColor))
				self.list3.append(getConfigListEntry(_("- Type"), LCD4linux.MPFritzType))
				self.list3.append(getConfigListEntry(_("- Picture Size"), LCD4linux.MPFritzPicSize))
				self.list3.append(getConfigListEntry(_("- Picture Position"), LCD4linux.MPFritzPicPos))
				self.list3.append(getConfigListEntry(_("- Picture Alignment"), LCD4linux.MPFritzPicAlign))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPFritzShadow))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPFritzFont))
			self.list3.append(getConfigListEntry(_("Calendar"), LCD4linux.MPCal))
			if LCD4linux.MPCal.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPCalLCD))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPCalPos))
				self.list3.append(getConfigListEntry(_("- Zoom"), LCD4linux.MPCalZoom))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPCalAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPCalSplit))
				self.list3.append(getConfigListEntry(_("- Type"), LCD4linux.MPCalType))
				self.list3.append(getConfigListEntry(_("- Type"), LCD4linux.MPCalTypeE))
				self.list3.append(getConfigListEntry(_("- Layout"), LCD4linux.MPCalLayout))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPCalColor))
				self.list3.append(getConfigListEntry(_("- Current Day Background Color"), LCD4linux.MPCalBackColor))
				self.list3.append(getConfigListEntry(_("- Caption Color"), LCD4linux.MPCalCaptionColor))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPCalShadow))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPCalFont))
			self.list3.append(getConfigListEntry(_("Dates List"), LCD4linux.MPCalList))
			if LCD4linux.MPCalList.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPCalListLCD))
				self.list3.append(getConfigListEntry(_("- Size"), LCD4linux.MPCalListSize))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPCalListPos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPCalListAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPCalListSplit))
				self.list3.append(getConfigListEntry(_("- maximum Lines"), LCD4linux.MPCalListLines))
				self.list3.append(getConfigListEntry(_("- max Width"), LCD4linux.MPCalListProzent))
				self.list3.append(getConfigListEntry(_("- Type"), LCD4linux.MPCalListType))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPCalListColor))
				self.list3.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.MPCalListShadow))
				self.list3.append(getConfigListEntry(_("- Font"), LCD4linux.MPCalListFont))
			self.list3.append(getConfigListEntry(_("Event Icon Bar"), LCD4linux.MPIconBar))
			if LCD4linux.MPIconBar.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPIconBarLCD))
				self.list3.append(getConfigListEntry(_("- Size"), LCD4linux.MPIconBarSize))
				self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPIconBarPos))
				self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPIconBarAlign))
				self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPIconBarSplit))
				self.list3.append(getConfigListEntry(_("- Type"), LCD4linux.MPIconBarType))
				self.list3.append(getConfigListEntry(_("- Popup Screen"), LCD4linux.MPIconBarPopup))
				self.list3.append(getConfigListEntry(_("- Popup LCD"), LCD4linux.MPIconBarPopupLCD))
			self.list3.append(getConfigListEntry(_("Rectangle 1"), LCD4linux.MPBox1))
			if LCD4linux.MPBox1.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPBox1LCD))
				self.list3.append(getConfigListEntry(_("- Position x"), LCD4linux.MPBox1x1))
				self.list3.append(getConfigListEntry(_("- Position y"), LCD4linux.MPBox1y1))
				self.list3.append(getConfigListEntry(_("- Size x"), LCD4linux.MPBox1x2))
				self.list3.append(getConfigListEntry(_("- Size y"), LCD4linux.MPBox1y2))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPBox1Color))
				self.list3.append(getConfigListEntry(_("- Background Color"), LCD4linux.MPBox1BackColor))
			self.list3.append(getConfigListEntry(_("Rectangle 2"), LCD4linux.MPBox2))
			if LCD4linux.MPBox2.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPBox2LCD))
				self.list3.append(getConfigListEntry(_("- Position x"), LCD4linux.MPBox2x1))
				self.list3.append(getConfigListEntry(_("- Position y"), LCD4linux.MPBox2y1))
				self.list3.append(getConfigListEntry(_("- Size x"), LCD4linux.MPBox2x2))
				self.list3.append(getConfigListEntry(_("- Size y"), LCD4linux.MPBox2y2))
				self.list3.append(getConfigListEntry(_("- Color"), LCD4linux.MPBox2Color))
				self.list3.append(getConfigListEntry(_("- Background Color"), LCD4linux.MPBox2BackColor))
			self.list3.append(getConfigListEntry(_("Recording"), LCD4linux.MPRecording))
			if LCD4linux.MPRecording.value != "0":
				self.list3.append(getConfigListEntry(_("- which LCD"), LCD4linux.MPRecordingLCD))
				self.list3.append(getConfigListEntry(_("-  Type"), LCD4linux.MPRecordingType))
				self.list3.append(getConfigListEntry(_("- Size"), LCD4linux.MPRecordingSize))
				if LCD4linux.MPRecordingType.value == "2":
					self.list3.append(getConfigListEntry(_("- Position"), LCD4linux.MPRecordingPos))
					self.list3.append(getConfigListEntry(_("- Alignment"), LCD4linux.MPRecordingAlign))
					self.list3.append(getConfigListEntry(_("- Split Screen"), LCD4linux.MPRecordingSplit))
			self["config"].setList(self.list3)
		elif self.mode == "Idle":
			self.list4 = []
			self.list4.append(getConfigListEntry(_("LCD Display"), LCD4linux.Standby))
			self.list4.append(getConfigListEntry(_("- Backlight Off [disable set Off=On]"), LCD4linux.StandbyLCDoff))
			self.list4.append(getConfigListEntry(_("- Backlight On"), LCD4linux.StandbyLCDon))
			self.list4.append(getConfigListEntry(_("- Backlight Weekend Off [disable set Off=On]"), LCD4linux.StandbyLCDWEoff))
			self.list4.append(getConfigListEntry(_("- Backlight Weekend On"), LCD4linux.StandbyLCDWEon))
			self.list4.append(getConfigListEntry(_("- LCD 1 Background Color"), LCD4linux.StandbyLCDColor1))
			self.list4.append(getConfigListEntry(_("- LCD 1 Background-Picture [ok]>"), LCD4linux.StandbyLCDBild1))
			self.list4.append(getConfigListEntry(_("- LCD 1 Brightness [no SPF]"), LCD4linux.StandbyHelligkeit))
			self.list4.append(getConfigListEntry(_("- LCD 2 Background Color"), LCD4linux.StandbyLCDColor2))
			self.list4.append(getConfigListEntry(_("- LCD 2 Background-Picture [ok]>"), LCD4linux.StandbyLCDBild2))
			self.list4.append(getConfigListEntry(_("- LCD 2 Brightness [no SPF]"), LCD4linux.StandbyHelligkeit2))
			self.list4.append(getConfigListEntry(_("- LCD 3 Background Color"), LCD4linux.StandbyLCDColor3))
			self.list4.append(getConfigListEntry(_("- LCD 3 Background-Picture [ok]>"), LCD4linux.StandbyLCDBild3))
			self.list4.append(getConfigListEntry(_("- LCD 3 Brightness [no SPF]"), LCD4linux.StandbyHelligkeit3))
			self.list4.append(getConfigListEntry(_("- Screens used for Changing"), LCD4linux.StandbyScreenMax))
			self.list4.append(getConfigListEntry(_("Screen 1 Changing Time"), LCD4linux.StandbyScreenTime))
			if LCD4linux.StandbyScreenTime.value != "0":
				self.list4.append(getConfigListEntry(_("- Screen 2 Changing Time"), LCD4linux.StandbyScreenTime2))
				self.list4.append(getConfigListEntry(_("- Screen 3 Changing Time"), LCD4linux.StandbyScreenTime3))
				self.list4.append(getConfigListEntry(_("- Screen 4 Changing Time"), LCD4linux.StandbyScreenTime4))
				self.list4.append(getConfigListEntry(_("- Screen 5 Changing Time"), LCD4linux.StandbyScreenTime5))
				self.list4.append(getConfigListEntry(_("- Screen 6 Changing Time"), LCD4linux.StandbyScreenTime6))
				self.list4.append(getConfigListEntry(_("- Screen 7 Changing Time"), LCD4linux.StandbyScreenTime7))
				self.list4.append(getConfigListEntry(_("- Screen 8 Changing Time"), LCD4linux.StandbyScreenTime8))
				self.list4.append(getConfigListEntry(_("- Screen 9 Changing Time"), LCD4linux.StandbyScreenTime9))
			self.list4.append(getConfigListEntry(_("Clock"), LCD4linux.StandbyClock))
			if LCD4linux.StandbyClock.value != "0":
				self.list4.append(getConfigListEntry(_("- which LCD"), LCD4linux.StandbyClockLCD))
				self.list4.append(getConfigListEntry(_("- Type"), LCD4linux.StandbyClockType))
				if LCD4linux.StandbyClockType.value[0] == "5":
					self.list4.append(getConfigListEntry(_("- Analog Clock"), LCD4linux.StandbyClockAnalog))
				elif LCD4linux.StandbyClockType.value[0] == "1":
					self.list4.append(getConfigListEntry(_("- Spacing"), LCD4linux.StandbyClockSpacing))
				self.list4.append(getConfigListEntry(_("- Size"), LCD4linux.StandbyClockSize))
				self.list4.append(getConfigListEntry(_("- Position"), LCD4linux.StandbyClockPos))
				self.list4.append(getConfigListEntry(_("- Alignment"), LCD4linux.StandbyClockAlign))
				self.list4.append(getConfigListEntry(_("- Split Screen"), LCD4linux.StandbyClockSplit))
				self.list4.append(getConfigListEntry(_("- Color"), LCD4linux.StandbyClockColor))
				self.list4.append(getConfigListEntry(_("- Shadow Edges"), LCD4linux.StandbyClockShadow))
				self.list4.append(getConfigListEntry(_("- Font"), LCD4linux.StandbyClock
