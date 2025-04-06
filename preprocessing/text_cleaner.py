from pyspark.sql import SparkSession
import pyspark.sql.functions as F

spark = SparkSession.builder \
    .appName("Wiki40B Preprocessing") \
    .config("spark.driver.memory", "8g")\
    .getOrCreate()

# load the parquet file
train_df = spark.read.parquet("0000.parquet")
valid_df = spark.read.parquet("validate_0000.parquet")

# text cleaning
def clean_text(text):
    import re
    text = re.sub(r'<[^>]+>', '', text)  # removing the HTML labels
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove non-alphabetic characters
    text = re.sub(r'\s+', ' ', text).strip().lower()  #Merge consecutive spaces and standardize case
    return text

# Register UDF
clean_text_udf = F.udf(clean_text, StringType())

# apply the cleaning
train_df = train_df.withColumn("cleaned_text", clean_text_udf(F.col("text")))
valid_df = valid_df.withColumn("cleaned_text", clean_text_udf(F.col("text")))

# Step 4: Tokenization (split into sentences)
# Using a simple split, you may want to use a more sophisticated tokenizer
train_sentences = train_df.select(F.explode(F.split(F.col("cleaned_text"), "[.!?]")).alias("sentence"))
valid_sentences = valid_df.select(F.explode(F.split(F.col("cleaned_text"), "[.!?]")).alias("sentence"))

# Step 5: Feature extraction using CountVectorizer
count_vectorizer = CountVectorizer(inputCol="sentence", outputCol="features")
pipeline = Pipeline(stages=[count_vectorizer])

# Fit and transform training data
pipeline_model = pipeline.fit(train_sentences)
train_features = pipeline_model.transform(train_sentences)

# Transform validation data
valid_features = pipeline_model.transform(valid_sentences)
