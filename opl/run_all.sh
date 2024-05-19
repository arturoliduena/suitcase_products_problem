#!/bin/bash

# Define the path to the OPL executable and model file
OPL_PATH="/Applications/CPLEX_Studio2211/opl/bin/x86-64_osx/oplrun"
MODEL_FILE="./Suitcase_Products/model.mod"
DATA_DIR="./Suitcase_Products"

# Check if the model file exists
if [ ! -f "$MODEL_FILE" ]; then
  echo "Model file not found: $MODEL_FILE"
  exit 1
fi

# Check if the data directory exists
if [ ! -d "$DATA_DIR" ]; then
  echo "Data directory not found: $DATA_DIR"
  exit 1
fi

# Loop through each .dat file in the data directory
for DATA_FILE in "$DATA_DIR"/*.dat; do
  # Check if any .dat files are found
  if [ ! -f "$DATA_FILE" ]; then
    echo "No .dat files found in the directory: $DATA_DIR"
    exit 1
  fi
  
  # Run the model against the current .dat file
  echo "Running model for data file: $DATA_FILE"
  "$OPL_PATH" "$MODEL_FILE" "$DATA_FILE"
done
