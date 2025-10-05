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
            # await session.run("MATCH (n) DETACH DELETE n")
            print("✅ Database cleared")

            # Entity IDs storage
            entity_ids = {}

            print("\n👥 Creating People...")
            people_data = [
                {
                    "id": str(uuid.uuid4()),
                    "type": "person",
                    "name": "Dr. Sarah Chen",
                    "email": "sarah.chen@techcorp.com",
                    "occupation": "Chief Technology Officer",
                    "birth_date": "1985-03-15T00:00:00Z",
                    "nationality": "American",
                    "created_at": datetime.utcnow().isoformat()
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "person",
                    "name": "Michael Rodriguez",
                    "email": "m.rodriguez@techcorp.com",
                    "occupation": "Senior Software Engineer",
                    "birth_date": "1990-07-22T00:00:00Z",
                    "nationality": "Mexican-American",
                    "created_at": datetime.utcnow().isoformat()
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "person",
                    "name": "Emily Watson",
                    "email": "emily.watson@techcorp.com",
                    "occupation": "Product Manager",
                    "birth_date": "1988-11-05T00:00:00Z",
                    "nationality": "British",
                    "created_at": datetime.utcnow().isoformat()
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "person",
                    "name": "Dr. David Kim",
                    "email": "david.kim@techcorp.com",
                    "occupation": "Data Scientist",
                    "birth_date": "1987-04-18T00:00:00Z",
                    "nationality": "Korean-American",
                    "created_at": datetime.utcnow().isoformat()
                }
            ]

            for person in people_data:
                await session.run(
                    "CREATE (p:Person:Entity $props)",
                    props=person
                )
                entity_ids[person["name"]] = person["id"]
                print(f"  ✓ {person['name']}")

            print("\n🏢 Creating Organizations...")
            orgs_data = [
                {
                    "id": str(uuid.uuid4()),
                    "type": "organization",
                    "name": "TechCorp Industries",
                    "industry": "Technology",
                    "organization_type": "Private Corporation",
                    "founded_date": "2015-01-15T00:00:00Z",
                    "employee_count": 750,
                    "website": "https://techcorp.com",
                    "created_at": datetime.utcnow().isoformat()
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "organization",
                    "name": "Innovate.io",
                    "industry": "Software",
                    "organization_type": "Startup",
                    "founded_date": "2019-03-20T00:00:00Z",
                    "employee_count": 75,
                    "website": "https://innovate.io",
                    "created_at": datetime.utcnow().isoformat()
                }
            ]

            for org in orgs_data:
                await session.run(
                    "CREATE (o:Organization:Entity $props)",
                    props=org
                )
                entity_ids[org["name"]] = org["id"]
                print(f"  ✓ {org['name']}")

            print("\n📍 Creating Locations...")
            locations_data = [
                {
                    "id": str(uuid.uuid4()),
                    "type": "location",
                    "name": "TechCorp HQ Building",
                    "address": "123 Market Street",
                    "city": "San Francisco",
                    "state": "California",
                    "country": "United States",
                    "location_type": "Office",
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "created_at": datetime.utcnow().isoformat()
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "location",
                    "name": "Moscone Convention Center",
                    "address": "747 Howard Street",
                    "city": "San Francisco",
                    "state": "California",
                    "country": "United States",
                    "location_type": "Conference Center",
                    "latitude": 37.7842,
                    "longitude": -122.4016,
                    "created_at": datetime.utcnow().isoformat()
                }
            ]

            for location in locations_data:
                await session.run(
                    "CREATE (l:Location:Entity $props)",
                    props=location
                )
                entity_ids[location["name"]] = location["id"]
                print(f"  ✓ {location['name']}")

            print("\n📅 Creating Events...")
            events_data = [
                {
                    "id": str(uuid.uuid4()),
                    "type": "event",
                    "name": "Q3 2024 Product Launch",
                    "event_type": "Product Launch",
                    "start_date": "2024-09-15T10:00:00Z",
                    "end_date": "2024-09-15T14:00:00Z",
                    "status": "completed",
                    "attendance": 250,
                    "created_at": datetime.utcnow().isoformat()
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "event",
                    "name": "AI Tech Summit 2024",
                    "event_type": "Conference",
                    "start_date": "2024-11-20T09:00:00Z",
                    "end_date": "2024-11-22T17:00:00Z",
                    "status": "planned",
                    "attendance": 5000,
                    "created_at": datetime.utcnow().isoformat()
                }
            ]

            for event in events_data:
                await session.run(
                    "CREATE (e:Event:Entity $props)",
                    props=event
                )
                entity_ids[event["name"]] = event["id"]
                print(f"  ✓ {event['name']}")

            print("\n📄 Creating Documents...")
            docs_data = [
                {
                    "id": str(uuid.uuid4()),
                    "type": "document",
                    "name": "Product Requirements Document",
                    "document_type": "Requirements",
                    "file_path": "/docs/prd/analytics_platform_v2.3.pdf",
                    "publication_date": "2024-06-01T00:00:00Z",
                    "page_count": 45,
                    "created_at": datetime.utcnow().isoformat()
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "document",
                    "name": "Technical Architecture Specification",
                    "document_type": "Technical Specification",
                    "file_path": "/docs/specs/tech_arch_v1.5.md",
                    "publication_date": "2024-07-15T00:00:00Z",
                    "page_count": 30,
                    "created_at": datetime.utcnow().isoformat()
                }
            ]

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
                ("Dr. Sarah Chen", "TechCorp Industries", "WORKS_FOR",
                 {"title": "Chief Technology Officer", "start_date": "2020-01-15T00:00:00Z"}),
                ("Michael Rodriguez", "TechCorp Industries", "WORKS_FOR",
                 {"title": "Senior Software Engineer", "start_date": "2021-03-01T00:00:00Z"}),
                ("Emily Watson", "TechCorp Industries", "WORKS_FOR",
                 {"title": "Product Manager", "start_date": "2021-06-15T00:00:00Z"}),
                ("Dr. David Kim", "TechCorp Industries", "WORKS_FOR",
                 {"title": "Data Scientist", "start_date": "2022-01-10T00:00:00Z"}),

                # MANAGES relationships
                ("Dr. Sarah Chen", "Michael Rodriguez", "MANAGES",
                 {"start_date": "2021-03-01T00:00:00Z"}),
                ("Dr. Sarah Chen", "Emily Watson", "MANAGES",
                 {"start_date": "2021-06-15T00:00:00Z"}),

                # COLLABORATES_WITH relationships
                ("Michael Rodriguez", "Dr. David Kim", "COLLABORATES_WITH",
                 {"project": "Analytics Platform", "start_date": "2024-01-15T00:00:00Z"}),
                ("Emily Watson", "Dr. David Kim", "COLLABORATES_WITH",
                 {"project": "Analytics Platform", "start_date": "2024-01-15T00:00:00Z"}),

                # MENTOR_OF relationship
                ("Dr. Sarah Chen", "Michael Rodriguez", "MENTOR_OF",
                 {"focus_area": "Technical Leadership", "start_date": "2022-01-01T00:00:00Z"}),

                # LOCATED_IN relationships
                ("TechCorp Industries", "TechCorp HQ Building", "LOCATED_IN",
                 {"primary": True}),

                # ATTENDED relationships
                ("Dr. Sarah Chen", "Q3 2024 Product Launch", "ATTENDED",
                 {"role": "Keynote Speaker"}),
                ("Emily Watson", "Q3 2024 Product Launch", "ATTENDED",
                 {"role": "Organizer"}),

                # HOSTED relationship
                ("Moscone Convention Center", "AI Tech Summit 2024", "HOSTED",
                 {"capacity_used": 5000}),

                # ORGANIZED relationship
                ("TechCorp Industries", "Q3 2024 Product Launch", "ORGANIZED",
                 {"role": "Host"}),

                # AUTHORED relationships
                ("Emily Watson", "Product Requirements Document", "AUTHORED",
                 {"role": "Primary Author", "date": "2024-06-01T00:00:00Z"}),
                ("Dr. Sarah Chen", "Technical Architecture Specification", "AUTHORED",
                 {"role": "Technical Lead", "date": "2024-07-15T00:00:00Z"}),
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
