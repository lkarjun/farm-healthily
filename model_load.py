from fastai.vision.all import PILImage, load_learner, Path
from os import path, remove
from urllib.request import urlretrieve

class LoadModel:

    def download_model(self, plant: str):
        '''Model downloading from google drive.'''
        models_plant = {'tomato': 'https://github.com/lkarjun/fastai-workouts/blob/master/models/tomato.pkl?raw=true',
                    'grapes': 'https://github.com/lkarjun/fastai-workouts/blob/master/models/grapes.pkl?raw=true',
                    'potato': 'https://github.com/lkarjun/fastai-workouts/blob/master/models/potato.pkl?raw=true',
                    'strawberry': 'https://github.com/lkarjun/fastai-workouts/blob/master/models/Strawberry.pkl?raw=true',
                       'peach': 'https://github.com/lkarjun/fastai-workouts/blob/master/models/peach.pkl?raw=true',
                       'cherry': 'https://github.com/lkarjun/fastai-workouts/blob/master/models/cherry.pkl?raw=true'}

        if path.exists(f'{plant}.pkl') == False:
            url = models_plant[plant]
            urlretrieve(url,f'{plant}.pkl')

    def predict(self, filename: str, plant: str):
        '''classifying image.'''
        print("-------------Model Downloading-------------")
        self.download_model(plant)
        # model = load_learner(Path.cwd()/'../models/export.pkl')
        print("-------------Model Downloaded-------------")
        
        model = load_learner(f"{plant}.pkl")
        img = PILImage.create(filename)
        pred_class, pred_idx, ful_tensor = model.predict(img)
        return str(pred_class)
    
    def remove_it(self, filename):
        '''removing uploaded photo'''
        remove(filename)
