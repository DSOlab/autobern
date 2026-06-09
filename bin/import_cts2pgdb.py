#!/usr/bin/env python3
"""
Import GPS time series data from .cts files into PostgreSQL database
"""
import os
import sys
import psycopg2
from datetime import datetime
from pathlib import Path

# Database connection parameters
DB_CONFIG = {
    'dbname': 'procsta',
    'user': 'mitsos',
    'password': 'sklo;ypo1985',  # Update if you have a password
    'host': 'localhost',
    'port': 5432
}

def parse_cts_file(filepath, station_id, mark_name_dso, reference_frame_id=None,
                   software_id=None, solution_type_id=None):
    """Parse a .cts file and return list of records"""
    records = []

    with open(filepath, 'r') as f:
        # Skip header line
        header = f.readline()

        for line_num, line in enumerate(f, start=2):
            line = line.strip()
            if not line:
                continue

            try:
                parts = line.split()
                if len(parts) < 16:
                    print(f"Warning: Skipping malformed line {line_num} in {filepath}")
                    continue

                # Parse observation date and time
                obs_date = parts[0]
                obs_time = parts[1]
                obs_timestamp = f"{obs_date} {obs_time}"

                # Parse ECEF coordinates and their sigmas
                ecef_x = float(parts[2])
                ecef_x_sigma = float(parts[3])
                ecef_y = float(parts[4])
                ecef_y_sigma = float(parts[5])
                ecef_z = float(parts[6])
                ecef_z_sigma = float(parts[7])

                # Parse geographic coordinates and their sigmas
                latitude = float(parts[8])
                latitude_sigma = float(parts[9])
                longitude = float(parts[10])
                longitude_sigma = float(parts[11])
                altitude = float(parts[12])
                altitude_sigma = float(parts[13])

                # Parse processing date and time
                processing_date = parts[14]
                processing_time = parts[15]
                processing_timestamp = f"{processing_date} {processing_time}"

                # Parse campaign (optional)
                campaign = parts[16] if len(parts) > 16 else None

                record = (
                    station_id, mark_name_dso,
                    obs_date, obs_time, obs_timestamp,
                    ecef_x, ecef_x_sigma,
                    ecef_y, ecef_y_sigma,
                    ecef_z, ecef_z_sigma,
                    latitude, latitude_sigma,
                    longitude, longitude_sigma,
                    altitude, altitude_sigma,
                    processing_date, processing_time, processing_timestamp,
                    campaign,
                    reference_frame_id, software_id, solution_type_id
                )
                records.append(record)

            except (ValueError, IndexError) as e:
                print(f"Error parsing line {line_num} in {filepath}: {e}")
                continue

    return records

def get_station_id(cursor, mark_name_dso):
    """Get station_id from mark_name_DSO"""
    cursor.execute(
        'SELECT station_id FROM "station" WHERE "mark_name_DSO" = %s',
        (mark_name_dso,)
    )
    result = cursor.fetchone()
    return result[0] if result else None

def get_reference_frame_id(cursor, name):
    """Get reference_frame_id by name"""
    cursor.execute(
        'SELECT reference_frame_id FROM "reference_frame" WHERE name = %s',
        (name,)
    )
    result = cursor.fetchone()
    return result[0] if result else None

def get_software_id(cursor, name):
    """Get software_id by name"""
    cursor.execute(
        'SELECT software_id FROM "software" WHERE name = %s',
        (name,)
    )
    result = cursor.fetchone()
    return result[0] if result else None

def get_solution_type_id(cursor, name):
    """Get solution_type_id by name"""
    cursor.execute(
        'SELECT solution_type_id FROM "solution_type" WHERE name = %s',
        (name,)
    )
    result = cursor.fetchone()
    return result[0] if result else None

