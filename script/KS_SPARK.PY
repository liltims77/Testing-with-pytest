# -*- coding: utf-8 -*-
"""
Description : A pyspark script to parse T24 XMLfiles nd store on sql server
Author : Gbenga Aleshinloye
Created on Feb 12 2021
"""
# import relevant libraries
from pyspark import SparkContext, SparkConf, SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import concat, col,lit
from pyspark.sql import functions as F
from pyspark.sql import Row
from datetime import datetime
from datetime import timedelta
import com.microsoft.spark.sqlanalytics
from com.microsoft.spark.sqlanalytics.Constants import Constants
from pyspark.sql.functions import col
import xml.etree.ElementTree as ET
import sys



# start spark session
appName = "XML parser 4"

spark = SparkSession.builder \
        .appName(appName) \
        .getOrCreate()

# Sqlserver database connection parameters 
p_target_server = target_server
p_target_database = target_database
p_adls_filepath = adls_filepath
p_target_schema = target_schema



#read table data into a spark dataframe
def read_query_to_dataframe(query):
    df = (spark.read
         .option(Constants.SERVER,p_target_server)
         .option(Constants.DATABASE,p_target_database)
         .option(Constants.QUERY, f"{query}")
         .synapsesql()
    )
    #return dataframe ouput
    return df

# insert the dataframe into the table provided.
def insert_dataframe_into_database(dframe, tablename, value_type):
    """ """
    
    if value_type.upper() == 'S':
        tab_name = f"{tablename}_TMP"
    elif value_type.upper() == 'M':
        tab_name = f"{tablename}_VALUES_TMP"
    
    (dframe.write 
     .option(Constants.SERVER,p_target_server)
     .option(Constants.DATABASE, p_target_database)
     .mode("append")
     .synapsesql(f"{p_target_database}.{p_target_schema}.{tab_name}")
    )
    
    
   

 # process single value.
