import sys
import os
import time
import logging

# Ensure we can import from local dir
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'ai_support_engine'))

import database
import auth_service
import rag_engine
import llm_engine

# Setup Logging to file for report
logging.basicConfig(level=logging.INFO, filename='TEST_REPORT_LOG.txt', filemode='w', format='%(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

def log(msg):
    logging.info(msg)

def test_full_system():
    log("=== STARTING FULL SYSTEM TEST ===\n")
    
    # 1. Test Authentication
    log("1. Testing Authentication...")
    database.init_db()
    
    # Create test user
    test_user = "system_test_user"
    if not database.get_user(test_user):
        auth_service.register_user(test_user, "password123")
    
    # Attempt Login
    user = auth_service.login_user(test_user, "password123")
    if user:
        log("   [PASS] Login successful.")
    else:
        log("   [FAIL] Login failed.")

    # 2. Test RAG Ingestion
    log("\n2. Testing RAG Ingestion...")
    start_time = time.time()
    rag_engine.ingest_documents()
    duration = time.time() - start_time
    log(f"   [INFO] Ingestion took {duration:.2f}s")
    
    # Check if files moved
    processed_files = os.listdir(rag_engine.DATA_PROCESSED_DIR)
    if len(processed_files) > 0:
         log(f"   [PASS] Found {len(processed_files)} files in processed folder: {processed_files}")
    else:
         log("   [WARN] No files in processed folder. (Files might already be processed)")

    # 3. Test RAG Query (Context Aware)
    log("\n3. Testing RAG Query (Context Expected)...")
    # Assuming one of the PDFs is about "Network Protocol Configuration"
    query = "How do I configure the network protocol?"
    start_time = time.time()
    
    cat, resolution = llm_engine.analyze_ticket("Network Issue", query)
    
    duration = time.time() - start_time
    log(f"   [INFO] Processing took {duration:.2f}s")
    log(f"   [INFO] Resolution Snippet: {resolution[:100]}...")
    
    if len(resolution) > 20: 
        log("   [PASS] Received a substantive response.")
    else:
        log("   [FAIL] Response too short.")

    # 4. Test Backup Knowledge (General Query)
    log("\n4. Testing General Knowledge (Fallback)...")
    query_gen = "How do I bake a cake?"
    start_time = time.time()
    
    cat_gen, res_gen = llm_engine.analyze_ticket("Baking", query_gen)
    
    duration = time.time() - start_time
    log(f"   [INFO] Processing took {duration:.2f}s")
    log(f"   [INFO] Resolution Snippet: {res_gen[:100]}...")
    
    if "ingredient" in res_gen.lower() or "flour" in res_gen.lower() or "mix" in res_gen.lower():
         log("   [PASS] General knowledge fallback worked.")
    else:
         log("   [WARN] Response might not be about baking. Check full log.")

    log("\n=== TEST COMPLETE ===")

if __name__ == "__main__":
    test_full_system()
