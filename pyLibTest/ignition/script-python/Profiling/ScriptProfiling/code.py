def log_profiling(script_name, start_time, end_time):
	import system
	import time
	
	# Define the logger
	logger = system.util.getLogger("Profiler")
	
	# Log the parameters passed into the function
	logger.info("[ScriptProfiling] log_profiling called with the following parameters:")
	logger.info("[ScriptProfiling] script_name: {}".format(script_name))
	logger.info("[ScriptProfiling] start_time: {}".format(start_time))
	logger.info("[ScriptProfiling] end_time: {}".format(end_time))

	enable_profiling = True  # Always enable profiling as no session-based control is used
	if not enable_profiling:
		logger.info("[ScriptProfiling] Profiling disabled for view.")
		return

	# Convert start_time and end_time to string in a proper SQL DATETIME format
	start_time_str = system.date.format(system.date.fromMillis(int(start_time * 1000)), "yyyy-MM-dd HH:mm:ss")
	end_time_str = system.date.format(system.date.fromMillis(int(end_time * 1000)), "yyyy-MM-dd HH:mm:ss")
	
	execution_time = end_time - start_time
	timestamp = system.date.now()

	# Log the data that will be inserted into the database
	logger.info("[ScriptProfiling] Preparing to log profiling data: {}, {}, {}, {}, {}".format(timestamp, script_name, execution_time, start_time_str, end_time_str))
	
	# Update query to store datetime values in string format
	query = "INSERT INTO profiling_logs (timestamp, script_name, execution_time, start_time, end_time) VALUES (?, ?, ?, ?, ?)"
	params = [timestamp, script_name, execution_time, start_time_str, end_time_str]
	
	try:
		system.db.runPrepUpdate(query, params, "pyLib")
		logger.info("[ScriptProfiling] Profiling data successfully logged to database.")
	except Exception as e:
		logger.error("[ScriptProfiling] Failed to log profiling data: {}".format(e))
		
def clear_db_data():
	import system
	"""
	Clears the profiling_logs table in the pyLib database.
	This function ensures data is only cleared once per session.
	"""
	try:
		# Clear the profiling_logs table
		clear_query = "DELETE FROM profiling_logs"
		system.db.runPrepUpdate(clear_query, [], "pyLib")
		logger = system.util.getLogger("Profiler")
		logger.info("[ScriptProfiling] All data in the profiling_logs table deleted successfully.")
	except Exception as e:
		logger = system.util.getLogger("Profiler")
		logger.error("[ScriptProfiling] Error deleting data from the profiling_logs table: {}".format(e))