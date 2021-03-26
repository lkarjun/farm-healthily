from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from os import path, remove
from fastai.vision.all import PILImage, load_learner, Path
from urllib.request import urlretrieve

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')


def download_model():
    '''Model downloading from google drive.'''
    if path.exists('export.pkl') == False:
        url = 'https://github.com/lkarjun/fastai-workouts/blob/master/models/leaf-diseases-classifier-v2.pkl?raw=true'
        urlretrieve(url,'export.pkl')

def predict(filename: str):
    '''classifying image.'''
    download_model()
    # model = load_learner(Path.cwd()/'../models/leaf-diseases-classifier-v2.pkl')
    model = load_learner("export.pkl")
    img = PILImage.create(filename)
    pred_class, pred_idx, ful_tensor = model.predict(img)
    return str(pred_class)


@app.get("/")
async def home(request: Request):
    '''home page'''
    return templates.TemplateResponse('index.html', context={'request': request})


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    '''Uploading file'''
    path = f"static/images/{file.filename}"
    print(file.filename)
    
    if 'image' in file.content_type:
        contents = await file.read()

        with open(path, 'wb') as f:
            f.write(contents)
        
        prediction = predict(path)
        print(prediction)
        remove(path)
    return {"File": file.filename, "predicted": prediction}