def import_cts_files(cts_directory, reference_frame=None, software=None):
    """Import all .cts and .cts_r files from directory"""

    # Connect to database
    print(f"Connecting to database '{DB_CONFIG['dbname']}'...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("✓ Connected successfully\n")
    except Exception as e:
        print(f"✗ Failed to connect to database: {e}")
        return

    # Get enumeration IDs - these are now REQUIRED
    reference_frame_id = get_reference_frame_id(cursor, reference_frame)
    if not reference_frame_id:
        print(f"✗ ERROR: Reference frame '{reference_frame}' not found in database")
        print(f"Available reference frames:")
        cursor.execute('SELECT name FROM "reference_frame" ORDER BY name')
        for row in cursor.fetchall():
            print(f"  - {row[0]}")
        cursor.close()
        conn.close()
        return

    software_id = get_software_id(cursor, software)
    if not software_id:
        print(f"✗ ERROR: Software '{software}' not found in database")
        print(f"Available software:")
        cursor.execute('SELECT name FROM "software" ORDER BY name')
        for row in cursor.fetchall():
            print(f"  - {row[0]}")
        cursor.close()
        conn.close()
        return

    print(f"✓ Using reference frame: {reference_frame} (ID: {reference_frame_id})")
    print(f"✓ Using software: {software} (ID: {software_id})")
    print()

    # Find all .cts and .cts_r files
    cts_files = list(Path(cts_directory).glob('*.cts')) + list(Path(cts_directory).glob('*.cts_r'))
    print(f"Found {len(cts_files)} files (.cts and .cts_r)\n")

    if not cts_files:
        print(f"No .cts or .cts_r files found in {cts_directory}")
        return

    total_records = 0
    successful_files = 0

    # Process each file
    for cts_file in sorted(cts_files):
        # Determine solution type based on file extension
        if cts_file.suffix == '.cts_r' or str(cts_file).endswith('.cts_r'):
            solution_type_name = 'Ultra_Rapid'
            mark_name_dso = cts_file.stem.replace('.cts', '')  # Handle .cts_r extension
        else:  # .cts files
            solution_type_name = 'Final'
            mark_name_dso = cts_file.stem

        solution_type_id = get_solution_type_id(cursor, solution_type_name)

        if not solution_type_id:
            print(f"✗ ERROR: Solution type '{solution_type_name}' not found in database")
            continue

        print(f"Processing {cts_file.name} (station: {mark_name_dso}, type: {solution_type_name})...")

        # Get station_id
        station_id = get_station_id(cursor, mark_name_dso)

        if station_id is None:
            print(f"  ✗ Warning: Station '{mark_name_dso}' not found in database, skipping")
            continue

        print(f"  Station ID: {station_id}, Solution Type ID: {solution_type_id}")

        # Parse the file
        try:
            records = parse_cts_file(cts_file, station_id, mark_name_dso,
                                   reference_frame_id, software_id, solution_type_id)
            print(f"  Parsed {len(records)} records")
        except Exception as e:
            print(f"  ✗ Error parsing file: {e}")
            continue

        if not records:
            print(f"  ✗ No valid records found")
            continue

        # Insert records into database
        try:
            insert_query = """
                INSERT INTO "gps_timeseries" (
                    station_id, mark_name_dso,
                    obs_date, obs_time, obs_timestamp,
                    ecef_x, ecef_x_sigma,
                    ecef_y, ecef_y_sigma,
                    ecef_z, ecef_z_sigma,
                    latitude, latitude_sigma,
                    longitude, longitude_sigma,
                    altitude, altitude_sigma,
                    processing_date, processing_time, processing_timestamp,
                    campaign,
                    reference_frame_id, software_id, solution_type_id
                ) VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s
                )
            """

            cursor.executemany(insert_query, records)
            conn.commit()

            total_records += len(records)
            successful_files += 1
            print(f"  ✓ Imported {len(records)} records\n")

        except Exception as e:
            conn.rollback()
            print(f"  ✗ Error inserting records: {e}\n")
            continue

    # Summary
    print("=" * 60)
    print(f"Import Summary:")
    print(f"  Files processed: {successful_files}/{len(cts_files)}")
    print(f"  Total records imported: {total_records}")
    print("=" * 60)

    # Show statistics
    cursor.execute("""
        SELECT
            mark_name_dso,
            COUNT(*) as record_count,
            MIN(obs_date) as first_date,
            MAX(obs_date) as last_date
        FROM "gps_timeseries"
        GROUP BY mark_name_dso
        ORDER BY mark_name_dso
    """)

    print("\nPer-station statistics:")
    print(f"{'Station':<10} {'Records':<10} {'First Date':<12} {'Last Date':<12}")
    print("-" * 50)
    for row in cursor.fetchall():
        print(f"{row[0]:<10} {row[1]:<10} {row[2]} {row[3]}")

    # Close connection
    cursor.close()
    conn.close()
    print("\n✓ Done!")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Import GPS time series data from .cts files')
    parser.add_argument('directory', nargs='?',
                       default='/home/mitsos/allcts',
                       help='Directory containing .cts files')
    parser.add_argument('--reference-frame', '-r',
                       required=True,
                       default='IGS20',
                       help='Reference frame name (REQUIRED, e.g., IGS20, IGS14)')
    parser.add_argument('--software', '-s',
                       default='BERNESE52',
                       help='Software name (default: BERNESE52)')

    args = parser.parse_args()
    cts_dir = args.directory

    if not os.path.exists(cts_dir):
        print(f"Error: Directory '{cts_dir}' not found")
        sys.exit(1)

    print("=" * 60)
    print("GPS Time Series Importer")
    print("=" * 60)
    print(f"Directory: {cts_dir}")
    print(f"Database: {DB_CONFIG['dbname']}")
    print(f"User: {DB_CONFIG['user']}")
    if args.reference_frame:
        print(f"Reference Frame: {args.reference_frame}")
    if args.software:
        print(f"Software: {args.software}")
    print("=" * 60)
    print()

    import_cts_files(cts_dir, args.reference_frame, args.software)
