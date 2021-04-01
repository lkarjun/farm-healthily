from fastapi import FastAPI, File, UploadFile, Form, Request, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from time import sleep

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')

model = None

def model_load():
    print("-------------importing modules-------------")
    global model
    from model_load import LoadModel
    model = LoadModel()
    print("-------------Importing completed-------------")


def predicting(filename, plant):
    '''using recrusive function wait until background process over.'''
    try:
        return model.predict(filename, plant)
    except:
        print("-------------Module Not Loadded-------------")
        sleep(1)
        return predicting(filename, plant)

@app.get("/")
async def home(request: Request, bg_task: BackgroundTasks):
    '''home page'''
    bg_task.add_task(model_load)
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
        
        prediction = predicting(filename = path, plant = plant)

        print(prediction)
        model.remove_it(path)
    return {"File": file.filename, "predicted": prediction}
