# Define the Python interpreter
PYTHON = python3

# Define the script to run
SCRIPT = Main.py

# Experiment 1
experiment1:
	@echo "Running experiment 1"
	@$(PYTHON) $(SCRIPT) greedy "price,weight,side_linear,side_quad,combined_linear,combined_quad" output/results_greedy.csv

# Experiment 2
experiment2:
	@echo "Running experiment 2"
	@$(PYTHON) $(SCRIPT) greedy "price" output/results_greedy_price.csv

# Experiment 3
experiment3:
	@echo "Running experiment 3"
	@$(PYTHON) $(SCRIPT) GRASP "price" output/results_GRASP_price.csv

# Run all experiments
all: experiment1 experiment2 experiment3

# Clean the output files
clean:
	@echo "Cleaning up"
	@rm -f output/results_greedy.csv output/results_greedy_price.csv output/results_GRASP_price.csv