def parse_xml_single_values(rdd):

    results = []
    if len(gv_etl_df) == 0 :                       
        #print(sv_etl_dict.keys())
        df_dict = {'RECID': rdd[0], 'SOURCE_INSERTUPDATE_DATE': rdd[2]}
        root = ET.fromstring(rdd[1])
        sv_xml_records = {child.tag.replace("c", ""):  child.text if child.text is not None else '' for child in root}
        xml_etl_data = {value:sv_xml_records.get(key, '') for key,value in sv_etl_dict.items() if value != 'RECID'}
        #process local reference table
        if lv_flag == 'Y' or flat_yn == 'Y':
            lv_xml_records = {}
            ch_xml_records = {}
            for child in root:
                if lv_flag == 'Y':
                    if child.tag.replace("c", "") == lv_xml_attribute_tag :
                        dict_attr = child.attrib
                        if bool(dict_attr):            
                            if "m" in dict_attr and "s" not in dict_attr:
                                if child.text is None :
                                    v_test = ''
                                else:
                                    v_test = child.text  
                                lv_xml_records[dict_attr["m"]] = v_test                  
                        else:
                            if child.text is None :
                                v_test = ''
                            else:
                                v_test = child.text  
                            lv_xml_records["1"] = v_test 

                if flat_yn == 'Y':                
                    if child.tag.replace("c", "") in ch_etl_dict.keys():
                        v_column_name = ch_etl_dict.get(child.tag.replace("c", ""))
                        if v_column_name in flt_column_dict.keys():
                            v_column_max = flt_column_dict.get(v_column_name) 
                            dict_attr = child.attrib
                            if bool(dict_attr): 
                                if "m" in dict_attr and "s" not in dict_attr:                                    
                                    if int(dict_attr["m"]) <= int(v_column_max) :
                                        v_full_column_name = v_column_name + "_" + dict_attr["m"]
                                        if child.text is None :
                                            v_test = ''
                                        else:
                                            v_test = child.text  
                                            ch_xml_records[v_full_column_name] = v_test                  
                            else:
                                if int(v_column_max) >= 1 :
                                    v_full_column_name = v_column_name + "_1" 
                                    if child.text is None :
                                        v_test = ''
                                    else:
                                        v_test = child.text  
                                    ch_xml_records[v_full_column_name] = v_test    

                    if child.tag.replace("c", "")  == lv_xml_attribute_tag :
                        if tr_lv_flag  == 'Y' and lv_flag == 'Y' :
                            dict_attr = child.attrib
                            if bool(dict_attr):
                                if "m" in dict_attr and "s" in dict_attr:
                                    m_index = dict_attr["m"]
                                    v_column_name = lv_etl_dict.get(m_index)
                                    v_column_index = dict_attr["s"]
                                    v_column_values = child.text
                                    if v_column_name in flt_column_dict.keys():
                                        v_column_max = flt_column_dict.get(v_column_name)
                                        if v_column_name in tr_lv_etl_dict.keys():                                         
                                            if int(v_column_index) <= int(v_column_max) :
                                                v_full_column_name = v_column_name + "_" + v_column_index
                                                if v_column_values is None :
                                                    v_test = ''
                                                else:
                                                    v_test = v_column_values  
                                                ch_xml_records[v_full_column_name] = v_test



            if  lv_xml_records :
                lv_xml_etl_data = {value:lv_xml_records.get(key, '') for key,value in lv_etl_dict.items()}
                #print(lv_xml_etl_data)
                xml_etl_data.update(lv_xml_etl_data)
            if  ch_xml_records :
                xml_etl_data.update(ch_xml_records)
        
        #print(xml_etl_data)
        # check for extra columns in the queue table 
        if extra_column_yn == 'Y':
            df_extra_col_list = df_extra_col.split(",") 
            #The starting point will be rdd column 3, so the calculation is i + 3
            df_extra_col_dict = {df_extra_col_list[i]: rdd[i + 3]  for i in range(len(df_extra_col_list))}
            df_dict.update(df_extra_col_dict)
            
        df_dict.update(xml_etl_data)
        #print(df_dict)

        results.append(df_dict)
    else:
        if len(gv_etl_df) == 2 :
            df_dict = {'RECID': rdd[0], 'SOURCE_INSERTUPDATE_DATE': rdd[2]}
            # check for extra columns in the queue table 
            if extra_column_yn == 'Y':
                df_extra_col_list = df_extra_col.split(",") 
                #The starting point will be rdd column 3, so the calculation is i + 3
                df_extra_col_dict = {df_extra_col_list[i]: rdd[i + 3]  for i in range(len(df_extra_col_list))}
                df_dict.update(df_extra_col_dict)
                
            root = ET.fromstring(rdd[1])
            sv_xml_records = {child.tag.replace("c", ""): child.text for child in root}
            column_name = gv_etl_dict['1']
            if column_name :
                for key in sv_xml_records:                
                    df_dict = {'RECID': rdd[0], column_name : sv_xml_records[key], 'SOURCE_INSERTUPDATE_DATE': rdd[2]}
                    # check for extra columns in the queue table 
                    if extra_column_yn == 'Y':
                        df_extra_col_list = df_extra_col.split(",") 
                        #The starting point will be rdd column 3, so the calculation is i + 3
                        df_extra_col_dict = {df_extra_col_list[i]: rdd[i + 3]  for i in range(len(df_extra_col_list))}
                        df_dict.update(df_extra_col_dict)
                    results.append(df_dict)
        
    #print(results)
    return results




