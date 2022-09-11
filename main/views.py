from django.shortcuts import render
from django.conf import settings
import pandas as pd
import joblib
import io
from PIL import Image as im
import torch
import json
import numpy as np
import cv2 as cv

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from .models import ImageModel
from .forms import ImageUploadForm

model = ImageModel
template_name = 'image/imagemodel_form.html'
fields = ["image"]

# main page
def index(request):
    return render(request, 'main/index.html')

# demand predict(VAR model)
def demand(request):
    if request.method == 'GET' :
        return render(request, 'main/demand.html')

    elif request.method == 'POST':
        days = int(request.POST.get('days'))
        counties = request.POST.get('counties')

        if counties == '강남구' :
            # load demand predict models
            gangnamModel = joblib.load('demand_models/model_gangnampickle.pkl')

            # data load
            df_gangnam= pd.read_csv('demand_models/df_gangnam.csv')

            # data preprocessing
            df_gangnam['대여일자'] = df_gangnam['대여일자'].replace('"','')
            df_gangnam = df_gangnam.set_index('대여일자')
            final_diff = df_gangnam.diff().dropna() 

            lagged_values_gangnam = final_diff.values[-6:]

            # forecast result
            result = pd.DataFrame(gangnamModel.forecast(y= lagged_values_gangnam, steps=30), index=final_diff.index[-30:], 
                                    columns=['개포동', '논현동', '대치동', '도곡동', '삼성동', '세곡동', '수서동', '신사동', '압구정동', '양재동','역삼동', '율현동', '일원동', '자곡동', '청담동'])

            a = result.iloc[days-1,:].sort_values(ascending=False)
            do_not_recommend = np.round(a.head(1).values)
            do_not_recommend_where = a.head(1).index[0]
            recommend = np.round(a.tail(1).values)
            recommend_where = a.tail(1).index[0]

            # context = {'counties':counties, 'result':result.to_html}
            context = {'counties': counties, 'result': result, 'days': days,
                        'do_not_recommend': do_not_recommend, 'do_not_recommend_where': do_not_recommend_where, 
                        'recommend':recommend, 'recommend_where': recommend_where}

        elif counties == '송파구' :
            # load demand predict models
            songpaModel=joblib.load('demand_models/model_songpapickle.pkl')
            
            # data load
            df_songpa = pd.read_csv('demand_models/df_songpa.csv')

            # data preprocessing
            df_songpa['대여일자'] = df_songpa['대여일자'].replace('"','')
            df_songpa = df_songpa.set_index('대여일자')
            final_diff = df_songpa.diff().dropna() 

            lagged_values_songpa = final_diff.values[-9:]

            # forecast result
            result = pd.DataFrame(songpaModel.forecast(y= lagged_values_songpa, steps=30), index = final_diff.index[-30:], 
                                    columns=['가락동', '거여동', '마천동', '문정동', '방이동', '삼전동', '석촌동', '송파동', '신천동', '오금동','잠실동', '장지동', '풍납동'])

            a = result.iloc[days-1,:].sort_values(ascending=False)
            do_not_recommend = np.round(a.head(1).values)
            do_not_recommend_where = a.head(1).index[0]
            recommend = np.round(a.tail(1).values)
            recommend_where = a.tail(1).index[0]

            # context = {'counties':counties, 'result':result.to_html}
            context = {'counties': counties, 'result': result, 'days': days,
                        'do_not_recommend': do_not_recommend, 'do_not_recommend_where': do_not_recommend_where, 
                        'recommend':recommend, 'recommend_where': recommend_where}

        else :
            # load demand predict models
            yeongModel=joblib.load('demand_models/model_yeoungpickle.pkl')

            # data load
            df_yeong = pd.read_csv('demand_models/df_yeong.csv')

            # data preprocessing
            df_yeong ['대여일자'] = df_yeong ['대여일자'].replace('"','')
            df_yeong  = df_yeong .set_index('대여일자')
            final_diff = df_yeong .diff().dropna() 

            lagged_values_yeong  = final_diff.values[-4:]

            # forecast result
            result = pd.DataFrame(yeongModel.forecast(y= lagged_values_yeong , steps=30), index = final_diff.index[-30:], columns=['구로동', '당산동', '당산동1가', '당산동2가', '당산동3가', '당산동4가', '당산동5가', '당산동6가',
                                    '대림동', '도림동', '문래동3가', '문래동4가', '문래동5가', '문래동6가', '신길동', '양평동1가',
                                    '양평동2가', '양평동3가', '양평동4가', '양평동5가', '양화동', '여의도동', '영등포동', '영등포동1가',
                                    '영등포동2가', '영등포동4가', '영등포동7가', '영등포동8가'])

            a = result.iloc[days-1,:].sort_values(ascending=False)
            do_not_recommend = np.round(a.head(1).values)
            do_not_recommend_where = a.head(1).index[0]
            recommend = np.round(a.tail(1).values)
            recommend_where = a.tail(1).index[0]

            # context = {'counties':counties, 'result':result.to_html}
            context = {'counties': counties, 'result': result, 'days': days,
                        'do_not_recommend': do_not_recommend, 'do_not_recommend_where': do_not_recommend_where, 
                        'recommend':recommend, 'recommend_where': recommend_where}

        return render(request, 'main/demand.html', context)

