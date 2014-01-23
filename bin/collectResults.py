#!/usr/bin/env python
'''
Created on Jan 23, 2014

@author: Bryan Lunt <blunt@sdsc.edu>
'''
from __future__ import print_function

import cipresbenchmark.BenchmarkLoader as BL

import argparse
import os
import re
import json

import sqlite3

def main():
	parser = argparse.ArgumentParser()
	args = parser.parse_args()
	
	script_abs_path = os.path.realpath(__file__)
	script_abs_dir  = os.path.dirname(script_abs_path)
	benchmark_system_dir   = os.path.realpath(os.path.join(script_abs_dir,'..'))
	
	#setup directories
	output_dir = os.path.join(benchmark_system_dir,"output")
	input_dir  = os.path.join(benchmark_system_dir,"inputs")
	benchmark_dir = os.path.join(benchmark_system_dir,"benchmarks")
	
	
	MemDB = sqlite3.connect(":memory:")
	
	
	#load all benchmarks (We need this in order to build the table)
	benchmarks = BL.load_benchmarks_from_path(benchmark_dir)
	
	for onebench in benchmarks:
		onebench.setUp();
		#create an appropriate table to hold the results of this benchmark
		
		NAME = onebench.name
		varnames = onebench.getVarnames()
		
		
		schemaString = "create table %s( %s, UUID, EXECUTION_TIME, COMMANDLINE varchar);" % (NAME, ",".join(varnames) )
		MemDB.execute(schemaString)
		
		individual_outputs = [i for i in os.listdir(output_dir) if os.path.isdir(i) and i.startswith(NAME + "_")]
		for one_output in individual_outputs:
			UUID = re.sub('.*__','',one_output)
			
			start = 0
			end = 0
			
			with open(os.path.join(one_output,'start.txt')) as startfile:
				start = int(startfile.read())
			
			with open(os.path.join(one_output,'done.txt')) as endfile:
				end = int(endfile.read())
			
			EXECUTION_TIME = end - start
			
			with open(os.path.join(one_output, 'PARAMETERS.json')) as paramfile:
				other_parameters = json.load(paramfile)
			
			all_params = dict()
			all_params.update(other_parameters)
			all_params['EXECUTION_TIME'] = EXECUTION_TIME
			all_params['UUID'] = UUID
			
			all_names = all_params.keys()
			all_values = [all_params[i] for i in all_names]
			
			insertString = "insert into %s(%s) values (%s)" % ( NAME, ','.join(all_names), ','.join(all_values))
			MemDb.execute(insertString)
		

if __name__ == "__main__":
	main()