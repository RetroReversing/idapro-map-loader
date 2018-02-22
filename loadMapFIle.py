import sys
from idautils import *
from idaapi import *

def parse_symbol_line(symbol_line,symbols_addresses):
    address, symbolName = line.split()
    int_address = int('0x'+address,16)
    symbols_addresses[int_address] = symbolName
    return symbols_addresses


all_symbols_addresses = {}
file_to_open = "./BIKE.MAP" # **PATH TO YOUR MAP FILE GOES HERE**
with open(file_to_open, "r") as ins:
    array = []
    found_entry_point = False
    
    for line in ins:
        if len(line) < 3:
            continue
        # break
        if line.startswith('Program entry point'):
            found_entry_point = True
            continue
        if line.startswith('  Address  Names'):
            print "line:",line
            continue
        if not found_entry_point:
            continue
        all_symbols_addresses = parse_symbol_line(line, all_symbols_addresses)
        array.append(line)

ea = BeginEA()
for funcea in Functions(SegStart(ea), SegEnd(ea)):
    functionName = GetFunctionName(funcea)
    print functionName

for segea in Segments():
    for funcea in Functions(segea, SegEnd(segea)):
        functionName = GetFunctionName(funcea)
        
        if funcea in all_symbols_addresses:
            new_name = all_symbols_addresses[funcea]
            if functionName != new_name:
                print "Oldname:",functionName, "NewName:", new_name
                idc.MakeName(funcea, new_name)

print "Complete"
