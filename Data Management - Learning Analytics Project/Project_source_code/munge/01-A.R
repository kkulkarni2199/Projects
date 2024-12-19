# Example preprocessing script.

#Loading the libraries
library(ProjectTemplate)
library(dplyr)
library(ggplot2)
library(tidyr)
library(reshape2)

# *************Perform pre-processing on the enrollment data files ********

############FIRST CYCLE################

# First make a vector of enrollment files across all runs
enroll_data_files = c("data/cyber-security-1_enrolments.csv", "data/cyber-security-2_enrolments.csv", 
                "data/cyber-security-3_enrolments.csv", "data/cyber-security-4_enrolments.csv", 
                "data/cyber-security-5_enrolments.csv", "data/cyber-security-6_enrolments.csv", 
                "data/cyber-security-7_enrolments.csv"
                )
# Empty list
enroll_data_list = list()
enroll_data_list_2 = list()

# Full Data Merged
for(i in seq_along(enroll_data_files)) {
  
  # Read data into dataframe
  enroll_data = read.csv(enroll_data_files[i])
  
  #Add new column to identify the run number of each row
  enroll_data = enroll_data %>%
    mutate(run_number = i)
  
  # Load the processed dataframes into the empty list
  if (is.data.frame(enroll_data)) {
    enroll_data_list_2[[i]] <- enroll_data
  }
}

merged_enroll_data_2 = bind_rows(enroll_data_list_2)
cache('merged_enroll_data_2')

# Data Cleaning

# Create vector of columns to exclude from processing
columns_to_exclude = c("fully_participated_at",	"purchased_statement_at", "employment_area")

# Set loop to process through each file
for(i in seq_along(enroll_data_files)) {
  
  # Read data into dataframe
  enroll_data = read.csv(enroll_data_files[i])
  
  # Replace unknown values with NA to perform data cleaning and exclude specific columns
  for (col in setdiff(names(enroll_data), columns_to_exclude)) {
    enroll_data[[col]] <- ifelse(enroll_data[[col]] == "Unknown", NA, enroll_data[[col]])
  }
  
  # Clean the NA values
  enroll_data = enroll_data[complete.cases(enroll_data), ]
  
  #Add new column to identify the run number of each row
  enroll_data = enroll_data %>%
    mutate(run_number = i)
  
  # Load the processed dataframes into the empty list
  if (is.data.frame(enroll_data)) {
    enroll_data_list[[i]] <- enroll_data
  }
}



# Clear out any null values in the list
enroll_data_list <- enroll_data_list[!sapply(enroll_data_list, is.null)]

# Combine the data frames into one dataframe
merged_enroll_data = bind_rows(enroll_data_list)
cache('merged_enroll_data')

# Drop out columns which are not useful in our inspection
filtered_enroll_data = subset(merged_enroll_data, select = -c(enrolled_at, unenrolled_at, role, fully_participated_at, purchased_statement_at, detected_country)) 
cache('filtered_enroll_data')

# Filter data to find out top 5 countries with highest learners in each run

# Specify the number of top countries to visualize
top_countries <- 5  

# Calculate the learner counts for each country in each run
country_counts <- filtered_enroll_data %>%
  group_by(run_number, country) %>%
  summarise(learner_count = n()) %>%
  arrange(run_number, desc(learner_count))

# Filter for the top N countries by learner count in each run
top_countries_data <- country_counts %>%
  group_by(run_number) %>%
  top_n(top_countries, learner_count) %>%
  ungroup()

cache('top_countries_data')

##############SECOND CYCLE#####################


# ******Leaving surveys******* #


# File Selection
leaving_files = c("data/cyber-security-1_leaving-survey-responses.csv", "data/cyber-security-2_leaving-survey-responses.csv",
                  "data/cyber-security-3_leaving-survey-responses.csv", "data/cyber-security-4_leaving-survey-responses.csv",
                  "data/cyber-security-5_leaving-survey-responses.csv", "data/cyber-security-6_leaving-survey-responses.csv",
                  "data/cyber-security-7_leaving-survey-responses.csv")

# Create Empty List
leaving_data_list = list()

# Read CSV data and add run number and add data to list
for(i in seq_along(leaving_files)){
  
  leaving_data = read.csv(leaving_files[i])
  
  if(nrow(leaving_data)>0){
    leaving_data$run_number = i
    leaving_data_list[[i]] = leaving_data
  } else {
    message("File", leaving_files[i], "is empty")
  }
}

# Add the data from list to a single dataframe
merged_leaving_data = bind_rows(leaving_data_list)
cache('merged_leaving_data')

# Filter Other Column because of insignificance
filtered_leaving_data = merged_leaving_data %>%
  filter(leaving_reason != "Other")
cache('filtered_leaving_data')

# calculating frequency for on each visualization
reason_freq = filtered_leaving_data %>%
  group_by(run_number, leaving_reason) %>%
  summarise(count = n()) %>%
  ungroup()
cache('reason_freq')

# Filter employement status in enrollment data

filtered_employee_data = filtered_enroll_data %>%
  filter(run_number > 3)

cache('filtered_employee_data')







