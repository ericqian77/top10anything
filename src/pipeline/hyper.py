from pathlib import Path
from typing import List
from tableauhyperapi import (
    HyperProcess,
    Telemetry,
    Connection,
    CreateMode,
    TableDefinition,
    SqlType,
    TableName,
    Inserter,
    HyperException,
    Name,
)
from .tableau import TableauDataRow

class HyperFileManager:
    """Manages Hyper file creation and data insertion"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.schema_name = "Extract"
        self.table_name = TableName(self.schema_name, "Rankings")
        
        # Define table schema
        self.table_def = TableDefinition(
            self.table_name,
            [
                TableDefinition.Column("topic", SqlType.text()),
                TableDefinition.Column("generated_at", SqlType.timestamp()),
                TableDefinition.Column("rank", SqlType.int()),
                TableDefinition.Column("item_name", SqlType.text()),
                TableDefinition.Column("score", SqlType.double()),
                TableDefinition.Column("advantages", SqlType.text()),
                TableDefinition.Column("metrics", SqlType.text()),
                TableDefinition.Column("sources", SqlType.text()),
                TableDefinition.Column("methodology", SqlType.text()),
                TableDefinition.Column("batch_id", SqlType.text())
            ]
        )
    
    def create_hyper_file(self, file_name: str, data: List[TableauDataRow]) -> Path:
        """Create a new Hyper file with the given data"""
        if not self.output_dir.exists():
            raise HyperException(f"Output directory does not exist: {self.output_dir}")
            
        hyper_path = self.output_dir / f"{file_name}.hyper"
        
        try:
            with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
                with Connection(hyper.endpoint, str(hyper_path), CreateMode.CREATE_AND_REPLACE) as connection:
                    # Create schema first
                    connection.catalog.create_schema(Name(self.schema_name))
                    
                    # Then create table
                    connection.catalog.create_table(self.table_def)
                    
                    # Insert data if any
                    if data:
                        with Inserter(connection, self.table_def) as inserter:
                            for row in data:
                                inserter.add_row([
                                    row.topic,
                                    row.generated_at,
                                    row.rank,
                                    row.item_name,
                                    row.score,
                                    row.advantages,
                                    row.metrics,
                                    row.sources,
                                    row.methodology,
                                    row.batch_id
                                ])
                            inserter.execute()
        except Exception as e:
            # Clean up partial file if creation fails
            if hyper_path.exists():
                hyper_path.unlink()
            raise HyperException(f"Failed to create Hyper file: {str(e)}") from e
        
        return hyper_path 