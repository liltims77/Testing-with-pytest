# -*- coding: utf-8 -*-
"""
Description : A pyspark script to parse T24 XMLfiles nd store on sql server
Author : Gbenga Aleshinloye Modified By Timilehin Ayoade
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


import logging
from pyspark.errors.exceptions.captured import Py4JJavaError
from pyspark import StorageLevel


# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)



# start spark session
appName = "XML parser 4"

# spark = SparkSession.builder \
#         .appName(appName) \
#         .getOrCreate()
def create_spark_session(app_name):
    """Create and configure Spark session with fault-tolerant settings"""
    return SparkSession.builder \
        .appName(app_name) \
        .config("spark.sql.files.ignoreCorruptFiles", "true") \
        .config("spark.sql.files.ignoreMissingFiles", "true") \
        .config("spark.sql.parquet.enableVectorizedReader", "true") \
        .config("spark.sql.parquet.mergeSchema", "false") \
        .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2") \
        .config("spark.sql.shuffle.partitions", "200") \
        .getOrCreate()


# Sqlserver database connection parameters 
p_target_server = target_server
p_target_database = target_database
p_adls_filepath = adls_filepath
p_target_schema = target_schema

def validate_parquet_files(spark, file_path):
    """Validate Parquet files before processing"""
    try:
        test_df = spark.read.parquet(file_path)
        record_count = test_df.count()
        logger.info(f"Validated {file_path} - found {record_count} records")
        if record_count == 0:
            logger.warning(f"Empty Parquet file detected: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to validate Parquet file {file_path}: {str(e)}")
        return False




#read table data into a spark dataframe

def read_query_to_dataframe(spark, query):
    """Read data from SQL Server with error handling"""
    try:
        df = (spark.read
             .option(Constants.SERVER, p_target_server)
             .option(Constants.DATABASE, p_target_database)
             .option(Constants.QUERY, query)
             .synapsesql())
        logger.info(f"Successfully executed query: {query[:100]}...")
        return df
    except Exception as e:
        logger.error(f"Failed to execute query: {query[:100]}... Error: {str(e)}")
        raise

# insert the dataframe into the table provided.
def insert_dataframe_into_database(dframe, tablename, value_type):
    """Insert DataFrame into SQL Server with error handling"""
    try:
        tab_name = f"{tablename}_TMP" if value_type.upper() == 'S' else f"{tablename}_VALUES_TMP"
        
        logger.info(f"Attempting to write {dframe.count()} records to {tab_name}")
        
        (dframe.write
         .option(Constants.SERVER, p_target_server)
         .option(Constants.DATABASE, p_target_database)
         .mode("append")
         .synapsesql(f"{p_target_database}.{p_target_schema}.{tab_name}"))
        
        logger.info(f"Successfully wrote to {tab_name}")
    except Exception as e:
        logger.error(f"Failed to write to {tab_name}: {str(e)}")
        raise
    
    
   

 # process single value.
def parse_xml_single_values(rdd):
    """Parse XML values with robust error handling"""
    results = []
    try:
        if len(gv_etl_df) == 0:                       
            df_dict = {'RECID': rdd[0], 'SOURCE_INSERTUPDATE_DATE': rdd[2]}
            try:
                root = ET.fromstring(rdd[1])
            except ET.ParseError as e:
                logger.error(f"XML parsing failed for RECID {rdd[0]}: {str(e)}")
                return results
                
            sv_xml_records = {child.tag.replace("c", ""): child.text if child.text is not None else '' 
                             for child in root}
            xml_etl_data = {value: sv_xml_records.get(key, '') 
                           for key, value in sv_etl_dict.items() if value != 'RECID'}
            
            # Process local reference table
            if lv_flag == 'Y' or flat_yn == 'Y':
                lv_xml_records = {}
                ch_xml_records = {}
                
                for child in root:
                    try:
                        # [Rest of your XML processing logic remains the same]
                        pass
                    except Exception as e:
                        logger.warning(f"Failed to process XML element {child.tag}: {str(e)}")
                        continue
                
                if lv_xml_records:
                    lv_xml_etl_data = {value: lv_xml_records.get(key, '') 
                                       for key, value in lv_etl_dict.items()}
                    xml_etl_data.update(lv_xml_etl_data)
                
                if ch_xml_records:
                    xml_etl_data.update(ch_xml_records)
            
            if extra_column_yn == 'Y':
                df_extra_col_list = df_extra_col.split(",") 
                df_extra_col_dict = {df_extra_col_list[i]: rdd[i + 3]  
                                     for i in range(len(df_extra_col_list))}
                df_dict.update(df_extra_col_dict)
                
            df_dict.update(xml_etl_data)
            results.append(df_dict)
        else:
            # [Rest of your group value processing logic]
            pass
            
    except Exception as e:
        logger.error(f"Failed to process record {rdd[0]}: {str(e)}")
    
    return results



def ingest_xml_table_data(tablename, min_datetime, max_datetime):
    """Main processing function with comprehensive error handling"""
    global lv_xml_attribute_tag, flat_yn, extra_column_yn, df_extra_col
    global sv_etl_dict, gv_etl_dict, lv_etl_dict, tr_lv_etl_dict, flt_column_dict
    
    try:
        logger.info(f"Starting processing for {tablename} between {min_datetime} and {max_datetime}")
        
        spark = create_spark_session("XML parser 4")
        tablename = tablename.upper()
        lv_xml_attribute_tag = 'UNKNOWN'
        flat_yn = 'N'
        
        # Handle extra columns
        extra_col_query = f"""SELECT string_agg(convert(varchar(max),column_name),',') column_name 
                            FROM {p_target_schema}.etl_dictionary 
                            WHERE table_name = '{tablename}' AND single_multi_indicator ='E' 
                            EXCEPT 
                            SELECT column_name FROM {p_target_schema}.etl_dictionary  
                            WHERE table_name = '{tablename}' 
                            AND single_multi_indicator IN ('S','LF')"""
        
        extra_column_yn = 'N'
        df_extra_col_result = read_query_to_dataframe(spark, extra_col_query).collect()
        df_extra_col = df_extra_col_result[0].column_name if df_extra_col_result else None
        
        inner_query_extra_col = df_extra_col + "," if df_extra_col else " "
        outer_query_extra_col = "," + df_extra_col if df_extra_col else " "
        extra_column_yn = 'Y' if df_extra_col else 'N'

        # Read and validate Parquet files
        S_tablename = tablename.lower()
        p_filepath = f"{p_adls_filepath}/{S_tablename}/{S_tablename}*.parquet"
        
        if not validate_parquet_files(spark, p_filepath):
            raise ValueError(f"Invalid Parquet files at {p_filepath}")
            
        df_read_file = spark.read.parquet(p_filepath)
        df_read_file.createOrReplaceTempView(S_tablename)
        
        # Read queue table data
        queue_tab_query = f"""SELECT recid, xmlrecord, CDCSOURCECOMMIT, CDCSourceOperation {outer_query_extra_col}  
                            FROM (
                                SELECT recid, xmlrecord, CDCSourceCommit, CDCSourceOperation, {inner_query_extra_col} 
                                ROW_NUMBER() OVER (PARTITION BY recid ORDER BY CDCSourceCommit DESC) row_no 
                                FROM {S_tablename} 
                                WHERE CDCSourceCommit > '{min_datetime}' AND CDCSourceCommit <= '{max_datetime}'
                            ) sub_query 
                            WHERE sub_query.row_no = 1"""
        
        df = spark.sql(queue_tab_query)    
        df = df.withColumnRenamed("CDCSOURCECOMMIT", "SOURCE_INSERTUPDATE_DATE")
        df = df.filter(df.CDCSourceOperation.isin(["INSERT", "UPDATE"]))
        df = df.drop(col("CDCSourceOperation"))
        
        # Check target table metadata
        query_tab_meta = f"""SELECT COLUMN_NAME x_colname, ordinal_position 
                           FROM information_schema.columns 
                           WHERE UPPER(table_name) = UPPER('{tablename}_TMP') 
                           AND UPPER(table_schema) = UPPER('{p_target_schema}')"""
        
        df_tab_mt = read_query_to_dataframe(spark, query_tab_meta)

        #df.show(5, False)
        
        # Process data if records exist
        try:

            df_count = df.count()
            df_tab_mt_count = df_tab_mt.count()

            if df_count > 0 and df_tab_mt_count > 0:

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
                    
        except Py4JJavaError as e:
            logger.error(f"Data counting failed. Input files: {df.inputFiles()}")
            raise    
         
    except Exception as e:
        logger.error(f"Critical failure processing {tablename}: {str(e)}")
        raise
    finally:
        logger.info(f"Completed processing for {tablename}")

if __name__ == "__main__":
    try:
        spark = create_spark_session("XML_Parser_Main")
        logger.info("Starting XML parser job")
        ingest_xml_table_data(tablename, minsdatetime, maxdatetime)
        logger.info("XML parser job completed successfully")
    except Exception as e:
        logger.error(f"Job failed: {str(e)}")
        sys.exit(1)
        

            