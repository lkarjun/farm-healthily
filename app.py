from fastapi import FastAPI, File, UploadFile, Form, Request, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from time import sleep

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')

model = None

def model_load():
    print("-------------importing module-------------")
    global model
    from model_load import LoadModel
    model = LoadModel()
    print("-------------Importing completed-------------")



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
        
        try:
            prediction = model.predict(filename = path, plant = plant)
        except:
            print("-----------------Putting sleep mode----------------")
            sleep(5)
            print("-----------------Offing sleep mode----------------")
            prediction = model.predict(filename = path, plant = plant)
        
        print(prediction)
        model.remove_it(path)
    return {"File": file.filename, "predicted": prediction}
