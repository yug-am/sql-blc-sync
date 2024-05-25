from translate_sql_to_blc import wrapper_func


def handle_queries(queries_str):
	show_logs = True 
	transformed_queries = wrapper_func(queries_str)
	#print(transformed_queries)
	if show_logs:
		for query in transformed_queries:
			print(query)
	return transformed_queries	

if __name__ == "__main__":	
	queries  = """INSERT INTO Plot (PlotId,  PlotInfo) VALUE('1','kl_clt_01');
INSERT INTO Plot (PlotId, PlotInfo) VALUE('2','kl_tvc_02');
INSERT INTO Plot (PlotId, PlotInfo) VALUE('3','dl_del_03');
INSERT INTO Khatauni (KId, Aadhar, PId) VALUE('101','81','1');
INSERT INTO Khatauni (KId, Aadhar, PId) VALUE('201','82','2');
			"""
	queries = queries.strip("\n")		
	sql_ls = queries.split("\n")
	#for sql in sql_ls:
		#print(sql)
	blc_transformed_ls  = handle_queries(queries)
	#check for table and blockchain hash
	if 0:
		print("Hashes dont match")
		exit()

			


		