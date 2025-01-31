from pathlib import Path
import tableauserverclient as TSC
from typing import List, BinaryIO
from datetime import datetime
from pipeline.tableau import TableauDataRow
from pipeline.hyper import HyperFileManager
from tableauhyperapi import (
    HyperProcess, 
    Telemetry, 
    Connection, 
    CreateMode,
    TableDefinition,
    SqlType,
    TableName,
    Name,
    Inserter
)
from tableauserverclient import JobItem  

class TableauCloudPublisher:
    """Handles publishing and updating data in Tableau Cloud"""
    
    def __init__(
        self, 
        server_url: str,
        site_name: str,
        token_name: str,
        token_value: str,
        datasource_name: str
    ):
        self.server_url = server_url
        self.site_name = site_name
        self.token_name = token_name
        self.token_value = token_value
        self.datasource_name = datasource_name
        
        # Initialize Tableau Server client
        self.tableau_auth = TSC.PersonalAccessTokenAuth(
            token_name=token_name,
            personal_access_token=token_value,
            site_id=site_name
        )
        self.server = TSC.Server(server_url, use_server_version=True)

    async def _get_datasource_id(self) -> str:
        """Get the ID of the target datasource"""
        all_datasources, _ = self.server.datasources.get()
        for datasource in all_datasources:
            if datasource.name == self.datasource_name:
                return datasource.id
        raise ValueError(f"Datasource '{self.datasource_name}' not found")

    async def _create_temp_hyper_file(self, data: List[TableauDataRow], temp_dir: Path) -> Path:
        """Create a temporary Hyper file with the provided data"""
        manager = HyperFileManager(temp_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_hyper_path = manager.create_hyper_file(f"temp_{timestamp}", data)
        return temp_hyper_path

    async def _check_datasource_type(self) -> bool:
 
        with self.server.auth.sign_in(self.tableau_auth):
            try:
                # get all datasources
                all_datasources, _ = self.server.datasources.get()
                

                # find target datasource
                target_datasource = None
                for datasource in all_datasources:
                    if datasource.name == self.datasource_name:

                        target_datasource = datasource
                        break
                
                if not target_datasource:
                    raise ValueError(f"Datasource '{self.datasource_name}' not found")
                
                # get datasource details
                self.server.datasources.populate_connections(target_datasource)
                

                # print datasource details for debugging
                print("\nDatasource details:")
                print(f"  - Name: {target_datasource.name}")
                print(f"  - ID: {target_datasource.id}")
                print(f"  - Type: {target_datasource.datasource_type}")
                print(f"  - Has extracts: {target_datasource.has_extracts}")
                

                if hasattr(target_datasource, 'connections'):
                    for conn in target_datasource.connections:
                        print(f"  - Connection type: {conn.connection_type}")
                        print(f"  - Server address: {conn.server_address}")
                        print(f"  - Connection attributes: {conn.__dict__}")
                
                is_live_to_hyper = (
                    target_datasource.has_extracts and
                    hasattr(target_datasource, 'connections') and
                    any(conn.connection_type == 'hyper' for conn in target_datasource.connections)
                )
                
                print(f"\nIs live-to-Hyper: {is_live_to_hyper}")
                return is_live_to_hyper
                
            except Exception as e:
                print(f"  ❌ Error checking datasource type: {str(e)}")
                raise

    async def update_hyper_data(
        self,
        request_id: str,
        actions: List[dict],
        payload: BinaryIO
    ) -> TSC.JobItem:
        """
        Update data in Tableau Cloud using the Hyper file
        
        Args:
            request_id: Unique identifier for the request
            actions: List of actions to perform (insert, replace, etc.)
            payload: Hyper file containing the data
            
        Returns:
            JobItem for tracking the update progress
        """
        with self.server.auth.sign_in(self.tableau_auth):
            try:
                # Get datasource ID
                datasource_id = await self._get_datasource_id()
                print(f"  - Found datasource ID: {datasource_id}")
                
                # Start upload session
                upload_session_id = self.server.fileuploads.initiate()
                print(f"  - Started upload session: {upload_session_id}")
                
                # Read file content and upload
                file_content = payload.read()
                self.server.fileuploads.append(
                    upload_session_id, 
                    file_content,
                    content_type='application/x-hyper'
                )
                print("  - Uploaded Hyper file")
                
                # Send update request
                job = self.server.datasources.update_hyper_data(
                    datasource_id,
                    upload_session_id,
                    actions,
                    request_id=request_id
                )
                print(f"  - Initiated update job: {job.id}")
                
                return job
                
            except Exception as e:
                print(f"  ❌ Error in update_hyper_data: {str(e)}")
                raise
            finally:
                # Reset file pointer position
                payload.seek(0)

    async def update_data(self, data: List[TableauDataRow], temp_dir: Path = None) -> str:
        """
        High-level method to update data in Tableau Cloud using a Hyper file
        """
        if temp_dir is None:
            temp_dir = Path("data/temp")
            temp_dir.mkdir(parents=True, exist_ok=True)

        temp_hyper_path = None
        try:
            # create temporary Hyper file
            temp_hyper_path = await self._create_temp_hyper_file(data, temp_dir)
            print("  - Created temporary Hyper file")
            print(f"  - Hyper file path: {temp_hyper_path}")
            

            with self.server.auth.sign_in(self.tableau_auth):
                # get existing datasource
                all_datasources, _ = self.server.datasources.get()
                datasource_item = next(
                    (ds for ds in all_datasources if ds.name == self.datasource_name),
                    None
                )

                
                if not datasource_item:
                    raise ValueError(f"Datasource '{self.datasource_name}' not found")
                
                # prepare update request
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                request_id = f"update_{timestamp}"
                

                # define update actions - use insert action to append data
                actions = [{
                    "action": "insert",
                    "source-schema": "Extract",  
                    "source-table": "Rankings",   
                    "target-schema": "Extract",
                    "target-table": "Rankings"

                }]
                
                # use update_hyper_data method to update data
                print("  - Updating datasource with insert action...")
                print(f"  - Using datasource: {datasource_item.name} (ID: {datasource_item.id})")
                print(f"  - Request ID: {request_id}")
                print(f"  - Actions: {actions}")
                

                job = self.server.datasources.update_hyper_data(
                    datasource_or_connection_item=datasource_item,
                    request_id=request_id,
                    actions=actions,
                    payload=str(temp_hyper_path)
                )
                
                if not job:
                    raise Exception("Failed to start update job")
                    
                print(f"  - Update job started with ID: {job.id}")
                return job.id

        except Exception as e:
            print(f"\n  ❌ Error during data update: {str(e)}")
            raise
        
        finally:
            # temporarily comment out cleanup code, keep temporary file for debugging
            if temp_hyper_path and Path(temp_hyper_path).exists():
                print(f"  - Debug: Temporary file kept at {temp_hyper_path}")


    async def wait_for_job(self, job_id: str, timeout: int = 300) -> TSC.JobItem:
        """Wait for job completion using TSC native method"""
        try:
            with self.server.auth.sign_in(self.tableau_auth):
                print(f"  - Waiting for job {job_id} completion (timeout: {timeout}s)")
                # use TSC built-in wait method
                final_job = self.server.jobs.wait_for_job(job_id, timeout=timeout)
                
                # print final status
                print(f"  - Final job status:")
                finish_code_map = {
                    0: "Success",
                    1: "Failed", 
                    2: "Cancelled"
                }

                print(f"    - Finish code: {final_job.finish_code} "
                     f"({finish_code_map.get(final_job.finish_code, 'Unknown')})")
                print(f"    - Created at: {final_job.created_at}")
                print(f"    - Started at: {final_job.started_at}")
                print(f"    - Completed at: {final_job.completed_at}")
                if final_job.notes:
                    print(f"    - Notes: {final_job.notes}")
                
                return final_job
                
        except TSC.ServerResponseError as e:
            print(f"  ❌ Tableau job failed: {e}")
            raise Exception(f"Tableau job error: {str(e)}")
        except Exception as e:
            print(f"  ❌ Error waiting for job: {str(e)}")
            raise  