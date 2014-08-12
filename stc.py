#!/usr/bin/env python
import getopt, fileinput, sys




                                                # its not always black and white 
black     = "\033[1;30m"
red       = "\033[31m"
green     = "\033[32m"
darkgreen = "\033[1;32m"
yellow    = "\033[0;33m"
blue      = "\033[34m"
white     = "\033[1;37m"
normal    = "\033[37m"
off       = "\033[0;37m"

def check_field(field, list):
        return any (f in field for f in list)

def colorize(line):
        
        date, time, timezone, MACB, source, sourcetype, type, user, host, short, desc, version, filename, inode, notes, format, extra = line.split(',')

        # file opening
        if "LNK" in source: 
          short = green + short + off
        if short.endswith('.lnk'):
          short = green + short + off
        if short.endswith('.LNK'):
          short = green + short + off
        if short.startswith('URL:file///'):
          short = green + short + off
        if check_field(short, ["opened by","CreateDate"]): 
          short = green + short + off
        if check_field(desc, ["URL:file///"]): 
          desc = green + desc + off

        # web history
        if check_field(source, ["LSO"]):
          source = yellow + source + off
        if check_field(sourcetype, ["Firefox 3 history","Internet Explorer","LSO","Flash Cookie"]):
          sourcetype = yellow + sourcetype + off
        if check_field(type, ["URL","LSO"]):
          type = yellow + type + off
        if check_field(short, ["visited","URL","Flash Cookie"]):
          short = yellow + short + off
        if check_field(desc, ["http://","LSO"]):
          desc = yellow + desc + off
        elif desc.startswith("URL"):
          desc = yellow + desc + off

        # deleted data
        if check_field(sourcetype, ["Deleted Registry","$Recycle.bin"]):
          sourcetype = black + sourcetype + off
        if check_field(short, ["DELETED","deleted","RECYCLE"]):
          short = black + short + off
        if check_field(desc, ["[DELETED]","RECYCLE"]):
          desc = black + desc + off
        if check_field(filename, ["RECYCLE"]):
          filename = black + filename + off

        # execution     
        if check_field(sourcetype, ["RunRMU key","UserAssist key","Prefetch","XP Prefetch"]):
          sourcetype = red + sourcetype + off
        if check_field(type, ["CMD typed","Last run","Time of Launch"]):
          type = red + type + off
        if check_field(short, ["RunMRU","UEME_","MUICache",".pf","was executed"]):
          short = red + short + off
        if check_field(desc, ["typed the following cmd",".pf"]):
          desc = red + desc + off

        # device or usb usage
        if check_field(sourcetype, ["SetupAPILog","MountPoints2 key"]):
          sourcetype = blue + sourcetype + off
        if check_field(type, ["Drive last mounted"]):
          type = blue + type + off
        if check_field(short, ["RemovableMedia","STORAGE/RemovableMedia","USB","/USB/Vid_","Enum/USBSTOR/Disk&Ven_","drive mounted","volume mounted","MountPoints2 key"]):
          short = blue + short + off

        # folder opening
        if check_field(short, ["ShellNoRoam/Bags","BagMRU"]):
          short = darkgreen + short + off

        # log file
        if check_field(source, ["LOG"]):
          source = white + source + off
        if check_field(sourcetype, ["Log","XP Firewall Log"]):
          sourcetype = white + sourcetype + off
        
        return date+','+time+','+timezone+','+MACB+','+source+','+sourcetype+','+type+','+user+','+host+','+short+','+desc+','+version+','+filename+','+inode+','+notes+','+format+','+extra

def main():

    try:
        if sys.argv[1] == '-h':
            print 'the dfir super timeline colorizer.'
            print '%s <logfile> (or stdin)\n' % sys.argv[0]
            print "- LEGEND -"
            print green + "File Opening"
            print yellow + "Web History"
            print black + "Deleted Data"
            print red + "Execution"
            print blue + "Device or USB Usage"
            print darkgreen + "Folder Opening"
            print white + "Log File"
            sys.exit()
    except SystemExit as e:
      sys.exit(e)
    except:
      pass

    for line in fileinput.input():
      print colorize(line),

if __name__ == '__main__':
    main()
