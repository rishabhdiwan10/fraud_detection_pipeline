import os
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, pandas_udf
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, FloatType
import xgboost as xgb
import pandas as pd

# Connect PySpark to Kafka
os.environ['PYSPARK_SUBMIT_ARGS'] = f'--packages org.apache.spark:spark-sql-kafka-0-10_2.12:{pyspark.__version__} pyspark-shell'

# Load the trained XGBoost model globally so Spark worker nodes can access it
model = xgb.XGBClassifier()
model.load_model("fraud_model.json")

# Define the Pandas UDF for high-performance, vectorized inference
@pandas_udf(FloatType())
def predict_fraud_udf(amount_series: pd.Series, is_intl_series: pd.Series) -> pd.Series:
    """ Applies the XGBoost model to micro-batches of streaming data. """
    # Reconstruct the feature dataframe expected by XGBoost
    features_df = pd.DataFrame({
        'amount': amount_series, 
        'is_international': is_intl_series
    })
    # Predict probability of class 1 (Fraud)
    probabilities = model.predict_proba(features_df)[:, 1]
    return pd.Series(probabilities)

def create_spark_session():
    return SparkSession.builder \
        .appName("RealTimeFraudScoring") \
        .master("local[*]") \
        .getOrCreate()

def process_stream():
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")

    # Define the exact data contract
    schema = StructType([
        StructField("transaction_id", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("merchant_id", StringType(), True),
        StructField("timestamp", StringType(), True),
        StructField("is_international", IntegerType(), True)
    ])

    print("Connecting to live Kafka stream...")
    
    # 1. Ingest
    raw_stream = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "transactions") \
        .option("startingOffsets", "latest") \
        .load()

    # 2. Parse JSON
    parsed_stream = raw_stream \
        .selectExpr("CAST(value AS STRING) as json_string") \
        .select(from_json(col("json_string"), schema).alias("data")) \
        .select("data.*")

    # 3. Predict Real-Time Fraud
    scored_stream = parsed_stream.withColumn(
        "fraud_probability", 
        predict_fraud_udf(col("amount"), col("is_international"))
    )

    # 4. Output to console
    print("Real-time AI scoring initiated. Waiting for transactions...")
    query = scored_stream.writeStream \
        .outputMode("append") \
        .format("console") \
        .trigger(processingTime='2 seconds') \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    process_stream()