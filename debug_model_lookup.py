#!/usr/bin/env python3
"""Debug script to test model lookup by external_identifier."""

from istari_digital_client.client import Client
from istari_digital_client.configuration import Configuration

ISTARI_ENVIRONMENT_URL = "https://fileservice-v2.stage.istari.app"
ISTARI_PAT = "QXBAvPHSCUW1twRGFZclcMmluhfc-RDJn5odJODccnt18gQUxnll6x5Ujk0J8HJaZS7QnU8"
MODEL_EXTERNAL_ID = "group3-uas-demo-wing-model"
EXPECTED_MODEL_ID = "957d1dad-97c6-4164-8913-576438d980ea"

print("Connecting to Istari...")
client = Client(config=Configuration(registry_url=ISTARI_ENVIRONMENT_URL, registry_auth_token=ISTARI_PAT))

print("\n=== Listing all models ===")
models = client.list_models()
print(f"Found {len(models.items)} models")

for i, m in enumerate(models.items):
    print(f"\n--- Model {i+1} ---")
    print(f"  ID: {m.id}")
    print(f"  Name: {m.name}")
    print(f"  Display Name: {m.display_name}")
    print(f"  Has file: {m.file is not None}")
    if m.file:
        print(f"  File ID: {m.file.id}")
        # Try to get file details
        try:
            file_details = client.get_file(m.file.id)
            print(f"  File external_identifier: {file_details.external_identifier}")
            if file_details.external_identifier == MODEL_EXTERNAL_ID:
                print(f"  *** MATCH FOUND! ***")
        except Exception as e:
            print(f"  Error getting file details: {e}")

print("\n=== Direct lookup of expected model ===")
try:
    expected_model = client.get_model(EXPECTED_MODEL_ID)
    print(f"Model ID: {expected_model.id}")
    print(f"Model Name: {expected_model.display_name}")
    if expected_model.file:
        print(f"File ID: {expected_model.file.id}")
        file_details = client.get_file(expected_model.file.id)
        print(f"File external_identifier: {file_details.external_identifier}")
except Exception as e:
    print(f"Error: {e}")

print("\n=== Testing the lookup logic from notebook ===")
ntop_model = None
models = client.list_models()
for m in models.items:
    if m.file:
        try:
            file_details = client.get_file(m.file.id)
            if file_details.external_identifier == MODEL_EXTERNAL_ID:
                ntop_model = m
                break
        except:
            pass

if ntop_model:
    print(f"Found model: {ntop_model.id} ({ntop_model.display_name})")
else:
    print(f"Model NOT FOUND with external_identifier '{MODEL_EXTERNAL_ID}'")
