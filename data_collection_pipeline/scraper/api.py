import json
import requests

def _convert_response_to_records(data):
    if data is None:
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        possible_keys = ["data", "records", "result", "results", "response", "responseData", "items", "content"]
        for key in possible_keys:
            value = data.get(key)
            if isinstance(value, list):
                return value
        return [data]
    return [{"value": data}]

def collect_endpoint(api):
    endpoint = api.get("endpoint")
    url = api.get("url")
    responses = api.get("responses", [])
    headers = api.get("headers", {})
    post_data_raw = api.get("post_data")

    all_records = []
    errors = []

    # ---------------------------------------------------------
    # UNIVERSAL REPLAY LOGIC: Applies to ANY endpoint with pagination
    # ---------------------------------------------------------
    if post_data_raw:
        try:
            base_payload = json.loads(post_data_raw)
            # Check if it looks like a request that supports pagination parameters
            if isinstance(base_payload, dict) and "page" in base_payload:
                safe_headers = {k: v for k, v in headers.items() if k.lower() != 'content-length'}
                
                current_page = 1
                total_pages = 1  # Will update dynamically from the first response

                print(f"  -> Universal Paginator active for {endpoint}...")

                while current_page <= total_pages:
                    base_payload["page"] = current_page
                    base_payload["limit"] = 100  # Request chunks of 100 per page

                    res = requests.post(url, headers=safe_headers, json=base_payload, timeout=45)
                    
                    if res.status_code == 200:
                        res_json = res.json()
                        outer_data = res_json.get("data", {}) if isinstance(res_json, dict) else {}
                        
                        # Extract pagination details on the first run
                        if current_page == 1 and isinstance(outer_data, dict):
                            pagination = outer_data.get("pagination", {})
                            if pagination and isinstance(pagination, dict):
                                total_pages = pagination.get("totalPages", 1)
                                print(f"  -> [{endpoint}] Total records: {pagination.get('totalRecord', 'Unknown')} across {total_pages} pages.")

                        actual_data = outer_data.get("data", {}) if isinstance(outer_data, dict) else outer_data
                        records = _convert_response_to_records(actual_data)

                        if not records:
                            break # Stop if no more records are returned

                        all_records.extend(records)
                        
                        # If the server doesn't use pagination objects, break out of loop after page 1
                        if total_pages <= 1:
                            break
                            
                        current_page += 1
                    else:
                        errors.append(f"Page {current_page} HTTP {res.status_code}")
                        break

                if all_records:
                    print(f"  -> Success! Extracted a total of {len(all_records)} records for {endpoint}.")

        except Exception as e:
            print(f"  -> Universal pagination skipped/failed for {endpoint}: {e}")

    # ---------------------------------------------------------
    # FALLBACK: Use browser intercepted data if universal replay didn't trigger or yield records
    # ---------------------------------------------------------
    if not all_records:
        for response in responses:
            status = response.get("status")
            data = response.get("data")
            if status is None or status < 200 or status >= 300:
                if status: errors.append(f"HTTP {status}")
                continue
            records = _convert_response_to_records(data)
            all_records.extend(records)

    return {
        "endpoint": endpoint,
        "url": url,
        "method": api.get("method"),
        "post_data": post_data_raw,
        "records": all_records,
        "responses": responses,
        "error": "; ".join(errors) if errors else None
    }