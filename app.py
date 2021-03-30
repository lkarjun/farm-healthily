from fastapi import FastAPI, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from os import path, remove
from fastai.vision.all import PILImage, load_learner, Path
from urllib.request import urlretrieve

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')


def download_model(plant: str):
    '''Model downloading from google drive.'''
    models_plant = {'tomato': 'https://github.com/lkarjun/fastai-workouts/blob/master/models/tomato.pkl?raw=true',
                    'grapes': 'https://github.com/lkarjun/fastai-workouts/blob/master/models/grapes.pkl?raw=true',
                    'potato': 'https://github.com/lkarjun/fastai-workouts/blob/master/models/potato.pkl?raw=true',
                    'strawberry': 'https://github.com/lkarjun/fastai-workouts/blob/master/models/Strawberry.pkl?raw=true'}

    if path.exists(f'{plant}.pkl') == False:
        url = models_plant[plant]
        urlretrieve(url,f'{plant}.pkl')

def predict(filename: str, plant: str):
    '''classifying image.'''
    # download_model(plant)
    model = load_learner(Path.cwd()/'../models/export.pkl')
    # model = load_learner(f"{plant}.pkl")
    img = PILImage.create(filename)
    pred_class, pred_idx, ful_tensor = model.predict(img)
    return str(pred_class)


@app.get("/")
async def home(request: Request):
    '''home page'''
    return templates.TemplateResponse('index.html', context={'request': request})


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...), plant = Form(...)):
    '''Uploading file'''
    path = f"static/images/{file.filename}"
    print(file.filename, "Requested plant classifier " + plant)
    
    if 'image' in file.content_type:
        contents = await file.read()

        with open(path, 'wb') as f:
            f.write(contents)
        
        prediction = predict(path, plant)
        print(prediction)
        remove(path)
    return {"File": file.filename, "predicted": prediction}
