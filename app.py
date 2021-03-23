# from pickle import load
from os import read
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from os import path
from fastai.vision.all import open_image, load_learner
from urllib.request import urlretrieve

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')


def download_model():
    '''Model downloading from google drive.'''
    if path.exists('export.pkl') == False:
        url = 'https://drive.google.com/uc?id=10CP_4IkQLpcIEDvRjKvJU2BJx7wKMTDz&export=download'
        urlretrieve(url,'export.pkl')

def predict(filename: str):
    '''classifying image.'''
    model = load_learner("")
    img = open_image(filename)
    pred_class, pred_idx = model.predict(img)
    return str(pred_class)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})


# @app.post("/files/")
# async def create_file(file: bytes = File(...)):
#     return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    print(file.filename)
    
    if 'image' in file.content_type:
        contents = await file.read()

        with open(f"static/images/{file.filename}", 'wb') as f:
            f.write(contents)
        
        # prediction = predict(f'static/images/{file.filename}')
    return {"File": file.filename, "predicted": 'Null'}