def ingest_xml_table_data(tablename,min_datetime,max_datetime):
    """
     This will parse and transforms XML into relational table.
     It takes as parameter the table name and returns the dataframe.    
    """
    global lv_xml_attribute_tag
    lv_xml_attribute_tag = 'UNKNOWN'
    global flat_yn
    flat_yn = 'N'
    tablename = tablename.upper()
    
    # fetch additional columns names that are part of the queue tables apart from recid and xmlrecord from etl_dictionary 
    extra_col_query = f"select string_agg(convert(varchar(max),column_name),',') column_name from {p_target_schema}.etl_dictionary \
              where table_name = '{tablename}'and single_multi_indicator ='E' \
              except \
              select column_name from {p_target_schema}.etl_dictionary  where table_name = '{tablename}' \
              and single_multi_indicator in ('S','LF')"
    
    
    global extra_column_yn
    extra_column_yn = 'N'
    global df_extra_col
    df_extra_col = read_query_to_dataframe(extra_col_query).collect()[0].column_name
    if df_extra_col is not None :
        inner_query_extra_col = df_extra_col + ","
        outer_query_extra_col = "," + df_extra_col 
        extra_column_yn = 'Y'
    else :
        inner_query_extra_col = " "
        outer_query_extra_col = " "
    

    S_tablename = tablename.lower()
    p_filepath = f"{p_adls_filepath}/{S_tablename}/{S_tablename}*.parquet"
    df_read_file = spark.read.parquet(p_filepath)
    df_read_file.createOrReplaceTempView(S_tablename)
    
    # read the newest (ranked) data from the queue table    
    queue_tab_query = f"select recid, xmlrecord,CDCSOURCECOMMIT,CDCSourceOperation {outer_query_extra_col}  \
        from (select recid, xmlrecord, CDCSourceCommit, CDCSourceOperation, {inner_query_extra_col} \
        row_number() over (partition by recid order by CDCSourceCommit  desc) row_no from {S_tablename} \
        where CDCSourceCommit > '{min_datetime}' and CDCSourceCommit <= '{max_datetime}') sub_query where sub_query.row_no = 1"
    
    df = spark.sql(queue_tab_query)    
    df = df.withColumnRenamed("CDCSOURCECOMMIT","SOURCE_INSERTUPDATE_DATE")
    allowoperation=["INSERT","UPDATE"]
    df = df.filter(df.CDCSourceOperation.isin(allowoperation))
    df = df.drop(col("CDCSourceOperation"))
   
    # check if target table is created and get it structure 
    query_tab_meta = f"select COLUMN_NAME x_colname,ordinal_position from information_schema.columns \
               where upper(table_name) = upper('{tablename}_TMP') and  upper(table_schema) = upper('{p_target_schema}') "
    
    df_tab_mt = read_query_to_dataframe(query_tab_meta)  
    

    #df.show(5, False)

    if df.count() > 0 and df_tab_mt.count() > 0:

        # get the single-value (sv) table's etl dictionary
        sv_etl_dict_query = f"SELECT column_name, xml_attribute_tag from {p_target_schema}.etl_dictionary where table_name = '{tablename}' and single_multi_indicator = 'S'"
        sv_etl_df = read_query_to_dataframe(sv_etl_dict_query).collect()
        
        # get the group-value (G) table's etl dictionary
        global gv_etl_df
        gv_etl_dict_query = f"SELECT column_name, xml_attribute_tag from {p_target_schema}.etl_dictionary where table_name = '{tablename}' and single_multi_indicator = 'G'"
        gv_etl_df = read_query_to_dataframe(gv_etl_dict_query).collect()  
        
        
        global sv_etl_dict
        global mv_etl_dict
        global gv_etl_dict
        sv_etl_dict = {val[1]:val[0] for val in sv_etl_df}
        gv_etl_dict = {val[1]:val[0] for val in gv_etl_df}
        #print(sv_etl_dict)

        # parse the single-value xml data
        transpose_column_query = f"SELECT column_name, xml_attribute_tag from {p_target_schema}.etl_dictionary where table_name = '{tablename}' and FLATTEN_INDICATOR = 'Y' and single_multi_indicator = 'M'" 
        check_transpose_column_query = read_query_to_dataframe(transpose_column_query).collect()
        global ch_etl_dict
        ch_etl_dict = {val[1]:val[0] for val in check_transpose_column_query}
        
        
        #parse local reference and local fields 
        global lv_flag 
        global tr_lv_flag
        lv_flag = 'N' 
        tr_lv_flag = 'N' 
        
        lv_att_query = f"SELECT max(xml_attribute_tag) xml_attribute_tag from {p_target_schema}.etl_dictionary where table_name = '{tablename}' and single_multi_indicator = 'LF'"
        lv_att_df  = read_query_to_dataframe(lv_att_query).collect()
        if len(lv_att_df) >  0 and lv_att_df[0][0] is not None :
            lv_att_df = spark.createDataFrame(lv_att_df)            
            lv_xml_attribute_tag = lv_att_df.select("xml_attribute_tag").collect()[0].xml_attribute_tag 
            lv_etl_dict_query = f"SELECT column_name, xml_local_ref_attr_tag from {p_target_schema}.etl_dictionary where table_name = '{tablename}' and single_multi_indicator = 'LF' AND xml_attribute_tag = '{lv_xml_attribute_tag}' "
            lv_etl_df = read_query_to_dataframe(lv_etl_dict_query).collect()
            if len(lv_etl_df) >  0:
                lv_flag = 'Y'
                global lv_etl_dict
                lv_etl_dict = {val[1]:val[0] for val in lv_etl_df}
                #print(lv_etl_dict)
                tr_lv_etl_dict_query = f"SELECT column_name, xml_local_ref_attr_tag from {p_target_schema}.etl_dictionary where table_name = '{tablename}' and single_multi_indicator = 'LF' and xml_attribute_tag = '{lv_xml_attribute_tag}'  and FLATTEN_INDICATOR = 'Y' "
                tr_lv_etl_df = read_query_to_dataframe(tr_lv_etl_dict_query).collect()
                if len(tr_lv_etl_df) >  0:
                    tr_lv_flag = 'Y'
                    global tr_lv_etl_dict
                    tr_lv_etl_dict = {val[0]:val[1] for val in tr_lv_etl_df}
                    
                
        if len(check_transpose_column_query) > 0:
            flat_yn = 'Y'            
        if flat_yn == 'Y':
            flt_column_query = f"SELECT b.column_name,max(cast(substring(a.column_name,(len(b.column_name) + 2), (len(a.column_name) - len(b.column_name))) as int))max_column from information_schema.columns a,{p_target_schema}.etl_dictionary b \
               where a.table_name = '{tablename}' and a.table_name = b.table_name and b.flatten_indicator = 'Y' and a.column_name like b.column_name+'_%' \
               group by b.column_name"  
            
            flt_column_df = read_query_to_dataframe(flt_column_query).collect()
            global flt_column_dict
            flt_column_dict = {val[0]:val[1] for val in flt_column_df}
            
            single_values = spark.createDataFrame(df.rdd.flatMap(parse_xml_single_values))                   
            single_values.cache()
            sv_temp_cols = tuple(single_values.columns)
            df_tab_mt.createOrReplaceTempView("df_tab_mt")
            sv_miss_col = f"select x_colname from df_tab_mt where trim(x_colname) not in {sv_temp_cols} "            
            df_miss_col = spark.sql(sv_miss_col)
            if df_miss_col.count() > 0 :
                miss_column_list= df_miss_col.rdd.map(lambda x: x[0]).collect()
                for item in miss_column_list:
                    single_values = single_values.withColumn(item,lit(''))
                
            single_values = single_values.na.replace('', None)    
            df_tab_mt = df_tab_mt.sort("ordinal_position")
            df_column_list= df_tab_mt.rdd.map(lambda x: x[0]).collect()
            single_values = single_values.select(df_column_list)
            insert_dataframe_into_database(single_values, tablename, 'S')
            
        else :
            single_values = spark.createDataFrame(df.rdd.flatMap(parse_xml_single_values))
            single_values.cache()
            sv_temp_cols = tuple(single_values.columns)
            df_tab_mt.createOrReplaceTempView("df_tab_mt")
            sv_miss_col = f"select x_colname from df_tab_mt where trim(x_colname) not in {sv_temp_cols} "            
            df_miss_col = spark.sql(sv_miss_col)
            if df_miss_col.count() > 0 :
                miss_column_list= df_miss_col.rdd.map(lambda x: x[0]).collect()
                for item in miss_column_list:
                    single_values = single_values.withColumn(item,lit(''))
                
            single_values = single_values.na.replace('', None)    
            df_tab_mt = df_tab_mt.sort("ordinal_position")
            df_column_list= df_tab_mt.rdd.map(lambda x: x[0]).collect()
            single_values = single_values.select(df_column_list)
            insert_dataframe_into_database(single_values, tablename, 'S')            
            
if __name__ == "__main__":
    ingest_xml_table_data(tablename,minsdatetime,maxdatetime)
            