from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, round as spark_round, datediff, to_date

def run_spark_analysis(filepath):
    """Run distributed analytics on healthcare dataset using Apache Spark"""

    spark = SparkSession.builder \
        .appName("HealthcareDataPlatform") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    print("[Spark] Loading dataset...")
    df = spark.read.csv(filepath, header=True, inferSchema=True)

    # Calculate length of stay
    df = df.withColumn("Length of Stay",
        datediff(to_date(col("Discharge Date")), to_date(col("Date of Admission")))
    )

    print("\n[Spark] === Patients by Medical Condition ===")
    df.groupBy("Medical Condition") \
      .agg(count("*").alias("Count"),
           spark_round(avg("Billing Amount"), 2).alias("Avg Billing"),
           spark_round(avg("Length of Stay"), 1).alias("Avg Stay (days)")) \
      .orderBy(col("Count").desc()) \
      .show()

    print("\n[Spark] === Admission Type Breakdown ===")
    df.groupBy("Admission Type") \
      .agg(count("*").alias("Count")) \
      .orderBy(col("Count").desc()) \
      .show()

    print("\n[Spark] === Billing by Insurance Provider ===")
    df.groupBy("Insurance Provider") \
      .agg(count("*").alias("Patients"),
           spark_round(avg("Billing Amount"), 2).alias("Avg Billing"),
           spark_round(avg("Length of Stay"), 1).alias("Avg Stay")) \
      .orderBy(col("Avg Billing").desc()) \
      .show()

    print("\n[Spark] === Test Results Distribution ===")
    df.groupBy("Test Results") \
      .agg(count("*").alias("Count")) \
      .orderBy(col("Count").desc()) \
      .show()

    print("\n[Spark] === Top 10 Doctors by Patient Count ===")
    df.groupBy("Doctor") \
      .agg(count("*").alias("Patient Count"),
           spark_round(avg("Billing Amount"), 2).alias("Avg Billing")) \
      .orderBy(col("Patient Count").desc()) \
      .limit(10) \
      .show()

    spark.stop()
    print("[Spark] Analysis complete.")

if __name__ == "__main__":
    run_spark_analysis("healthcare_dataset.csv")
