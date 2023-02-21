from fastapi import APIRouter, BackgroundTasks, UploadFile, Depends
from fastapi.responses import StreamingResponse

from src.services.files import FilesService

router = APIRouter(
    prefix='/files',
    tags=['files']
)


@router.post('/upload', name='Загрузить файл')
def upload(backgroud_tasks: BackgroundTasks, file: UploadFile, files_service: FilesService = Depends()):
    backgroud_tasks.add_task(files_service.upload, file.file)

@router.get('/download', name='Скачать файл')
def download(files_service: FilesService = Depends()):
    report = files_service.download()
    return StreamingResponse(report, media_type='text/csv',
                             headers={'Content-Disposition': 'attachment; filename=report.csv'})