# helmet detect model(yolo v5 model)
def helmet(request):
    if request.method == 'GET':
        return render(request, 'main/helmet.html')

    elif request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        img = request.FILES.get('image')
        img_instance = ImageModel(
            image=img
        )
        img_instance.save()

        uploaded_img_qs = ImageModel.objects.filter().last()
        img_bytes = uploaded_img_qs.image.read()
        img = im.open(io.BytesIO(img_bytes))

        # resize to (416,416) ; fill in the blanks with black
        image = np.array(img)
        size = (416,416)
        base_pic=np.zeros((size[1],size[0],3),np.uint8)
        h,w=image.shape[:2]
        ash=size[1]/h
        asw=size[0]/w
        if asw<ash:
            sizeas=(int(w*asw),int(h*asw))
        else:
            sizeas=(int(w*ash),int(h*ash))
        image = cv.resize(image,dsize=sizeas)
        base_pic[int(size[1]/2-sizeas[1]/2):int(size[1]/2+sizeas[1]/2),
        int(size[0]/2-sizeas[0]/2):int(size[0]/2+sizeas[0]/2),:]=image

        # make border ; for detect when pictures are full
        nTop = nBottom = nLeft = nRight = 70
        img = cv.copyMakeBorder(base_pic, nTop, nBottom, nLeft, nRight, 
                            borderType=cv.BORDER_CONSTANT)

        path_hubconfig = "yolov5_code"
        path_weightfile = "best.pt"

        model = torch.hub.load(path_hubconfig, 'custom',
                                path=path_weightfile, source='local')

        results = model(img, size=640)

        # save detected img
        results.render()
        for img in results.ims:
            img_base64 = im.fromarray(img)
            img_base64.save("media/yolo_out/image0.jpg", format="JPEG")

        # save confidence score
        results_df = results.pandas().xyxy[0]
        results_df = results_df[results_df['class']==0][['confidence','class']]
        results_json = results_df.to_json(orient="records")
        score = json.loads(results_json)
        final_score = score[0]['confidence']

        file_path = 'media/yolo_out/score.json' # score.json path
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(score, file)

        inference_img = "/media/yolo_out/image0.jpg"

        form = ImageUploadForm()
        context = {
            "form": form,
            "inference_img": inference_img,
            "score": final_score
        }
        return render(request, 'main/helmet.html', context)

# parking detect model(yolo v5 model)
def parking(request):
    if request.method == 'GET' :
        return render(request, 'main/parking.html')