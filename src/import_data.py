import click
from ingest import ingest_file  # Your existing ingestion script
from process import process_and_store  # Your existing processing script

@click.command()
@click.option('--file_path', prompt='Enter the path to the data file', help='Path to the CSV file containing meter data.')
@click.option('--db_url', default='postgresql://postgres:mynewpassword123@localhost:5432/cps_energy', help='Database connection URL.')
def import_data(file_path, db_url):
    """Import meter data from a CSV file and store it in the database."""
    try:
        # Ingest the data
        data = ingest_file(file_path)
        click.echo(f"Ingested {len(data)} records from {file_path}")

        # Process and store the data
        processed = process_and_store(data, db_url)
        click.echo(f"Successfully stored {processed} records in the database.")

    except FileNotFoundError:
        click.echo(f"Error: File not found at {file_path}", err=True)
    except Exception as e:
        click.echo(f"An error occurred: {str(e)}", err=True)

if __name__ == '__main__':
    import_data()