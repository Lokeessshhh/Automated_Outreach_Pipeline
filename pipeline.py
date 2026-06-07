import os
import time
import requests
from dotenv import load_dotenv

# Load configuration
load_dotenv()

OCEAN_API_KEY = os.getenv("OCEAN_API_KEY")
PROSPEO_API_KEY = os.getenv("PROSPEO_API_KEY")
BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_NAME = os.getenv("SENDER_NAME")

SLEEP_TIME = 3

def stage_1_ocean_io(seed_domain):
    """STAGE 1 - Find lookalike companies via Ocean.io"""
    print(f"\n[STAGE 1] Finding lookalike companies for: {seed_domain}")
    url = "https://api.ocean.io/v3/search/companies"
    headers = {
        "X-Api-Token": OCEAN_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "companiesFilters": {
            "lookalikeDomains": [seed_domain]
        },
        "size": 5
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        results = data.get("companies", [])
        domains = [item.get("company", {}).get("domain") for item in results if item.get("company", {}).get("domain")]
        
        # Ensure we only return 5 domains even if the API returns more
        domains = domains[:5]
        print(f"Found {len(domains)} lookalike domains.")
        return domains
    except Exception as e:
        print(f"Error in Stage 1: {e}")
        try:
            print(f"Response body: {response.text}")
        except:
            pass
        return []

def stage_2_prospeo(domains):
    """STAGE 2 - Find decision makers via Prospeo"""
    print(f"\n[STAGE 2] Finding decision makers for {len(domains)} companies...")
    url = "https://api.prospeo.io/search-person"
    headers = {"X-KEY": PROSPEO_API_KEY, "Content-Type": "application/json"}
    prospects = []

    for domain in domains:
        print(f"Searching {domain}...")
        payload = {
            "page": 1,
            "filters": {
                "company": {"websites": {"include": [domain]}},
                "person_seniority": {
                    "include": ["C-Suite", "Founder/Owner", "Vice President", "Director"]
                }
            }
        }
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            # LIMIT: Only take the top 1 prospect per domain
            for item in data.get("results", [])[:1]:
                person = item.get("person", {})
                company = item.get("company", {})
                prospects.append({
                    "person_id": person.get("person_id"),
                    "first_name": person.get("first_name", "there"),
                    "last_name": person.get("last_name", ""),
                    "title": person.get("current_job_title", ""),
                    "company_name": company.get("name", domain),
                    "domain": domain
                })
            time.sleep(SLEEP_TIME)
        except Exception as e:
            print(f"Skipping {domain}: {e}")
            try:
                print(f"Response: {response.text}")
            except:
                pass

    print(f"Collected {len(prospects)} prospects.")
    return prospects

def stage_3_prospeo_enrich(prospects):
    """STAGE 3 - Get emails via Prospeo enrich-person"""
    # LIMIT: Only enrich the first 5 prospects
    prospects_to_enrich = prospects[:5]
    print(f"\n[STAGE 3] Getting emails for {len(prospects_to_enrich)} prospects...")
    url = "https://api.prospeo.io/enrich-person"
    headers = {"X-KEY": PROSPEO_API_KEY, "Content-Type": "application/json"}

    final_contacts = []
    seen_emails = set()

    for p in prospects_to_enrich:
        if not p.get("person_id"):
            continue
        print(f"Enriching {p['first_name']} {p['last_name']} ({p['domain']})...")
        payload = {
            "only_verified_email": False,
            "data": {"person_id": p["person_id"]}
        }
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            person = data.get("person", {})
            email_obj = person.get("email", {})
            email = email_obj.get("email") if email_obj else None
            company = data.get("company", {})
            company_name = company.get("name", p["company_name"]) if company else p["company_name"]

            if email and email not in seen_emails:
                final_contacts.append({
                    "first_name": p["first_name"],
                    "name": f"{p['first_name']} {p['last_name']}",
                    "email": email,
                    "title": p["title"],
                    "company": company_name
                })
                seen_emails.add(email)
            time.sleep(SLEEP_TIME)
        except Exception as e:
            print(f"Enrich error for {p['first_name']}: {e}")
            try:
                print(f"Response: {response.text}")
            except:
                pass

    print(f"Verified {len(final_contacts)} emails.")
    return final_contacts

def stage_4_brevo(contacts):
    """STAGE 4 - Send outreach emails via Brevo"""
    print(f"\n[STAGE 4] Sending emails...")
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json"
    }
    
    for c in contacts:
        subject = f"Quick question, {c['first_name']}"
        body = f"Hi {c['first_name']},\n\nI came across {c['company']} and was really impressed by the work you're doing as {c['title']}.\nI wanted to reach out personally — we're building something that I think could be\ngenuinely useful for teams like yours. Would you be open to a quick 15-min call this week?"
        
        payload = {
            "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
            "to": [{"email": c["email"], "name": c["name"]}],
            "subject": subject,
            "textContent": body
        }
        
        try:
            print(f"Firing email to {c['email']}...")
            res = requests.post(url, headers=headers, json=payload, timeout=30)
            res.raise_for_status()
            time.sleep(SLEEP_TIME)
        except Exception as e:
            print(f"Brevo error for {c['email']}: {e}")
            try:
                print(f"Brevo response: {res.text}")
            except:
                pass

def main():
    print("--- PIPELINE START ---")
    seed = input("Enter seed domain: ").strip()
    if not seed: return

    domains = stage_1_ocean_io(seed)
    if not domains: return
    
    prospects = stage_2_prospeo(domains)
    if not prospects: return
    
    contacts = stage_3_prospeo_enrich(prospects)
    if not contacts: return
    
    # SAFETY CHECKPOINT
    print("\n" + "="*40)
    print("CONTACT SUMMARY")
    print("="*40)
    for i, c in enumerate(contacts, 1):
        print(f"{i}. {c['name']} <{c['email']}> | {c['title']} @ {c['company']}")
    
    confirm = input(f"\nSend {len(contacts)} emails? (Y/N): ").strip().upper()
    if confirm == 'Y':
        stage_4_brevo(contacts)
        print("\nPipeline complete.")
    else:
        print("\nOperation cancelled.")

if __name__ == "__main__":
    main()
