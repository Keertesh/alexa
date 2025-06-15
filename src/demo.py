from agents.data_ingestion_agent import DataIngestionAgent

# Sample data with valid and invalid records
sample_data = [
    {"id": 1, "name": "John Doe", "age": 30, "email": "john.doe@example.com"},
    {"id": 2, "name": "Jane Smith", "age": "twenty-five", "email": "jane.smith@example.com"},  # Invalid age
    {"id": 3, "name": "Alice Brown", "age": 40, "email": "alice.brown"},  # Invalid email
    {"id": 4, "name": "Bob Green", "age": 22, "email": "bob.green@example.com"},
    {"id": 5, "name": "Charlie Black", "age": 35, "email": "charlie.black@example.com"},
    {"id": 6, "name": "David White", "age": -5, "email": "david.white@example.com"},  # Invalid age (negative)
    {"id": 7, "name": "Eve Blue", "age": 28, "email": "eve.blue@example"},  # Invalid email
    {"id": 8, "name": "Frank Red", "age": "unknown", "email": "frank.red@example.com"},  # Invalid age
    {"id": 9, "name": "Grace Pink", "age": 50, "email": "grace.pink@example.com"},
    {"id": 10, "name": "Henry Yellow", "age": 60, "email": "henry.yellow@example.com"},
    # Missing 'name'
    {"id": 11, "age": 33, "email": "missing.name@example.com"},
    # Missing 'email'
    {"id": 12, "name": "Missing Email", "age": 29},
    # Missing 'age'
    {"id": 13, "name": "Missing Age", "email": "missing.age@example.com"},
    # Duplicate ID (assuming id should be unique, though not explicitly stated in current validation)
    {"id": 1, "name": "Duplicate ID", "age": 45, "email": "duplicate.id@example.com"},
    # Valid record after several invalid ones
    {"id": 14, "name": "Olivia Purple", "age": 27, "email": "olivia.purple@example.com"}
]

# Create an instance of DataIngestionAgent
agent = DataIngestionAgent()

# Load data from the sample list
agent.load_data_from_list(sample_data)

# Print validated data
print("Validated Data (from Demo):")
for record in agent.get_validated_data():
    print(record)

# Print rejected records
print("\nRejected Records (from Demo):")
for record_summary in agent.get_rejected_records_summary():
    print(record_summary)
