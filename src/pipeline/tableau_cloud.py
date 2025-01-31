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
        """
        检查数据源是否是 live-to-Hyper 类型
        
        Returns:
            bool: True 如果是 live-to-Hyper 类型，False 否则
        """
        with self.server.auth.sign_in(self.tableau_auth):
            try:
                # 获取所有数据源
                all_datasources, _ = self.server.datasources.get()
                
                # 找到目标数据源
                target_datasource = None
                for datasource in all_datasources:
                    if datasource.name == self.datasource_name:
                        target_datasource = datasource
                        break
                
                if not target_datasource:
                    raise ValueError(f"Datasource '{self.datasource_name}' not found")
                
                # 获取数据源的详细信息
                self.server.datasources.populate_connections(target_datasource)
                
                # 打印数据源信息用于调试
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
                
                # 检查是否是 live-to-Hyper 类型
                # 通常 live-to-Hyper 数据源会有特定的连接类型和属性
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
            # 创建临时 Hyper 文件
            temp_hyper_path = await self._create_temp_hyper_file(data, temp_dir)
            print("  - Created temporary Hyper file")
            print(f"  - Hyper file path: {temp_hyper_path}")
            
            with self.server.auth.sign_in(self.tableau_auth):
                # 获取现有数据源
                all_datasources, _ = self.server.datasources.get()
                datasource_item = next(
                    (ds for ds in all_datasources if ds.name == self.datasource_name),
                    None
                )
                
                if not datasource_item:
                    raise ValueError(f"Datasource '{self.datasource_name}' not found")
                
                # 准备更新请求
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                request_id = f"update_{timestamp}"
                
                # 定义更新动作 - 使用 insert action 追加数据
                actions = [{
                    "action": "insert",
                    "source-schema": "Extract",  
                    "source-table": "Rankings",   
                    "target-schema": "Extract",
                    "target-table": "Rankings"
                }]
                
                # 使用 update_hyper_data 方法更新数据
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
            # 暂时注释掉清理代码，保留临时文件用于调试
            if temp_hyper_path and Path(temp_hyper_path).exists():
                print(f"  - Debug: Temporary file kept at {temp_hyper_path}")

    async def wait_for_job_completion(self, job_id: str, timeout: int = 300) -> bool:
        """
        Wait for a job to complete
        
        Args:
            job_id: The ID of the job to wait for
            timeout: Maximum time to wait in seconds (default: 300)
            
        Returns:
            bool: True if job completed successfully, False otherwise
        """
        with self.server.auth.sign_in(self.tableau_auth):
            try:
                # 获取作业状态
                job = self.server.jobs.get_by_id(job_id)
                
                # 打印作业基本信息
                print(f"  - Job ID: {job.id}")
                print(f"  - Job type: {job.type}")
                print(f"  - Job mode: {job.mode}")
                
                # 检查作业进度
                if hasattr(job, 'progress'):
                    print(f"  - Job progress: {job.progress}")
                    
                # 检查作业完成状态
                if hasattr(job, 'completed_at'):
                    print(f"  - Job completed at: {job.completed_at}")
                    
                # 检查作业结果
                if hasattr(job, 'progress') and job.progress == 100:
                    print("  ✅ Data update completed successfully")
                    return True
                elif hasattr(job, 'error_message') and job.error_message:
                    print(f"  ❌ Job failed with error: {job.error_message}")
                    return False
                else:
                    # 作业仍在进行中
                    print(f"  - Job is in progress: {job.progress if hasattr(job, 'progress') else 'Unknown'}%")
                    return None
                
            except Exception as e:
                print(f"  ❌ Error checking job status: {str(e)}")
                # 发生异常时返回 False，表示检查失败
                return False  