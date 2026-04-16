import time
import requests

def run_tests():
    url_upload = "http://localhost:8000/api/upload"
    url_chat = "http://localhost:8000/api/chat"

    print("Waiting 5s for server to start...")
    time.sleep(5)
    
    print("Test 1: Uploading Document (Chunking and vectorizing)...")
    try:
        with open("test_support_faq.txt", "rb") as f:
            files = {"file": ("test_support_faq.txt", f, "text/plain")}
            res = requests.post(url_upload, files=files)
            print("Upload Status:", res.status_code)
            print("Upload Response:", res.json())

        time.sleep(1)

        print("\nTest 2: Querying LLM combining RAG...")
        payload = {"query": "How do I reset my antigravity device?"}
        res2 = requests.post(url_chat, json=payload)
        
        print("\nChat Status Code:", res2.status_code)
        
        if res2.status_code == 200:
            data = res2.json()
            print("\n================== LLM GENERATED RESPONSE ==================")
            print(data.get('response'))
            print("============================================================")
            print("Sources utilized:", data.get('context_sources'))
        else:
            print(f"Error ({res2.status_code}): {res2.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Is Uvicorn running on 8000?")
    except Exception as e:
        print(f"Test failed with error: {str(e)}")

if __name__ == "__main__":
    run_tests()
