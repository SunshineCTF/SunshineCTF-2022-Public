#!/usr/bin/env python3
import os
import sys
import string
import subprocess

GRSF_START_COMMON = '/*GRSF'
GRSF_START = ':'
GRSF_START_RAW = 'RAW:'
GRSF_END = '*/"@@"'
GRSF_END_ALT = '*/grsf("'
GRSF_END_ALT_RAW = '*/"'
GRSF_AFTER = '")/*GRSFEND*/'
GRSF_AFTER_RAW = '"/*GRSFEND*/'
GRSF_AFTER_COMMON = '/*GRSFEND*/'

GRSF_ALL = False
GRSF_REMOVE = False
GRSF_TOOL_PATH = None
GRSF_VERBOSE = 0

def set_grsf_tool_path(s):
	global GRSF_TOOL_PATH
	GRSF_TOOL_PATH = s

def grsf(action, s):
	p = subprocess.Popen([GRSF_TOOL_PATH, action], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	out, _ = p.communicate(s.encode("utf8"))
	
	if p.returncode != 0:
		raise RuntimeError("grsf tool failed: %d" % p.returncode)
	
	if GRSF_VERBOSE >= 4:
		print("genrandstr returned %r" % out)
	return out

def shouldProcessLine(line):
	return GRSF_END in line or GRSF_AFTER_COMMON in line

def escape(bs):
	ret = []
	printable = set(ord(c) for c in string.ascii_letters + string.digits + string.punctuation)
	for b in bs:
		if b == ord("\\"):
			ret.append("\\\\")
		elif b in printable:
			ret.append(chr(b))
		else:
			ret.append("\\x%02x" % b)
	return "".join(ret)

def processFile(fin):
	touched = False
	lines = []
	line_num = 0
	
	for line in fin:
		line_num += 1
		line_pos = 0
		try:
			while shouldProcessLine(line[line_pos:]):
				# Find the '/*GRSF(RAW)?:' part of the line
				if GRSF_START_COMMON not in line[line_pos:]:
					raise ValueError("GRSF annotation has incorrect start sequence: %r" % (line[line_pos:]))
				
				start_idx = line.index(GRSF_START_COMMON, line_pos) + len(GRSF_START_COMMON)
				
				# Determine if it is '/*GRSF:' or '/*GRSFRAW:'
				if line[start_idx:].startswith(GRSF_START):
					raw = False
					start_idx += len(GRSF_START)
				elif line[start_idx:].startswith(GRSF_START_RAW):
					raw = True
					start_idx += len(GRSF_START_RAW)
				else:
					raise ValueError("Invalid start sequence: %r" % (line[start_idx - len(GRSF_START_COMMON):start_idx + 4] + "..."))
				
				# Find the end of the GRSF comment
				if GRSF_END in line:
					# Token is '*/"@@"', meaning the GRSF string hasn't yet been generated
					end_idx = line.index(GRSF_END, line_pos)
					already_generated = False
					
					# Tail is everything after '"@@"'
					tail_idx = end_idx + len(GRSF_END)
				else:
					token = GRSF_END_ALT_RAW if raw else GRSF_END_ALT
					
					# Token should be '*/"' or '*/grsf("', meaning the raw GRSF string has already been generated
					end_idx = line.index(token, line_pos)
					
					# Points just after the opening quotation in '*/"' or '*/grsf("'
					grsf_start_idx = end_idx + len(token)
					already_generated = True
					
					# Find the '"/*GRSFEND*/' or '")/*GRSFEND*/' token
					token = GRSF_AFTER_RAW if raw else GRSF_AFTER
					grsf_end_idx = line.index(token, line_pos)
					
					# Tail is everything after '/*GRSFEND*/'
					tail_idx = grsf_end_idx + len(token)
				
				# Update current line position so we don't re-scan this GRSF annotation
				line_pos = tail_idx
				
				# Extract the string_to_encode part of '/*GRSF(RAW)?:string_to_encode*/'
				string_to_encode = line[start_idx:end_idx]
				
				# Lazy and unsafe way to convert character sequences like "\n"
				str_to_eval = '"%s"' % string_to_encode
				if GRSF_VERBOSE >= 2:
					print("Encoding: %s" % str_to_eval)
				string_to_encode = eval(str_to_eval)
				
				# Should we strip all generated GRSF strings?
				if GRSF_REMOVE:
					if not already_generated:
						continue
					
					# Rebuild the line as '.../*GRSF(RAW)?:string_to_encode*/"@@"...'
					new_line = line[:end_idx] + GRSF_END
					line_pos = len(new_line)
					new_line += line[tail_idx:]
					line = new_line
					touched = True
					continue
				
				if already_generated:
					# Extract the encoded_str part of '/*GRSF(RAW)?:string_to_encode*/(grsf\()?"encoded_str"\)?/*GRSFEND*/'
					encoded_str = line[grsf_start_idx:grsf_end_idx]
					encoded_str = eval('"%s"' % encoded_str)
					
					if not GRSF_ALL:
						# Decode the encoded_str and check if it matches string_to_encode
						actual = grsf("decode", encoded_str).decode("utf8")
						if actual == string_to_encode:
							continue
						
						if GRSF_VERBOSE >= 2:
							print("GRSF Mismatch: %r != %r" % (actual, string_to_encode))
				
				if GRSF_VERBOSE == 1:
					print("Encoding: %s" % str_to_eval)
				
				randstr = grsf("encode", string_to_encode)
				
				# Rebuild line with newly generated string
				end_token = GRSF_END_ALT_RAW if raw else GRSF_END_ALT
				after_token = GRSF_AFTER_RAW if raw else GRSF_AFTER
				new_line = line[:end_idx] + end_token + escape(randstr) + after_token
				
				# Very important to update line_pos here because the line's length probably changed
				line_pos = len(new_line)
				new_line += line[tail_idx:]
				line = new_line
				touched = True
			
			# No more GRSF annotations in this line, so we're done with it
			# print("Final line: %r" % line)
			lines.append(line)
		except Exception as e:
			e.args = (line_num,) + e.args
			raise
	return touched, lines

def main(argc, argv):
	if argc < 3:
		print("Usage: %s path/to/genrandstr file.grsf.c {fileN.grsf.c...}" % argv[0])
		return
	
	set_grsf_tool_path(argv[1])
	
	global GRSF_VERBOSE
	GRSF_VERBOSE = int(os.getenv("GRSF_VERBOSE", "1"), 0)
	
	if os.getenv("GRSF_ALL"):
		if GRSF_VERBOSE >= 3:
			print("Will regenerate all strings")
		global GRSF_ALL
		GRSF_ALL = True
	
	if os.getenv("GRSF_REMOVE"):
		if GRSF_VERBOSE >= 3:
			print("Will remove all strings")
		global GRSF_REMOVE
		GRSF_REMOVE = True
	
	for fname in argv[2:]:
		with open(fname) as fin:
			touched, lines = processFile(fin)
		
		if touched:
			with open(fname, "w") as fout:
				fout.writelines(lines)


if __name__ == "__main__":
	main(len(sys.argv), sys.argv)
