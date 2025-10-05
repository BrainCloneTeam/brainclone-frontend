"""
Standalone script to quickly populate GraphAura Neo4j database.
This can be run independently or integrated into your application.

Usage:
    python populate_db.py
"""

import asyncio
from neo4j import AsyncGraphDatabase
from datetime import datetime
import uuid
from data import locations_data, people_data, docs_data, events_data, orgs_data

# Configuration - Update these with your Neo4j credentials
NEO4J_URI = "neo4j+s://5df056dc.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Q_yYWRfoFx2IBXhz51c3z4IXnJyaiHhnOdje71loHNc"
NEO4J_DATABASE = "neo4j"


async def populate_database():
    """Populate the database with synthetic data."""

    driver = AsyncGraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USER, NEO4J_PASSWORD)
    )

    try:
        await driver.verify_connectivity()
        print("✅ Connected to Neo4j")

        async with driver.session(database=NEO4J_DATABASE) as session:

            # Clear existing data (optional - comment out if you want to keep existing data)
            print("\n🗑️  Clearing existing data...")
            await session.run("MATCH (n) DETACH DELETE n")
            print("✅ Database cleared")

            # Entity IDs storage
            entity_ids = {}

            print("\n👥 Creating People...")

            for person in people_data:
                await session.run(
                    "CREATE (p:Person:Entity $props)",
                    props=person
                )
                entity_ids[person["name"]] = person["id"]
                print(f"  ✓ {person['name']}")

            print("\n🏢 Creating Organizations...")

            for org in orgs_data:
                await session.run(
                    "CREATE (o:Organization:Entity $props)",
                    props=org
                )
                entity_ids[org["name"]] = org["id"]
                print(f"  ✓ {org['name']}")

            print("\n📍 Creating Locations...")

            for location in locations_data:
                await session.run(
                    "CREATE (l:Location:Entity $props)",
                    props=location
                )
                entity_ids[location["name"]] = location["id"]
                print(f"  ✓ {location['name']}")

            print("\n📅 Creating Events...")

            for event in events_data:
                await session.run(
                    "CREATE (e:Event:Entity $props)",
                    props=event
                )
                entity_ids[event["name"]] = event["id"]
                print(f"  ✓ {event['name']}")

            print("\n📄 Creating Documents...")

            for doc in docs_data:
                await session.run(
                    "CREATE (d:Document:Entity $props)",
                    props=doc
                )
                entity_ids[doc["name"]] = doc["id"]
                print(f"  ✓ {doc['name']}")

            print("\n🔗 Creating Relationships...")

            # WORKS_FOR relationships
            relationships = [
                # Existing relationships
                ("Dr. Sarah Chen", "TechCorp Industries", "WORKS_FOR",
                 {"title": "Chief Technology Officer", "start_date": "2020-01-15T00:00:00Z"}),
                ("Michael Rodriguez", "TechCorp Industries", "WORKS_FOR",
                 {"title": "Senior Software Engineer", "start_date": "2021-03-01T00:00:00Z"}),
                ("Emily Watson", "TechCorp Industries", "WORKS_FOR",
                 {"title": "Product Manager", "start_date": "2021-06-15T00:00:00Z"}),
                ("Dr. David Kim", "TechCorp Industries", "WORKS_FOR",
                 {"title": "Data Scientist", "start_date": "2022-01-10T00:00:00Z"}),

                ("Dr. Sarah Chen", "Michael Rodriguez", "MANAGES",
                 {"start_date": "2021-03-01T00:00:00Z"}),
                ("Dr. Sarah Chen", "Emily Watson", "MANAGES",
                 {"start_date": "2021-06-15T00:00:00Z"}),

                ("Michael Rodriguez", "Dr. David Kim", "COLLABORATES_WITH",
                 {"project": "Analytics Platform", "start_date": "2024-01-15T00:00:00Z"}),
                ("Emily Watson", "Dr. David Kim", "COLLABORATES_WITH",
                 {"project": "Analytics Platform", "start_date": "2024-01-15T00:00:00Z"}),

                ("Dr. Sarah Chen", "Michael Rodriguez", "MENTOR_OF",
                 {"focus_area": "Technical Leadership", "start_date": "2022-01-01T00:00:00Z"}),

                ("TechCorp Industries", "TechCorp HQ Building", "LOCATED_IN",
                 {"primary": True}),

                ("Dr. Sarah Chen", "Q3 2024 Product Launch", "ATTENDED",
                 {"role": "Keynote Speaker"}),
                ("Emily Watson", "Q3 2024 Product Launch", "ATTENDED",
                 {"role": "Organizer"}),

                ("Moscone Convention Center", "AI Tech Summit 2024", "HOSTED",
                 {"capacity_used": 5000}),

                ("TechCorp Industries", "Q3 2024 Product Launch", "ORGANIZED",
                 {"role": "Host"}),

                ("Emily Watson", "Product Requirements Document", "AUTHORED",
                 {"role": "Primary Author", "date": "2024-06-01T00:00:00Z"}),
                ("Dr. Sarah Chen", "Technical Architecture Specification", "AUTHORED",
                 {"role": "Technical Lead", "date": "2024-07-15T00:00:00Z"}),

                # New WORKS_FOR relationships
                ("Jennifer Thompson", "Dr. Sarah Chen", "MANAGES",
                 {"start_date": "2020-01-15T00:00:00Z"}),
                ("Jennifer Thompson", "Raj Patel", "MANAGES",
                 {"start_date": "2022-08-15T00:00:00Z"}),
                ("Jennifer Thompson", "Aisha Mohammed", "MANAGES",
                 {"start_date": "2021-11-10T00:00:00Z"}),
                ("Emily Watson", "Lisa Anderson", "MANAGES",
                 {"start_date": "2023-02-01T00:00:00Z"}),
                ("Carlos Mendes", "Thomas Mueller", "MANAGES",
                 {"start_date": "2019-04-01T00:00:00Z"}),
                ("Thomas Mueller", "Dr. Yuki Tanaka", "MANAGES",
                 {"start_date": "2020-06-15T00:00:00Z"}),

                # New COLLABORATES_WITH relationships
                ("Michael Rodriguez", "Kevin Zhang", "COLLABORATES_WITH",
                 {"project": "Backend Infrastructure", "start_date": "2023-06-15T00:00:00Z"}),
                ("Lisa Anderson", "Emily Watson", "COLLABORATES_WITH",
                 {"project": "UX Redesign Initiative", "start_date": "2024-03-01T00:00:00Z"}),
                ("Raj Patel", "Aisha Mohammed", "COLLABORATES_WITH",
                 {"project": "Security Automation", "start_date": "2024-02-10T00:00:00Z"}),
                ("Dr. David Kim", "Dr. Yuki Tanaka", "COLLABORATES_WITH",
                 {"project": "AI Research Partnership", "start_date": "2024-05-01T00:00:00Z"}),
                ("Jennifer Thompson", "Carlos Mendes", "COLLABORATES_WITH",
                 {"project": "Strategic Partnership", "start_date": "2024-01-20T00:00:00Z"}),

                # New MENTOR_OF relationships
                ("Jennifer Thompson", "Dr. Sarah Chen", "MENTOR_OF",
                 {"focus_area": "Executive Leadership", "start_date": "2020-06-01T00:00:00Z"}),
                ("Emily Watson", "Lisa Anderson", "MENTOR_OF",
                 {"focus_area": "Product Design", "start_date": "2023-03-15T00:00:00Z"}),
                ("Dr. David Kim", "Kevin Zhang", "MENTOR_OF",
                 {"focus_area": "Data Engineering", "start_date": "2023-07-01T00:00:00Z"}),
                ("Thomas Mueller", "Dr. Yuki Tanaka", "MENTOR_OF",
                 {"focus_area": "AI Research", "start_date": "2020-08-01T00:00:00Z"}),

                # New LOCATED_IN relationships
                ("Innovate.io", "Innovate.io Office", "LOCATED_IN",
                 {"primary": True}),
                ("TechCorp Industries", "TechCorp Austin Campus", "LOCATED_IN",
                 {"primary": False}),
                ("DataFlow Analytics", "DataFlow Analytics HQ", "LOCATED_IN",
                 {"primary": True}),
                ("CloudSecure Systems", "CloudSecure Seattle Office", "LOCATED_IN",
                 {"primary": True}),
                ("AI Solutions Lab", "AI Solutions Lab Facility", "LOCATED_IN",
                 {"primary": True}),
                ("MediTech Solutions", "MediTech Solutions Campus", "LOCATED_IN",
                 {"primary": True}),

                # New ATTENDED relationships
                ("Michael Rodriguez", "Q3 2024 Product Launch", "ATTENDED",
                 {"role": "Technical Presenter"}),
                ("Dr. David Kim", "Q3 2024 Product Launch", "ATTENDED",
                 {"role": "Demo Presenter"}),
                ("Jennifer Thompson", "AI Tech Summit 2024", "ATTENDED",
                 {"role": "Panel Speaker"}),
                ("Dr. Sarah Chen", "AI Tech Summit 2024", "ATTENDED",
                 {"role": "Keynote Speaker"}),
                ("Thomas Mueller", "AI Tech Summit 2024", "ATTENDED",
                 {"role": "Workshop Leader"}),
                ("Dr. Yuki Tanaka", "AI Tech Summit 2024", "ATTENDED",
                 {"role": "Researcher Presenter"}),
                ("Lisa Anderson", "Annual Developer Conference 2024", "ATTENDED",
                 {"role": "UX Track Speaker"}),
                ("Raj Patel", "Annual Developer Conference 2024", "ATTENDED",
                 {"role": "DevOps Workshop Leader"}),
                ("Aisha Mohammed", "Cybersecurity Workshop Series", "ATTENDED",
                 {"role": "Lead Instructor"}),
                ("Maria Garcia", "Women in Tech Networking Event", "ATTENDED",
                 {"role": "Organizer"}),
                ("Emily Watson", "Women in Tech Networking Event", "ATTENDED",
                 {"role": "Speaker"}),
                ("Carlos Mendes", "Startup Pitch Competition", "ATTENDED",
                 {"role": "Judge"}),
                ("Dr. David Kim", "Machine Learning Bootcamp", "ATTENDED",
                 {"role": "Instructor"}),
                ("Kevin Zhang", "Open Source Contributors Meetup", "ATTENDED",
                 {"role": "Contributor"}),
                ("Michael Rodriguez", "Open Source Contributors Meetup", "ATTENDED",
                 {"role": "Presenter"}),

                # New HOSTED relationships
                ("TechCorp HQ Building", "Q3 2024 Product Launch", "HOSTED",
                 {"capacity_used": 250}),
                ("Boston Conference Hall", "Annual Developer Conference 2024", "HOSTED",
                 {"capacity_used": 3500}),
                ("Tech Innovation Hub", "Cybersecurity Workshop Series", "HOSTED",
                 {"capacity_used": 85}),
                ("Innovate.io Office", "Startup Pitch Competition", "HOSTED",
                 {"capacity_used": 500}),
                ("Tech Innovation Hub", "Women in Tech Networking Event", "HOSTED",
                 {"capacity_used": 200}),
                ("MediTech Solutions Campus", "Healthcare Innovation Symposium", "HOSTED",
                 {"capacity_used": 800}),
                ("AI Solutions Lab Facility", "Machine Learning Bootcamp", "HOSTED",
                 {"capacity_used": 50}),
                ("Tech Innovation Hub", "Open Source Contributors Meetup", "HOSTED",
                 {"capacity_used": 120}),

                # New ORGANIZED relationships
                ("TechCorp Industries", "Annual Developer Conference 2024", "ORGANIZED",
                 {"role": "Co-organizer"}),
                ("CloudSecure Systems", "Cybersecurity Workshop Series", "ORGANIZED",
                 {"role": "Host"}),
                ("TechCorp Industries", "Women in Tech Networking Event", "ORGANIZED",
                 {"role": "Sponsor"}),
                ("GreenTech Ventures", "Startup Pitch Competition", "ORGANIZED",
                 {"role": "Host"}),
                ("MediTech Solutions", "Healthcare Innovation Symposium", "ORGANIZED",
                 {"role": "Host"}),
                ("AI Solutions Lab", "Machine Learning Bootcamp", "ORGANIZED",
                 {"role": "Host"}),
                ("TechCorp Industries", "TechCorp Team Building Retreat", "ORGANIZED",
                 {"role": "Host"}),

                # New AUTHORED relationships
                ("Michael Rodriguez", "Technical Architecture Specification", "AUTHORED",
                 {"role": "Contributing Engineer", "date": "2024-07-15T00:00:00Z"}),
                ("James O'Brien", "Q3 2024 Financial Report", "AUTHORED",
                 {"role": "Primary Author", "date": "2024-10-01T00:00:00Z"}),
                ("Sophie Laurent", "Employee Handbook 2024", "AUTHORED",
                 {"role": "Editor", "date": "2024-01-01T00:00:00Z"}),
                ("Aisha Mohammed", "Security Best Practices Guide", "AUTHORED",
                 {"role": "Primary Author", "date": "2024-08-20T00:00:00Z"}),
                ("Maria Garcia", "Marketing Strategy Q4 2024", "AUTHORED",
                 {"role": "Primary Author", "date": "2024-09-01T00:00:00Z"}),
                ("Dr. Sarah Chen", "AI Ethics Framework", "AUTHORED",
                 {"role": "Lead Author", "date": "2024-07-01T00:00:00Z"}),
                ("Dr. Yuki Tanaka", "AI Ethics Framework", "AUTHORED",
                 {"role": "Contributing Researcher", "date": "2024-07-01T00:00:00Z"}),
                ("Michael Rodriguez", "API Documentation v4.2", "AUTHORED",
                 {"role": "Technical Writer", "date": "2024-09-15T00:00:00Z"}),
                ("Kevin Zhang", "API Documentation v4.2", "AUTHORED",
                 {"role": "Contributing Developer", "date": "2024-09-15T00:00:00Z"}),
                ("Lisa Anderson", "User Research Report - Q2 2024", "AUTHORED",
                 {"role": "Lead Researcher", "date": "2024-07-10T00:00:00Z"}),
                ("Emily Watson", "User Research Report - Q2 2024", "AUTHORED",
                 {"role": "Product Lead", "date": "2024-07-10T00:00:00Z"}),
                ("Dr. Sarah Chen", "Partnership Agreement - Innovate.io", "AUTHORED",
                 {"role": "Technical Signatory", "date": "2024-05-15T00:00:00Z"}),
                ("Carlos Mendes", "Partnership Agreement - Innovate.io", "AUTHORED",
                 {"role": "CEO Signatory", "date": "2024-05-15T00:00:00Z"}),

                # PARTNER_WITH relationships (Organization to Organization)
                ("TechCorp Industries", "Innovate.io", "PARTNER_WITH",
                 {"partnership_type": "Technology Partnership", "start_date": "2024-05-15T00:00:00Z"}),
                ("TechCorp Industries", "DataFlow Analytics", "PARTNER_WITH",
                 {"partnership_type": "Data Services", "start_date": "2023-09-01T00:00:00Z"}),
                ("CloudSecure Systems", "TechCorp Industries", "PARTNER_WITH",
                 {"partnership_type": "Security Services", "start_date": "2022-06-10T00:00:00Z"}),
                ("GreenTech Ventures", "Innovate.io", "PARTNER_WITH",
                 {"partnership_type": "Investment", "start_date": "2021-11-20T00:00:00Z"}),
                ("AI Solutions Lab", "TechCorp Industries", "PARTNER_WITH",
                 {"partnership_type": "Research Collaboration", "start_date": "2023-03-01T00:00:00Z"}),

                # REVIEWED relationships (Documents)
                ("Dr. Sarah Chen", "Product Requirements Document", "REVIEWED",
                 {"review_date": "2024-06-05T00:00:00Z", "status": "Approved"}),
                ("Jennifer Thompson", "Technical Architecture Specification", "REVIEWED",
                 {"review_date": "2024-07-20T00:00:00Z", "status": "Approved"}),
                ("James O'Brien", "Marketing Strategy Q4 2024", "REVIEWED",
                 {"review_date": "2024-09-05T00:00:00Z", "status": "Approved"}),

                # SPOKE_AT relationships (Person to Event)
                ("Dr. Sarah Chen", "Annual Developer Conference 2024", "SPOKE_AT",
                 {"topic": "Future of Cloud Architecture", "session_date": "2024-10-06T14:00:00Z"}),
                ("Jennifer Thompson", "AI Tech Summit 2024", "SPOKE_AT",
                 {"topic": "Engineering Leadership in AI Era", "session_date": "2024-11-21T10:00:00Z"}),
                ("Aisha Mohammed", "Cybersecurity Workshop Series", "SPOKE_AT",
                 {"topic": "Zero Trust Security Models", "session_date": "2024-09-20T14:00:00Z"}),

                # SPONSORED relationships (Organization to Event)
                ("TechCorp Industries", "AI Tech Summit 2024", "SPONSORED",
                 {"sponsorship_level": "Platinum", "amount": 50000}),
                ("CloudSecure Systems", "Cybersecurity Workshop Series", "SPONSORED",
                 {"sponsorship_level": "Gold", "amount": 15000}),
                ("GreenTech Ventures", "Startup Pitch Competition", "SPONSORED",
                 {"sponsorship_level": "Diamond", "amount": 75000}),

                # INVESTED_IN relationships
                ("GreenTech Ventures", "Innovate.io", "INVESTED_IN",
                 {"investment_date": "2021-11-20T00:00:00Z", "amount": 5000000, "round": "Series A"}),
                ("GreenTech Ventures", "QuantumLeap Computing", "INVESTED_IN",
                 {"investment_date": "2022-08-15T00:00:00Z", "amount": 3000000, "round": "Seed"}),
            ]

            for source_name, target_name, rel_type, props in relationships:
                props["created_at"] = datetime.utcnow().isoformat()
                props["weight"] = props.get("weight", 1.0)
                props["confidence_score"] = props.get("confidence_score", 0.95)

                await session.run(f"""
                    MATCH (source:Entity {{id: $source_id}})
                    MATCH (target:Entity {{id: $target_id}})
                    CREATE (source)-[r:{rel_type} $props]->(target)
                """,
                                  source_id=entity_ids[source_name],
                                  target_id=entity_ids[target_name],
                                  props=props
                                  )
                print(f"  ✓ {source_name} -{rel_type}-> {target_name}")

            # Verify results
            print("\n📊 Database Statistics:")

            result = await session.run("""
                MATCH (n)
                RETURN labels(n)[0] as type, count(n) as count
                ORDER BY type
            """)
            async for record in result:
                print(f"  {record['type']}: {record['count']} nodes")

            result = await session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as type, count(r) as count
                ORDER BY type
            """)
            print("\n  Relationships:")
            async for record in result:
                print(f"  {record['type']}: {record['count']}")

            print("\n✨ Database populated successfully!")

    finally:
        await driver.close()


if __name__ == "__main__":
    asyncio.run(populate_database())
